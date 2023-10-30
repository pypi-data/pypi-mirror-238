''' Class representing the OpenGateClient '''

# pylint: disable=E0401
# pylint: disable=W0611
# pylint: disable=C0303
# pylint: disable=C0301
# pylint: disable=E1101

from typing import Dict, Optional
import requests
import pandas as pd
from datapoints.datapoints import DataPointsBuilder
from datasets.datasets import DataSetsBuilder
from timeseries.timeseries import TimeSeriesBuilder
from entities.entities import EntitiesBuilder
from ai_models.ai_models import AIModelsBuilder
from ai_pipelines.ai_pipelines import AIPipelinesBuilder
from ai_transformers.ai_transformers import AITransformersBuilder
from rules.rules import RulesBuilder

class OpenGateClient:
    ''' Class representing the OpenGateClient '''
    def __init__(self, url: str = None, user: Optional[str] = None, password: Optional[str] = None, api_key: Optional[str] = None) -> None:
        self.url: str = url
        self.user: Optional[str] = user
        self.password: Optional[str] = password
        self.api_key: Optional[str] = api_key
        self.headers: Dict[str, str] = {}
        self.client: OpenGateClient = self
        requests.packages.urllib3.disable_warnings()

        if not url:
            raise ValueError('You have not provided a URL')

        if user and password:
            data_user = {
                'email': self.user,
                'password': self.password
            }
            try:
                login_url = self.url + '/north/v80/provision/users/login'
                request = requests.post(login_url, json=data_user, timeout=5000, verify=False)
                request.raise_for_status()
                response_json = request.json()
                if 'user' in response_json:
                    self.headers.update({
                        'Authorization': f'Bearer {response_json["user"]["jwt"]}',
                    })
                else:
                    raise ValueError('Empty response received')

            except requests.exceptions.HTTPError as err:
                raise requests.exceptions.HTTPError(f'Request failed: {err}')
            except requests.exceptions.RequestException as error:
                raise requests.exceptions.RequestException(f'Connection failed: {error}')
        elif api_key:
            self.headers.update({
                'X-ApiKey': self.api_key
            })
        else:
            raise ValueError('You have not provided an API key or user and password')
               
    def data_sets(self) -> DataSetsBuilder:
        ''' Represents the builder of datasets '''
        return DataSetsBuilder(self)
    
    def timeseries(self) -> TimeSeriesBuilder:
        ''' Represents the builder of timeseries '''
        return TimeSeriesBuilder(self)
    
    def entities(self) -> EntitiesBuilder:
        ''' Represents the builder of entities '''
        return EntitiesBuilder(self)
    
    def data_points_builder(self) -> DataPointsBuilder:
        ''' Represents the builder of datapoints '''
        return DataPointsBuilder(self)
    
    def ai_models_builder(self) -> AIModelsBuilder:
        ''' Represents the builder of artificial intelligence models '''
        return AIModelsBuilder(self)

    def ai_pipelines_builder(self) -> AIPipelinesBuilder:
        ''' Represents the builder of artificial intelligence models '''
        return AIPipelinesBuilder(self)
    
    def ai_transformers_builder(self) -> AITransformersBuilder:
        ''' Represents the builder of artificial intelligence models '''
        return AITransformersBuilder(self)
    
    def rules_builder(self) -> RulesBuilder:
        ''' Represents the builder of artificial intelligence models '''
        return RulesBuilder(self)
    
client = OpenGateClient(url='https://172.19.18.132:9082', api_key="bdef865c-bad0-4587-917f-6b7de8cf7d59")


#Set new model id in model_config

