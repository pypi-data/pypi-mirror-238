# functionality defining the shape and properties of computation nodes, and how
# they connect to each other in pipelines
from abc import ABC, abstractclassmethod
import json
import re
import requests

import vectorshift
from vectorshift.consts import *

# A parent class for all nodes. Shouldn't be initialized by the user directly.
class NodeTemplate(ABC):
    # TODO: think about where we might want to use @property.
    # Right now, some subclasses support an optional typechecking flag in
    # case we want to do future typchecking. See the pattern below of checking
    # if _typecheck is in kwargs. If we stick with this pattern, SDK users
    # shouldn't know that the _typecheck arg exists.
    def __init__(self):
        # Each node has a certain type, also called an "ID" in Mongo. The _id
        # of the node is formed by appending a counter to the node type.
        self.node_type:str = None
        self._id:str = None
        # Every node has zero or more inputs or outputs. Each output itself 
        # is a list (in case one input takes in/aggregates multiple outputs)
        self._inputs:dict[str, list[NodeOutput]] = {}
        
    # Inputs are a dictionary of NodeOutputs keyed by input fields (the in-edge 
    # labels in the no-code graph/the target handle for the node's in-edge).
    def inputs(self): return self._inputs
    
    # Outputs should be a dictionary of NodeOutputs keyed by output fields (the
    # out-edge labels/the source handle for the node's out-edge). Invariant: 
    # a key should equal the corresponding value's output_field.
    # For syntactic sugar, class-specific methods can also return specific 
    # outputs rather than the entire dict, e.g. the method "output()" that 
    # directly gives the NodeOutput object for nodes that only have one output.
    def outputs(self): raise NotImplementedError("Subclasses should implement this!")

    # The dictionary that corresponds with the JSON serialization of the node. 
    # This should return a subset of how a node object is stored as part of a
    # pipeline in Mongo, specifically, the following attributes: type, id, and
    # data (and all subfields therein). This should only be called after an id
    # has been assigned to the node.
    # NB: the JSON fields id/data.id and type/data.nodeType are the same.
    @abstractclassmethod
    def to_json_rep(self):
        # If the node references a user-defined object that lives on the VS
        # platform (other pipelines, integrations, files, vectorstores,
        # transformations), calling this function will involve an API call
        # to get the details of that user-defined object.
        # TODO: could refactor the setting _id and node_type logic to here.
        raise NotImplementedError("Subclasses should implement this!")
    
    # From a Python dict representing how a node is stored in JSON, create a
    # node object. IMPORTANTLY, this does NOT initialize the _inputs param 
    # with NodeOutput values (and thus doesn't perform typechecks); we expect 
    # NodeOutputs to be inserted post_hoc, and assume they're valid.
    @staticmethod
    @abstractclassmethod
    def _from_json_rep(json_data:dict):
        _ = json_data # if linter complains
        raise NotImplementedError("Subclasses should implement this!")
    
    @classmethod 
    def from_json_rep(cls, json_data: dict):
        n:NodeTemplate = cls._from_json_rep(json_data)
        n._id = json_data["id"]
        n._inputs = {k: [] for k in n._inputs.keys()}
        return n
    
    def __str__(self): return json.dumps(self.to_json_rep())

# A wrapper class for outputs from nodes, for basic "type"-checks and to figure
# out how nodes connect to each other. NOT the same as OutputNode, which is 
# a node that represents the final result of a pipeline.
class NodeOutput:
    def __init__(self, source:NodeTemplate, output_field:str, output_type:str):
        # The Node object producing this output.
        self.source = source
        # The specific output field from the source node (the node handle).
        self.output_field = output_field
        # A string roughly corresponding to the output type. (Strings are 
        # flimsy, but they will do the job.) TODO: This isn't really used now, 
        # but in the future this field could be used to ascribe general data 
        # types to outputs for better "type"-checking if needed.
        self.output_type = output_type
    def __str__(self):
        return f"Node output of type {self.output_type}"

# Each node subclasses NodeTemplate and takes in class-specific parameters 
# depending on what the node does. Node classes below are organized by their
# order and structure of appearance in the no-code editor.

# Let's try to avoid more than one level of subclassing.

###############################################################################
# HOME                                                                        #
###############################################################################

