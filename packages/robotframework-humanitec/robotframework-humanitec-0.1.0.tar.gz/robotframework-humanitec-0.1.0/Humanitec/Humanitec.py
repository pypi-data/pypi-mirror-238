"""
This library is experimental. It aims for functionality and quick proof of concept.

It will become a proepr dynamic library later on.
"""

import swagger_client
from swagger_client import Configuration, ApiClient
from swagger_client.models import DeltaResponse, DeltaMetadataRequest, DeltaRequest, DeploymentRequest, DeploymentResponse, ApplicationResponse
from swagger_client.api import DeltaApi, ApplicationApi

import os
import json
import requests

from robot.api.deco import library, keyword, not_keyword
from robot.libraries.BuiltIn import BuiltIn

@library
class Humanitec():
    """
    This is an alpha version of a Robot Framework library for Humanitec. All keywords work synchronously.

    == Setup ==
    The library expects 2 environment variables:
    - *HUMANITEC_ORG_ID* : the id of the organisation the test case or task accesses
    - *HUMANITEC_TOKEN* : API token from Humanitec

    If these environment variables do not exist, the library won't work.
    """

    _api_client: ApiClient = None
    _configuration: Configuration = None
    
    def __init__(self):
        self.org_id = os.environ.get('HUMANITEC_ORG_ID')

    @not_keyword
    def api_client(self):
        if self._api_client is None:
            self._api_client = swagger_client.ApiClient(configuration=self.get_swagger_configuration())
        return self._api_client
    
    @not_keyword
    def get_swagger_configuration(self):
        if self._configuration is None:
            self._configuration = Configuration()
            self._configuration.api_key['Authorization']=os.environ.get('HUMANITEC_TOKEN')
            self._configuration.api_key_prefix['Authorization']='Bearer'
            self._configuration.debug=True
            self._configuration.logger_file=BuiltIn().replace_variables('${OUTPUT_DIR}/swagger-debug.log')
        return self._configuration

    @keyword(tags=['swagger-client', 'app'])
    def get_all_apps(self):
        """
        Retrieves a list of all applications available in the current organization.
        """
        api_instance: ApplicationApi = swagger_client.ApplicationApi(api_client=self.api_client())

        api_response: ApplicationResponse = api_instance.orgs_org_id_apps_get(self.org_id)

        return api_response

    @keyword(tags=['swagger-client', 'delta'])
    def create_delta(self, app_id:str, env: str= 'development', comment: str = 'New delta from Robot Framework'):
        """
        Creates a new delta.

        The returned dictionary contains the delta id (among other items).
        """
        api_instance: DeltaApi = swagger_client.DeltaApi(api_client=self.api_client())
        metadata: DeltaMetadataRequest = swagger_client.DeltaMetadataRequest(name=comment, env_id=env)
        body: DeltaRequest = swagger_client.DeltaRequest(metadata=metadata) # DeltaRequest | A Deployment Delta to create.
        
        api_response: DeltaResponse = api_instance.orgs_org_id_apps_app_id_deltas_post(body, self.org_id, app_id)

        return api_response

    @keyword(tags=['swagger-client','delta'])
    def deploy_delta(self, app_id: str, delta_id: str, env: str= 'development', comment: str = 'Deployed by Robot Framework'):
        """
        Deploy a delta with a given id for a given application.

        Returns the response dictionary from the deployment.
        """
        # create an instance of the API class
        api_instance: DeltaApi = swagger_client.DeploymentApi(api_client=self.api_client())
        body: DeploymentRequest = swagger_client.DeploymentRequest(delta_id=delta_id, comment=comment) # DeploymentRequest | The Delta describing the change to the Environment and a comment.

        api_response: DeploymentResponse = api_instance.orgs_org_id_apps_app_id_envs_env_id_deploys_post(body, self.org_id, app_id, env)
        
        return api_response

    @not_keyword
    def request_all_deltas(self, app_id:str, env: str ='development',archived: bool =False):
        """
        Gets all deltas of an application.
        """
        config = self.get_swagger_configuration()
        headers = {
            'Authorization' : f'{config.api_key_prefix["Authorization"]} {config.api_key["Authorization"]}'
        }

        response= requests.get(url=f'{config.host}/orgs/{self.org_id}/apps/{app_id}/deltas?archived={archived}&env={env}',headers=headers)
        response.raise_for_status()
        return json.loads(response.text)
    
    @keyword(name="Get Deltas For Application")
    def get_all_deltas(self, app_id: str, env: str='development', archived=False):
        """
        Gets all deltas of an application.

        _Uses internally requests-module as the generated swagger-client is not working for this endpoint_
        """
        return self.request_all_deltas(app_id, env, archived)

    @not_keyword
    def __broken_get_all_deltas(self, app_id: str, env: str='development', archived=False):
        """
        Due errors in swagger-codegen (and maybe inconsistency in Humanitec openapi spec on top?), swagger-client
        runs in to errors for this endpoint. The issue is that DeltaResponse does not allow None (null) values for 'shared'
        Module.DeltasResponse have the same issue with 'add', 'update' and 'remove' despite it should be allowed according to documentation.
        On the one side, it looks like the openapi spec 0.24.1 is missing nullable markers for those attributes, on the other hand even with 
        marker added, swagger-codegen still makes fields mandatory.

        We have to use requests module instead (see get_all_deltas)
        """
        
        api_instance: DeltaApi = swagger_client.DeltaApi(api_client=self.api_client)

        api_response: DeltaResponse = api_instance.orgs_org_id_apps_app_id_deltas_get(self.org_id, app_id, archived=archived, env=env)
        
        return api_response