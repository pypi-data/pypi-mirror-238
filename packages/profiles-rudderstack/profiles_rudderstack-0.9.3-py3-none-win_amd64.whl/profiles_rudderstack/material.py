from typing import Optional, List, Dict, Iterator, Literal
from google.protobuf import json_format
from profiles_rudderstack.contract import Contract
from profiles_rudderstack.utils import remap_credentials
from profiles_rudderstack.logger import Logger
from profiles_rudderstack.tunnel.tunnel_pb2_grpc import WhtServiceStub
import profiles_rudderstack.tunnel.tunnel_pb2 as tunnel_pb2
from snowflake.snowpark.session import Session
from profiles_rudderstack.wh import ProfilesConnector
from profiles_rudderstack.wh.connector_base import ConnectorBase
import pandas as pd

class WhtWarehouseClient:
    # Static props for caching, wh connection is same for all models in a pb project
    __snowpark_sesion: Optional[Session] = None
    __wh_connection: Optional[ConnectorBase] = None
    __schema: Optional[str] = None
    __wh_type: Optional[Literal['snowflake', 'redshift']] = None

    def __init__(self, material_ref: int, wht_service: WhtServiceStub, is_null_ctx: bool) -> None:
        self.snowpark_session = WhtWarehouseClient.__snowpark_sesion
        self.wh_connection = WhtWarehouseClient.__wh_connection
        self.schema = WhtWarehouseClient.__schema
        self.wh_type = WhtWarehouseClient.__wh_type
        self.logger = Logger("WhtWarehouseClient")

        self.__wht_service = wht_service
        self.__material_ref = material_ref

        if not is_null_ctx and (WhtWarehouseClient.__snowpark_sesion is None and WhtWarehouseClient.__wh_connection is None):
            creds_response: tunnel_pb2.GetWarehouseCredentialsResponse = wht_service.GetWarehouseCredentials(tunnel_pb2.GetWarehouseCredentialsRequest(
                material_ref=self.__material_ref,
            ))
            creds = json_format.MessageToDict(creds_response.credentials)
            self.schema = creds.get("schema", None)
            self.wh_type = creds.get("type", None)
            # Use snowpark for snowflake, otherwise use warehouse connector
            if self.wh_type == "snowflake":
                creds = remap_credentials(creds)

                self.snowpark_session = Session.builder.configs(creds).create()
            elif self.wh_type == "redshift":
                s3_config = creds.get("s3", None)
                if s3_config is None:
                    self.logger.warn("its recommended to provide s3 config in siteconfig to get added performance benefit in redshift (https://stackoverflow.com/questions/38402995/how-to-write-data-to-redshift-that-is-a-result-of-a-dataframe-created-in-python)")
                
                # json_format converts int to float, so we need to convert it back
                creds.update({"port": int(creds.get("port", 0))})

                self.wh_connection = ProfilesConnector(creds, s3_config=s3_config)

            WhtWarehouseClient.__snowpark_sesion = self.snowpark_session
            WhtWarehouseClient.__wh_connection = self.wh_connection
            WhtWarehouseClient.__schema = self.schema
            WhtWarehouseClient.__wh_type = self.wh_type
        

    def query_sql_with_result(self, sql: str) -> pd.DataFrame:
        if self.wh_type == "snowflake":
            return self.snowpark_session.sql(sql).to_pandas(block=True)
        else:
            return self.wh_connection.run_query(sql)

    def query_sql_without_result(self, sql: str):
        self.__wht_service.QuerySqlWithoutResult(tunnel_pb2.QuerySqlWithoutResultRequest(
            material_ref=self.__material_ref,
            sql=sql,
        ))
    
    def query_template_without_result(self, template: str):
        self.__wht_service.QueryTemplateWithoutResult(tunnel_pb2.QueryTemplateWithoutResultRequest(
            material_ref=self.__material_ref,
            template=template,
        ))

    def write_df_to_table(self, df, table: str, append_if_exists: bool = False):
        table_name = table.upper()
        df.columns = df.columns.str.upper()
        if self.wh_type == "snowflake":
            self.snowpark_session.write_pandas(df, table_name=table_name, auto_create_table=True, overwrite=False if append_if_exists else True)
        else:
            self.wh_connection.write_to_table(df, table_name, self.schema, if_exists="append" if append_if_exists else "replace")


