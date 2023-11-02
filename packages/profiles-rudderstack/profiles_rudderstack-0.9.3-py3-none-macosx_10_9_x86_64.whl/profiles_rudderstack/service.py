import json, grpc, importlib.util, importlib.metadata, pkg_resources
from packaging.requirements import Requirement
from typing import Callable, List, Union
import traceback

from profiles_rudderstack.model import BaseModelType
from profiles_rudderstack.recipe import PyNativeRecipe
from profiles_rudderstack.material import WhtMaterial
from profiles_rudderstack.utils import RefManager
from profiles_rudderstack.project import WhtProject
from profiles_rudderstack.logger import Logger
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import PythonServiceServicer, WhtServiceStub

class ProfilesRpcService(PythonServiceServicer):
    def __init__(self, ref_manager: RefManager, wht_service: WhtServiceStub, current_supported_schema_version: int, pb_version: str):
        self.logger = Logger("ProfilesRpcService")
        self.current_supported_schema_version = current_supported_schema_version
        self.pb_version = pb_version
        self.ref_manager = ref_manager
        self.wht_service = wht_service

    def __register_model_type(self, package: str, project: WhtProject):
        requirement = Requirement(package)
        module = importlib.import_module(requirement.name)
        if module is None:
            return f"{requirement.name} not found" 

        registerFunc: Callable[[WhtProject],None] = getattr(module, "register_extensions")
        if registerFunc is None:
            return f"RegisterModelType not found in {requirement.name}"

        registerFunc(project)
        return None
    
    def RegisterPackages(self, request: tunnel_pb2.RegisterPackagesRequest, context):
        try:
            not_installed: List[str] = []
            for package in request.packages:
                try:
                    pkg_resources.require(package)
                except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
                    not_installed.append(package)
            
            if not_installed:
                error_message = "The following package(s) are not installed or their version is not correct: {}.".format(", ".join(not_installed))
                context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                context.set_details(error_message)
                return tunnel_pb2.RegisterPackagesResponse()
            
            project = WhtProject(request.project_ref, self.current_supported_schema_version, self.pb_version, self.ref_manager, self.wht_service)
            for package in request.packages:
                err = self.__register_model_type(package, project)
                if err is not None:
                    context.set_code(grpc.StatusCode.INVALID_ARGUMENT)
                    context.set_details("while registering packages: " + err)
                    return tunnel_pb2.RegisterPackagesResponse()
            
            return tunnel_pb2.RegisterPackagesResponse()
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.RegisterPackagesResponse()
    
    def GetPackageVersion(self, request: tunnel_pb2.GetPackageVersionRequest, context):
        model_type_ref = self.ref_manager.get_ref(request.model_type)
        if model_type_ref is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model type not found")
            return tunnel_pb2.GetPackageVersionResponse()

        package = model_type_ref["package"]
        version = importlib.metadata.version(package)
        return tunnel_pb2.GetPackageVersionResponse(version=version)
    
    def ModelFactory(self, request: tunnel_pb2.ModelFactoryRequest, context):
        try:
            model_type_ref = self.ref_manager.get_ref(request.model_type)
            if model_type_ref is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details("model type not found")
                return tunnel_pb2.ModelFactoryResponse()
            
            build_spec = json.loads(request.build_spec)
            wht_model_ref, py_model_fef, contract_ref = model_type_ref["factory_func"](request.base_proj_ref, request.model_name, build_spec)
            return tunnel_pb2.ModelFactoryResponse(wht_model_ref=wht_model_ref, python_model_ref=py_model_fef, contract_ref=contract_ref)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.ModelFactoryResponse()
        
    
    ### Model methods

    def GetMaterialRecipe(self, request: tunnel_pb2.GetMaterialRecipeRequest, context):
        model: Union[BaseModelType, None] = self.ref_manager.get_ref(request.py_model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("get metaerial recipe: model not found")
            return tunnel_pb2.GetMaterialRecipeResponse()
        
        try:
            recipe = model.get_material_recipe()
            recipe_ref = self.ref_manager.create_ref(recipe)
            return tunnel_pb2.GetMaterialRecipeResponse(recipe_ref=recipe_ref)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.GetMaterialRecipeResponse()
    
    def DescribeRecipe(self, request: tunnel_pb2.DescribeRecipeRequest, context):
        recipe: Union[PyNativeRecipe, None] = self.ref_manager.get_ref(request.recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("describe recipe: recipe not found")
            return tunnel_pb2.DescribeRecipeResponse()
        
        try:
            this = WhtMaterial(request.material_ref, self.wht_service)
            description, extension = recipe.describe(this)
            return tunnel_pb2.DescribeRecipeResponse(description=description, extension=extension)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.DescribeRecipeResponse()
    
    def PrepareRecipe(self, request: tunnel_pb2.PrepareRecipeRequest, context):
        recipe: Union[PyNativeRecipe, None] = self.ref_manager.get_ref(request.recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("prepare recipe: recipe not found")
            return tunnel_pb2.PrepareRecipeResponse()
        
        try:
            this = WhtMaterial(request.material_ref, self.wht_service)
            recipe.prepare(this)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
        return tunnel_pb2.PrepareRecipeResponse()
    
    def ExecuteRecipe(self, request: tunnel_pb2.ExecuteRecipeRequest, context):
        recipe: Union[PyNativeRecipe, None] = self.ref_manager.get_ref(request.recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("recipe not found")
            return tunnel_pb2.ExecuteRecipeResponse()
        
        try:
            this = WhtMaterial(request.material_ref, self.wht_service)
            recipe.execute(this)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
        return tunnel_pb2.ExecuteRecipeResponse()
    
    def GetRecipeHash(self, request: tunnel_pb2.GetRecipeHashRequest, context):
        recipe: Union[PyNativeRecipe, None] = self.ref_manager.get_ref(request.recipe_ref)
        if recipe is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("recipe not found")
            return tunnel_pb2.GetRecipeHashResponse()
        
        try:
            hash = recipe.hash()
            return tunnel_pb2.GetRecipeHashResponse(hash=hash)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.GetRecipeHashResponse()
    
    def Validate(self, request: tunnel_pb2.ValidateRequest, context):
        model: Union[BaseModelType, None] = self.ref_manager.get_ref(request.py_model_ref)
        if model is None:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("model not found")
            return tunnel_pb2.ValidateResponse()

        try:
            isValid, reason = model.validate()
            return tunnel_pb2.ValidateResponse(valid=isValid, reason=reason)
        except Exception as e:
            context.set_code(grpc.StatusCode.UNKNOWN)
            tb = traceback.format_exc()
            context.set_details(tb)
            return tunnel_pb2.ValidateResponse()

    ### Ping
    
    def Ping(self, request, context):
        return tunnel_pb2.PingResponse(message="ready")