# Input nodes themselves don't have inputs; they define the start of a pipeline.
class InputNode(NodeTemplate):
    def __init__(self, name:str, input_type:str):
        super().__init__()
        self.node_type = "customInput"
        self.name = name
        # Text or File
        if input_type not in INPUT_NODE_TYPES:
            raise ValueError(f"Input node type {input_type} not supported.")
        self.input_type = input_type
        
    def output(self): 
        # Input nodes can produce anything in INPUT_NODE_TYPES, so we mark
        # the specific type here.
        return NodeOutput(
            source=self, 
            output_field="value", 
            output_type=self.input_type
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        # TODO: category and task_name can probably be made into class variables too.
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "inputName": self.name,
                "inputType": self.input_type.capitalize(),
                "category": "input",
                "task_name": "input"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return InputNode(
            name=json_data["data"]["inputName"], 
            input_type=json_data["data"]["inputType"].lower()
        )

# Outputs are the end of the pipeline and so only take inputs.
class OutputNode(NodeTemplate):
    def __init__(self, name:str, output_type:str, input:NodeOutput):
        super().__init__()
        self.node_type = "customOutput"
        self.name = name
        # Text or File
        if output_type not in OUTPUT_NODE_TYPES:
            raise ValueError(f"Output node type {output_type} not supported.")
        self.output_type = output_type
        self._inputs = {"value": [input]}

    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "outputName": self.name,
                "outputType": self.output_type.capitalize(),
                "category": "output",
                "task_name": "output"
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return OutputNode(
            name=json_data["data"]["outputName"], 
            output_type=json_data["data"]["outputType"].lower(),
            input=None
        )

# Text data. This is possibly even a little redundant because we can pass in
# plaintext inputs as additional params to nodes (without instantiating them
# as separate nodes) through code. Right now though I'm trying to get a 1:1 
# correspondance between no-code and code construction; we can discuss this.
class TextNode(NodeTemplate):
    # Text nodes can either just be blocks of text in themselves, or also take
    # other text nodes as inputs (e.g. with text variables like {{Context}}, 
    # {{Task}}). In the latter case, an additional argument text_inputs should
    # be passed in as a dict of input variables to Outputs.
    def __init__(self, text:str, text_inputs:dict[str, NodeOutput] = None, **kwargs):
        super().__init__()
        self.node_type = "text"
        self.text = text
        # if there are required inputs, they should be of the form {{}} - each
        # of them is a text variable
        text_vars = re.findall(r'\{\{([^{}]+)\}\}', self.text)
        text_vars = [v.strip() for v in text_vars]
        self.text_vars = []
        # remove duplicates while preserving order
        [self.text_vars.append(v) for v in text_vars if v not in self.text_vars]
        
        # if there are variables, we expect them to be matched with inputs
        # they should be passed in a dictionary with the
        # arg name text_inputs. E.g. {"Context": ..., "Task": ...}
        if text_inputs:
            if type(text_inputs) != dict:
                raise TypeError("text_inputs must be a dictionary of text variables to node outputs.")
            if "_typecheck" in kwargs and kwargs["_typecheck"]:
            # example type check: input variables should correspond to text
                for output in text_inputs.values():
                    if output.output_type != "text":
                        raise ValueError("Values in text_inputs must have type 'text'.")
            num_inputs = len(text_inputs.keys())
            num_vars = len(self.text_vars)
            if num_inputs != num_vars:
                raise ValueError(f"Number of text inputs ({num_inputs}) does not match number of text variables ({num_vars}).")
            if sorted(list(set(text_inputs.keys()))) != sorted(self.text_vars):
                raise ValueError("Names of text inputs and text variables do not match.")
            # wrap each NodeOutput into a singleton list to fit the type
            self._inputs = {k: [v] for k, v in text_inputs.items()}
        else:
            if len(self.text_vars) > 0:
                raise ValueError("text_inputs must be passed in if there are text variables.")
            
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        input_names = self.text_vars if len(self.text_vars) > 0 else None
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "text": self.text,
                "inputNames": input_names,
                "formatText": True,
                "category": "task",
                "task_name": "text",
            } 
        }
        
    def _from_json_rep(json_data:dict):
        text_inputs = None
        if json_data["data"]["inputNames"]:
            text_inputs = {}
            for name in json_data["data"]["inputNames"]:
                text_inputs[name] = None
        return TextNode(
            text=json_data["data"]["text"],
            text_inputs=text_inputs
        )

