import torch
from omegaconf import DictConfig, OmegaConf
from omegaconf.errors import UnsupportedValueType
import os
import datetime
import hashlib
import copy
import logging

logging.basicConfig(level=logging.INFO)



class SessionManager:


    def save_memoization(self, module_spec, input_data, output_data):
        # Generate a hash for the module specification and input data
        key = hashlib.sha256(str(module_spec).encode() + str(input_data).encode()).hexdigest()

        entry = {
            "module_spec": module_spec,
            "input": input_data,
            "output": output_data
        }

        self.cfg['memoization'][key] = entry
        self._save_session()

    def load_memoization(self, module_spec, input_data):
        key = hashlib.sha256(str(module_spec).encode() + str(input_data).encode()).hexdigest()
        return self.cfg['memoization'].get(key, None)

    def get_tensor_metadata(self):
        # Retrieve metadata for saved tensors
        return self.cfg.get("tensors", [])

import os
import asyncio
import threading
from omegaconf import OmegaConf
import contextvars
from collections import OrderedDict

def get_session():
    if Session.current_session.get() is None:
        Session.current_session.set(Session())
    return Session.current_session.get()

class Session:
    """A context manager for saving and loading session data: tensors, api calls, configuration and caching"""
    current_session = contextvars.ContextVar('session', default=None)

    def __init__(self, session_file = None):
        if session_file and not os.path.exists(session_file):
            with open(session_file,"w") as f:
                pass
            print(f"Creating new session at {session_file}")

        self._path = session_file
        self._async_lock = asyncio.Lock()
        self._thread_lock = threading.Lock()
        self._config = OmegaConf.load(self._path) if self._path else OmegaConf.create()
        self._open = True
        Session.current_session.set(self)
        if not hasattr(self,"_thread_lock_acquired"):
            self._thread_lock_acquired = False

        try:
            assert isinstance(self.tensor_savepath, str)
        except:
            if self._path is None:
                self.tensor_savepath = "saved_tensors.pt"
            else:
                self.tensor_savepath = os.path.join(os.path.dirname(os.path.abspath(session_file)), "saved_tensors.pt")

    def reload(self):
        """Called to ensure config is up-to-date"""
        if self._path:
            self.__setattr__("_config", OmegaConf.load(self._path), False)

    # Synchronous context manager methods
    def __enter__(self):
        Session.current_session.set(self)
        self._config = OmegaConf.load(self._path)
        self._thread_lock.acquire()
        self._thread_lock_acquired = True
        self._open = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Session.current_session.set(None)
        if self._thread_lock_acquired or self._open:
            if self._path: OmegaConf.save(self._config, self._path)
            self._thread_lock_acquired = False
            self._thread_lock.release()
        else:
            print("Warning: exiting a Session that was closed, no save performed")

    # Asynchronous context manager methods
    async def __aenter__(self):
        Session.current_session.set(self)
        self._config = OmegaConf.load(self._path)

        if self._config._thread_lock_acquired:
            raise RuntimeError("The session was first entered without 'async' in 'with Session', close it before entering 'async with Session'.")

        await self._async_lock.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self._thread_lock_acquired:
            raise RuntimeError("The session was first entered without 'async' in 'with Session', close it before entering 'async with Session'.")

        if self._path: OmegaConf.save(self._config, self._path)
        self._async_lock.release()
        Session.current_session.set(None)

    def open(self):
        Session.current_session.set(self)
        self._open = True
        if not self._thread_lock_acquired:
            self._thread_lock.acquire()
            self._thread_lock_acquired = True
        self._config = OmegaConf.load(self._path)
        return self

    def close(self):
        if self._thread_lock_acquired:
            if self._path: OmegaConf.save(self._config, self._path)
            self._thread_lock.release()
            self._thread_lock_acquired = False
        self._open = False
        Session.current_session.set(None)

    def add_requests(self, provider, type, job_id, requests):
        _api = dict(self._api)
        if not provider in _api:
            _api[provider] = dict()
        if not type in _api[provider]:
            _api[provider][type] = dict()
        if not job_id in _api[provider][type]:
            _api[provider][type][job_id] = {"requests": requests, "responses": []}
        else:
            _api[provider][type][job_id][requests]+=requests
        self._api = _api
        assert self._config._api[provider][type][job_id]["requests"]

    def add_responses(self, provider, type, job_id, responses, override = False):
        """Append an api response payload to response list."""
        self.reload()
        _api = dict(self._api)
        if override:
            _api[provider][type][job_id]["responses"] = responses
        else:
            _api[provider][type][job_id]["responses"].append(responses)
        self._api = _api

    def get_responses(self, provider, type, job_id = -1):
        self.reload()
        return [job["responses"] if job else None for job in self.get_job(job_id, type, provider)[-1]]

    def get_job(self, job_id = -1, type = None, provider = None):
        self.reload()
        if isinstance(provider,int):
            provider = list(self._api.keys())[provider]
        if isinstance(type,int) and provider is not None:
            type = list(self._api[provider].keys())[type]
        if isinstance(job_id,int) and provider is not None and type is not None:
            try:
                job_id = list(self._api[provider][type].keys())[job_id]
            except IndexError:
                return ([],[],[])
        if all([isinstance(m,str) for m in [provider, type, job_id]]):
            job = self._api.get(provider, {}).get(type, {}).get(job_id, None)
            return ([],[],[]) if job is None else ([provider], [type], [job])
            if not api_data:
                return None
        # Prepare a list of all possible jobs
        providers, types, result = [], [], []
        if provider is None:
            for _provider in self._api.keys():
                p, t, j = self.get_job(job_id, type, _provider)
                providers, types, result = providers + p, types + t, result + j
        else:
            provider = [provider]

        if type is None and provider is not None:
            for _provider in provider:
                for _type in self._api[_provider].keys():
                    p, t, j = self.get_job(job_id, _type, _provider)
                    providers, types, result = providers + p, types + t, result + j
        else:
            type = [type]

        if job_id is None and type is not None and provider is not None:
            for _type in type:
                for _provider in provider:
                    for _job_id in self._api[_provider][_type].keys():
                        p, t, j = self.get_job(_job_id, _type, _provider)
                        providers, types, result = providers + p, types + t, result + j

        return providers, types, result

    @property
    def prompts(self, job_id = None, type = None, provider = None):
        provider, type, job = self.get_job(job_id, type, provider)
        if job is None:
            return None
        if type == "chat":
            from .text import Chat
            from .tensor import ChatTensor
            return ChatTensor([Chat.from_messages(*resp["messages"]) for resp in job["requests"]])
        elif type == "embeddings":
            from .text import Text
            from .tensor import TextTensor
            return TextTensor([Text.from_messages(*resp["messages"]) for resp in job["requests"]])

    @property
    def completions(self, job_id = -1, type = None, provider = None):
        self.order_responses(job_id, type, provider)
        provider, type, job = self.get_job(job_id, type, provider)
        result = []
        for p,t,j in zip(provider, type, job):
            if not j:
                pass
            if t == "chat":
                from .text import Chat
                from .tensor import ChatTensor
                result += [ChatTensor([Chat.from_messages(list(resp["messages"])) for resp in j["requests"]])]
            elif t == "embedding":
                import torch
                result+=[torch.tensor([resp["data"][0]["embedding"] for resp in j["requests"]])]
        return result


    def extract_prompts(self, dict_list):
        if dict_list is None: return None
        if isinstance(dict_list[0], list):
            dict_list = [m[0] for m in dict_list]
        return [(entry["input"] if "embedding" in entry else entry["messages"][1]["content"]) for entry in dict_list]

    def order_responses(self, provider = None, type = None, job_id = None):
        """Order all responses for a given job using keys or indexes, or order all resposnses"""
        self.reload()
        provider, type, jobs = self.get_job(job_id, type, provider)
        for job in jobs:
            if isinstance(job, dict) and isinstance(next(iter(job["responses"])), list):
                requests_unordered, responses_unordered = tuple(job.get("responses", []))
                requests_ordered = self.extract_prompts(job.get("requests", []))

                ordered_responses = []
                try:
                    used_entries = []
                    for req_oredered in requests_ordered:
                        for i, (req, resp) in enumerate(zip(requests_unordered, responses_unordered)):
                            if req == req_oredered and i not in used_entries:
                                ordered_responses.append(resp)
                                used_entries.append(i)
                                break

                except Exception as e:
                    print(f"Error while ordering API responses: {e}")

                self.add_responses(provider, type, job_id, ordered_responses, override = True)
                return ordered_responses


    def __setattr__(self, name, value, save = True):
        if name in ["_config", "_path", "_async_lock", "_thread_lock", "_open"]:
            # Use the base class's __setattr__ to prevent recursive calls
            super().__setattr__(name, value)
            if name == "_config" and self._path and save:
                OmegaConf.save(self._config, self._path)
        elif self._open:
            # Decompose the current configuration
            tensor_savepath = self._config.pop('tensor_savepath', None)
            tensors_metadata = self._config.pop('tensors', [])

            # Filter attributes starting with an underscore
            underscore_attrs = OrderedDict((k, v) for k, v in self._config.items() if k.startswith('_'))
            for k in underscore_attrs.keys():
                self._config.pop(k, None)

            self._config['tensor_savepath'] = tensor_savepath
            if isinstance(value, torch.Tensor):
                timestamp = datetime.datetime.now().isoformat()
                try:
                    tensors = torch.load(tensor_savepath)
                    tensors[name] = value
                    torch.save(tensors, tensor_savepath)
                except FileNotFoundError:
                    torch.save({name:value}, tensor_savepath)

                metadata = {
                    "id": name,
                    "object": str(type(value)),
                    "created": timestamp,
                    "shape": tuple(value.shape)
                }
                if name in [m["id"] for m in tensors_metadata]:
                    tensors_metadata = [m for m in tensors_metadata if m["id"]!=name]
                self._config.tensors = list(tensors_metadata) + [metadata]
            else:
                self._config['tensors'] = tensors_metadata
                try:
                    if not name.startswith('_'):
                        self._config[name] = value
                        if name in [m["id"] for m in self._config["tensors"]]:
                            print(f"Saving non-tensor with the same name as a saved tensor {name}, the tensor will be unobtainable (but remains saved)")
                    else:
                        underscore_attrs[name] = value

                except UnsupportedValueType:
                    raise UnsupportedValueType("Session can only fold primitive types and TextTenor objects.")

            # Merge underscore attributes at the end
            for k, v in underscore_attrs.items():
                self._config[k] = v

            if self._path and save:
                OmegaConf.save(self._config, self._path)
        else:
            raise RuntimeError("RuntimeError: Attempted to save attr in a closed session")

    @property
    def tensors(self):
        tensors = torch.load(self._config["tensor_savepath"])
        return tensors

    def __getattr__(self, name):
        # Load the latest configuration from the file
        if self._path: self._config = OmegaConf.load(self._path)
        try:
            _ = (self._config.tensors)
        except:
            self.tensors = []
        if not hasattr(self._config, name) and name in [m["id"] for m in self._config["tensors"]]:
            return self.tensors[name]

        # Return the attribute from the latest configuration
        try:
            attr = self._config[name]
        except KeyError:
            raise AttributeError(f"'{type(self).__name__}' object has no attribute '{name}'")

        return attr

    def __getitem__(self, entry):
        return self.__getattr__(entry)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def _delete(self):
        # Cleanup: remove the session file
        os.remove(self._path)

    def __del__(self):
        if not self._path:  # remove saved tensors when working withouta a savefile
            try:
                tensors = torch.load(self.config_path.tensor_savepath)
                tensors = [(k,v) for k,v in tensors.items() if k not in [m['name'] for m in self._config.tensors]]
                os.remove(self.config_path.tensor_savepath)
            except FileNotFoundError:
                pass