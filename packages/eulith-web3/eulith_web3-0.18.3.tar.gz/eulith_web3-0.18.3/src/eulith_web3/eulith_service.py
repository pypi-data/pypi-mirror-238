import urllib.parse
import uuid
from typing import cast, Optional, List, Dict, Union

import requests
from eth_typing import URI, ChecksumAddress, HexStr
from web3.types import RPCResponse, RPCEndpoint, TxParams

from eulith_web3 import whitelists_v2
from eulith_web3.ace import AceImmediateTx, AcePingResponse
from eulith_web3.erc20 import EulithERC20, TokenSymbol
from eulith_web3.exceptions import EulithRpcException
from eulith_web3.pendle import PendleMarketSymbol
from eulith_web3.requests import EulithShortOnRequest, EulithShortOffRequest, EulithAaveV2StartLoanRequest
from eulith_web3.response import raise_if_error
from eulith_web3.swap import EulithSwapRequest, EulithSwapProvider, EulithLiquiditySource
from eulith_web3.uniswap import EulithUniV3StartLoanRequest, EulithUniV3StartSwapRequest, EulithUniV3SwapQuoteRequest, \
    EulithUniswapPoolLookupRequest
from eulith_web3.websocket import EulithWebsocketProvider, SubscribeRequest, EulithWebsocketRequestHandler, \
    SubscriptionHandle
from eulith_web3.whitelists import ClientWhitelistHash, CurrentWhitelists, AcceptedEnableArmorSignature


def ensure_formatted_ws_url(eulith_url: str) -> str:
    if eulith_url.startswith("http://"):
        return "ws" + eulith_url[4:]
    elif eulith_url.startswith("https://"):
        return "wss" + eulith_url[5:]
    return eulith_url


def get_headers(token: str) -> Dict:
    """
    Function returns a dictionary of headers to be used in an HTTP request.

    :param token: The bearer token to be included in the Authorization header.
    :type token: str

    :return: A dictionary of headers to be used in an HTTP request.
    :rtype: Dict

    Example:
        get_headers("https://www.exampletokenwebsite.com", "token123")
    Returns: {
        'Authorization': 'Bearer token123',
        'Content-Type': 'application/json'
    }
    """

    headers = {
        'Authorization': 'Bearer ' + token,
        'Content-Type': 'application/json'
    }

    return headers


def add_params_to_url(url: str, params) -> str:
    """
    This function takes in a URL and a dictionary of parameters and adds the parameters to the URL as query parameters.
    Eulith relies on query params to specify your atomic tx id or gnosis safe address, for example.

    :param url: The URL to which the parameters will be added.
    :type url: str
    :param params: The dictionary of parameters that will be added to the URL.
    :type params: Dict

    :return: The URL with the added parameters as query parameters.
    :rtype: str

    Example:
        add_params_to_url("https://www.example.com", {"param1": "value1", "param2": "value2"})
        Returns: "https://www.example.com?param1=value1&param2=value2"
    """

    url_parts = urllib.parse.urlparse(url)
    query = dict(urllib.parse.parse_qsl(url_parts.query))
    query.update(params)

    return url_parts._replace(query=urllib.parse.urlencode(query)).geturl()


class AtomicTxParams:
    def __init__(self, tx_id: str, safe_address: str, trading_key: str):
        self.tx_id = tx_id
        self.safe_address = safe_address
        self.trading_key = trading_key

    def inject_in_body(self, post_body: Dict):
        post_body.update({
            'auth_address': self.trading_key
        })

        if self.tx_id:
            post_body.update({
                'atomic_tx_id': self.tx_id,
            })

        if self.safe_address:
            post_body.update({
                'gnosis_address': self.safe_address
            })


