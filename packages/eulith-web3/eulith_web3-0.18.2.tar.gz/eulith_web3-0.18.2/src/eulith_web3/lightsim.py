from dataclasses import dataclass


@dataclass
class LightSimulationProposal:
    proposal_id: int
    to_enable: bool
    safe_address: str
    network_id: int
    proposer_sub: str
    safe_owner_sub: str
    status: str

    @classmethod
    def from_json(cls, j: dict) -> "LightSimulationProposal":
        return cls(**j)


@dataclass
class LightSimulationSubmitResponse:
    proposal: LightSimulationProposal
    approved: bool

    @classmethod
    def from_json(cls, j: dict) -> "LightSimulationSubmitResponse":
        proposal = LightSimulationProposal.from_json(j["proposal"])
        approved = j["approved"]
        return cls(proposal=proposal, approved=approved)


@dataclass
class LightSimulationHashInput:
    safe_address: str
    chain_id: int
    proposer_id: int
    safe_owner_id: int
    to_enable: bool
    proposal_id: int

    @classmethod
    def from_json(cls, j: dict) -> "LightSimulationHashInput":
        return cls(**j)

    def typed_data(self) -> dict:
        types = {
            "EIP712Domain": [
                {"name": "name", "type": "string"},
                {"name": "version", "type": "string"},
            ],
            "LightSimulationProposalHashInput": [
                {"name": "safeAddress", "type": "string"},
                {"name": "chainId", "type": "int32"},
                {"name": "proposerId", "type": "int32"},
                {"name": "safeOwnerId", "type": "int32"},
                {"name": "toEnable", "type": "bool"},
                {"name": "proposalId", "type": "int32"},
            ],
        }

        payload = {
            "types": types,
            "primaryType": "LightSimulationProposalHashInput",
            "domain": {"name": "EulithLightSimulationProposal", "version": "1"},
            "message": {
                "safeAddress": self.safe_address,
                "chainId": self.chain_id,
                "proposerId": self.proposer_id,
                "safeOwnerId": self.safe_owner_id,
                "toEnable": self.to_enable,
                "proposalId": self.proposal_id,
            },
        }

        return payload
