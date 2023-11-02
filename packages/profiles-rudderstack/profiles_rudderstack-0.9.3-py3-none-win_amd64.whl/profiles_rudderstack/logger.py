import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2

class Logger:
    def __init__(self, name: str) -> None:
        self.__name = name
        from profiles_rudderstack.wht_service import WhtService
        self.__whtService = WhtService

    def info(self, message: str) -> None:
        self.__whtService.LogInfo(tunnel_pb2.LogRequest(
            name=self.__name,
            message=message,
        ))

    def warn(self, message: str) -> None:
        self.__whtService.LogWarn(tunnel_pb2.LogRequest(
            name=self.__name,
            message=message,
        ))
    
    def error(self, message: str) -> None:
        self.__whtService.LogError(tunnel_pb2.LogRequest(
            name=self.__name,
            message=message,
        ))

    def debug(self, message: str) -> None:
        self.__whtService.LogDebug(tunnel_pb2.LogRequest(
            name=self.__name,
            message=message,
        ))