class EulithService:
    """
    Embedded class to represent data of the Eulith API and provides methods to interact with the API.

    :ivar eulith_url: URL of the Eulith API
    :type eulith_url: URI
    :ivar eulith_token: Refresh token for the Eulith API
    :type eulith_token: str
    :ivar private: bool switches on whether transactions are routed through a private mempool or not
    :type private: bool
    :ivar atomic: Boolean indicating if the current transaction is atomic
    :type atomic: bool
    :ivar tx_id: ID of the current transaction
    :type tx_id: str
    :ivar eulith_provider: HTTP provider instance to make requests to the Eulith API
    :type eulith_provider: WebsocketProviderV2
    """

    def __init__(self, eulith_url: str, eulith_token: str, private: bool = False, auth_address: Optional[str] = None) -> None:
        """
        :param eulith_url: URL of the Eulith API
        :type eulith_url: Union[URI, str]
        :param eulith_token: Refresh token for the Eulith API
        :type eulith_token: str
        """

        self.token = eulith_token

        url_params = {}

        if private:
            url_params['private'] = 'true'

        if auth_address:
            url_params['auth_address'] = auth_address

        self.eulith_url = URI(add_params_to_url(ensure_formatted_ws_url(eulith_url), url_params))

        self.atomic_params: Optional[AtomicTxParams] = None
        self.headers = get_headers(self.token)

        self.eulith_provider = EulithWebsocketProvider(uri=self.eulith_url, bearer_token=self.token)

    def is_atomic(self):
        if not self.atomic_params:
            return False

        return self.atomic_params.tx_id

    def send_transaction(self, params) -> RPCResponse:
        """
        Sends a transaction to the blockchain via the Eulith RPC provider, handling exceptions that may occur
        when making a request with the make_request method from the HTTPProvider class.

        :param params: Dictionary containing the parameters for the transaction
        :type params: dict

        :returns: The response from the Eulith API
        :rtype: RPCResponse

        :raises EulithRpcException: If there was an error with the RPC request
        """

        params = list(params)

        if self.atomic_params and len(params) > 0:
            self.atomic_params.inject_in_body(params[0])

        resp = self.eulith_provider.make_request(RPCEndpoint("eth_sendTransaction"), params)
        raise_if_error(resp)
        return resp

    def create_new_contract(self, trading_key: str, contract_type: Optional[str] = None, deploy_new_safe: bool = True):
        params = {
            'authorized_address': trading_key
        }

        if contract_type:
            params['contract_type'] = contract_type

        if not deploy_new_safe:
            params['safe_already_exists'] = True

        response = self.eulith_provider.make_request(RPCEndpoint("eulith_new_contract"), [params])
        raise_if_error(response)
        return response

    def start_transaction(self, trading_key: str, safe_address: str):
        """
        Starts a Eulith atomic transaction. Anything transaction you send within an atomic transaction
        will get confirmed as a single unit. Everything operation in the unit will succeeds,
        or the whole transactions fails. The state of the blockchain is frozen while your atomic transaction
        is processing; there can't be any sandwiches, state changes, etc, in between your atomic operations.
        """

        self.atomic_params = AtomicTxParams(str(uuid.uuid4()), safe_address, trading_key)

    def commit(self) -> TxParams:
        """
        Serializes the current pending atomic tx into a single transactional unit, and returns
        the unsigned params. To get the atomic transaction on-chain, you need to sign these params
        and submit the transaction as a signed payload. The Eulith API handles this automatically for you.

        :returns: A dictionary containing the transaction parameters.
        :rtype: TxParams

        :raises EulithRpcException: If the request fails or the response from the server contains an error.
        """

        if not self.is_atomic():
            raise EulithRpcException('cannot commit outside atomic context')

        params = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        response = self.eulith_provider.make_request(RPCEndpoint("eulith_commit"), [params])
        raise_if_error(response)
        return cast(TxParams, response['result'])

    def commit_for_ace(self) -> AceImmediateTx:
        """
        Variant of `commit` which returns a typed data payload rather than an unsigned transaction. The client should
        then sign the payload and send it back to the server via the `send_ace_transaction` method.

        Use this method when you are using an ACE server for signing rather than signing transactions directly from the
        Python client.

        :returns: The typed data to be signed by the client.
        :rtype: AceImmediateTx
        """

        params = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        response = self.eulith_provider.make_request(RPCEndpoint("eulith_commit_for_ace"), [params])
        raise_if_error(response)
        return AceImmediateTx.from_json(response["result"])

    def rollback(self):
        """
        Rollback here refers to discarding txs added to the atomic tx bundle during the call.
        """

        if not self.is_atomic():
            return

        params = {}
        self.atomic_params.inject_in_body(params)
        self.atomic_params = None

        response = self.eulith_provider.make_request(RPCEndpoint("eulith_discard_atomic_transactions"), [params])
        raise_if_error(response)
        return

    def swap_quote(self, params: EulithSwapRequest) -> (bool, RPCResponse):
        """
        Makes a request to the Eulith API to obtain a quote for a token swap. The returned quote is by default
        the best price across multiple DEX aggregators.

        :param params: Request parameters
        :type params: EulithSwapRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            sell_token: EulithERC20
            buy_token: EulithERC20
            sell_amount: float
            recipient: Optional[ChecksumAddress]
            route_through: Optional[EulithSwapProvider]
            slippage_tolerance: Optional[float]
            liquidity_source: Optional[EulithLiquiditySource]

            sell_address = params.get('sell_token').address
            buy_address = params.get('buy_token').address
            parsed_params = {
                'sell_token': sell_address,
                'buy_token': buy_address,
                'sell_amount': params.get('sell_amount')
            }
            recipient = params.get('recipient', None)
            route_through = params.get('route_through', None)
            liquidity_source = params.get('liquidity_source', None)
            slippage_tolerance = params.get('slippage_tolerance', None)

            if recipient:
                parsed_params['recipient'] = recipient
            if route_through:
                parsed_params['route_through'] = route_through
            if liquidity_source:
                parsed_params['liquidity_source'] = liquidity_source
            if slippage_tolerance:
                parsed_params['slippage_tolerance'] = slippage_tolerance

            if self.is_atomic():
                rpc_method = "eulith_swap_atomic"
                self.atomic_params.inject_in_body(parsed_params)
            else:
                rpc_method = "eulith_swap"

            response = self.eulith_provider.make_request(RPCEndpoint(rpc_method), [parsed_params])
            raise_if_error(response)

            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def short_on(self, params: EulithShortOnRequest) -> (bool, RPCResponse):
        """
        Request the Eulith API to open a levered short position on a token.

        :param params: Request params
        :type params: EulithShortOnRequest
            collateral_token (EulithERC20) -- ERC20 token to be used as collateral.
            short_token (EulithERC20) -- ERC20 token to be shorted.
            collateral_amount (float) -- A float representing the amount of the `collateral_token` to be used.

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            # Extract the addresses of the collateral and short tokens from the `params` argument.
            collateral_address = params.get('collateral_token').address
            short_address = params.get('short_token').address

            # Create a dictionary of parameters for the request with the token addresses and collateral amount.
            parsed_params = {
                'collateral_token': collateral_address,
                'short_token': short_address,
                'collateral_amount': params.get('collateral_amount')
            }

            if self.atomic_params:
                self.atomic_params.inject_in_body(parsed_params)
            else:
                return False, RPCResponse(error='cannot call short on outside of an atomic context')

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_short_on"), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def short_off(self, params: EulithShortOffRequest) -> (bool, RPCResponse):
        """
        Makes a request to the Eulith API to unwind an existing short.

        :param params: Request params
        :type params: EulithShortOffRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            collateral_address = params.get('collateral_token').address
            short_address = params.get('short_token').address

            parsed_params = {
                'collateral_token': collateral_address,
                'short_token': short_address,
                'repay_short_amount': params.get('repay_short_amount'),
                'true_for_unwind_a': params.get('true_for_unwind_a', True)
            }

            if self.atomic_params:
                self.atomic_params.inject_in_body(parsed_params)
            else:
                return False, RPCResponse(error='cannot call short on outside of an atomic context')

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_short_off"), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def start_uniswap_v3_loan(self, params: EulithUniV3StartLoanRequest) -> (bool, RPCResponse):
        """
        Makes a request to start a loan in Uniswap V3. This loan is its own atomic structure, meaning
        after you start a loan you have immediate access to the borrow tokens. Transactions you send
        after starting the loan are included in the loan until you call finish_inner to close the loan and
        return one layer up in the nested atomic structure.

        Note that loans have to execute in an atomic transaction. You can't execute a loan on its own.

        :param params: Request params
        :type params: EulithUniV3StartLoanRequest

        :returns: A tuple of a boolean indicating success and an `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            borrow_token_a = params.get('borrow_token_a').address
            borrow_amount_a = params.get('borrow_amount_a')
            borrow_token_b = params.get('borrow_token_b', None)
            borrow_amount_b = params.get('borrow_amount_b', None)
            pay_transfer_from = params.get('pay_transfer_from', None)
            recipient = params.get('recipient', None)

            parsed_params = {
                'borrow_token_a': borrow_token_a,
                'borrow_amount_a': borrow_amount_a
            }

            if borrow_token_b:
                parsed_params['borrow_token_b'] = borrow_token_b.address
            if borrow_amount_b:
                parsed_params['borrow_amount_b'] = borrow_amount_b
            if pay_transfer_from:
                parsed_params['pay_transfer_from'] = pay_transfer_from
            if recipient:
                parsed_params['recipient'] = recipient

            if self.atomic_params:
                self.atomic_params.inject_in_body(parsed_params)
            else:
                return False, RPCResponse(error='cannot call short on outside of an atomic context')

            response = self.eulith_provider.make_request(RPCEndpoint('eulith_start_uniswapv3_loan'), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def start_uniswap_v3_swap(self, params: EulithUniV3StartSwapRequest) -> (bool, RPCResponse):
        """
        Starting a uniswap V3 swap, a trade of one token for another on the Uniswap v3 protocol.

        This swap is its own atomic structure, meaning after you start a swap you have immediate access to the
        buy_tokens tokens. Transactions you send after starting the swap are included in the loan until you call
        finish_inner to close the swap and return one layer up in the nested atomic structure.

        :param params: Request params
        :type params: EulithUniV3StartSwapRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            sell_token = params.get('sell_token').address
            amount = params.get('amount')
            pool_address = params.get('pool_address')
            fill_or_kill = params.get('fill_or_kill')
            sqrt_limit_price = params.get('sqrt_limit_price')
            recipient = params.get('recipient', None)
            pay_transfer_from = params.get('pay_transfer_from', None)

            parsed_params = {
                'sell_token': sell_token,
                'amount': amount,
                'pool_address': pool_address,
                'fill_or_kill': fill_or_kill,
                'sqrt_limit_price': sqrt_limit_price
            }

            if recipient:
                parsed_params['recipient'] = recipient

            if pay_transfer_from:
                parsed_params['pay_transfer_from'] = pay_transfer_from

            if self.atomic_params:
                self.atomic_params.inject_in_body(parsed_params)
            else:
                return False, RPCResponse(error='must call in atomic context')

            response = self.eulith_provider.make_request(RPCEndpoint('eulith_start_uniswapv3_swap'), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def start_aave_v2_loan(self, params: EulithAaveV2StartLoanRequest) -> (bool, RPCResponse):
        """
        Start a loan using the Aave V2 protocol

        :param params: Request params
        :type params: EulithAaveV2StartLoanRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            tokens = params.get('tokens')
            token_params = []
            for t in tokens:
                token_params.append({
                    'token_address': t.get('token_address').address,
                    'amount': t.get('amount')
                })

            parsed_params = {
                'tokens': token_params,
            }

            if self.atomic_params:
                self.atomic_params.inject_in_body(parsed_params)
            else:
                return False, RPCResponse(error='must call in atomic context')

            response = self.eulith_provider.make_request(RPCEndpoint('eulith_start_aavev2_loan'), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def finish_inner(self) -> (bool, RPCResponse):
        """
        Uniswap & Aave flash loans and swaps are their own "sub atomic" structures. So when you start
        one of those actions, you have to finish it by calling this method. "Finishing" here means you close the
        transaction and append it to the outer atomic structure.

        :return: A tuple that contains a boolean indicating if the request was successful, and a `RPCResponse`
        :rtype: (bool, RPCResponse)

        :raises HTTPError: In case of an error in the HTTP request.
        """
        params = {}

        if self.atomic_params:
            self.atomic_params.inject_in_body(params)
        else:
            return False, RPCResponse(error='must call in atomic context')

        try:
            response = self.eulith_provider.make_request(RPCEndpoint('eulith_finish_inner'), [params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def uniswap_v3_quote(self, params: EulithUniV3SwapQuoteRequest) -> (bool, RPCResponse):
        """
        Request a quote from Uniswap V3 for a swap between two tokens.

        :param params: Request params
        :type params: EulithUniV3SwapQuoteRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            parsed_params = {
                'sell_token': params.get('sell_token').address,
                'buy_token': params.get('buy_token').address,
                'amount': params.get('amount'),
                'true_for_amount_in': params.get('true_for_amount_in', True)
            }

            fee = params.get('fee', None)
            if fee:
                parsed_params['fee'] = fee.value

            response = self.eulith_provider.make_request(RPCEndpoint('eulith_uniswapv3_quote'), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def lookup_univ3_pool(self, params: EulithUniswapPoolLookupRequest) -> (bool, RPCResponse):
        """
        Looking up information about UniSwap V3 pools.

        :param params: Request params
        :type params: EulithUniswapPoolLookupRequest

        :returns: A tuple of a boolean indicating success and a `RPCResponse` object.
        :rtype: (bool, RPCResponse)

        :raises: requests.exceptions.HTTPError if there was an error making the request.
        """

        try:
            parsed_params = {
                'token_a': params.get('token_a').address,
                'token_b': params.get('token_b').address,
                'fee': params.get('fee').value
            }
            response = self.eulith_provider.make_request(RPCEndpoint('eulith_uniswapv3_pool_lookup'), [parsed_params])
            raise_if_error(response)
            return True, response
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def lookup_token_symbol(self, symbol: TokenSymbol) -> (bool, ChecksumAddress, int):
        """
        Look up token information by ERC20 symbol.

        :param symbol: Token symbol to look up.
        :type symbol: TokenSymbol

        :return: A tuple containing a boolean indicating the success of the request,
                 the contract address of the token, and the number of decimals of the token.
        :rtype: tuple(bool, ChecksumAddress, int)
        """

        try:
            res = self.eulith_provider.make_request(RPCEndpoint("eulith_erc_lookup"), [{'symbol': symbol}])
            raise_if_error(res)
            parsed_res = res.get('result', [])
            if len(parsed_res) != 1:
                return False, RPCResponse(error=f"unexpected response for {symbol} lookup, token isn't recognized"), -1
            return True, parsed_res[0].get('contract_address'), parsed_res[0].get('decimals')
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e)), -1

    def get_gmx_addresses(self) -> (bool, dict):
        """
        Returns a dictionary of GMX contract addresses.

        :return: A tuple containing a boolean indicating success or failure, and a dictionary of GMX contract addresses.
        :rtype: tuple
        """
        try:
            res = self.eulith_provider.make_request(RPCEndpoint("eulith_gmx_address_lookup"), None)
            raise_if_error(res)
            result = res.get('result', {})
            return True, result
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def get_gmx_positions(self, wallet_address: ChecksumAddress, collateral_tokens: List[EulithERC20],
                          index_tokens: List[EulithERC20], is_long: List[bool]) -> (bool, dict):
        """
        Get positions of the given wallet for a given set of collateral and index tokens and directions

        :param wallet_address: The address to get the positions of
        :type wallet_address: ChecksumAddress
        :param collateral_tokens: List of the collateral tokens the positions belong to
        :type collateral_tokens: List[EulithERC20]
        :param index_tokens: List of the index tokens the positions belong to
        :type index_tokens: List[EulithERC20]
        :param is_long: List of the direction of each position True is long False is short
        :type is_long: List[bool]
        :return: A tuple with the status and result
        :rtype: (bool, dict)
        """
        try:
            collateral_addresses = []
            index_addresses = []

            for t in collateral_tokens:
                collateral_addresses.append(t.address)

            for t in index_tokens:
                index_addresses.append(t.address)

            params = {
                'wallet_address': wallet_address,
                'collateral_addresses': collateral_addresses,
                'index_addresses': index_addresses,
                'is_long': is_long
            }

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_gmx_position_lookup"), [params])
            raise_if_error(res)
            result = res.get('result', {})
            return True, result
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def request_gmx_mint_glp(self, pay_token: EulithERC20, pay_amount: float, slippage: Optional[float]) -> (bool, dict):
        """
        Requests to mint GLP tokens by providing pay_token and pay_amount.
        Returns minimum GLP tokens to be minted, minimum USD value and transactions to be executed to take the position.
        We handle some of this logic server-side to keep the client light and simple.

        :param pay_token: The token to pay with
        :type pay_token: EulithERC20
        :param pay_amount: The amount of pay_token to use
        :type pay_amount: float
        :param slippage: The slippage tolerance as a percentage, defaults to None, in percentage units i.e. 0.01
        :type slippage: Optional[float]
        :return: A tuple containing whether the request was successful and the resulting dictionary
        :rtype: Tuple[bool, dict]
        """
        try:
            params = {
                'pay_token_address': pay_token.address,
                'pay_amount': pay_amount,
            }

            if slippage:
                params['slippage'] = slippage

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_mint_and_stake_glp"), [params])
            raise_if_error(res)
            result = res.get('result', {})
            return True, result
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def get_pt_quote(self, buy_pt_amount: float, market_address: ChecksumAddress) -> (bool, dict):
        try:
            params = {
                'market_address': market_address,
                'exact_pt_out': buy_pt_amount,
            }

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_pendle_pt_quote"), [params])
            raise_if_error(res)
            result = res.get('result', {})
            return True, result
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def submit_new_armor_hash(self, tx_hash: str, existing_safe_address: Optional[ChecksumAddress] = None) -> bool:
        try:
            params = {
                'tx_hash': tx_hash
            }

            if existing_safe_address:
                params['safe_address'] = existing_safe_address

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_armor_hash"), [params])
            raise_if_error(res)
            result = res.get('result', False)
            return result
        except EulithRpcException:
            return False

    def get_deployed_execution_contracts(self) -> (bool, dict):
        try:
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_contracts"), {})
            raise_if_error(response)
            contracts = response['result']['contracts']
            return True, contracts
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def submit_safe_signature(self, module_address: str, owner_address: str,
                              signature: str, signed_hash: str, signature_type: str) -> (bool, dict):
        try:
            params = {
                'module_address': module_address,
                'owner_address': owner_address,
                'signature': str(signature),
                'signed_hash': signed_hash,
                'signature_type': signature_type
            }

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_enable_safe_signature"), [params])
            raise_if_error(res)
            result = res.get('result', False)
            return True, result
        except requests.exceptions.HTTPError as e:
            return False, RPCResponse(error=str(e))

    def get_enable_safe_tx(self, auth_address: str, owner_threshold: int, owners: List[str]) -> (bool, TxParams):
        try:
            params = {
                'auth_address': auth_address,
                'owner_threshold': owner_threshold,
                'owners': owners
            }

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_get_setup_safe_tx"), [params])
            raise_if_error(res)
            result = res.get('result', {})
            return True, result
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def submit_enable_safe_tx_hash(self, tx_hash: str, *, has_ace: bool) -> (bool, dict):
        try:
            params = {
                'tx_hash': tx_hash,
                'has_ace': has_ace,
            }

            res = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_setup_safe_hash"), [params])
            raise_if_error(res)
            result = res.get('result', False)
            return result, {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def create_draft_client_whitelist(self, auth_address: str, addresses: List[str]) -> (int, dict):
        try:
            params = {
                "auth_address": auth_address,
                "addresses": addresses
            }

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_create_draft_client_whitelist"), [params])
            raise_if_error(response)
            return response["result"]["list_id"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def create_draft_client_whitelist_v2(self, request: whitelists_v2.rpc.CreateRequest) -> whitelists_v2.rpc.CreateResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_create_draft_client_whitelist_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.CreateResponse, json_rpc["result"])

    def append_to_draft_client_whitelist(self, auth_address: str, addresses: List[str], chain_id: Optional[int]) -> (int, dict):
        try:
            params = {
                "auth_address": auth_address,
                "addresses": addresses,
            }

            if chain_id:
                params['chain_id'] = chain_id

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_append_to_draft_client_whitelist"), [params])
            raise_if_error(response)
            return response["result"]["list_id"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def append_to_draft_client_whitelist_v2(self, request: whitelists_v2.rpc.AppendRequest) -> whitelists_v2.rpc.AppendResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_append_to_draft_client_whitelist_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.AppendResponse, json_rpc["result"])

    def get_draft_client_whitelist_hash(self, list_id: int) -> (Optional[ClientWhitelistHash], dict):
        try:
            params = {
                "list_id": list_id
            }

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_draft_client_whitelist_hash"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def get_draft_client_whitelist_hash_v2(self, request: whitelists_v2.rpc.GetHashRequest) -> whitelists_v2.rpc.GetHashResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_get_draft_client_whitelist_hash_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.GetHashResponse, json_rpc["result"])

    def submit_draft_client_whitelist_signature(self, list_id: int, owner_address: str, signature: str, signed_hash: str) -> (bool, dict):
        try:
            params = {
                "list_id": list_id,
                "owner_address": owner_address,
                "signature": signature,
                "signed_hash": signed_hash,
            }

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_draft_client_whitelist_signature"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def submit_draft_client_whitelist_signature_v2(self,
                                                   request: whitelists_v2.rpc.SubmitSignatureRequest) -> whitelists_v2.rpc.SubmitSignatureResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_draft_client_whitelist_signature_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.SubmitSignatureResponse, json_rpc["result"])

    def get_current_client_whitelist(self, auth_address: str, chain_id: Optional[int]) -> (CurrentWhitelists, dict):
        try:
            params = {
                "auth_address": auth_address,
            }

            if chain_id:
                params['chain_id'] = chain_id

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_current_client_whitelist"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def get_current_client_whitelist_v2(self, request: whitelists_v2.rpc.GetCurrentRequest) -> whitelists_v2.rpc.GetCurrentResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_get_current_client_whitelist_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.GetCurrentResponse, json_rpc["result"])

    def delete_draft_client_whitelist_v2(self, request: whitelists_v2.rpc.DeleteRequest) -> whitelists_v2.rpc.DeleteResponse:
        json_rpc = self.eulith_provider.make_request(RPCEndpoint("eulith_delete_draft_client_whitelist_v2"), [request])
        raise_if_error(json_rpc)
        return cast(whitelists_v2.rpc.DeleteResponse, json_rpc["result"])

    def propose_light_simulation(self, safe_address: str, chain_id: int, to_enable: bool) -> (dict, dict):
        try:
            params = dict(safe_address=safe_address, chain_id=chain_id, to_enable=to_enable)
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_propose_light_simulation"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return None, RPCResponse(error=str(e))

    def get_light_simulation_proposal_hash(self, proposal_id: int) -> (dict, dict):
        try:
            params = dict(proposal_id=proposal_id)
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_light_simulation_proposal_hash"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return None, RPCResponse(error=str(e))

    def submit_light_simulation_signature(self, proposal_id: int, owner_address: str, signature: str, signed_hash: str) -> (dict, dict):
        try:
            params = dict(proposal_id=proposal_id, owner_address=owner_address, signature=signature, signed_hash=signed_hash)
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_submit_light_simulation_proposal_signature"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return None, RPCResponse(error=str(e))

    def get_active_light_simulation_proposals(self) -> (dict, dict):
        try:
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_active_light_simulation_proposals"), [])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return None, RPCResponse(error=str(e))

    def delete_light_simulation_proposal(self, proposal_id: int) -> (dict, dict):
        try:
            params = dict(proposal_id=proposal_id)
            response = self.eulith_provider.make_request(RPCEndpoint("eulith_delete_light_simulation_proposal"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return None, RPCResponse(error=str(e))

    def get_accepted_enable_armor_signatures(self, auth_address: str) -> (List[AcceptedEnableArmorSignature], dict):
        try:
            params = {
                "auth_address": auth_address,
            }

            response = self.eulith_provider.make_request(RPCEndpoint("eulith_get_enable_module_sigs"), [params])
            raise_if_error(response)
            return response["result"], {}
        except EulithRpcException as e:
            return False, RPCResponse(error=str(e))

    def ping_ace(self, auth_address: str) -> (AcePingResponse, dict):
        params = {
            "auth_address": auth_address,
        }
        response = self.eulith_provider.make_request(RPCEndpoint("eulith_ping_ace"), [params])
        raise_if_error(response)
        return response["result"], {}

    def send_ace_transaction(self, signature: str, ace_immediate_tx: AceImmediateTx) -> (HexStr, dict):
        params = {
            "signature": signature,
            "immediate_tx": ace_immediate_tx.to_json(),
        }

        response = self.eulith_provider.make_request(RPCEndpoint("eulith_send_ace_transaction"), [params])
        raise_if_error(response)
        return response["result"], {}

    def pendle_swap(self, sell_token: Union[EulithERC20, PendleMarketSymbol],
                    buy_token: Union[EulithERC20, PendleMarketSymbol], sell_amount: float, slippage: float,
                    pendle_market: ChecksumAddress, recipient: Optional[ChecksumAddress] = None):
        sell_token = sell_token.address if isinstance(sell_token, EulithERC20) else sell_token.value
        buy_token = buy_token.address if isinstance(buy_token, EulithERC20) else buy_token.value

        params = {
            'sell_token': sell_token,
            'buy_token': buy_token,
            'sell_amount': sell_amount,
            'slippage_tolerance': slippage,
            'market': pendle_market
        }

        if recipient:
            params['recipient'] = recipient

        if self.atomic_params:
            self.atomic_params.inject_in_body(params)

        res = self.eulith_provider.make_request(RPCEndpoint("eulith_pendle_swap"), [params])
        raise_if_error(res)

        return res

    def get_subscriptions(self):
        return self.eulith_provider.active_subscriptions

    def subscribe(self, subscription_request: SubscribeRequest, handler: EulithWebsocketRequestHandler) -> SubscriptionHandle:
        return self.eulith_provider.subscribe(subscription_request, handler)

    def terminate(self):
        self.eulith_provider.terminate()
