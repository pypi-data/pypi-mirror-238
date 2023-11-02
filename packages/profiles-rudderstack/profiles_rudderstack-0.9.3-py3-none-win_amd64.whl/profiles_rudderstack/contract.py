import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2

class Contract:
    def __init__(self, contract_ref: int) -> None:
        self.__contract_ref = contract_ref

    def get_contract_ref(self) -> int:
        return self.__contract_ref

def build_contract(contract: str) -> Contract:
    """Builds a contract from a string

    Args:
        contract (str): The contract to be built

    Returns:
        Contract: The built contract
    """
    # This is a workaround as WhtService is not available globally while initialisation
    from profiles_rudderstack.wht_service import WhtService
    contractRes: tunnel_pb2.BuildContractResponse = WhtService.BuildContract(
        tunnel_pb2.BuildContractRequest(contract=contract)
    )
    return Contract(contractRes.contract_ref)