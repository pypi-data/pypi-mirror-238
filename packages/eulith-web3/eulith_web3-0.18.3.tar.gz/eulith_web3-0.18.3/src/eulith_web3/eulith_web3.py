import time
from typing import Union, Any, cast, Callable, Optional, List
from warnings import warn

import web3.middleware
from eth_typing import URI, ChecksumAddress, HexStr
from eth_utils import is_hex_address
from hexbytes import HexBytes
from web3 import Web3
from web3.types import RPCEndpoint, RPCResponse, TxParams, TxReceipt

from eulith_web3 import whitelists_v2
from eulith_web3.ace import get_ace_immediate_tx_typed_data, get_ace_immediate_tx_hash, AcePingResponse
from eulith_web3.common import INT_FEE_TO_FLOAT_DIVISOR, ETHEREUM_STATUS_SUCCESS
from eulith_web3.contract_bindings.safe.i_safe import ISafe
from eulith_web3.erc20 import TokenSymbol, EulithWETH, EulithERC20
from eulith_web3.eulith_service import EulithService
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.lightsim import LightSimulationProposal, LightSimulationHashInput, LightSimulationSubmitResponse
from eulith_web3.requests import EulithShortOnRequest, EulithShortOffRequest, EulithAaveV2StartLoanRequest, FlashRequest
from eulith_web3.response import raise_if_error, check_tx_receipt
from eulith_web3.safe_utils.transaction_data import get_enable_module_typed_data
from eulith_web3.signer import Signer
from eulith_web3.signing import normalize_signature
from eulith_web3.swap import EulithSwapRequest
from eulith_web3.uniswap import EulithUniswapV3Pool, EulithUniV3StartLoanRequest, EulithUniV3StartSwapRequest, \
    EulithUniV3SwapQuoteRequest, EulithUniswapPoolLookupRequest, UniswapPoolFee
from eulith_web3.whitelists import get_client_whitelist_typed_data, CurrentWhitelists, AcceptedEnableArmorSignature


