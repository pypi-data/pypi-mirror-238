#MonsterAPIClient.py

"""
Monster API Python client to connect to Generative AI models on monsterapi

Base URL: https://api.monsterapi.ai/v1/generate/{model}

## Available models:

LLMs:
1. falcon-7b-instruct
2. falcon-40b-instruct
3. mpt-30B-instruct
4. mpt-7b-instruct
5. openllama-13b-base
6. llama2-7b-chat

Image Gen:
1. txt2img - stable-diffusion v1.5
2. sdxl - stable-diffusion XL V1.0
3. pix2pix -  Instruct-pix2pix
4. img2img - Image to Image using Stable Diffusion

Speech Gen:
1. sunoai-bark - Bark (Sunoai Bark)
2. whisper -  (Whisper Large V2)
"""
import os
import time
import json
import logging
import requests
import mimetypes
from requests_toolbelt.multipart.encoder import MultipartEncoder

from typing import Optional, Literal, Union, List, Dict, Iterable
from pydantic import BaseModel, Field
from functools import wraps

from monsterapi.InputDataModels import LLMInputModel1, LLMInputModel2, SDInputModel, MODELS_TO_DATAMODEL, FileField
from monsterapi.deployDataModels import LLMServingParams, CustomImageParams, DEPLOY_SERVICES

# Use LOGGING_LEVEL environment variable to set logging level
# Default logging level is INFO
level = os.environ.get('LOGGING_LEVEL', 'INFO')

if level == 'DEBUG':
    logging.basicConfig(level=logging.DEBUG)
elif level == 'INFO':
    logging.basicConfig(level=logging.INFO)
elif level == 'WARNING':
    logging.basicConfig(level=logging.WARNING)
elif level == 'ERROR':
    logging.basicConfig(level=logging.ERROR)
elif level == 'CRITICAL':
    logging.basicConfig(level=logging.CRITICAL)

logger = logging.getLogger(__name__)