class WhtContext:
    def __init__(self, material_ref: int, wht_service: WhtServiceStub) -> None:
        self.__material_ref = material_ref
        self.__wht_service = wht_service
        is_null_ctx = self.is_null_context()
        self.client = WhtWarehouseClient(material_ref, wht_service, is_null_ctx)
        self.snowpark_session = self.client.snowpark_session

    def is_null_context(self) -> bool:
        nullCtxResponse: tunnel_pb2.IsNullContextResponse = self.__wht_service.IsNullContext(tunnel_pb2.IsNullContextRequest(
            material_ref=self.__material_ref,
        ))
        return nullCtxResponse.is_null_ctx

class WhtModel:
    def __init__(self, material_ref: int, wht_service: WhtServiceStub) -> None:
        self.__material_ref = material_ref
        self.__wht_service = wht_service
        self.logger = Logger("WhtModel")

    def name(self) -> str:
        """Get the name of the model

        Returns:
            str: Name of the model
        """
        nameResponse: tunnel_pb2.ModelNameResponse = self.__wht_service.ModelName(tunnel_pb2.NameRequest(
            material_ref=self.__material_ref,
        ))

        return nameResponse.model_name
    
    def entity(self) -> Optional[Dict]:
        """
        Get the entity of the model
        
        Returns:
            Dict: Entity of the model
        """
        entityResponse: tunnel_pb2.EntityResponse = self.__wht_service.Entity(tunnel_pb2.EntityRequest(material_ref=self.__material_ref))
        entity = json_format.MessageToDict(entityResponse.entity)
        if len(entity) == 0:
            return None
        
        return entity

