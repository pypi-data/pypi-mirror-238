import os
from typing import IO, List, Optional
from tonic_textual.classes.api_responses.single_detection_result import SingleDetectionResult
from tonic_textual.classes.custom_model import CustomModel
from tonic_textual.classes.generator_config import GeneratorConfig
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.api_responses.redaction_response import RedactionResponse
from tonic_textual.enums.pii_state import PiiState
from tonic_textual.services.dataset import DatasetService
from tonic_textual.services.datasetfile import DatasetFileService
from tonic_textual.classes.dataset import Dataset
from tonic_textual.classes.datasetfile import DatasetFile
from tonic_textual.classes.tonic_exception import DatasetNameAlreadyExists
from urllib.parse import urlencode
import requests;

class TonicTextual:
    '''Wrapper class for invoking Tonic Textual API

    Parameters
    ----------
    base_url : str
        The url to your Tonic instance. Do not include trailing backslashes
    api_key : str
        Your api token, this argument is optional.  It is recommended instead that you provide your api key by setting TONIC_TEXTUAL_API_KEY in your environment

    Examples
    --------
    >>> TonicTextual("http://localhost:3000")
    '''
    def __init__(self, base_url : str, api_key: Optional[str] = None):
        if api_key is None:
            api_key = os.environ.get("TONIC_TEXTUAL_API_KEY")
            if api_key is None:
                raise Exception("No api key provided.  Please provide an api key or set TONIC_TEXTUAL_API_KEY environment variable.")
        self.api_key = api_key
        self.client = HttpClient(base_url, self.api_key)
        self.dataset_service = DatasetService(self.client)
        self.datasetfile_service = DatasetFileService(self.client)

    def create_dataset(self, dataset_name:str):
        """Create a dataset, which is a collection of 1 or more files.

        Parameters
        -----
        dataset_name : str
            The name of the dataset.  Dataset names must be unique.


        Returns
        -------
        Dataset
            The newly created dataset


        Raises
        ------

        DatasetNameAlreadyExists
            If a dataset with the same name already exists

        """
        try:
            self.client.http_post("/api/dataset", data={"name": dataset_name})
        except requests.exceptions.HTTPError as e:
            if e.response.status_code==409:
                raise DatasetNameAlreadyExists(e)

        return self.get_dataset(dataset_name)

    def delete_dataset(self, dataset_name: str):
        params = { "datasetName": dataset_name}
        self.client.http_delete("/api/dataset/delete_dataset_by_name?" + urlencode(params))




    def get_dataset(self, dataset_name : str) -> Dataset:
        '''Get instance of Workspace class with specified workspace_id.

        Parameters
        ----------
        dataset_name : str
            The name for your dataset

        Returns
        -------
        Dataset

        Examples
        --------
        >>> dataset = tonic.get_dataset("llama_2_chatbot_finetune_v5")
        '''
        return self.dataset_service.get_dataset(dataset_name)

    def get_files(self, dataset_id: str) -> List[DatasetFile]:
        """
        Gets all files

        Returns
        ------
        List[DatasetFile]
        A list of all files
        """
        return self.datasetfile_service.get_files(dataset_id)
      
    def unredact_bulk(self, redacted_strings: List[str]) -> List[str]:
            """Un-redacts a list of strings.
            
            Parameters
            ----------
            redacted_strings : List[str]
                The list of redacted strings you want to un-redact.
    
            Returns
            -------
            List[str]
                The list of un-redacted strings.
            """
            
            response = self.client.http_post("/api/unredact", data=redacted_strings)            
            return response
    
    def unredact(self, redacted_string: str) -> str:
            """Un-redacts a string.
            
            Parameters
            ----------
            redacted_string : str
                The redacted string you want to un-redact.
    
            Returns
            -------
            str
                The un-redacted string
            """
            
            response = self.client.http_post("/api/unredact", data=[redacted_string])            
            return response
    
    def redact(self, string: str, generatorConfig: GeneratorConfig = dict(), customModels: List[str] = []) -> RedactionResponse:
            """Redacts a string.
            
            Parameters
            ----------
            string : str
                The string to redact
            
            generatorConfig: GeneratorConfig
                A dictionary of PII entities which states whether a given entity is to be redacted, synthesized, or ignored.
    
            customModels: List[str]
                A list of custom model names to use during identification.  To see a list of custom models to which you have access use the get_custom_models function.

            Returns
            -------
            RedactionResponse
                The redacted string along with ancillary information.
            """
            
            invalid_pii_states = [v for v in list(generatorConfig.values()) if v not in PiiState._member_names_]
            if(len(invalid_pii_states)>0):
                 raise Exception("Invalid generator config.  Possible values are Off, Synthesis, and Redaction.")                 

            endpoint = "/api/redact"
            response = self.client.http_post(endpoint, data={"text": string, "generatorConfig": generatorConfig, "customModels": customModels})
            
            de_id_results = [SingleDetectionResult(x["start"], x["end"], x["label"], x["text"], x["score"]) for x in list(response["deIdentifyResults"])]

            return RedactionResponse(response["originalText"], response["redactedText"], response["usage"], de_id_results)
    

    def get_custom_models(self) -> List[CustomModel]:
        """Return all custom models owned by the user
         
        Returns
        -------
        List[CustomModel]
            A list of all custom models owned by the user
        """

        with requests.Session() as session:
            response = self.client.http_get("/api/models", session=session)
            models: List[CustomModel] = []
            for model in response:
                id = model['id']
                name = model['name']
                entities = model['entities']
                entityNames = [entity['label'] for entity in entities]
                models.append(CustomModel(id, name, entityNames))
            
            return models