class EulithWeb3(Web3):
    """
    The main drop-in replacement for Web3.py for users of Eulith

    :ivar eulith_service: internal methods to help with Eulith functionality
    :type eulith_data: eulith_web3.eulith_service.EulithService
    :ivar middleware_onion: web3py middleware
    :type middleware_onion: MiddlewareOnion
    :ivar v0: versioned namespace for Eulith interactions
    :type v0: v0
    """

    def __init__(self,
                 eulith_url: Union[URI, str],
                 eulith_token: str = None,
                 signing_middle_ware: Any = None,
                 private: bool = False,
                 **kwargs
                 ) -> None:
        """
        :param eulith_url: The Eulith endpoint; different endpoints will point this library to different chains.
        :type eulith_url: Union[URI, str]
        :param eulith_token: The refresh token used to authenticate the Eulith API
        :type eulith_token: str
        :param signing_middle_ware: The signing middleware used to sign transactions.
        :type signing_middle_ware: Any
        :param private: Flag that indicates whether transactions are routed through a private mempool
        :type private: bool
        :param kwargs: Varying number of keyword or named arguments that should be passed to the `Web3` class.
        :type kwargs: dict
        """

        auth_address = signing_middle_ware.address if signing_middle_ware else None

        self.eulith_service = EulithService(eulith_url, eulith_token, private, auth_address)
        kwargs.update({
            'provider': self.eulith_service.eulith_provider
        })
        super().__init__(**kwargs)

        self.wallet_address = None

        if signing_middle_ware:
            self.wallet_address = signing_middle_ware.address
            self.signer = signing_middle_ware.signer
            self.middleware_onion.add(signing_middle_ware)

        self.middleware_onion.add(eulith_atomic_middleware)
        self.middleware_onion.add(web3.middleware.request_parameter_normalizer)
        self.middleware_onion.add(web3.middleware.pythonic_middleware, "eulith_pythonic")
        self.v0 = v0(self)

        # Config for `wait_for_transaction_receipt_with_confirmations`
        self.default_confirmations = 3
        self._cached_confirmations_timeout_secs = None

    def terminate(self):
        self.eulith_service.terminate()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.terminate()

    def is_atomic(self):
        return self.eulith_service.is_atomic()

    def _eulith_send_atomic(self, params) -> RPCResponse:
        """
        This function is used to send an atomic transaction.

        :param params: A dictionary that contains the parameters required for the transaction.
        :type params: dict

        :return: A `RPCResponse` object that holds the response from the server.
        :rtype: RPCResponse
        """
        return self.eulith_service.send_transaction(params)

    def eulith_start_transaction(self, account: str, gnosis: str = "") -> None:
        """
        Begins an atomic transaction with your wallet as the authorized address,
        or optionally with your gnosis safe as msg.sender

        :param account: Your ETH wallet address
        :type account: str
        :param gnosis: Optional. Gnosis Safe address.
        :type gnosis: str, optional

        :raises TypeError: If the `account` is not a hex-formatted address or the `gnosis` is not a hex-formatted address.
        """

        if not is_hex_address(account):
            raise TypeError("account must be a hex-formatted address")
        if len(gnosis) > 0 and not is_hex_address(gnosis):
            raise TypeError("gnosis must either be blank or a hex-formatted address")
        self.eulith_service.start_transaction(account, gnosis)

    def eulith_commit_transaction(self) -> TxParams:
        """
        Serializes your pending atomic unit into a single transaction and returns the params to be signed

        :returns: The parameters of the committed transaction.
        :rtype: TxParams
        """

        return self.eulith_service.commit()

    def eulith_rollback_transaction(self):
        """
        Rollback a transaction, discard the current atomic transaction
        """

        self.eulith_service.rollback()

    def eulith_contract_address(self, account: str) -> str:
        """
        Retrieve the toolkit contract address bearing a one-to-one relationship to the `account` address.
        One toolkit contract is generated per wallet address.

        :param account: The hex formatted address of the account.
        :type account: str

        :returns: The hex formatted address of the contract. If no contract is found, an empty string is returned.
        :rtype: str

        :raises: TypeError: If `account` is not a hex formatted address.
        :raises: EulithRpcException: If an error occurs while making the request.
        """

        if not is_hex_address(account):
            raise TypeError("`account` must be a hex formatted address")

        status, contracts = self.eulith_service.get_deployed_execution_contracts()

        if not status:
            raise EulithRpcException(contracts)

        for c in contracts:
            if c['authorized_address'].lower() == account.lower():
                return c['contract_address']
        return ""

    def eulith_create_contract_if_not_exist(self, account: str) -> str:
        """
        Check if a toolkit contract exists for an account, and creates a new unique contract for the account
        if it doesn't already exist.

        :param account: The hex formatted address of the account.
        :type account: str

        :return: The hex formatted address of the contract.
        :rtype: str
        """

        c = self.eulith_contract_address(account)
        if c == "":
            c = self.eulith_create_contract(account)

        return c

    def eulith_create_contract(self, account: str,
                               contract_type: Optional[str] = None,
                               deploy_new_safe: bool = True) -> Union[str, TxParams]:
        """
        Creates a new toolkit or armor contract for the specified authorized wallet address (account).
        Toolkit contracts are deployed by us, we require the client to deploy their own armor contract.
        Hence, you might either get a contract address back as a string or a ready-to-sign TxParams
        object that you will need to sign and send yourself.

        :param deploy_new_safe: (bool) If true, deploy Armor and Safe at the same time. Otherwise, deploy armor only
        and specify the existing Safe at a later step. Only relevant if contract_type == 'armor'.
        :param account: The hex formatted address of the account.
        :type account: str
        :param contract_type: Optional contract type, defaults to toolkit contract.
                              Can also pass `armor` to generate new DeFi armor deployment transaction
        :type contract_type: Optional[str]

        :return: The hex formatted address of the newly created contract.
        :rtype: str
        """

        if not is_hex_address(account):
            raise TypeError("account must be a hex formatted address")

        if contract_type and contract_type != 'armor':
            raise TypeError(f"we currently only support toolkit and armor contracts. "
                            f"If you're trying to deploy a toolkit contract, leave contract_type blank. "
                            f"Unrecognized type: {contract_type}")

        response = self.eulith_service.create_new_contract(account, contract_type, deploy_new_safe)
        result = response['result']

        if not contract_type:
            tx_receipt = self.wait_for_transaction_receipt_with_confirmations(result['new_contract_tx_hash'])
            check_tx_receipt(tx_receipt)
            return result['contract_address']
        elif contract_type == 'armor':
            return result

    def eulith_swap_quote(self, params: EulithSwapRequest) -> [float, List[TxParams]]:
        """
        Gets a swap quote which contains information about the price and liquidity of assets. Returns the price of the
        quote and the transactions needed to execute the trade

        :param params: The parameters for the swap.
        :type params: EulithSwapRequest

        :returns: A tuple containing the price of the swap and a list of `TxParams` objects that represent
                  the transactions required for the swap.
        :rtype: Tuple[float, List[TxParams]]

        :raises: EulithRpcException: If there is an error in the response from the Ethereum node.
        """

        if not self.is_atomic():
            warn('Performing swaps outside an atomic context is deprecated', DeprecationWarning, stacklevel=2)

        status, result = self.eulith_service.swap_quote(params)

        if status:
            price = result.get('result', {}).get('price', 0.0)
            txs = result.get('result', {}).get('txs', [])
            return price, txs
        else:
            raise EulithRpcException(result)

    # If the eulith_data.atomic flag is not set, the function will wait for each transaction receipt using the
    # wait_for_transaction_receipt_with_confirmations method
    def eulith_send_multi_transaction(self, txs: [TxParams]) -> Optional[TxReceipt]:
        """
        Sends multiple transactions to the blockchain (or appends to the current atomic context) in a single batch,
        with each transaction executed one after the other (order is preserved).

        :param txs: List of `TxParams` objects, each representing a single transaction to be executed.
        :type txs: List[TxParams]
        """

        r = None

        for tx in txs:
            tx_hash = self.eth.send_transaction(tx)
            if not self.is_atomic():
                r = self.wait_for_transaction_receipt_with_confirmations(tx_hash)
                check_tx_receipt(r)

        return r

    def eulith_get_erc_token(self, symbol: TokenSymbol) -> Union[EulithERC20, EulithWETH]:
        """
        Obtains an instance of either the `EulithERC20` or `EulithWETH` class based on the provided token symbol.

        :param symbol: Symbol of the token to look up.
        :type symbol: TokenSymbol

        :returns: An instance of either the `EulithERC20` or `EulithWETH` class.
        :rtype: Union[EulithERC20, EulithWETH]

        :raises: EulithRpcException if there was an error with the RPC request
        """

        status, contract_address_or_error, decimals = self.eulith_service.lookup_token_symbol(symbol)
        if status:
            if symbol == TokenSymbol.WETH:
                return EulithWETH(self, contract_address_or_error)
            else:
                return EulithERC20(self, contract_address_or_error, decimals)
        else:
            raise EulithRpcException(contract_address_or_error)

    def parse_uni_quote_to_swap_request(self, res, fill_or_kill: bool, recipient: Optional[ChecksumAddress],
                                        pay_transfer_from: Optional[ChecksumAddress]) -> (float, UniswapPoolFee, EulithUniV3StartSwapRequest):
        """
        This function takes in the result of Uniswap swap quote and converts it into a swap request that can be passed
        to the `start_swap` function. Rather than manually extracting and formatting the necessary data,
        this function does the work for you. The parse_uni_quote_to_swap_request function returns an instance of the
        EulithUniV3StartSwapRequest class, which is the expected input type for the start_uniswap_v3_swap function.
        This makes it easy to pass the swap request directly to the start_uniswap_v3_swap function after it has been
        generated by the parse_uni_quote_to_swap_request function.

        :param res: The result of a Uniswap swap quote, which is a dictionary containing information about the swap.
        :type res: dict
        :param fill_or_kill: Default True doesn't allow any partial fills. If the order can't be filled
                             fully at the specified price, we revert.
        :type fill_or_kill: bool
        :param recipient: The Ethereum address of the recipient of the swap. This is an optional parameter.
        :type recipient: Optional[ChecksumAddress]
        :param pay_transfer_from: The Ethereum address of the account that will pay the sell_token to cover the swap.
        :type pay_transfer_from: Optional[ChecksumAddress]

        :returns: A tuple containing the price of the swap, the pool fee, and the swap request.
        :rtype: Tuple(float, UniswapPoolFee, EulithUniV3StartSwapRequest)
        """

        # Get the result of the Uniswap swap quote from the 'result' key of the res dictionary.
        result = res.get('result')

        price = result.get('price')
        sell_token_address = result.get('sell_token')
        sell_token = EulithERC20(self, sell_token_address)
        amount = result.get('amount')
        pool_address = result.get('pool_address')
        limit_price = result.get('sqrt_limit_price')
        fee = result.get('fee')
        true_for_amount_in = result.get('true_for_amount_in')

        if not true_for_amount_in:
            amount *= -1.0  # make negative if we want exact amount out

        swap_request = EulithUniV3StartSwapRequest(sell_token=sell_token,
                                                   amount=amount,
                                                   pool_address=self.to_checksum_address(pool_address),
                                                   fill_or_kill=fill_or_kill,
                                                   sqrt_limit_price=limit_price,
                                                   recipient=recipient,
                                                   pay_transfer_from=pay_transfer_from)

        return price, UniswapPoolFee(fee), swap_request

    def wait_for_transaction_receipt_with_confirmations(self, tx_hash: HexBytes, *, confirmations=0) -> TxReceipt:
        """
        Wait for a receipt for the transaction hash, optionally waiting for a number of confirmed blocks before
        returning.

        If calling this function from within `EulithWeb3` with `confirmations` greater than zero, prefer setting it to
        `confirmations=self.default_confirmations`. This is so that test code running against Anvil can set
        `self.default_confirmations` to 0 and avoid timing out waiting for blocks that will never come.

        :param tx_hash: The hash of the transaction to wait for.
        :type tx_hash: HexBytes
        :param confirmations: If greater than zero, this function will wait until
                              current_block_number == tx_block_number + confirmations
        :type confirmations: int

        :return: The receipt of the transaction.
        :rtype: TxReceipt
        """
        tx_receipt = self.eth.wait_for_transaction_receipt(tx_hash)

        if confirmations == 0:
            return tx_receipt

        attempts = 0
        max_attempts = 3
        timeout_secs = self._get_confirmation_timeout_secs()
        last_block_number_seen = None

        while True:
            attempts += 1

            current_block_number = self.eth.get_block_number()
            if current_block_number >= tx_receipt["blockNumber"] + confirmations:
                return tx_receipt

            if last_block_number_seen is not None and current_block_number > last_block_number_seen:
                # We have made progress, so we can reset the number of attempts.
                attempts = 0

            last_block_number_seen = current_block_number

            if attempts == max_attempts:
                raise EulithRpcException(f"failed to confirm transaction {tx_receipt['transactionHash']}")

            # We do not do exponential backoff here as we expect blocks to be created at a regular rate.
            time.sleep(timeout_secs)

    def _get_confirmation_timeout_secs(self) -> float:
        if self._cached_confirmations_timeout_secs is not None:
            return self._cached_confirmations_timeout_secs

        # The duration of time to wait for confirmation is strongly dependent on how quickly the chain creates new
        # blocks, which varies from chain to chain (e.g., Arbitrum is much faster than Ethereum mainnet). We take the
        # average time of the last 3 blocks, add half a second as a hedge, and cap the timeout at 30 seconds.
        current_block = self.eth.get_block("latest")
        current_block_minus_3 = self.eth.get_block(current_block["number"] - 3)
        timeout_secs = (current_block["timestamp"] - current_block_minus_3["timestamp"]) / 3.0
        timeout_secs += 0.5
        timeout_secs = min(timeout_secs, 30.0)

        self._cached_confirmations_timeout_secs = timeout_secs
        return self._cached_confirmations_timeout_secs