class WhtMaterial:
    def __init__(self, material_ref: int, wht_service: WhtServiceStub, wht_ctx: Optional[WhtContext] = None):
        self.__material_ref = material_ref
        self.__wht_service = wht_service
        self.model = WhtModel(material_ref, wht_service)
        if wht_ctx is None:
            self.wht_ctx = WhtContext(material_ref, wht_service)
        else:
            self.wht_ctx = wht_ctx
        self.logger = Logger("WhtMaterial")
        
    def name(self) -> str:
        """Get the name of the material

        Returns:
            str: Name of the material
        """
        nameResponse: tunnel_pb2.NameResponse = self.__wht_service.Name(tunnel_pb2.NameRequest(
            material_ref=self.__material_ref,
        ))

        return nameResponse.material_name.upper()
    
    def get_output_folder(self) -> str:
        """Get the output folder of the material

        Returns:
            str: Output folder of the material
        """
        outputFolderResponse: tunnel_pb2.OutputFolderResponse = self.__wht_service.OutputFolder(tunnel_pb2.OutputFolderRequest(
            material_ref=self.__material_ref,
        ))

        return outputFolderResponse.output_folder

    def de_ref(self, model_path: str, contract: Optional[Contract] = None):
        """Dereference a material
        
        Args:
            model_path (str): Path to the model
            contract (Contract, optional): Input Contract to be applied. Defaults to None.
            
        Returns:
            WhtMaterial: Dereferenced material
        """
        deRefResponse: tunnel_pb2.DeRefResponse = self.__wht_service.DeRef(tunnel_pb2.DeRefRequest(
            material_ref=self.__material_ref,
            model_path=model_path,
            contract_ref= contract.get_contract_ref() if contract is not None else None,
        ))

        return WhtMaterial(deRefResponse.material_ref, self.__wht_service, self.wht_ctx)
    
    def de_ref_optional(self, model_path: str, contract: Optional[Contract] = None):
        """Dereference a material as optional
        
        Args:
            model_path (str): Path to the model
            contract (Contract, optional): Input Contract to be applied. Defaults to None.
            
        Returns:
            Optional[WhtMaterial]: Dereferenced material
        """
        deRefOptionalResponse: tunnel_pb2.DeRefOptionalResponse = self.__wht_service.DeRefOptional(tunnel_pb2.DeRefRequest(
            material_ref=self.__material_ref,
            model_path=model_path,
            contract_ref= contract.get_contract_ref() if contract is not None else None,
        ))

        if deRefOptionalResponse.is_null:
            return None

        return WhtMaterial(deRefOptionalResponse.material_ref, self.__wht_service, self.wht_ctx)
    
    def de_ref_preferred(self, model_path: str, contract: Optional[Contract] = None):
        """Dereference a material as preferred
        
        Args:
            model_path (str): Path to the model
            contract (Contract, optional): Input Contract to be applied. Defaults to None.
            
        Returns:
            Optional[WhtMaterial]: Dereferenced material
        """
        deRefPreferredResponse: tunnel_pb2.DeRefOptionalResponse = self.__wht_service.DeRefPreferred(tunnel_pb2.DeRefRequest(
            material_ref=self.__material_ref,
            model_path=model_path,
            contract_ref= contract.get_contract_ref() if contract is not None else None,
        ))

        if deRefPreferredResponse.is_null:
            return None

        return WhtMaterial(deRefPreferredResponse.material_ref, self.__wht_service, self.wht_ctx)
    
    def get_columns(self):
        """Get the columns of the material

        Returns:
            List[dict]: List of columns
        """
        getAllColsResponse: tunnel_pb2.GetColumnsResponse = self.__wht_service.GetColumns(tunnel_pb2.GetColumnsRequest(
            material_ref=self.__material_ref,
        ))

        return [{"name": col.name, "type": col.type} for col in getAllColsResponse.columns]
    
    def get_table_data(self, select_columns: Optional[List[str]] = None) -> pd.DataFrame:
        """Get the table data of the material.

        Args:
            select_columns (List[str], optional): List of columns to be selected. Defaults to None.

        Returns:
            DataFrame: Table data as pandas dataframe
        """
        getSelectorSqlRes = self.__wht_service.GetSelectorSql(tunnel_pb2.GetSelectorSqlRequest(
            material_ref=self.__material_ref,
            columns=select_columns,
        ))
        select_query = getSelectorSqlRes.sql

        if self.wht_ctx.client.wh_type == "snowflake":
            return self.wht_ctx.client.snowpark_session.sql(select_query).to_pandas(block=True)
        else:
            return self.wht_ctx.client.wh_connection.run_query(select_query)
        
    def get_table_data_batches(self, select_columns: Optional[List[str]] = None) -> Iterator[pd.DataFrame]:
        """Get the table data of the material in batches.

        Args:
            select_columns (List[str], optional): List of columns to be selected. Defaults to None.

        Raises:
            Exception: Batching is not supported for non-snowflake warehouses
            
        Returns:
            Iterator[DataFrame]: Table data as pandas dataframe
        """
        getSelectorSqlRes = self.__wht_service.GetSelectorSql(tunnel_pb2.GetSelectorSqlRequest(
            material_ref=self.__material_ref,
            columns=select_columns,
        ))
        select_query = getSelectorSqlRes.sql

        if self.wht_ctx.snowpark_session is not None:
            return self.wht_ctx.snowpark_session.sql(select_query).to_pandas_batches(block=True)
        
        raise Exception("Batching is not supported for non-snowflake warehouses")

    def write_output(self, df: pd.DataFrame, append_if_exists: bool = False):
        """Write the dataframe as the output of the material

        Args:
            df (pd.DataFrame): DataFrame to be written
            append_if_exists (bool, optional): Append to the table if it exists. Defaults to False.
        """
        tableName = self.name()
        df.columns = df.columns.str.upper()
        if self.wht_ctx.client.wh_type == "snowflake":
            self.wht_ctx.client.snowpark_session.write_pandas(df, table_name=tableName, auto_create_table=True, overwrite=False if append_if_exists else True)
        else:
            self.wht_ctx.client.wh_connection.write_to_table(df, tableName, self.wht_ctx.client.schema, if_exists="append" if append_if_exists else "replace")
    
    def execute_text_template(self, template: str) -> str:
        templateResponse: tunnel_pb2.ExecuteTextTemplateResponse = self.__wht_service.ExecuteTextTemplate(tunnel_pb2.ExecuteTextTemplateRequest(
            material_ref=self.__material_ref,
            template=template,
        ))

        return templateResponse.result