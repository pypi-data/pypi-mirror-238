from requests.exceptions import HTTPError

class DatasetNameAlreadyExists(Exception):
    """
        When there is an attempt to create a dataset with a name that already exists
    """
    def __init__(self, errors):
        # Call the base class constructor with the parameters it needs
        super().__init__("Dataset name already exists, please choose another name")

        # Now for your custom code...
        self.errors = errors

class DatasetFileMatchesExistingFile(HTTPError):
    """
        When there is an attempt to upload a file with content that matches that of a file that already exists in the dataset
    """
    def __init__(self, errors):
        super().__init__(errors.response.content or "Dataset file matches existing file, please choose another file")

        self.errors = errors