# Namespace
class v0:
    """
    Simplified and versioned access to the methods and functionality of `EulithWeb3`.
    """

    def __init__(self, ew3: EulithWeb3):
        """
        Initialize the `v0` class by taking an instance of `EulithWeb3` as an argument.

        :param ew3: An instance of the `EulithWeb3` class.
        :type ew3: EulithWeb3
        """

        self.ew3 = ew3

    def send_multi_transaction(self, txs: List[TxParams]) -> TxReceipt:
        """
        Sends multiple transactions to the blockchain (or appends to the current atomic context) in a single batch,
        with each transaction executed one after the other (order is preserved).

        :param txs: List of `TxParams` objects, each representing a single transaction to be executed.
        :type txs: List[TxParams]
        """

        return self.ew3.eulith_send_multi_transaction(txs)

    def start_atomic_transaction(self, account: str, gnosis: str = "") -> "AtomicContextManager":
        """
        Begins an atomic transaction with your wallet as the authorized address,
        or optionally with your gnosis safe as msg.sender

        Use the return value as a context manager to automatically discard the atomic transaction on error. You still need to explicitly commit.

            with ew3.v0.start_atomic_transaction(account):
               ...
               tx_params = ew3.v0.commit_atomic_transaction()

        :param account: Your ETH wallet address
        :type account: str
        :param gnosis: Optional. Gnosis Safe address.
        :type gnosis: str, optional

        :raises TypeError: If the `account` is not a hex-formatted address or the `gnosis` is not a hex-formatted address.
        """

        self.ew3.eulith_start_transaction(account, gnosis)
        return AtomicContextManager(self.ew3)

    def commit_atomic_transaction(self) -> TxParams:
        """
        Serializes your pending atomic unit into a single transaction and returns the params to be signed

        :returns: The parameters of the committed transaction.
        :rtype: TxParams
        """

        r = self.ew3.eulith_commit_transaction()
        if "message" in r:
            # TODO: armor-policy specific exception
            raise EulithRpcException(r)
        return r

    def commit_atomic_transaction_for_ace(self, signer: Signer) -> HexStr:
        """
        Serializes your pending atomic unit into an immediate transaction request for your ACE server, sends the
        unsigned transaction to the ACE server for signing, submits the signed transaction to the network, and returns
        the transaction hash.

        :param signer: The signer to sign the transaction request for ACE. Note that this signer is for authentication
                       of the transaction request with ACE, *not* for signing the transaction itself, which is done by
                       the private key on ACE.
        :type signer: Signer

        :returns: The hash of the atomic transaction.
        :rtype: HexStr
        """
        ace_immediate_tx = self.ew3.eulith_service.commit_for_ace()
        typed_data = get_ace_immediate_tx_typed_data(ace_immediate_tx)
        message_hash = get_ace_immediate_tx_hash(ace_immediate_tx)
        signed_typed_data = signer.sign_typed_data(typed_data, message_hash)
        serialized_signed_typed_data = normalize_signature(signed_typed_data)
        tx_hash, error = self.ew3.eulith_service.send_ace_transaction(serialized_signed_typed_data, ace_immediate_tx)
        if error:
            raise EulithRpcException(error)

        return tx_hash

    def rollback_atomic_transaction(self):
        """
        Rollback a transaction, discard the current atomic transaction
        """

        return self.ew3.eulith_rollback_transaction()

    def get_toolkit_contract_address(self, account: str) -> str:
        """
        Retrieve the toolkit contract address bearing a one-to-one relationship to the `account` address.
        One toolkit contract is generated per wallet address.

        :param account: The hex formatted address of the account.
        :type account: str

        :returns: The hex formatted address of the contract. If no contract is found, an empty string is returned.
        :rtype: str

        :raises: TypeError: If `account` is not a hex formatted address.
        :raises: EulithRpcException: If an error occurs while making the request.
        """

        return self.ew3.eulith_contract_address(account)

    def get_armor_and_safe_addresses(self, authorized_trading_address: str) -> (str, str):
        """
        Get the armor and safe addresses for a specific authorized_trading_address.

        This method retrieves the armor and safe addresses associated with the provided authorized_trading_address.

        :param authorized_trading_address: The Ethereum address (str) to search for.
        :return: A tuple (str, str) containing the contract address and safe address, respectively.
                 If no match is found, an empty tuple ('', '') is returned.

        :raises EulithRpcException: If there is an issue fetching the deployed execution contracts.
        """
        status, contracts = self.ew3.eulith_service.get_deployed_execution_contracts()

        if not status:
            raise EulithRpcException(contracts)

        for c in contracts:
            if c['authorized_address'].lower() == authorized_trading_address.lower():
                return c['contract_address'], c['safe_address']

        return '', ''

    def ensure_toolkit_contract(self, account: str) -> str:
        """
        Check if a toolkit contract exists for an account, and creates a new unique contract for the account
        if it doesn't already exist.

        :param account: The hex formatted address of the account.
        :type account: str

        :return: The hex formatted address of the contract.
        :rtype: str
        """

        return self.ew3.eulith_create_contract_if_not_exist(account)

    def create_toolkit_contract(self, account: str) -> str:
        """
        Creates a new toolkit contract for the specified authorized wallet address (account).

        :param account: The hex formatted address of the account.
        :type account: str

        :return: The hex formatted address of the newly created contract.
        :rtype: str
        """

        return self.ew3.eulith_create_contract(account)

    def get_armor_deploy_tx(self, account: str, deploy_new_safe: bool = True) -> TxParams:
        """
        Generates transaction to create a new armor and safe contract for the specified authorized wallet address (account).

        :param deploy_new_safe: (bool) If true, deploy Armor and Safe at the same time. Otherwise, deploy armor only
        and specify the existing Safe at a later step
        :param account: The hex formatted address of the account.
        :type account: str

        :return: The TxParams to sign and send in order to deploy your new armor and safe contracts.
        :rtype: TxParams
        """
        return self.ew3.eulith_create_contract(account, 'armor', deploy_new_safe)

    def ensure_valid_api_token(self):
        pass

    def get_erc_token(self, symbol: TokenSymbol) -> Union[EulithERC20, EulithWETH]:
        """
        Obtains an instance of either the `EulithERC20` or `EulithWETH` class based on the provided token symbol.

        :param symbol: Symbol of the token to look up.
        :type symbol: TokenSymbol

        :returns: An instance of either the `EulithERC20` or `EulithWETH` class.
        :rtype: Union[EulithERC20, EulithWETH]

        :raises: EulithRpcException if there was an error with the RPC request
        """

        return self.ew3.eulith_get_erc_token(symbol)

    def get_swap_quote(self, params: EulithSwapRequest) -> (float, List[TxParams]):
        """
        Gets a swap quote which contains information about the price and liquidity of assets. Returns the price of the
        quote and the transactions needed to execute the trade

        :param params: The parameters for the swap.
        :type params: EulithSwapRequest

        :returns: A tuple containing the price of the swap and a list of `TxParams` objects that represent
                  the transactions required for the swap.
        :rtype: Tuple(float, List[TxParams])

        :raises: EulithRpcException: If there is an error in the response from the Ethereum node.
        """

        if not self.ew3.is_atomic():
            warn('Performing swaps outside an atomic context is deprecated', DeprecationWarning)

        return self.ew3.eulith_swap_quote(params)

    def short_on(self, params: EulithShortOnRequest) -> float:
        """
        Request the Eulith API to open a levered short position on a token.

        :param params: Request parameters
        :type params: EulithShortOnRequest

        :return: the leverage of the short position
        :rtype: float

        :raises EulithRpcException: if the short position request fails
        """

        status, res = self.ew3.eulith_service.short_on(params)
        if status:
            leverage = res.get('result', {}).get('leverage', 0.0)
            return leverage
        else:
            raise EulithRpcException(res)

    def short_off(self, params: EulithShortOffRequest) -> float:
        """
        Makes a request to the Eulith API to unwind an existing short.

        :param params: Request parameters
        :type params: EulithShortOffRequest

        :return: The amount of released collateral.
        :rtype: float

        :raises EulithRpcException: If the short off request fails.
        """

        status, res = self.ew3.eulith_service.short_off(params)
        if status:
            released_collateral = res.get('result', {}).get('released_collateral', 0.0)
            return released_collateral
        else:
            raise EulithRpcException(res)

    def get_univ3_pool(self, params: EulithUniswapPoolLookupRequest) -> EulithUniswapV3Pool:
        """
        Looking up information about UniSwap V3 pools.

        :param params: Request parameters
        :type params: EulithUniswapPoolLookupRequest

        :return: An instance of `EulithUniswapV3Pool` class representing the Uniswap pool information.
        :rtype: EulithUniswapV3Pool

        :raises EulithRpcException: If the Uniswap V3 pool lookup fails or if the response from the server is unexpected.
        """

        status, res = self.ew3.eulith_service.lookup_univ3_pool(params)
        if status:
            result = res.get('result')
            if len(result) != 1:
                raise EulithRpcException(f"uniswap v3 pool lookup came back with an unexpected response: {result}")
            inner_result = result[0]

            token_zero = inner_result.get('token_zero')
            token_one = inner_result.get('token_one')
            fee = inner_result.get('fee')
            pool_address = inner_result.get('pool_address')
            return EulithUniswapV3Pool(self.ew3, self.ew3.to_checksum_address(pool_address), UniswapPoolFee(fee),
                                       self.ew3.to_checksum_address(token_zero), self.ew3.to_checksum_address(token_one))
        else:
            raise EulithRpcException(res)

    # returns fee (float) as percent: i.e. 0.001 = 0.1%
    def start_flash_loan(self, params: Union[EulithUniV3StartLoanRequest, EulithAaveV2StartLoanRequest]) -> float:
        """
        Initiates a flash loan. A flash loan is a type of loan that can be taken and repaid within a single transaction.
        This is a generic wrapper around Uniswap flash loans and Aave flash loans. You can pass either as the params
        and it will handle the request appropriately.

        :param params: The parameters required to initiate the flash loan.
        :type params: Union[EulithUniV3StartLoanRequest, EulithAaveV2StartLoanRequest]

        :return: The fee of the flash loan.
        :rtype: float

        :raises EulithRpcException: If there was an error with the request to the Ethereum node.
        """

        param_keys = params.keys()
        if 'borrow_token_a' in param_keys:
            status, res = self.ew3.eulith_service.start_uniswap_v3_loan(params)
        else:
            status, res = self.ew3.eulith_service.start_aave_v2_loan(params)

        if status:
            fee = int(res.get('result'), 16)
            return fee / INT_FEE_TO_FLOAT_DIVISOR
        else:
            raise EulithRpcException(res)

    def start_uni_swap(self, params: EulithUniV3StartSwapRequest) -> float:
        """
        Starting a uniswap V3 swap, a trade of one token for another on the Uniswap v3 protocol.

        This swap is its own atomic structure, meaning after you start a swap you have immediate access to the
        buy_tokens tokens. Transactions you send after starting the swap are included in the loan until you call
        finish_inner to close the swap and return one layer up in the nested atomic structure.

        :param params: Request parameters
        :type params: EulithUniV3StartSwapRequest

        :return: The fee of the Uniswap V3 swap, represented as a percentage.
        :rtype: float

        :raises EulithRpcException: If there was an error with the request to the Eulith server
        """

        status, res = self.ew3.eulith_service.start_uniswap_v3_swap(params)
        if status:
            fee = int(res.get('result'), 16)
            return fee / INT_FEE_TO_FLOAT_DIVISOR
        else:
            raise EulithRpcException(res)

    def get_univ3_best_price_quote(self, sell_token: EulithERC20, buy_token: EulithERC20, amount: float,
                                   true_for_amount_in: Optional[bool] = True, fill_or_kill: Optional[bool] = True,
                                   recipient: Optional[ChecksumAddress] = None,
                                   pay_transfer_from: Optional[ChecksumAddress] = None) -> (float, float, EulithUniV3StartSwapRequest):
        """
        Get the best price quote for a given token exchange on Uniswap V3.

        :param sell_token: The token that is to be sold.
        :type sell_token: EulithERC20
        :param buy_token: The token that is to be bought.
        :type buy_token: EulithERC20
        :param amount: The amount of the trade. If true_for_amount_in, this is the exact sell_amount in. Otherwise, the exact buy_amount out.
        :type amount: float
        :param true_for_amount_in: Whether the `amount` is in `sell_token` IN or `buy_token` OUT. Defaults to True.
        :type true_for_amount_in: Optional[bool]
        :param fill_or_kill: Default True doesn't allow any partial fills. If the order can't be filled fully at the specified price, revert.
        :type fill_or_kill: Optional[bool]
        :param recipient: The address of the recipient of the `buy_token`. Defaults to msg.sender
        :type recipient: Optional[ChecksumAddress]
        :param pay_transfer_from: The address to pay the sell side of the transaction. Defaults to msg.sender
        :type pay_transfer_from: Optional[ChecksumAddress]

        :return: A tuple containing three values:
            - price (float): The price of the `buy_token` in terms of `sell_token`.
            - fee (float): The fee for the transaction.
            - swap_request (EulithUniV3StartSwapRequest): The swap request details. These can be immediately used to execute the swap
        :rtype: Tuple(float, float, EulithUniV3StartSwapRequest)

        :raises EulithRpcException: If the status of the response from the `uniswap_v3_quote` method is False.
        """

        parsed_params = EulithUniV3SwapQuoteRequest(
            sell_token=sell_token,
            buy_token=buy_token,
            amount=amount,
            true_for_amount_in=true_for_amount_in,
            fee=None)
        status, res = self.ew3.eulith_service.uniswap_v3_quote(parsed_params)
        if status:
            price, fee, swap_request = self.ew3.parse_uni_quote_to_swap_request(res, fill_or_kill, recipient,
                                                                                pay_transfer_from)
            return price, fee / INT_FEE_TO_FLOAT_DIVISOR, swap_request
        else:
            raise EulithRpcException(res)

    def finish_inner(self) -> int:
        """
        Finishes the actual exchange of tokens in the swap or loan
        and returns the scope back to the outer atomic context. Remember, uniswap swaps and loans are SUB ATOMIC,
        meaning they have their own atomic structure that you can add to. When you're done with those transactions
        you need to close them with this method

        :returns: The number of transactions appended to the root atomic transaction
        :rtype: int

        :raises EulithRpcException: If there was an error with the RPC request.
        """

        status, res = self.ew3.eulith_service.finish_inner()
        if status:
            return int(res.get('result'), 16)
        else:
            raise EulithRpcException(res)

    # returns price (float), fee (float) as percent: i.e. 0.001 = 0.1%
    def start_flash(self, params: FlashRequest) -> (float, float):
        """
        A generic wrapper for any kind of flash transaction between any two tokens.


        :param params: The FlashRequest object containing information about the flash
        :type params: FlashRequest

        :returns: A tuple of two floats representing (price, fee) of the flash.
                  If take and pay are the same token, the price is 1.0
        :rtype: Tuple(float, float)
        """

        amount = params.get('take_amount')
        pay_transfer_from = params.get('pay_transfer_from', None)
        recipient = params.get('recipient', None)

        if params.get('take').address.lower() == params.get('pay').address.lower():
            fee = self.start_flash_loan(EulithUniV3StartLoanRequest(
                borrow_token_a=params.get('take'),
                borrow_amount_a=amount,
                borrow_token_b=None,
                borrow_amount_b=None,
                pay_transfer_from=pay_transfer_from,
                recipient=recipient
            ))

            return 1.0, fee
        else:
            price, fee, swap_request = self.get_univ3_best_price_quote(params.get('pay'),
                                                                       params.get('take'),
                                                                       amount,
                                                                       False, True, recipient, pay_transfer_from)
            fee = self.start_uni_swap(swap_request)
            return price, fee

    def pay_flash(self) -> int:
        """
        Pays and closes an open flash transaction.

        :returns: The number of transactions in the current atomic unit.
        :rtype: int
        """

        return self.finish_inner()

    def get_gmx_addresses(self) -> dict:
        """
        Returns the addresses of various contracts used by GMX protocol.

        :return: A dictionary with the contract addresses as values and their names as keys.
        :rtype: dict
        """
        status, result = self.ew3.eulith_service.get_gmx_addresses()
        if status:
            return result
        else:
            raise EulithRpcException(result)

    def deploy_new_armor(self, authorized_trading_address: ChecksumAddress,
                         existing_safe_address: Optional[ChecksumAddress] = None,
                         override_tx_params: TxParams = None) -> (str, str):
        """
        Deploys new armor contract using the current wallet configured in EulithWeb3. Note that the
        deploying wallet is NOT the same thing as the authorized_address on the armor contract. The user
        must choose the authorized trading address and pass it into this method.

        :param existing_safe_address: Deploy Armor into an existing safe instead of setting up a new one.
        :param authorized_trading_address: (str) The address authorized to execute trades through the new armor contract
        :type authorized_trading_address: ChecksumAddress
        :param override_tx_params: (TxParams, optional) The optional transaction parameters
                                   to override default values (like gas, gas_price, etc). Defaults to None.
        :type override_tx_params: TxParams
        :return: (tuple) A tuple of armor and safe addresses.
        :rtype: tuple

        :raises EulithRpcException: If submitting new armor tx hash to the server fails.
        :type: EulithRpcException
        """

        deploy_new_safe = existing_safe_address is None

        deploy_armor_tx = self.get_armor_deploy_tx(authorized_trading_address, deploy_new_safe)

        if override_tx_params:
            deploy_armor_tx.update(override_tx_params)

        h = self.ew3.eth.send_transaction(deploy_armor_tx)
        tx_receipt = self.ew3.wait_for_transaction_receipt_with_confirmations(
            h, confirmations=self.ew3.default_confirmations)
        check_tx_receipt(tx_receipt)

        accepted = self.ew3.eulith_service.submit_new_armor_hash(h.hex(), existing_safe_address)

        if not accepted:
            raise EulithRpcException("failed to submit new armor tx hash to the server")

        return self.get_armor_and_safe_addresses(authorized_trading_address)

    def submit_enable_module_signature(self, authorized_trading_address: str, signer: Signer) -> bool:
        """
        Submits a signature to enable a module for a safe. Note that the signature must come from a safe owner,
        but submitting a signature here DOES NOT add the signing address as an owner of the safe. The owners are
        specified in a later initialization step.

        :param authorized_trading_address: (str) The address authorized to execute trades through the new armor contract
        :type authorized_trading_address: ChecksumAddress
        :param signer: The signer to apply the signature to enable the armor module
        :type signer: Signer

        :return: Status true or false
        :rtype: bool
        """
        aa, sa = self.get_armor_and_safe_addresses(authorized_trading_address)
        safe = ISafe(self.ew3, self.ew3.to_checksum_address(sa))

        enable_module_tx = safe.enable_module(self.ew3.to_checksum_address(aa), override_tx_parameters={
            'gas': 0,
            'nonce': 0,
        })

        checksum_sa = self.ew3.to_checksum_address(sa)

        enable_data = enable_module_tx.get('data')
        nonce = safe.nonce()
        tx_hash = safe.get_transaction_hash(checksum_sa, 0, enable_data,
                                            0, 0, 0, 0, '0x0000000000000000000000000000000000000000',
                                            '0x0000000000000000000000000000000000000000', nonce)

        typed_data_payload = get_enable_module_typed_data(checksum_sa, self.ew3.eth.chain_id, enable_data)
        signature = signer.sign_typed_data(typed_data_payload, tx_hash)

        serialized_signature = normalize_signature(signature)

        status, result = self.ew3.eulith_service.submit_safe_signature(aa, str(signer.address),
                                                                       serialized_signature,
                                                                       f'0x{tx_hash.hex()}', 'enable_module')

        if not status:
            raise EulithRpcException(result)

        return True

    def enable_armor(self, auth_address: str, owner_threshold: int, owners: List[str],
                     override_tx_params: TxParams = None, has_ace: bool = False) -> bool:
        """
        Enable the armor for the contract by creating and submitting an initialization transaction. Note that
        the owners passed here MUST include the addresses of the signatures you submitted in the enable
        module step AND you must have submitted at least `owner_threshold` signatures in that step.

        :param auth_address: The authorized address of the Armor contract.
        :type auth_address: str
        :param owner_threshold: The minimum number of owner signatures required to authorize a transaction on the safe
        :type owner_threshold: int
        :param owners: A list of owner addresses that are allowed to manage the contract.
        :type owners: List[str]
        :param override_tx_params: Optional dictionary to override transaction parameters.
        :type override_tx_params: TxParams, optional
        :param has_ace: Whether ACE is enabled for the armor contract to be created
        :type has_ace: bool

        :return: True if the transaction is successfully submitted, False otherwise.
        :rtype: bool

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        status, result = self.ew3.eulith_service.get_enable_safe_tx(auth_address, owner_threshold, owners)
        if not status:
            raise EulithRpcException(result)

        if override_tx_params:
            result.update(override_tx_params)
        else:
            result.update({'from': self.ew3.wallet_address})

        h = self.ew3.eth.send_transaction(result)
        tx_receipt = self.ew3.wait_for_transaction_receipt_with_confirmations(
            h, confirmations=self.ew3.default_confirmations)
        check_tx_receipt(tx_receipt)

        status, error = self.ew3.eulith_service.submit_enable_safe_tx_hash(h.hex(), has_ace=has_ace)
        if error:
            raise EulithRpcException(error)
        return status

    def create_draft_client_whitelist(self, auth_address: str, addresses: List[str]) -> int:
        """
        DEPRECATED: Use create_draft_client_whitelist_v2 instead.

        Create a draft of the client whitelist for an Armor contract. This method only creates a draft; to enable the
        whitelist, use `submit_draft_client_whitelist_signature` to submit signatures from the threshold of owners of
        the Armor's safe.

        :param auth_address: The authorized trading key address associated with the whitelist.
        :type auth_address: str
        :param addresses: The list of addresses to include on the whitelist.
        :type addresses: List[str]

        :return: An opaque identifier for the whitelist, to be passed to `submit_draft_client_whitelist_signature`.
        :rtype: int

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        warn('This API is deprecated. Use create_draft_client_whitelist_v2 instead.', DeprecationWarning)

        list_id, error = self.ew3.eulith_service.create_draft_client_whitelist(auth_address, addresses)
        if error:
            raise EulithRpcException(error)

        return list_id

    def create_draft_client_whitelist_v2(self, auth_address: str, addresses: List[whitelists_v2.AddressOnChain]) -> int:
        """
        Create a draft of the client whitelist for an Armor contract. This method only creates a draft; to enable the
        whitelist, use `submit_draft_client_whitelist_signature_v2` to submit signatures from the threshold of owners of
        the Armor's safe.

        :param auth_address: The authorized trading key address associated with the whitelist.
        :param addresses: The list of addresses to include on the whitelist.

        :return: An opaque identifier for the whitelist, to be passed to `submit_draft_client_whitelist_signature_v2`.

        :raises EulithRpcException:
        """
        request = whitelists_v2.rpc.CreateRequest(auth_address=auth_address, addresses=addresses)
        response = self.ew3.eulith_service.create_draft_client_whitelist_v2(request)
        return response["list_id"]

    def append_to_draft_client_whitelist(self, auth_address: str, addresses: List[str], chain_id: Optional[int] = None) -> int:
        """
        DEPRECATED: Use append_to_draft_client_whitelist_v2 instead.

        Appends to an existing draft, or otherwise creates a new draft whitelist if no draft currently exists

        :param auth_address: The authorized trading key address associated with the whitelist.
        :type auth_address: str
        :param addresses: The list of addresses to include on the whitelist.
        :type addresses: List[str]
        :param chain_id: Append to the whitelist pertaining to the network with this chain id

        :return: An opaque identifier for the whitelist, to be passed to `submit_draft_client_whitelist_signature`.
        :rtype: int

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        warn('This API is deprecated. Use append_to_draft_client_whitelist_v2 instead.', DeprecationWarning)

        list_id, error = self.ew3.eulith_service.append_to_draft_client_whitelist(auth_address, addresses, chain_id)
        if error:
            raise EulithRpcException(error)

        return list_id

    def append_to_draft_client_whitelist_v2(self, auth_address: str, addresses: List[whitelists_v2.AddressOnChain]) -> whitelists_v2.Whitelist:
        """
        Appends to an existing draft, or otherwise creates a new draft whitelist if no draft currently exists

        :param auth_address: The authorized trading key address associated with the whitelist.
        :param addresses: The list of addresses to include on the whitelist.

        :raises EulithRpcException:
        """
        request = whitelists_v2.rpc.AppendRequest(auth_address=auth_address, addresses=addresses)
        response = self.ew3.eulith_service.append_to_draft_client_whitelist_v2(request)
        return response["draft"]

    def submit_draft_client_whitelist_signature(self, list_id: int, signer: Signer) -> bool:
        """
        DEPRECATED: Use submit_draft_client_whitelist_signature_v2 instead.

        Submit a signature for a draft client whitelist in order to enable it once signatures have been received from
        the threshold of owners.

        :param list_id: The ID of the whitelist, as returned by `create_draft_client_whitelist`.
        :type list_id: int
        :param signer: The signer to sign the whitelist hash with. Must be an owner of the safe.
        :type signer: Signer

        :return: True if the whitelist was enabled, False otherwise.
        :rtype: bool

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        warn('This API is deprecated. Use submit_draft_client_whitelist_signature_v2 instead.', DeprecationWarning)

        hsh, error = self.ew3.eulith_service.get_draft_client_whitelist_hash(list_id)
        if error:
            raise EulithRpcException(error)

        typed_data_payload = get_client_whitelist_typed_data(hsh["hash_input"])
        signature = signer.sign_typed_data(typed_data_payload, HexBytes(hsh["hash"]))
        serialized_signature = normalize_signature(signature)

        status, error = self.ew3.eulith_service.submit_draft_client_whitelist_signature(list_id, signer.address, serialized_signature, hsh["hash"])
        if error:
            raise EulithRpcException(error)

        return status

    def submit_draft_client_whitelist_signature_v2(self, list_id: int, signer: Signer) -> whitelists_v2.rpc.SubmitSignatureResponse:
        """
        Submit a signature for a draft client whitelist in order to enable it once signatures have been received from
        the threshold of owners.

        :param list_id: The ID of the whitelist, as returned by `create_draft_client_whitelist_v2`.
        :param signer: The signer to sign the whitelist hash with. Must be an owner of the safe.

        :raises EulithRpcException:
        """
        hash_request = whitelists_v2.rpc.GetHashRequest(list_id=list_id)
        hash_response = self.ew3.eulith_service.get_draft_client_whitelist_hash_v2(hash_request)

        typed_data = whitelists_v2.HashInputEip712(hash_response["hash_input"]).typed_data()
        signature = signer.sign_typed_data(typed_data, HexBytes(hash_response["hash"]))
        serialized_signature = normalize_signature(signature)

        submit_request = whitelists_v2.rpc.SubmitSignatureRequest(list_id=list_id, signer_address=signer.address, signature=serialized_signature,
                                                                  hash=hash_response["hash"])
        return self.ew3.eulith_service.submit_draft_client_whitelist_signature_v2(submit_request)

    def get_current_client_whitelist(self, auth_address: str, chain_id: Optional[int] = None) -> CurrentWhitelists:
        """
        DEPRECATED: Use get_current_client_whitelist_v2 instead.

        Retrieve the current draft and published versions of the auth address's client whitelist.

        :param auth_address: The owner of the whitelist to retrieve.
        :type auth_address: str
        :param chain_id: Get current whitelist pertaining to the network with this chain id

        :return: The client's active and draft whitelists, either of which may be null.
        :rtype: CurrentWhitelists

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        warn('This API is deprecated. Use get_current_client_whitelist_v2 instead.', DeprecationWarning)

        whitelist, error = self.ew3.eulith_service.get_current_client_whitelist(auth_address, chain_id)
        if error:
            raise EulithRpcException(error)

        return whitelist

    def get_current_client_whitelist_v2(self, auth_address: str) -> whitelists_v2.rpc.GetCurrentResponse:
        """
        Retrieve the current draft and published versions of the auth address's client whitelist.

        :param auth_address: The owner of the whitelist to retrieve.

        :raises EulithRpcException:
        """
        request = whitelists_v2.rpc.GetCurrentRequest(auth_address=auth_address)
        return self.ew3.eulith_service.get_current_client_whitelist_v2(request)

    def delete_draft_client_whitelist_v2(self, list_id: int) -> whitelists_v2.Whitelist:
        """
        Delete a draft client whitelist.

        :param list_id: The ID of the whitelist, as returned by `create_draft_client_whitelist_v2`.

        :return: the whitelist that was deleted

        :raises EulithRpcException:
        """
        request = whitelists_v2.rpc.DeleteRequest(list_id=list_id)
        response = self.ew3.eulith_service.delete_draft_client_whitelist_v2(request)
        return response["deleted"]

    def propose_light_simulation(self, safe_address: str, chain_id: int, to_enable: bool) -> LightSimulationProposal:
        """
        Propose that light simulation be enabled/disabled for transactions on the Safe.

        The proposal must be approved by a threshold of Safe owners, using `submit_light_simulation_signature`.

        :param safe_address: the Safe
        :param chain_id: the chain the Safe is deployed on
        :param to_enable: True to enable, False to disable
        :return: the proposal
        """
        response, error = self.ew3.eulith_service.propose_light_simulation(safe_address, chain_id, to_enable)
        if error:
            raise EulithRpcException(error)

        return LightSimulationProposal.from_json(response["proposal"])

    def submit_light_simulation_signature(self, signer: Signer, proposal_id: int) -> LightSimulationSubmitResponse:
        """
        Submit a Safe owner's approval for a light simulation proposal.

        A threshold of Safe owners must approve the proposal for it to go into effect.

        :param signer: a Safe owner
        :param proposal_id: the ID of the proposal, as returned by `propose_light_simulation`
        :return: the proposal and whether it was approved
        """
        hash_response, error = self.ew3.eulith_service.get_light_simulation_proposal_hash(proposal_id)
        if error:
            raise EulithRpcException(error)

        hash_input = LightSimulationHashInput.from_json(hash_response["hash_input"])
        typed_data_payload = hash_input.typed_data()
        signature = signer.sign_typed_data(typed_data_payload, HexBytes(hash_response["hash"]))
        serialized_signature = normalize_signature(signature)

        response, error = self.ew3.eulith_service.submit_light_simulation_signature(proposal_id, signer.address, serialized_signature,
                                                                                    hash_response["hash"])
        if error:
            raise EulithRpcException(error)

        return LightSimulationSubmitResponse.from_json(response)

    def get_active_light_simulation_proposals(self) -> List[LightSimulationProposal]:
        """
        Get all active light simulation proposals for the user.

        Active proposals are those that are neither deleted nor approved. Proposals start in the 'active' state.

        :return: the list of proposals
        """
        response, error = self.ew3.eulith_service.get_active_light_simulation_proposals()
        if error:
            raise EulithRpcException(error)

        return [LightSimulationProposal.from_json(p) for p in response["proposals"]]

    def delete_light_simulation_proposal(self, proposal_id: int) -> LightSimulationProposal:
        """
        Delete a light simulation proposal.

        :param proposal_id: the ID of the proposal to delete
        :return: the deleted proposal
        """
        response, error = self.ew3.eulith_service.delete_light_simulation_proposal(proposal_id)
        if error:
            raise EulithRpcException(error)

        return LightSimulationProposal.from_json(response["proposal"])

    def get_accepted_enable_armor_signatures(self, auth_address: str) -> List[AcceptedEnableArmorSignature]:
        """
        Retrieve the current draft and published versions of the user's client whitelist.

        :param auth_address: The authorized trading address of the armor to query
        :type auth_address: str

        :return: A list of all the currently accepted enable armor signatures
        :rtype: List[AcceptedEnableArmorSignature]

        :raises EulithRpcException: If there is an issue with the Eulith RPC request.
        """
        signatures, error = self.ew3.eulith_service.get_accepted_enable_armor_signatures(auth_address)
        if error:
            raise EulithRpcException(error)

        return signatures

    def ping_ace(self, auth_address: str) -> AcePingResponse:
        """
        Ping the ACE server associated with the current auth address.

        :return: The response from the ACE server
        :rtype: Optional[AcePingResponse]
        """
        ping_response, error = self.ew3.eulith_service.ping_ace(auth_address)
        if error:
            raise EulithRpcException(error)

        return ping_response

    def check_tx_receipt_diag(self, tx_receipt: TxReceipt):
        if tx_receipt["status"] != ETHEREUM_STATUS_SUCCESS:
            self.ew3.eulith_service.eulith_provider.make_request("trace_transaction", [tx_receipt['transactionHash'].hex()])
            hash = tx_receipt['transactionHash'].hex()
            raise EulithRpcException(f"transaction reverted ({hash})")


def eulith_atomic_middleware(
        make_request: Callable[[RPCEndpoint, Any], Any], web3: "Web3") -> Callable[[RPCEndpoint, Any], RPCResponse]:
    def middleware(method: RPCEndpoint, params: Any) -> RPCResponse:
        if method != "eth_sendTransaction" or not web3.is_atomic():
            resp = make_request(method, params)
            raise_if_error(resp)
            return resp

        return cast(EulithWeb3, web3)._eulith_send_atomic(params)

    return middleware


class AtomicContextManager:
    def __init__(self, ew3: EulithWeb3) -> None:
        self.ew3 = ew3

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        # ok to unconditionally rollback because it's a no-op if already committed
        self.ew3.v0.rollback_atomic_transaction()
