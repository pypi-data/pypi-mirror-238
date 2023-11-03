# functionality for defining and working with Vector Store objects
import requests
import json

import vectorshift
from vectorshift.consts import (
    VECTORSTORE_DEFAULT_CHUNK_SIZE,
    VECTORSTORE_DEFAULT_CHUNK_OVERLAP,
    API_VECTORSTORE_FETCH_ENDPOINT,
    API_VECTORSTORE_SAVE_ENDPOINT,
    API_VECTORSTORE_LOAD_ENDPOINT,
    API_VECTORSTORE_QUERY_ENDPOINT,
    API_VECTORSTORE_LIST_VECTORS_ENDPOINT,
)

class VectorStore:
    # initializes a new Vector Store
    def __init__(
        self,
        name: str,
        description: str = '',
        chunk_size: int = VECTORSTORE_DEFAULT_CHUNK_SIZE,
        chunk_overlap: int = VECTORSTORE_DEFAULT_CHUNK_OVERLAP,
        is_hybrid: bool = False,
        id: str = None
    ):
        self.name = name
        self.description = description
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.is_hybrid = is_hybrid
        self.id = id

    # converts Vector Store object to JSON representation
    def to_json_rep(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'chunkSize': self.chunk_size,
            'chunkOverlap': self.chunk_overlap,
            'isHybrid': self.is_hybrid,
        }
    
    def to_json(self):
        return json.dumps(self.to_json_rep())
    
    @staticmethod
    def from_json_rep(json_data: dict[str, any]):
        return VectorStore(
            name=json_data.get('name'),
            description=json_data.get('description'),
            chunk_size=json_data.get('chunkSize', VECTORSTORE_DEFAULT_CHUNK_SIZE),
            chunk_overlap=json_data.get('chunkOverlap', VECTORSTORE_DEFAULT_CHUNK_OVERLAP),
            is_hybrid=json_data.get('isHybrid', False),
            id=json_data.get('id'),
        )
    
    @staticmethod
    def from_json(json_str: str):
        json_data = json.loads(json_str)
        return VectorStore.from_json_rep(json_data)

    def __repr__(self):
        # TODO: format this reprerentation to be more readable
        return f'VectorStore({", ".join(f"{k}={v}" for k, v in self.to_json_rep().items())})'

    # TODO: Add validation for vectorstore_id and pipeline_id (in pipeline.py)
    # to prevent 5XX errors
    @staticmethod
    def fetch(
        vectorstore_name: str = None,
        vectorstore_id: str = None,
        username: str = None,
        org_name: str = None,
        public_key: str = None,
        private_key: str = None
    ):
        if vectorstore_id is None and vectorstore_name is None:
            raise ValueError("Must specify either vectorstore_id or vectorstore_name.")
        if vectorstore_name is not None and username is None and org_name is not None:
            raise ValueError("Must specify username if org_name is specified.")

        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            data={
                'vectorstore_id': vectorstore_id,
                'vectorstore_name': vectorstore_name,
                'username': username,
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching vectorstore object: {response.text}')
        response = response.json()

        return VectorStore.from_json_rep(response)

    def save(
        self,
        update_existing: bool = False,
        public_key: str = None,
        private_key: str = None,
    ):
        if update_existing and not self.id:
            raise ValueError("Error updating: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.")
        # if update_existing is false, save as a new vectorstore
        if not update_existing:
            self.id = None

        # API_VECTORSTORE_SAVE_ENDPOINT handles saving and updating vectorstore 
        # depending on whether or not the JSON has an id (logic in api repo)
        response = requests.post(
            API_VECTORSTORE_SAVE_ENDPOINT,
            data=({'vectorstore': self.to_json()}),
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )

        if response.status_code != 200:
            raise Exception(f'Error saving vectorstore object: {response.text}')
        response = response.json()
        self.id = response.get('id')

        return response

    def load_vectors(
        self,
        value,
        value_type: str = 'File',
        chunk_size: int = None,
        chunk_overlap: int = None,
        metadata: dict = None,
        public_key: str = None,
        private_key: str = None,
    ):
        if not self.id:
            raise ValueError("Error loading vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.")

        chunk_size = chunk_size or self.chunk_size
        chunk_overlap = chunk_overlap or self.chunk_overlap

        data = {
            'vectorstore_id': self.id,
            'type': value_type,
            'chunk_size': chunk_size,
            'chunk_overlap': chunk_overlap,
            'metadata': json.dumps(metadata),
        }

        headers={
            'Public-Key': public_key or vectorshift.public_key,
            'Private-Key': private_key or vectorshift.private_key,
        }

        if value_type == 'File':
            if isinstance(value, str):
                with open(value, 'rb') as f:
                    files = {'value': f}
                    response = requests.post(
                        API_VECTORSTORE_LOAD_ENDPOINT,
                        data=data,
                        headers=headers,
                        files=files,
                    )
            else:
                files = {'value': value}
                response = requests.post(
                    API_VECTORSTORE_LOAD_ENDPOINT,
                    data=data,
                    headers=headers,
                    files=files,
                )

        else:
            data['value'] = value
            response = requests.post(
                API_VECTORSTORE_LOAD_ENDPOINT,
                data=data,
                headers=headers,
            )

        if response.status_code != 200:
            raise Exception(f'Error loading vectors: {response.text}')
        response = response.json()

        return response

    def query(
        self,
        query: str,
        max_docs: int = 5,
        filter: dict = None,
        rerank: bool = False,
        public_key: str = None,
        private_key: str = None,
    ):
        filter = filter or {}
        response = requests.post(
            API_VECTORSTORE_QUERY_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'query': query,
                'max_docs': max_docs,
                'filter': filter,
                'rerank': rerank,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        response = response.json()

        return response

    def list_vectors(self, max_vectors: int = None):
        if not self.id:
            raise ValueError("Error listing vectors: vectorstore object does not have an existing ID. It must be saved as a new vectorstore.")
        response = requests.post(
            API_VECTORSTORE_LIST_VECTORS_ENDPOINT,
            data={
                'vectorstore_id': self.id,
                'max_vectors': max_vectors,
            },
            headers={
                'Public-Key': vectorshift.public_key,
                'Private-Key': vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error listing vectors: {response.text}')
        response = response.json()

        return response

    def delete_vectors(self, vector_ids: list = None, filter: dict = None):
        raise NotImplementedError("Delete vectors is not yet implemented.")
