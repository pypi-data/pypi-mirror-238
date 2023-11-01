from ._core import AddressOnChain, HashInput


class AddressOnChainEip712:
    x: AddressOnChain

    def __init__(self, x: AddressOnChain) -> None:
        self.x = x

    @classmethod
    def type(cls) -> list:
        return [
            {"name": "address", "type": "address"},
            {"name": "chainId", "type": "int32"},
        ]

    @classmethod
    def type_name(cls) -> str:
        return "AddressOnChain"

    def typed_data(self) -> dict:
        types = {
            "EIP712Domain": eip712_domain_type(),
            self.type_name(): self.type(),
        }

        payload = {
            "types": types,
            "primaryType": self.type_name(),
            "domain": eip712_domain(),
            "message": {
                "address": self.x["address"],
                "chainId": self.x["chain_id"],
            }
        }

        return payload


class HashInputEip712:
    x: HashInput

    def __init__(self, x: HashInput) -> None:
        self.x = x

    @classmethod
    def eip712_type(cls) -> list:
        return [
            {"name": "authAddress", "type": "address"},
            {"name": "whitelistedAddresses", "type": "AddressOnChain[]"},
            {"name": "sub", "type": "string"},
        ]

    @classmethod
    def eip712_type_name(cls) -> str:
        return "HashInput"

    def typed_data(self) -> dict:
        types = {
            "EIP712Domain": eip712_domain_type(),
            AddressOnChainEip712.type_name(): AddressOnChainEip712.type(),
            self.eip712_type_name(): self.eip712_type(),
        }

        payload = {
            "types": types,
            "primaryType": self.eip712_type_name(),
            "domain": eip712_domain(),
            "message": {
                "authAddress": self.x["auth_address"],
                "whitelistedAddresses": [
                    {
                        "address": address_on_chain["address"],
                        "chainId": address_on_chain["chain_id"],
                    } for address_on_chain in self.x["whitelisted_addresses"]],
                "sub": self.x["sub"],
            }
        }

        return payload


def eip712_domain() -> dict:
    return {"name": "EulithWhitelist", "version": "1"}


def eip712_domain_type() -> list:
    return [
        {"name": "name", "type": "string"},
        {"name": "version", "type": "string"},
    ]