def retry_on_status(codes={400}, retries=3, delay=5):
    """
    Decorator that retries the function when it raises a requests.HTTPError with certain status codes.

    :param codes: The HTTP status codes to retry on, default is {400}.
    :param retries: The number of retries, default is 3.
    :param delay: The delay between retries in seconds, default is 5.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retries):
                try:
                    result = func(*args, **kwargs)
                    return result
                except requests.HTTPError as e:
                    if e.response.status_code in codes:
                        time.sleep(delay)
                    else:
                        raise e
            raise Exception("Maximum retry attempts reached, request failed.")
        return wrapper
    return decorator


class MClient():
    """
    ## Monster API Client

    Monster API Python client for connecting to Generative AI Models on Monster API.

    This class provides methods for interacting with the Monster API to generate content using various Gen AI models.

    Args:
    - `api_key` (Optional[str]): The API key for authentication. If set to None, it will be fetched from the 'MONSTER_API_KEY' environment variable.
    - `base_url` (str): The base URL for the Monster API.

    Raises:
    - `ValueError`: If the 'api_key' is not provided and the 'MONSTER_API_KEY' environment variable is not set.

    Attributes:
    - `auth_token` (str): The MONSTER_API_KEY token used for API requests.
    - `models_to_data_model` (dict): A mapping of available models to their corresponding data models.

    Usage:
    - Import the Module:

    **python**

    ```
    from monsterapi import client
    ```

    Set Your API Key:
    You can set the `MONSTER_API_KEY` environment variable to your API key:

    **bash**
    ```
    export MONSTER_API_KEY=<your_api_key>
    ```

    Or, pass the `api_key` parameter to the client constructor:

    **python**
    ```
    client = client(api_key=<your_api_key>)
    ```


    See list of available models:

    **python**

    ```     
    print(client.models_to_data_model) 
    ```
    """
    def __init__(self, api_key: Optional[str] = None, base_url: str = 'https://api.monsterapi.ai/v1'):
        self.boundary = '---011000010111000001101001'
        
        if api_key is not None:
            self.auth_token = api_key
        else:
            self.auth_token = os.environ.get('MONSTER_API_KEY')
            if not self.auth_token:
                raise ValueError("MONSTER_API_KEY environment variable not set!")
        
        self.headers = {
            "accept": "application/json",
            'Authorization': 'Bearer ' + self.auth_token}
        self.base_url = base_url
        self.models_to_data_model = MODELS_TO_DATAMODEL
        

    def get_response(self, model, data: dict):
        """
        -------------------

        Get a response from the Monster API for a specified model and input data.

        Args:
        - `model` (str): The name of the model to use for generating content.
        - `data` (dict): The input data for the model.

        Returns:
        - `dict`: The response JSON containing the process_id for the given payload from the Monster API.

        Raises:
        - `ValueError`: If the provided 'model' is not a valid model name.
        - `FileNotFoundError`: If a file specified in 'data' is not found.
        - `ValueError`: If the size of a file specified in 'data' is greater than 8MB (not supported).

        **Usage:**
        ```python
        # Fetching a response
        response = client.get_response(model='falcon-7b-instruct', data={
            "prompt": "Your prompt here",
            # ... other parameters
        })
        print(response["process_id"])
        ```

        """
        if model not in self.models_to_data_model:
            raise ValueError(f"Invalid model: {model}!")

        dataModel = self.models_to_data_model[model](**data)
        
        form_data = {}
        files = {}
        
        # Convert model data to dictionary
        for key, value in dataModel.dict().items():
            form_data[key] = str(value)

        # Check for file fields
        for key, value in dataModel.__annotations__.items():
            if value == FileField:
                field_value = dataModel.__getattribute__(key)
                if not field_value.startswith('http'):
                    if os.path.exists(field_value):
                        file_type, _ = mimetypes.guess_type(field_value)
                        files[key] = (field_value, file_type)
                    else:
                        raise FileNotFoundError(f"File {field_value} not found!")
        
        # Combine form_data and files into a single dictionary
        for key, (file_path, file_type) in files.items():
            file_data = open(file_path, 'rb')
            # if size of file_data is greater than 8MB then raise error
            if os.path.getsize(file_path) > 8 * 1024 * 1024:
                raise ValueError(f"File size of {file_path} is greater than 8MB, currently not supported!")
            form_data[key] = (os.path.basename(file_path), file_data, file_type)
        
        multipart_encoder = MultipartEncoder(
            fields=form_data,
            boundary=self.boundary
        )
        
        headers = self.headers.copy()
        headers['Content-Type'] = f"multipart/form-data; boundary={self.boundary}"

        url = f"{self.base_url}/generate/{model}"

        response = requests.post(
            url,
            headers=headers,
            data=multipart_encoder
        )
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        return response.json()
    
    def get_status(self, process_id):
        """
        -------------------

        Get the status of a process by its ID.

        Args:
        - `process_id` (str): The ID of the process for which to retrieve the status.

        Returns:
        - `dict`: The status information as a JSON dictionary from the Monster API. Options Include - IN_QUEUE, IN_PROGRESS, COMPLETED, FAILED

        Raises:
        - `requests`.exceptions.HTTPError: If there is an HTTP error while making the request.

        **Usage:**
        ```python
        status = client.get_status("your_process_id")
        print(status)
        ```


        """
        # /v1/status/{process_id}
        url = f"{self.base_url}/status/{process_id}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        return response.json()
    
    def wait_and_get_result(self, process_id, timeout=100):
        """
        --------------------

        Wait for a process to complete and get the result.

        Args:
        - `process_id` (str): The ID of the process for which to wait and retrieve the result.
        - `timeout` (int): The maximum time to wait for the process to complete (in seconds).

        Returns:
        - `dict`: The result JSON from the Monster API when the process is completed.

        Raises:
        - `TimeoutError`: If the process times out and doesn't complete within the specified 'timeout'.
        - `RuntimeError`: If the process fails to complete with an error message.

        **Usage:**
        ```python
        # Waiting for result
        result = client.wait_and_get_result("your_process_id")
        print(result)
        ```


        """
        start_time = time.time()
        while True:
            elapsed_time = time.time() - start_time

            if elapsed_time >= timeout:
                raise TimeoutError(f"Process {process_id} timed out after {timeout} seconds.")

            status = self.get_status(process_id)
            if status['status'].lower() == 'completed':
                return status['result']
            elif status['status'].lower() == 'failed':
                raise RuntimeError(f"Process {process_id} failed! {status}")
            else:
                logger.debug(f"Process {process_id} is still running, status is {status['status']}. Waiting ...")
                time.sleep(0.01)
    
    def get_streaming_response(self, response: requests.Response) -> Iterable[List[str]]:
        for chunk in response.iter_lines(chunk_size=8192,
                                        decode_unicode=False,
                                        delimiter=b"\0"):
            if chunk:
                data = json.loads(chunk.decode("utf-8"))
                output = data["text"]
                yield output

    def get_response_sync_api(self, model, data: dict) -> dict:
        self.models_to_data_model[model](**data)
        model_tag = model.split('-')[-1]
        url = self.base_url + "/generate"
        response = requests.post(
            url,
            headers=self.headers,
            json=data
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        
        if data.get("stream",False):
            return self.get_streaming_response(response)
        else:
            return response.json()


    def generate(self, model, data: dict, timeout: int = 100) -> dict:
        """
        ------------------

        Directly generate results using a specified model and input data.

        Args:
        - `model` (str): The name of the model to use for generating content.
        - `data` (dict): The input data for the model.

        Returns:
        - `dict`: The generated content as a JSON dictionary from the Monster API.

        Raises:
        - `ValueError`: If the provided 'model' is not a valid model name.
        - `FileNotFoundError`: If a file specified in 'data' is not found.
        - `ValueError`: If the size of a file specified in 'data' is greater than 8MB (not supported).
        - `TimeoutError`: If the process times out and doesn't complete within a specified time.
        - `RuntimeError`: If the process fails to complete with an error message.

        **Usage:**
        ```python
        result = client.generate(model='falcon-7b-instruct', data={
            "prompt": "Your prompt here",
            # ... other parameters
        })
        ```

        *Note: Input Model Payload Parameters can be found [here](./docs/InputModelPayload.md)*


        """
        if "quickserve" in model:
            return self.get_response_sync_api(model, data)
        else:
            response = self.get_response(model, data)
            process_id = response['process_id']
            return self.wait_and_get_result(process_id, timeout=timeout)

    
    def deploy(self, service: Literal["llm", "custom_image"], params: dict):
        """
        Deploy a LLM model on monsterapi all you need is basemodel path and lora adapter path if needed and GPU VRam requirement. 

        Parameters:
        -----------
            service: str Service to deploy currently only 'llm' is implemented.
            params: dict deployLLMInputDataModel see monsterapi/deployDataModels.py for more details

        Returns:

        """
        if service not in DEPLOY_SERVICES:
            raise ValueError(f"Invalid service: {service}!")

        # Validate data payload with pydantic model
        if service == "llm":
            LLMServingParams(**params)
        elif service == "custom_image":
            CustomImageParams(**params)

        url = f"{self.base_url}/deploy/{service}"
        response = requests.post(
            url,
            headers=self.headers,
            json=params
        )
        
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        
        return response.json()

    @retry_on_status(codes={501}, retries=3, delay=5)
    def get_deployment_status(self, deployment_id: str):
        url = f"{self.base_url}/deploy/status/{deployment_id}"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        
        return response.json()

    def get_deployment_logs(self, deployment_id: str, n_lines = 100):
        url = f"{self.base_url}/deploy/logs/{deployment_id}"
        response = requests.get(url, headers=self.headers, params={"n_lines": n_lines})
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        return response.json()

    def get_list_of_deployments(self):
        url = f"{self.base_url}/deploy/list"
        response = requests.get(url, headers=self.headers)
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
        
        return response.json()
    
    def terminate_deployment(self, deployment_id: str):
        url = f"{self.base_url}/deploy/terminate"
        data = {
            "deployment_id": deployment_id,
            "actor": "user"
        }
        response = requests.post(
            url,
            headers=self.headers,
            json=data
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            response_content = response.json()
            logger.info(e)
            logger.info(response_content)

            # Construct a new error message containing the original message and the JSON response.
            new_error_message = f"{str(e)} - Response: {response_content}"
            
            # Raise the new error
            raise requests.HTTPError(new_error_message, response=response)
       
        return response.json()
