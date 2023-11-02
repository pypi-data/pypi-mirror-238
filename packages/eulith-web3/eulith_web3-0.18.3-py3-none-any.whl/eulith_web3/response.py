from web3.types import RPCResponse, TxReceipt

from eulith_web3.common import ETHEREUM_STATUS_SUCCESS
from eulith_web3.exceptions import EulithRpcException


def raise_if_error(resp: RPCResponse):
    """
    Checks if the resp object passed as an argument to the handle_rpc_response function contains a key 'error'.
    If the key 'error' exists in the dictionary 'resp' and if its value is not an empty string, we handle RPC response
    from the API and raise EulithRpcException

    :param resp: RPC response from the API
    :type resp: RPCResponse

    :raises EulithRpcException: If the 'error' field in the RPC response is not empty
    """

    if 'error' in resp:
        raise EulithRpcException("RPC Error: " + str(resp.get('error')))


def check_tx_receipt(tx_receipt: TxReceipt):
    if tx_receipt["status"] != ETHEREUM_STATUS_SUCCESS:
        hash = tx_receipt['transactionHash'].hex()
        raise EulithRpcException(f"transaction reverted ({hash})")
