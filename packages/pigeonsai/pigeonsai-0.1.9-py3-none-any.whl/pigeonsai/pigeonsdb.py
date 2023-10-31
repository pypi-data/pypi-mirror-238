import requests
import json
import warnings
from tenacity import retry, wait_exponential, stop_after_attempt
from tqdm import tqdm
import logging
import time
import os
from concurrent.futures import ThreadPoolExecutor
from tenacity import retry, stop_after_attempt, wait_exponential, stop_after_attempt
from tenacity import retry, retry_if_exception_type, wait_fixed, stop_after_attempt
from requests.exceptions import HTTPError
import openai 

logger = logging.getLogger(__name__)

API_URL = "https://api.pigeonsai.com/api/v1"
GET_DB_INFO_API = "https://api.pigeonsai.com/api/v1/sdk/get-db-info"
base_url_search = "http://upsert.pigeonsai.com/search"
base_url_add = "http://upsert.pigeonsai.com/add"
SEARCH_URL = "http://upsert.pigeonsai.com/search"
base_url = "http://upsert.pigeonsai.com"



@retry(stop=stop_after_attempt(5), wait=wait_exponential(multiplier=1, min=2, max=30))
def post_request(url, headers, data):
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code != 200:
        raise Exception("Request failed with status code: {}".format(response.status_code))
    return response


def get_openai_embedding(texts, model="text-embedding-ada-002"):
    openai.api_key = os.environ["OPENAI_API_KEY"]
    response = openai.Embedding.create(input=texts, model=model)
    embeddings = [item['embedding'] for item in response['data']]
    return embeddings


class PigeonsDBError(Exception):
    pass


