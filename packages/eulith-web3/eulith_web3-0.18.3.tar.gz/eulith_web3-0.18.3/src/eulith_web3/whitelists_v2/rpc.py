from typing import List, Optional, TypedDict

from ._core import AddressOnChain, HashInput, Whitelist


class CreateRequest(TypedDict):
    auth_address: str
    addresses: List[AddressOnChain]


class CreateResponse(TypedDict):
    list_id: int


class GetHashRequest(TypedDict):
    list_id: int


class GetHashResponse(TypedDict):
    hash_input: HashInput
    hash: str


class SubmitSignatureRequest(TypedDict):
    list_id: int
    signer_address: str
    signature: str
    hash: str


class SubmitSignatureResponse(TypedDict):
    signature_count: int
    signature_threshold: int
    whitelist: Whitelist


class DeleteRequest(TypedDict):
    list_id: int


class DeleteResponse(TypedDict):
    deleted: Whitelist


class GetCurrentRequest(TypedDict):
    auth_address: str


class GetCurrentResponse(TypedDict):
    active: Optional[Whitelist]
    draft: Optional[Whitelist]


class AppendRequest(TypedDict):
    auth_address: str
    addresses: List[AddressOnChain]


class AppendResponse(TypedDict):
    draft: Whitelist
