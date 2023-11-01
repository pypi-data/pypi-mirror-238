from typing import List, TypedDict


class AddressOnChain(TypedDict):
    address: str
    chain_id: int


class Whitelist(TypedDict):
    list_id: int
    auth_address: str
    sorted_addresses: List[AddressOnChain]
    is_draft: bool


class HashInput(TypedDict):
    auth_address: str
    whitelisted_addresses: List[AddressOnChain]
    sub: str
