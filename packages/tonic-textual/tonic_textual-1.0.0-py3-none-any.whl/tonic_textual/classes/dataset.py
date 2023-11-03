from __future__ import annotations
from typing import List, Dict
import os
import json
from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper
from urllib.parse import urlencode
import requests.exceptions;
import requests
import pandas as pd
from tonic_textual.classes.tonic_exception import DatasetFileMatchesExistingFile
from tonic_textual.classes.httpclient import HttpClient
from tonic_textual.classes.datasetfile import DatasetFile


class Dataset:
    """
    Class to represent and access a Tonic Textual Dataset.

    Parameters
    ----------
    id: str
        Dataset id.

    name: str
        Dataset name.

    files: Dict
        Serialized DatasetFile objects.

    client: HttpClient
        The http client to use.
    """
    def __init__(self, id: str, name: str, files: List[Dict], client: HttpClient):
        self.id = id
        self.name = name
        self.client = client
        self.files = [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in files]

        if len(self.files) > 0:
            self.num_columns = max([f.num_columns for f in self.files])
        else:
            self.num_columns = None

        self.num_rows_per_request = 1000
        self.total_rows_fetched = 0

        self._total_rows_fetched_in_current_file = 0
        self._cur_file_idx = 0

    def reset(self):
        self.total_rows_fetched = 0
        self._cur_file_idx = 0
        self._total_rows_fetched_in_current_file = 0

    def upload_then_add_file(self, file_path: str, file_name:str):
        """
        Uploads a file to the dataset.

        Parameters
        --------
        file_path: str
            The absolute path of the file to be uploaded
        file_name: IO[bytes]
            The name of the file to be saved to Tonic Textual

        Raises
        ------

        DatasetFileMatchesExistingFile
            If the contents of the file matches an existing file

        """
        file_size = os.path.getsize(file_path)
        with open(file_path, 'rb') as f:
            with tqdm(desc=f"[INFO] Uploading", total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
                reader_wrapper = CallbackIOWrapper(t.update, f, "read")

                files = {
                    'document': (None, json.dumps({"fileName": file_name, "csvConfig":{}, "datasetId": self.id}), 'application/json'),
                    'file': reader_wrapper
                }
                try:
                    updated_dataset = self.client.http_post(f"/api/dataset/{self.id}/files/upload", files=files)
                    #numRows is null when a file is first uploaded
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code==409:
                        raise DatasetFileMatchesExistingFile(e)
                    else:
                        raise e
        self.files = [DatasetFile(f['fileId'],f['fileName'],f.get('numRows'),f['numColumns'], f['processingStatus'], f.get('processingError')) for f in updated_dataset["files"]]

    def fetch_df(self) -> pd.DataFrame:
        """
        Paginated fetch returning dataset as pandas dataframe

        Returns
        -------
        pd.DataFrame
            Data in pandas dataframe
        """
        self.reset()
        data = self._fetch()

        columns = ['col'+str(x) for x in range(self.num_columns)]

        if len(data)==0:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame(data, columns=columns)

    def fetch_json(self) -> str:
        """
        Paginated fetch returning dataset as json

        Returns
        -------
        Dataset
            Data in json format
        """
        return json.dumps(self._fetch())

    def _fetch(self) -> List[List[str]]:
        """
        Paginated fetch of dataset.

         Returns
        -------
        List[List[str]]
            The data.
        """

        if(self._cur_file_idx >= len(self.files)):
            return []

        response = []

        with requests.Session() as session:
            while True:
                response += self._fetch_current_file(session)
                if self._cur_file_idx>=len(self.files):
                    break
        return response

    def _fetch_current_file(self, session: requests.Session) -> List[List[str]]:
        if(self._cur_file_idx>=len(self.files)):
            return []
        file = self.files[self._cur_file_idx]
        rows_left = file.num_rows - self._total_rows_fetched_in_current_file
        if rows_left==0:
            self._total_rows_fetched_in_current_file = 0
            self._cur_file_idx += 1
            if self._cur_file_idx>=len(self.files):
                return []
            file = self.files[self._cur_file_idx]
            rows_left = file.num_rows - self._total_rows_fetched_in_current_file
        num_rows_to_fetch = min(self.num_rows_per_request, rows_left)
        params = {'startingRow': self._total_rows_fetched_in_current_file, 'numRows': num_rows_to_fetch}
        response = self.client.http_get(f"/api/dataset/{self.id}/files/{file.id}/get_data?" + urlencode(params), session=session)
        self.total_rows_fetched += len(response)
        self._total_rows_fetched_in_current_file += len(response)
        if len(response) != num_rows_to_fetch: # safeguard against infinite loop
            self._total_rows_fetched_in_current_file = 0
            self._cur_file_idx += 1

        return response

    def fetch_all_df(self) -> pd.DataFrame:
        """
        Fetch all data in the dataset as pandas dataframe

        Returns
        -------
        pd.DataFrame
            Data in pandas dataframe
        """
        data = self._fetch_all()

        if self.num_columns is None:
            return pd.DataFrame()

        #RAW file, not CSV
        if self.num_columns == 0:
            if len(data)==0:
                return pd.DataFrame(columns=["text"])
            return pd.DataFrame(data, columns=["text"])

        columns = ['col'+str(x) for x in range(self.num_columns)]
        if len(data)==0:
            return pd.DataFrame(columns=columns)
        else:
            return pd.DataFrame(data, columns=columns)

    def fetch_all_json(self) -> str:
        """
        Fetch all data in the dataset as pandas json

        Returns
        -------
        str
            Data in json format
        """
        return json.dumps(self._fetch_all())

    def _fetch_all(self) -> List[List[str]]:
        """
        Fetch all data from the dataset.

        Returns
        -------
        List[List[str]]
            The data.
        """
        response = []
        with requests.Session() as session:
            for file in self.files:
                try:
                    more_data = self.client.http_get(f"/api/dataset/{self.id}/files/{file.id}/get_data", session=session)
                    response += more_data
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code==409:
                        continue
                    else:
                        raise e
            return response

    def get_processed_files(self) -> List[DatasetFile]:
        """
        Get all files in dataset that have completed being processed.  The data in these files will be returned when data is requested.

        Returns
        ------
        List[DatasetFile]:
            The list of files
        """
        return list(filter(lambda x: x.processing_status=="Completed" ,self.files))

    def get_queued_files(self) -> List[DatasetFile]:
        """
        Get all files in dataset that are awaiting being processed.

        Returns
        ------
        List[DatasetFile]:
            The list of files
        """
        return list(filter(lambda x: x.processing_status=="Queued" ,self.files))

    def get_running_files(self) -> List[DatasetFile]:
        """
        Get all files in dataset that are currently being processed.

        Returns
        ------
        List[DatasetFile]:
            The list of files
        """
        return list(filter(lambda x: x.processing_status=="Running" ,self.files))

    def get_failed_files(self) -> List[DatasetFile]:
        """
        Get all files in dataset that encountered an error when being processed.  These files are effectively ignored.

        Returns
        ------
        List[DatasetFile]:
            The list of files
        """
        return list(filter(lambda x: x.processing_status=="Failed" ,self.files))

    def describe(self):
        """
        Print the dataset name, id, and list of files.

        Examples
        --------
        >>> workspace.describe()
        Dataset: your_dataset_name [dataset_id]
        Number of Files: 2
        Number of Rows: 1000
        """

        print("Dataset: " + self.name + " [" + self.id + "]")
        print("Number of Files: " + str(len(self.get_processed_files())))
        print("Files that are waiting for processing: " + ", ".join([str((f.id,f.name)) for f in self.get_queued_files()+self.get_running_files()]))
        print("Files that encountered errors while processing: " + ", ".join([str((f.id,f.name)) for f in self.get_failed_files()]))
        print("Number of Rows: " + str(sum([x.num_rows if x.num_rows is not None else 0 for x in self.files])))
        print("Number of rows fetched: " + str(self.total_rows_fetched))