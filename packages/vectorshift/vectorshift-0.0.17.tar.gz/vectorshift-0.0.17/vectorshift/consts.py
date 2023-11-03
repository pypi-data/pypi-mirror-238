from dotenv import load_dotenv
import os

# Pipeline input and output types.
INPUT_NODE_TYPES = ['text', 'file']
OUTPUT_NODE_TYPES = ['text', 'file']

# VectorStore parameters.
VECTORSTORE_DEFAULT_CHUNK_SIZE = 400
VECTORSTORE_DEFAULT_CHUNK_OVERLAP = 0

# Node-specific parameters.
# TODO: this might be redundant (e.g. llm-openai-node.js)
# Map of LLMs to token limits
SUPPORTED_OPENAI_LLMS = {
    'gpt-3.5-turbo': 4096,
    'gpt-3.5-turbo-16k': 16384,
    'gpt-4': 8192,
    'gpt-4-32k': 32768
}
SUPPORTED_ANTHROPIC_LLMS = {'claude-v2': 100000}
# Map of image gen models to possible sizes (in both dimensions; if in the 
# future non-square images can be generated we'll update this), and # of
# possible images to generate
SUPPORTED_IMAGE_GEN_MODELS = {
    'DALL·E 2': ([256, 512, 1024], list(range(1, 5))),
    'Stable Diffusion XL': ([512], [1])
}
SUPPORTED_SPEECH_TO_TEXT_MODELS = ['OpenAI Whisper']
CHAT_MEMORY_TYPES = ['Full - Formatted', 'Full - Raw', 'Message Buffer', 'Token Buffer']
# A doubly-nested dictionary. In the first level, we map the integration node type (as stored in the object's type field in the Mongo integrations table) to
# a dict of supported functions for that integration (as will be described in 
# the node's data.function.name field in the Mongo pipeline table). In the 
# second level, each function name is mapped to its task/display name and its
# input/output details. Note: the function name should be added to the resulting 
# object value's name field if working with Mongo.
# TODO: This is analogous to app/src/reactflow/nodes/integration-schema.js, I 
# wonder if we could combine them somehow.
INTEGRATION_PARAMS = {
    'Salesforce': {
        'run_sql_query': {
            'taskName': 'salesforce.run_sql_query',
            'displayName': 'Run SQL Query',
            'inputs': [{ 
                'name': 'sql_query', 
                'displayName': 'SQL Query', 
                'multiInput': True 
            }],
            'outputs': [{ 'name': 'output', 'displayName': 'Output'}],
            'fields': []
        },
    },
    'Google Drive': {
        'read_files': {
            'taskName': 'google_drive.read_files',
            'displayName': 'Read Files',
            'inputs': [],
            'outputs': [{ 'name': 'output', 'displayName': 'Output' }],
            'fields': []
        },
        'save_files': {
            'taskName': 'google_drive.save_files',
            'displayName': 'Save Files',
            'inputs': [
                { 'name': 'name', 'displayName': 'Name', 'multiInput': False },
                { 'name': 'files', 'displayName': 'Files', 'multiInput': True },
            ],
            'outputs': [],
            'fields': []
        },
    },
    'Microsoft': {},
    'Notion': {
        'read_data': {
            'taskName': 'notion.read_data',
            'displayName': 'Read Data',
            'inputs': [],
            'outputs': [{ 'name': 'output', 'displayName': 'Output' }],
            'fields': []
        }
    },
    'Airtable': {
        'read_tables': {
            'taskName': 'airtable.read_tables',
            'displayName': 'Read Tables',
            'inputs': [],
            'outputs': [{'name': 'output', 'displayName': 'Output'}],
            'fields': [{
                'name': 'selectedTables', 
                'displayName': 'Select Tables', 
                'type': 'button', 
                'completedValue': 'Tables Selected'
            }],
        },
    },
    'Hubspot': {
        'search_contacts': {
            'taskName': 'hubspot.search_companies',
            'displayName': 'Search Companies',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        },
        'search_companies': {
            'taskName': 'hubspot.search_companies',
            'displayName': 'Search Companies',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        },
        'search_deals': {
            'taskName': 'hubspot.search_deals',
            'displayName': 'Search Deals',
            'inputs': [
                {'name': 'query', 'displayName': 'Query', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        }
    },
    'SugarCRM': {
        'get_records': {
            'taskName': 'sugar_crm.get_records',
            'displayName': 'Get Records',
            'inputs': [
                {'name': 'module', 'displayName': 'Module', 'multiInput': False},
                {'name': 'filter', 'displayName': 'Filter', 'multiInput': False},
            ],
            'outputs': [
                {'name': 'output', 'displayName': 'Output'}
            ],
            'fields': [],
        }
    }
}

# Relevant API endpoints the SDK code needs. Could also refactor to get rid of
# MODE entirely.
load_dotenv()
MODE = os.environ.get('ENVIRONMENT', 'PROD')
DOMAIN = 'http://localhost:8000' if MODE != 'PROD' else 'https://api.vectorshift.ai'

API_FILE_FETCH_ENDPOINT = f'{DOMAIN}/api/files/fetch'
API_INTEGRATION_FETCH_ENDPOINT = f'{DOMAIN}/api/integrations/fetch'
API_TRANSFORMATION_FETCH_ENDPOINT = f'{DOMAIN}/api/transformations/fetch'

API_VECTORSTORE_SAVE_ENDPOINT = f'{DOMAIN}/api/vectorstores/add'
API_VECTORSTORE_FETCH_ENDPOINT = f'{DOMAIN}/api/vectorstores/fetch'
API_VECTORSTORE_LOAD_ENDPOINT = f'{DOMAIN}/api/vectorstores/load'
API_VECTORSTORE_QUERY_ENDPOINT = f'{DOMAIN}/api/vectorstores/query'
API_VECTORSTORE_LIST_VECTORS_ENDPOINT = f'{DOMAIN}/api/vectorstores/list-vectors'

API_PIPELINE_SAVE_ENDPOINT = f'{DOMAIN}/api/pipelines/add'
API_PIPELINE_FETCH_ENDPOINT = f'{DOMAIN}/api/pipelines/fetch'
API_PIPELINE_RUN_ENDPOINT = f'{DOMAIN}/api/pipelines/run'