class PigeonsDB:
    __connection = None
    __index_p = None

    @staticmethod
    def init(dbname, API_KEY=None):
        if API_KEY == None:
            API_KEY = os.getenv('PIGEONSAI_API_KEY')
        if not API_KEY:
            raise ValueError("Missing PIGEONSAI_API_KEY")
        if not dbname:
            raise ValueError("Missing Database Name")
        index_p, connect = _get_db_info(api_key=API_KEY, dbname=dbname)
        
        print(index_p)
        
        logger.info("Initialized Connection")
        if connect:
            
            PigeonsDB.__connection = connect
            PigeonsDB.__index_p = index_p
            
        else:
            raise PigeonsDBError("API key or DB name not found")


    def search(query, k=5, nprobe=10, namespace="documents", metadata_filters=None, keywords=None, rerank=False, encode="openai") -> list:
        # if PigeonsDB.__connection is None:
        #     logger.error("Connection to PigeonsDB is not initialized. Please initialize the connection before proceeding.")
        #     return
        
        # if encode == False and not isinstance(query, list):
        #     logger.error("When 'encode' is set to False, the 'query' must be a list of vectors. Please provide a list of vectors as the query.")
        #     return
        
        # if encode == True and not isinstance(query, str):
        #     logger.error("When 'encode' is set to True, the 'query' must be a string. Please provide a string as the query.")
        #     return
        
        # if encode == False and rerank == True:
        #     logger.warning("Warning: When 'encode' is False PigeonsDB is not able to rerank on keywords, since a string is not passed in.")
        
        if metadata_filters is not None:
            if not isinstance(metadata_filters, list):
                raise ValueError("metadata_filters must be a list of dictionaries.")
            for item in metadata_filters:
                if not isinstance(item, dict) or len(item) != 1:
                    raise ValueError("Each item in metadata_filters must be a dictionary with exactly one key-value pair.")
            metadata_filters = [{"key": k, "value": v} for item in metadata_filters for k, v in item.items()]

        if encode == "openai":
            query_list = []
            query_list.append(query)
            query = get_openai_embedding(query)[0]
                    
                
        headers = {"Content-Type": "application/json"}
        headers["Host"] = "knative.pigeonsai.com"
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "query_text": query,
            "nprobe": nprobe,
            "k": k,
            "namespace": namespace,
            "metadata_filters": metadata_filters,
            "keywords": keywords,
            "rerank": rerank,
            "encode":False
        }

        start_time = time.time()
        response = requests.post(base_url_search, headers=headers, data=json.dumps(data))
        res = json.loads(response.text)
            
        if keywords:
            filtered_res = []
            for item in res:
                if all(keyword in item['text'] for keyword in keywords):
                    filtered_res.append(item)
            return filtered_res

        return res




    @staticmethod
    def add(documents: list, vectors=None, namespace: str = "documents" ,metadata_list=None, encode="openai"):
        def send_request(chunk, vector_chunk=None):
            url = base_url_add
            headers = {"Content-Type": "application/json"}
            headers["Host"] = "knative.pigeonsai.com"

            data = {
                "connection": PigeonsDB.__connection,
                "index_path": PigeonsDB.__index_p,
                "documents": chunk,
                "namespace": namespace,
                "metadata_list": metadata_list,
                "encode":encode
            }
            if vector_chunk is not None:
                data["vectors"] = vector_chunk

            response = None 

            @retry(wait=wait_fixed(5), stop=stop_after_attempt(4), retry=retry_if_exception_type(HTTPError))
            def retry_request():
                nonlocal response 
                response = requests.post(url, headers=headers, data=json.dumps(data))
                response.raise_for_status()
                return response

            try:
                response = retry_request()
                print("Response: ",response)
                logger.info(response.status_code)
            except HTTPError as http_err:
                if response and response.status_code == 502:
                    logger.error(f"HTTP error occurred: {http_err}. Retrying...")
                    logger.error(f"Response: {response}")
                else:
                    logger.error(f"Other HTTP error occurred: {http_err}.")
                    logger.error(f"Response: {response if response else 'No response'}")
                    return response.status_code if response else None
            except Exception as err:
                logger.error(f"Other error occurred: {err}")
                logger.error(f"Response: {response if response else 'No response'}")
                return response.status_code if response else None
        
            
            
        if encode == "openai":
            encode = False
            vectors = get_openai_embedding(documents)
            if vectors is None:
                logger.error("When 'encode' is False, 'vectors' cannot be None.")
                return
            if len(vectors) != len(documents):
                logger.error("The number of vectors and documents must be equal.")
                return 

            chunk_size = 1000
            chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]
            vector_chunks = [vectors[i:i + chunk_size] for i in range(0, len(vectors), chunk_size)]  
            for chunk, vector_chunk in zip(tqdm(chunks), vector_chunks):
                send_request(chunk, vector_chunk)

        else:            
            if vectors is None:
                logger.error("When 'encode' is False, 'vectors' cannot be None.")
                return
            if len(vectors) != len(documents):
                logger.error("The number of vectors and documents must be equal.")
                return 

            chunk_size = 1000
            chunks = [documents[i:i + chunk_size] for i in range(0, len(documents), chunk_size)]
            vector_chunks = [vectors[i:i + chunk_size] for i in range(0, len(vectors), chunk_size)]  
            for chunk, vector_chunk in zip(tqdm(chunks), vector_chunks):
                send_request(chunk, vector_chunk)




    @staticmethod
    def delete(object_ids: list, namespace="documents"):

        if PigeonsDB.__connection is None:
            raise PigeonsDBError("Connection not initialized.")
        url = f"{base_url}/delete"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "object_ids": object_ids,
            "namespace": namespace,

        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.info(response.json())


    @staticmethod
    def delete_by_metadata(metadata_filters: list, namespace="documents"):
        if PigeonsDB.__connection is None:
            raise PigeonsDBError("Connection not initialized.")
        url = f"{base_url}/delete_by_metadata"
        headers = {"Content-Type": "application/json"}
        data = {
            "connection": PigeonsDB.__connection,
            "index_path": PigeonsDB.__index_p,
            "metadata_filters": metadata_filters,
            "namespace": namespace,
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        logger.info(response.json())


def _get_db_info(api_key: str, dbname: str):
    url = GET_DB_INFO_API
    headers = {"Content-Type": "application/json"}
    data = {"api_key": api_key, "dbname": dbname}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code != 200:
        raise PigeonsDBError("API_KEY or db_name doesn't match.")

    db_info = response.json().get('DB info', {})
    index_p = db_info.get('s3_identifier')
    keys = ['dbname', 'user', 'password', 'host']
    connect = {key: db_info.get(key) for key in keys}

    return index_p, connect