# Nodes representing file data, taking no inputs.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
class FileNode(NodeTemplate):
    def __init__(self, file_names:list[str], 
                 public_key:str=None, private_key:str=None):
        super().__init__()
        self.node_type = 'file'
        if file_names is None or file_names == []:
            raise ValueError('File names must be specified.')
        self.file_names = file_names
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # files take no inputs
    
    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def output(self):
        return NodeOutput(source=self, output_field='files', output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch files.')
        # Note: there's currently no way in the API code to get files owned 
        # by another user, nor is there a way to get files by their ID.
        response = requests.get(
            API_FILE_FETCH_ENDPOINT,
            data={
                'file_names': self.file_names,
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching files: {response.text}')
        # list of JSONs for each file
        files_json = response.json()
        return {
            'id': self._id, 
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'selectedFiles': files_json, 
                'category': 'task',
                'task_name': 'file'
            }
        }

    @staticmethod 
    def _from_json_rep(json_data:dict):
        file_names = [file_data['name'] for file_data in json_data['data']['selectedFiles']]
        return FileNode(
            file_names=file_names
        )

# Nodes representing entire other pipelines, a powerful tool for abstraction.
# When the node is executed, the pipeline it represents is executed with the
# supplied inputs, and the overall pipeline's output becomes the node's output.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
# TODO: We could also create (via another class?) a way to take in an existing
# Pipeline object into the constructor.
class PipelineNode(NodeTemplate):
    def __init__(self, pipeline_id:str=None, pipeline_name:str=None, 
                 inputs=dict[str, NodeOutput],
                 username:str=None, org_name:str=None,
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'pipeline'
        if pipeline_name is None and pipeline_id is None:
            raise ValueError('Either the pipeline ID or name should be specified.')
        self.pipeline_id = pipeline_id 
        self.pipeline_name = pipeline_name 
        self.username = username
        self.org_name = org_name 
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # We'd like to know what the input and output names are upon 
        # initialization so we can validate that the inputs dict matches up.
        # So the API call to get the pipeline JSON is located in the
        # constructor here (compare to other nodes, where it's in to_json_rep)
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch pipeline.')
        response = requests.get(
            API_PIPELINE_FETCH_ENDPOINT,
            data={
                'pipeline_id': pipeline_id,
                'pipeline_name': pipeline_name,
                'username': username,
                'org_name': org_name,
            },
            headers={
                'Public-Key': public_key or vectorshift.public_key,
                'Private-Key': private_key or vectorshift.private_key,
            }
        )
        if response.status_code != 200:
            raise Exception(response.text)
        # No need to construct a Pipeline object here.
        self.pipeline_json = response.json()
        self.pipeline_id = self.pipeline_json['id']
        self.pipeline_name = self.pipeline_json['name']
        # The list of inputs provided should have keys matching the input names
        # defined by the integration function
        input_names = [
            i['name'] for i in self.pipeline_json['inputs'].values()
        ]
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'Pipeline node inputs do not match expected input names: expected f{input_names}')
        
        self.batch_mode = kwargs.get('batch_mode', False)

        self._inputs = {
            input_name: [inputs[input_name]] for input_name in input_names
        }

    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def outputs(self):
        os = {}
        for o in self.pipeline_json['outputs'].values():
            output_field = o['name']
            os[output_field] = NodeOutput(
                source=self, output_field=output_field, output_type=None
            )
        return os
    
    def to_json_rep(self):
        pipeline_field_json = {
            # TODO: To my knowledge there is no way for the API to currently
            # return the "category" of a pipeline (favorite, my, imported etc.)
            # But this is stored in a pipeline node's representation as-is 
            # right now. For now I'm just excluding the field, as it doesn't 
            # seem to be used.
            'id': self.pipeline_json['id'],
            'name': self.pipeline_json['name'],
            'inputs': self.pipeline_json['inputs'],
            'outputs': self.pipeline_json['outputs'],
            # TODO: we just use the name as a placeholder; if this field is 
            # important we'll have to figure out a way to determine whether or
            # not the user/org name in this pipeline is different from the 
            # user/org name of whoever is writing this code (perhaps through
            # the Config class?). Same issue in TransformationNode.
            'displayName': self.pipeline_json['name']
        }

        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'pipeline': pipeline_field_json,
                'batchMode': self.batch_mode,
                'category': 'pipeline',
                'task_name': 'pipeline'
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict):
        return PipelineNode(
            pipeline_id=json_data['data']['pipeline']['id'],
            pipeline_name=json_data['data']['pipeline']['name'],
            # We don't have a way to recover the username/org name, or the 
            # API key
            inputs={
                i['name']: [None]
                for i in json_data['data']['pipeline']['inputs'].values()
            }
        )
    
# Integrations with third parties.
### USES USER-CREATED OBJECT - see comments in VectorStoreNode
# TODO: we can add a refactor in the opposite direction of the dataloader nodes
# i.e. making specific node classes for each kind of integration rather than
# having them all be in one node
class IntegrationNode(NodeTemplate):
    def __init__(self, integration:str, integration_name:str, function:str, 
                 inputs=dict[str, list[NodeOutput]],
                 public_key:str=None, private_key:str=None, **kwargs):
        super().__init__()
        self.node_type = 'integration'
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key

        # The specific integration is stored in two sub-fields under the 
        # data field in the node's JSON representation. One field contains 
        # details of the integration itself, which requires an API call to
        # retrieve the integration object from Mongo. The other contains 
        # details of the function to run with the integration, which defines
        # the inputs/outputs of the node and can be deduced from the 
        # constructor arguments provided.
        if integration not in INTEGRATION_PARAMS.keys():
            raise ValueError(f'Invalid integration {integration}.')
        if function not in INTEGRATION_PARAMS[integration].keys():
            raise ValueError(f'Invalid function {function} for integration {integration}.')
        self.integration = integration 
        self.integration_name = integration_name
        self.function = function
        self.function_params = INTEGRATION_PARAMS[self.integration][self.function]
        # add the function name to the function params
        self.function_params['name'] = self.function

        # The list of inputs provided should have keys matching the input names
        # defined by the integration function. 
        # Note: each input to an integration node could be a list of 
        # NodeOutputs (multiple in-edges to a node's input field, e.g. saving
        # multiple files to Drive at once). This is different from the input
        # structure for pipeline and transformation nodes.
        input_names = [
            i['name'] for i in self.function_params['inputs']
        ]
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'Integration node inputs do not match expected input names: expected f{input_names}')
        
        # Specific integrations require additional argument parameters passed
        # in via the constructor rather than NodeOutputs.
        self.airtable_tables = None
        if self.integration == 'Airtable' and self.function == 'read_tables':
            # Expect a list of dicts with base and table IDs and names for each
            # table to load from
            if not ('airtable_tables' in kwargs):
                raise ValueError('Base and table names and IDs must be provided to read Airtable tables.')
            for t in kwargs['airtable_tables']:
                if 'base_id' not in t or 'base_name' not in t or 'table_id' not in t or 'table_id' not in t:
                    raise ValueError('Missing base or table names or IDs.') 
                self.airtable_tables = kwargs['airtable_tables']

        self._inputs = { 
            input_name: inputs[input_name] for input_name in input_names 
        }
    
    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def outputs(self):
        os = {}
        for o in self.function_params['outputs']:
            output_field = o['name']
            os[output_field] = NodeOutput(
                source=self, output_field=output_field, output_type=None
            )
        return os
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch integration.')
        # Note: there's currently no way in the API code to get integrations
        # owned by another user, nor is there a way to get integrations by 
        # their ID.
        response = requests.get(
            API_INTEGRATION_FETCH_ENDPOINT,
            data={
                'integration_name': self.integration_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching integration: {response.text}")
        integration_json = response.json()
        # don't need to store integration parameters in node's JSON
        if 'params' in integration_json:
            del integration_json['params']

        json_rep = {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'integration': integration_json,
                'function': self.function_params,
                'category': 'integration',
                'task_name': self.function_params['taskName']
            }
        }
        if self.integration == 'Airtable' and self.function == 'read_tables':
            json_rep['selectedTables'] = self.airtable_tables
        return json_rep
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return IntegrationNode(
            integration=json_data['data']['integration']['type'],
            integration_name=json_data['data']['integration']['name'],
            function=json_data['data']['function']['name'],
            # For IntegrationNodes, we must pass in the input names to the 
            # constructor, as they will be validated against the integration 
            # and function upon initialization.
            inputs={ 
                i['name']: [None] 
                for i in json_data['data']['function']['inputs'].values()
            }
        )

### USES USER-CREATED OBJECT - see comments in VectorStoreNode
class TransformationNode(NodeTemplate):
    def __init__(self, transformation_name:str, inputs=dict[str, NodeOutput],
                 public_key:str=None, private_key:str=None):
        super().__init__()
        self.node_type = 'transformation'
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        self.transformation_name = transformation_name
        # We make an API call to get the transformation JSON here to get the
        # desired outputs - see PipelineNode
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch transformation.')
        # Note: there's currently no way in the API code to get files owned 
        # by another user, nor is there a way to get files by their ID.
        response = requests.get(
            API_TRANSFORMATION_FETCH_ENDPOINT,
            data={
                'transformation_name': self.transformation_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f'Error fetching transformation: {response.text}')
        self.transformation_json = response.json()
        input_names = self.transformation_json['inputs']
        # The list of inputs provided should have keys matching the input names
        # defined by the transformation
        if sorted(list(inputs.keys())) != sorted(input_names):
            raise ValueError(f'Transformation node inputs do not match expected input names: expected f{input_names}')

        self._inputs = {
            input_name: [inputs[input_name]] for input_name in input_names
        } 
    
    def outputs(self):
        os = {}
        for output_field in self.transformation_json['outputs'].keys():
            os[output_field] = NodeOutput(
                source=self, output_field=output_field, output_type=None
            )
        return os
    
    def to_json_rep(self):
        transformation_field_json = {
            'id': self.transformation_json['id'],
            'name': self.transformation_json['name'],
            'description': self.transformation_json['description'],
            'inputs': self.transformation_json['inputs'],
            'outputs': self.transformation_json['outputs'],
            # In the app repo this calls a helper function to format pipeline
            # names. For the time being this will be the same as the name as
            # the only case in which it isn't the name are if it's owned by the
            # user (which is impossible right now). TODO: may need to fix. Same
            # issue in PipelineNode.
            'displayName': self.transformation_json['name'],
        }

        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id,
                'nodeType': self.node_type,
                'transformation': transformation_field_json,
                'category': 'transformation',
                'task_name': 'transformation'
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return TransformationNode(
            transformation_name=json_data['data']['transformation']['name'],
            inputs={
                input_name: [None] 
                for input_name in json_data['data']['transformation']['inputs']
            }
        )

# File save nodes have no outputs.
class FileSaveNode(NodeTemplate):
    def __init__(self, name_input:NodeOutput, files_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = "fileSave"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if name_input.output_type != "text":
                raise ValueError("Name must be of type text.")
        self._inputs = {
            "name": [name_input],
            # files aggregates one or more node outputs
            "files": files_input
        }
    
    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "category": "task",
                "task_name": "save_file"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        _ = json_data 
        return FileSaveNode(
            name_input=None,
            files_input=[]
        )

###############################################################################
# LLMS                                                                        #
###############################################################################

class OpenAILLMNode(NodeTemplate):
    def __init__(self, model:str, system_input:NodeOutput, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "llmOpenAI"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            # example simple type-check: inputs should be text
            if system_input.output_type != "text" or prompt_input.output_type != "text":
                raise ValueError("LLM inputs must be text.")
        if model not in SUPPORTED_OPENAI_LLMS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model 
        # the user might have passed in more model params through kwargs
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ["max_tokens", "temperature", "top_p"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_OPENAI_LLMS[self.model]:
            raise ValueError(f"max_tokens {self.max_tokens} is too large for model {self.model}.")
        self._inputs = {"system": [system_input], "prompt": [prompt_input]}
    
    def output(self): 
        return NodeOutput(source=self, output_field="response", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "maxTokens": self.max_tokens,
                "temperature": str(round(self.temp, 2)),
                "topP": str(round(self.top_p, 2)),
                "category": "task",
                "task_name": "llm_openai"
            }
        }
       
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return OpenAILLMNode(
            model=json_data["data"]["model"],
            system_input=None,
            prompt_input=None,
            max_tokens=json_data["data"]["maxTokens"],
            temperature=float(json_data["data"]["temperature"]),
            top_p=float(json_data["data"]["topP"])
        )
        
class AnthropicLLMNode(NodeTemplate):
    def __init__(self, model:str, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "llmAnthropic"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if prompt_input.output_type != "text":
                raise ValueError("LLM inputs must be text.")
        if model not in SUPPORTED_ANTHROPIC_LLMS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model 
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ["max_tokens", "temperature", "top_p"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_OPENAI_LLMS[self.model]:
            raise ValueError(f"max_tokens {self.max_tokens} is too large for model {self.model}.")
        self._inputs = {"prompt": [prompt_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="response", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "maxTokens": self.max_tokens,
                "temperature": str(round(self.temp, 2)),
                "topP": str(round(self.top_p, 2)),
                "category": "task",
                "task_name": "llm_anthropic"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return AnthropicLLMNode(
            model=json_data["data"]["model"],
            prompt_input=None,
            max_tokens=json_data["data"]["maxTokens"],
            temperature=float(json_data["data"]["temperature"]),
            top_p=float(json_data["data"]["topP"])
        )

###############################################################################
# MULTIMODAL                                                                  #
###############################################################################

class ImageGenNode(NodeTemplate):
    def __init__(self, model:str, image_size:int, num_images:int, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "imageGen"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if prompt_input.output_type != "text":
                raise ValueError("Image generation inputs must be text.")
        if model not in SUPPORTED_IMAGE_GEN_MODELS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model
        if image_size not in SUPPORTED_IMAGE_GEN_MODELS[self.model][0]:
            raise ValueError(f"Invalid image size {image_size}.")
        if num_images not in SUPPORTED_IMAGE_GEN_MODELS[self.model][1]:
            raise ValueError(f"Invalid number of images {num_images}.")
        self.image_size = image_size 
        self.num_images = num_images 
        self._inputs = {"prompt": [prompt_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="images", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "size": f"{self.image_size}x{self.image_size}",
                "imageCount": self.num_images,
                "category": "task",
                "task_name": "generate_image"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        image_size_str = json_data["data"]["size"]
        image_size = int(image_size_str[:image_size_str.index('x')])
        return ImageGenNode(
            model=json_data["data"]["model"],
            image_size=image_size,
            num_images=int(json_data["data"]["imageCount"]),
            prompt_input=None,
        )
    
class SpeechToTextNode(NodeTemplate):
    def __init__(self, model:str, audio_input:NodeOutput):
        super().__init__()
        self.node_type = "speechToText"
        if model not in SUPPORTED_SPEECH_TO_TEXT_MODELS:
            raise ValueError(f"Invalid model {model}.")
        self.model = model
        self._inputs = {"audio": [audio_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="text", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "category": "task",
                "task_name": "speech_to_text"
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return SpeechToTextNode(
            model=json_data["data"]["model"],
            audio_input=None
        )

###############################################################################
# DATA LOADERS                                                                #
###############################################################################

# The specific data loaded by the nodes is given by the class name.
# TODO: Right now we have a different class to represent each type of data 
# loader available in the no-code platform. I think this could be significantly
# abstracted since most of the internal logic is the same.

class FileLoaderNode(NodeTemplate):
    def __init__(self, file_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if file_input.output_type != "InputNode.file":
                raise ValueError("Must take a file from an input node.")
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"file": [file_input]}
                
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "File",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_file"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return FileLoaderNode(
            file_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class CSVQueryNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, csv_input:NodeOutput, **kwargs):
        super().__init__()
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if query_input.output_type != "text":
                raise ValueError("CSV query input must have type 'text'.")
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input], "csv": [csv_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output() 
        return {o.output_field: o}

    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "CSV Query",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "query_csv"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return CSVQueryNode(
            query_input=None,
            csv_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class URLLoaderNode(NodeTemplate):
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"url": [url_input]}
    
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "URL",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_url"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return URLLoaderNode(
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
        
class WikipediaLoaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Wikipedia",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_wikipedia"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return WikipediaLoaderNode(
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class YouTubeLoaderNode(NodeTemplate):
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"url": [url_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "YouTube",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_youtube"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return YouTubeLoaderNode(
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class ArXivLoaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Arxiv",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_arxiv"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return ArXivLoaderNode(
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class SerpAPILoaderNode(NodeTemplate):
    def __init__(self, api_key_input:NodeOutput, query_input:NodeOutput, **kwargs):
        super().__init__()
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if api_key_input.output_type != "text":
                raise ValueError("API key input must have type text.")
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"apiKey": [api_key_input], "query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "SerpAPI",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_serpapi"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return SerpAPILoaderNode(
            api_key_input=None,
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class GitLoaderNode(NodeTemplate):
    def __init__(self, repo_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"repo": [repo_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Git",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_git"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return GitLoaderNode(
            repo_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class NotionLoaderNode(NodeTemplate):
    def __init__(self, token_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"token": [token_input], "database": [database_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Notion",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_notion"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return NotionLoaderNode(
            token_input=None,
            database_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class ConfluenceLoaderNode(NodeTemplate):
    def __init__(self, username_input:NodeOutput, api_key_input:NodeOutput, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {
            "username": [username_input],
            "apiKey": [api_key_input],
            "url": [url_input]
        }
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Confluence",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_confluence"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return ConfluenceLoaderNode(
            username_input=None,
            api_key_input=None,
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

###############################################################################
# VECTORDB                                                                    #
###############################################################################

class VectorDBLoaderNode(NodeTemplate):
    def __init__(self, documents_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = "vectorDBLoader"
        self.func, self.chunk_size, self.chunk_overlap = "default", VECTORSTORE_DEFAULT_CHUNK_SIZE, VECTORSTORE_DEFAULT_CHUNK_OVERLAP
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"documents": documents_input}
    
    def output(self):
        return NodeOutput(source=self, output_field="database", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "load_vector_db"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return VectorDBLoaderNode(
            input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class VectorDBReaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "vectorDBReader"
        self.func, self.max_docs_per_query = "default", 2
        for optional_param_arg in ["func", "max_docs_per_query"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input], "database": [database_input]}
    
    def output(self):
        # assume the reader returns the query result post-processed back into text
        return NodeOutput(source=self, output_field="results", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "query_vector_db",
                "maxDocsPerQuery": self.max_docs_per_query
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return VectorDBReaderNode(
            query_input=None,
            database_input=None,
            func=json_data["data"]["function"],
            max_docs_per_query=json_data["data"]["maxDocsPerQuery"]
        )
        
# With a couple of other nodes, this node references an existing object that
# lives in the VS platform, what we generally refer to as a "user-created 
# object" here. Thus, to access it, we need to make an API call to the server
# code in order to get the JSON and store the relevant parameters in the node.
class VectorStoreNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, public_key:str, private_key:str,
                 vectorstore_id=None, vectorstore_name=None, 
                 username=None, org_name=None, max_docs_per_query=1):
        super().__init__()
        self.node_type = 'vectorStore'
        if vectorstore_id is None and vectorstore_name is None:
            raise ValueError('Either the vectorstore ID or name should be specified.')
        self.vectorstore_id = vectorstore_id
        self.vectorstore_name = vectorstore_name
        self.username = username 
        self.org_name = org_name
        self.max_docs_per_query = max_docs_per_query
        # we'll need to use the API key when fetching the user-defined 
        # vectorstore
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # we don't store vectorstore-specific params like chunk params, since 
        # that is a property of the vectorstore and not the node
        self._inputs = {'query': [query_input]}
    
    # If this node was loaded from JSON and changed to reference another
    # vectorstore object, we need to use the API key to query the new object.
    # This setter provides an explicit way to make sure the API key is in the 
    # node (if the key weren't initialized globally).
    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key

    def output(self):
        return NodeOutput(source=self, output_field='results', output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch vectorstore.')
        # There's currently no notion of "sharing" vectorstores (so username
        # and org_name aren't required right now), but there probably will be 
        # one in the future.
        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            data={
                'vectorstore_id': self.vectorstore_id,
                'vectorstore_name': self.vectorstore_name,
                'username': self.username,
                'org_name': self.org_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching vectorstore: {response.text}")
        vectorstore_json = response.json()
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id, 
                'nodeType': self.node_type,
                'maxDocsPerQuery': self.max_docs_per_query,
                # we just copy everything over, including the vectors (if any)
                'vectorStore': vectorstore_json,
                'category': 'task',
                'task_name': 'query_vectorstore'
            }
        }

    @staticmethod 
    def _from_json_rep(json_data:dict):
        # there isn't a way to recover the API key from the JSON rep; it can
        # be set with set_api_key; also as mentioned above, (author) username
        # and org name data isn't currently saved in Mongo
        return VectorStoreNode(
            query_input=None,
            vectorstore_id=json_data['data']['vectorStore']['id'],
            vectorstore_name=json_data['data']['vectorStore']['name'], 
            max_docs_per_query=json_data['data']['maxDocsPerQuery']
        )

###############################################################################
# LOGIC                                                                       #
###############################################################################

# NB: To establish that these nodes specifically represent logic/control flow,
# these class names are prefixed with "Logic".
class LogicConditionNode(NodeTemplate):
    # inputs should comprise all in-edges, which are the names of all conditions 
    # and values along with the NodeOutputs they correspond to.
    # conditions is a list of (cond, val), where if cond is True the node 
    # returns val (where val is an input name).
    # default is what the node returns in the (final) else case.
    def __init__(self, inputs:list[tuple[str, NodeOutput]], 
                 conditions:list[tuple[str, str]], else_value:str):
        super().__init__()
        self.node_type = "condition"
        input_names = [i[0] for i in inputs]
        if len(set(input_names)) != len(input_names):
            raise ValueError("Duplicate input names.")
        for cond in conditions:
            if cond[1] not in input_names:
                raise ValueError(f"Returned value {cond[1]} of condition {cond[0]} was not specified in inputs.")
        if else_value not in input_names:
            raise ValueError(f"Returned value {else_value} of else condition was not specified in inputs.")
        self.input_names = input_names
        self.conditions = conditions
        # NB: self.predicates maps to the JSON "conditions" field. The result
        # of the corresponding predicate in the input argument conditions is
        # the same-indexed element in self.output_names.
        self.predicates = [cond[0] for cond in conditions]
        self.output_names = [cond[1] for cond in conditions] + [else_value]
        # each separate input is an in-edge to the node, with the input name
        # being the user-provided name
        self._inputs = {i[0]: [i[1]] for i in inputs}
    
    # Unlike most other nodes, this node has several outputs, corresponding to
    # each of the specified conditions (and the else case).
    def outputs(self):
        # the outputs are labelled "output-0", "output-1", etc. followed by
        # "output-else"
        os = {}
        for ind in range(len(self.predicates)):
            o = NodeOutput(
                source=self, 
                output_field=f"output-{ind}", 
                output_type=None)
            os[o.output_field] = o
        else_o = NodeOutput(source=self, output_field="output-else", output_type=None)
        os[else_o.output_field] = else_o
        return os
    
    # If a user currently wants to index into a specific output, they need to 
    # call the outputs() method and then index into it by name (e.g. 
    # "output-2", "output-else"), or use the helper functions below.
    def output_index(self, i:int) -> NodeOutput:
        if i < 0 or i >= len(self.predicates):
            raise ValueError("Index out of range.")
        os = self.outputs()
        return os[f"output-{i}"]
    
    def output_else(self) -> NodeOutput: 
        os = self.outputs()
        return os["output-else"]
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "conditions": self.predicates,
                "inputNames": self.input_names,
                "outputs": self.output_names,
                "category": "condition"
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict):
        predicates = json_data["data"]["conditions"]
        output_names = json_data["data"]["outputs"]
        return LogicConditionNode(
            inputs=[(name, None) for name in json_data["data"]["inputNames"]],
            conditions=[(predicates[i], output_names[i]) for i in range(len(predicates))],
            else_value=output_names[-1]
        )
    
class LogicMergeNode(NodeTemplate):
    def __init__(self, inputs:list[NodeOutput]):
        super().__init__()
        self.node_type = "merge"
        self._inputs = {
            # The JSON name for the in-edge is "input", although the displayed
            # name is "inputs".
            "input": inputs
        }
        
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": "default",
                "category": "merge"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        _ = json_data
        return LogicMergeNode(
            inputs=[]
        )

###############################################################################
# CHAT                                                                        #
###############################################################################

class ChatMemoryNode(NodeTemplate):
    # Chat memory nodes don't take input
    def __init__(self, memory_type:str, **kwargs):
        super().__init__()
        if memory_type not in CHAT_MEMORY_TYPES:
            raise ValueError(f"Invalid chat memory type {memory_type}.")
        self.node_type = "chatMemory"
        self.memory_type = memory_type
        self.memory_window_values = {
            # for full text, memory_window isn't used (just take the full text)
            CHAT_MEMORY_TYPES[0]: 0,
            CHAT_MEMORY_TYPES[1]: 0,
            CHAT_MEMORY_TYPES[2]: 10,
            CHAT_MEMORY_TYPES[3]: 2048
        }
        # self.memory_window is set to the value corresponding to 
        # self.memory_type's entry in memory_window_values, which may be 
        # overridden by the constructor arg memory_window
        if "memory_window" in kwargs:
            if self.memory_type in CHAT_MEMORY_TYPES[:2]:
                raise ValueError("Memory window shouldn't be specified if the chat memory is the full text.")
            self.memory_window_values[self.memory_type] = kwargs["memory_window"]
        self.memory_window = self.memory_window_values[self.memory_type]
    
    def output(self):
        return NodeOutput(source=self, output_field="value", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "memoryType": self.memory_type,
                "memoryWindow": self.memory_window,
                "memoryWindowValues": self.memory_window_values,
                "category": "memory",
                "task_name": "load_memory"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        n = ChatMemoryNode(
            memory_type=json_data["data"]["memoryType"]
        )
        # overwrite with JSON values
        n.memory_window = json_data["data"]["memoryWindow"]
        n.memory_window_values = json_data["data"]["memoryWindowValues"]
        return n