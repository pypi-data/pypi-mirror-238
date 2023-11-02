import inspect
from google.protobuf import struct_pb2, json_format
import json
from typing import Type, cast
from types import FrameType
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import WhtServiceStub
from profiles_rudderstack.model import BaseModelType
from profiles_rudderstack.utils import RefManager
from profiles_rudderstack.logger import Logger
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2

class WhtProject:
    def __init__(self, project_ref: int, current_supported_schema_version: int, pb_version: str, ref_manager: RefManager, wht_service: WhtServiceStub):
        self.__project_ref = project_ref
        self.__wht_service = wht_service
        self.__ref_manager = ref_manager
        self.current_supported_schema_version = current_supported_schema_version
        self.pb_version = pb_version
        self.logger = Logger("WhtProject")

    def __create_factory_func(self, model_class: Type[BaseModelType], model_type: str):
        def factory(base_proj_ref:int, model_name: str, build_spec: dict):
            model = model_class(build_spec, self.current_supported_schema_version, self.pb_version)
            entityKey = model.get_entity_key()

            new_py_model_res: tunnel_pb2.NewPythonModelResponse = self.__wht_service.NewPythonModel(tunnel_pb2.NewPythonModelRequest(
                name=model_name,
                model_type=model_type,
                build_spec=json.dumps(build_spec),
                base_proj_ref=base_proj_ref,
                entity_key=entityKey,
            ))

            wht_model_ref = new_py_model_res.model_ref
            py_model_ref = self.__ref_manager.create_ref(model)
            contract = model.get_contract()

            return wht_model_ref, py_model_ref, contract.get_contract_ref() if contract else None
        
        return factory

    def register_model_type(self, modelClass: Type[BaseModelType]):
        package_name = ""
        # Get the package name from caller, from RegisterExtensions
        frame_type = cast(FrameType, cast(FrameType, inspect.currentframe()).f_back)
        package_info = inspect.getmodule(frame_type)
        if package_info:
            mod = package_info.__name__.split('.')
            package_name = mod[0]
            self.logger.info(f"Registering {modelClass.TypeName} from {package_name}")

        model_type = modelClass.TypeName
        schema = struct_pb2.Struct()
        json_format.ParseDict(modelClass.BuildSpecSchema, schema)

        self.__wht_service.RegisterModelType(tunnel_pb2.RegisterModelTypeRequest(
            model_type=model_type, 
            build_spec_schema=schema,
            project_ref=self.__project_ref,
        ))

        factory = self.__create_factory_func(modelClass, model_type)
        self.__ref_manager.create_ref_with_key(model_type, {
            "factory_func": factory,
            "package": package_name,
        })