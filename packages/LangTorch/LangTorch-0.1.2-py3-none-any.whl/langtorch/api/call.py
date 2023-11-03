import asyncio
import json
from typing import List
import openai
import os
import hashlib
import json
import logging
import time
from pathlib import Path
import pandas as pd
from retry import retry
import nest_asyncio

nest_asyncio.apply()

from ..session import get_session
from .api_threading import execute_api_requests_in_parallel
from .functions import generate_schema_from_function
from .utils import override


def auth(key_or_path=None):
    """
    Authenticates with the OpenAI API by setting the API key either directly or by reading from a file.

    Parameters:
        key_or_path (str, optional): Directly provided API key for authentication or path to the file containing the API key.

    Raises:
        Exception: If the key file cannot be read or does not contain valid authentication information.
    """

    # Check if key_or_path is a file path
    is_file_path = False
    if key_or_path is not None:
        is_file_path = os.path.isfile(key_or_path)

    if is_file_path:
        # If it's a file path, read the keys from the file
        try:
            with open(key_or_path) as f:
                keys = json.load(f)
                openai.api_key = keys["openai_api_key"]
                openai.organization = keys["openai_organization"]
                os.environ["OPENAI_API_KEY"] = keys["openai_api_key"]
                os.environ["OPENAI_ORGANIZATION"] = keys["openai_organization"]
        except:
            raise Exception("Authentication failed: Unable to read or parse the key file.")
    elif key_or_path is not None:
        # If it's not a file path, assume it's an API key
        os.environ["OPENAI_API_KEY"] = key_or_path
        openai.api_key = key_or_path
    else:
        # If key_or_path is None, try to read from a default path
        default_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'api_keys.json')
        try:
            with open(default_path) as f:
                keys = json.load(f)
                openai.api_key = keys["openai_api_key"]
                openai.organization = keys["openai_organization"]
                os.environ["OPENAI_API_KEY"] = keys["openai_api_key"]
                os.environ["OPENAI_ORGANIZATION"] = keys["openai_organization"]
        except:
            raise Exception("Authentication failed: Unable to read or parse the default key file.")


def call(prompt, system_message, model="gpt-3.5-turbo-0613", as_str=False):
    """
    Sending a single system message prompt to get a response.

    Parameters:
        prompt (str): The input message to send to the model.
        system_message (str): Message that sets the behavior of the model.
        model (str, optional): The specific model to be used. Default is "gpt-3.5-turbo-0613".
        as_str (bool, optional): If True, returns just the 'choices' text from the response. If False, returns the entire response object. Default is False.

    Returns:
        Union[openai.ChatCompletion, str]: The chat response object, or a string if as_str is True.
    """
    messages = [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}] if isinstance(prompt, str) else [{"role": "system", "content": system_message}]+[{"role": r, "content": c} for r,c in prompt]
    chat = openai.ChatCompletion.create(model=model, messages=messages)
    return chat if not as_str else chat.choices[0]['message']['content']



def chat_strings(prompts, system_messages, model="gpt-3.5-turbo-0613", temperature=1, top_p=1, n=1,
                 stop=None, max_tokens=None, presence_penalty=0, frequency_penalty=0,
                 functions=None, function_call="none", **kwargs):
    """
        Prepares a list of chat strings in JSON format for batch processing. Each string represents a separate chat prompt for the OpenAI API.

        Parameters:
            prompts (List[str] or List[Tuple[str,str]]): List of prompts or (role, prompt) pairs.
            system_messages (List[str]): List of system messages to guide the model's behavior.
            model (str, optional): Model name to use. Default is "gpt-3.5-turbo-0613".
            temperature (float, optional): Sampling temperature. Default is 1.
            top_p (float, optional): Nucleus sampling parameter. Default is 1.
            n (int, optional): Number of chat completion choices to generate. Default is 1.
            stop (str or List[str], optional): Up to 4 sequences where the API will stop generating further tokens.
            max_tokens (int, optional): Maximum number of tokens to generate.
            presence_penalty (float, optional): Penalty for new tokens based on their presence so far.
            frequency_penalty (float, optional): Penalty for new tokens based on their frequency so far.
            functions (List[dict], optional): List of functions defined in the OpenAI schema.
            function_call (str, optional): The type of function call to make. Default is "none".
            **kwargs: Ignored additional parameters.

        Returns:
            List[str]: A list of request strings in JSON format.
        """

    params = {"temperature": temperature,
              "top_p": top_p,
              "n": n,
              "stop": stop,
              "max_tokens": max_tokens,
              "presence_penalty": presence_penalty,
              "frequency_penalty": frequency_penalty,
              "functions": functions,
              "function_call": function_call}

    default_values = {"temperature": 1, "top_p": 1, "n": 1, "stop": None, "max_tokens": None, "presence_penalty": 0, "frequency_penalty": 0, "functions": None, "function_call": "none"}

    jobs = [{"model": model,
             "messages": [{"role": "system", "content": system_message}, {"role": "user", "content": prompt}] if isinstance(prompt, str) else
                [{"role": "system", "content": system_message}]+[{"role": r, "content": c} for r,c in prompt],
             **{param: value for param, value in params.items() if value != default_values[param]}}
            for prompt, system_message in zip(prompts, system_messages)]

    return [json.dumps(job, ensure_ascii=False) for job in jobs]




def chat(prompts, system_messages, model="gpt-3.5-turbo-0613", api_key=None, verbose = False, as_str = False, **kwargs):
    """
    Processes a list of chat prompts in parallel, saving the results to a specified file.

    Parameters:
        prompts (List[str] or List[Tuple[str,str]] or str): List or single prompt or list of (role, prompt) pairs to send to the model.
        system_messages (List[str] or str): List or single system message to guide the model's behavior.
        save_filepath (str, optional): Path to save the results. Default is "chat_temp.txt".
        model (str, optional): Model name to use. Default is "gpt-3.5-turbo-0613".
        api_key (str, optional): API key for authentication. If None, uses environment variable.
        verbose (bool, optional): If True, enables detailed logging. Default is True.
        as_str (bool, optional): If True, returns only the model's message as string, otherwise returns the entire response object. Default is False.
        **kwargs: Additional parameters to be passed to the `chat_strings` function.

    Returns:
        Union[Coroutine, openai.ChatCompletion, str]: Coroutine object representing the asynchronous execution of the API requests if save_filepath is provided. Otherwise, returns the chat response object, or a string if as_str is True.
    """

    session = get_session()
    session._api = {"openai": {"limits": dict(), "embeddings": dict(), "chat": dict()}}

    if "T" in kwargs:
        kwargs["temperature"] = kwargs["T"]
    if not isinstance(system_messages, list): system_messages = [system_messages]
    if not isinstance(prompts, list): # If no save_filepath we assume we can skip saving
        if session._path is None:
            return call(prompts, system_messages[0], model = model, as_str = as_str)
        else:
            prompts = [prompts]
    if len(system_messages) == 1: system_messages = system_messages * len(prompts)
    request_strings = chat_strings(prompts, system_messages, model, **kwargs)
    if api_key is None:
        try:
            api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise KeyError('No OpenAI API key. Set os.environ["OPENAI_API_KEY"] = YOUR KEY')

    requests = [json.loads(request_string) for request_string in request_strings]

    job_id = hashlib.sha256(str(time.time()).encode()).hexdigest()
    session.add_requests("openai", "chat", job_id, requests)

    job = execute_api_requests_in_parallel(
        session=session,
        request_type="chat",
        job_id=job_id,
        request_url="https://api.openai.com/v1/chat/completions",
        api_key = api_key,
        logging_level=logging.INFO if verbose else logging.ERROR,
        max_requests_per_minute = 200 if "gpt-4" in request_strings[0] else 3_500 * 0.5,
        max_tokens_per_minute = 40_000 * 0.5 if "gpt-4" in request_strings[0] else 90_000 * 0.5,
    )

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(job)
    except Exception as E:
        asyncio.run(job)

    return session.completions(job_id, as_str = as_str)

@override
def embed(texts, to_csv = True, as_np = False, as_file = False, api_key=None, verbose = False):
    """
    Retrieves embeddings for the given texts from the OpenAI API and saves the results in a file.

    Parameters:
        texts (List[str]): List of texts for which to get embeddings.
        save_filepath (str, optional): Path to save the results. Default is "embedding_temp.txt".
        to_csv (bool, optional):
        as_np (bool, optional):
        api_key (str, optional): API key for authentication. If None, uses environment variable.
        verbose (bool, optional): If True, enables detailed logging. Default is True.

    Returns:
        dict: The embeddings from the saved results file, loaded as a Python dictionary.
    """

    session = get_session()
    session._api = {"openai": {"limits": {"embeddings": 0, "gpt-3.5": 0, "gpt4": 0}, "embeddings": [], "chat": []}}

    if as_np: to_csv = False
    if api_key is None:
        try:
            api_key = os.environ["OPENAI_API_KEY"]
        except KeyError:
            raise KeyError('No OpenAI API key. Set os.environ["OPENAI_API_KEY"] = YOUR KEY')
    if isinstance(texts, str) : texts = [texts]
    if len(texts) == 1:
        output = openai.Embedding.create(input=str(texts[0]), model="text-embedding-ada-002")['data'][0]['embedding']
        return pd.DataFrame({'text':texts,'embedding':[output]}) if to_csv else output


    # Request strings for jobs (I assume you have a list of jobs you want to process)
    jobs = [{"model": "text-embedding-ada-002", "input": str(x) + "\n"} for x in texts]
    request_strings = [json.dumps(job, ensure_ascii=False) for job in jobs]

    # Execute API requests in parallel and save results to a file
    job = execute_api_requests_in_parallel(
        request_strings=request_strings,
        session=session,
        request_type='embeddings',
        request_url="https://api.openai.com/v1/embeddings",
        api_key=api_key,
        max_requests_per_minute=3_000 * 0.5,
        max_tokens_per_minute=250_000 * 0.5,
        token_encoding_name="cl100k_base",
        max_attempts=3,
        logging_level=logging.INFO if verbose else logging.ERROR,
    )
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(job)
    except:
        asyncio.run(job)

    if as_file: return File(save_filepath)

    file = File(save_filepath)
    result = File(save_filepath).load()
    if result is None: return File(save_filepath)
    if file.status == "loaded,ordered":  # Replace with ordered
        file.save_ordered(save_filepath, "", False)

    file.save_ordered(save_filepath)

    if not to_csv:
        if not as_np: return result
        else:
            import numpy as np
            return np.array([m[1]["data"][0]["embedding"] for m in result])
    else:
        df = file.to_df()
        df.to_csv(Path(save_filepath).with_suffix('.csv').as_posix().replace('.csv','_df.csv'))
        return df


get_embedding = embed  ## Alternative function name

class File:
    def __init__(self, path, session_manager, garbage_collect=False):
        self.path = path
        self.session_manager = session_manager
        self.values = None
        self.type = None
        self.status = "unloaded,unordered"
        self.garbage_collect = garbage_collect

    def what_type(self, values):
        try:
            return "embedding" if "embedding" in values[0][0]["model"] else "chat"
        except:
            return
    # @retry(tries=3, delay=1, backoff=2)

    def extract_prompts(self, dict_list):
        if dict_list is None: return None
        if isinstance(dict_list[0], list):
            dict_list = [m[0] for m in dict_list]
        return [(entry["input"] if self.type == "embedding" else entry["messages"][1]["content"]) for entry in dict_list]

    def eval_file(self, path):
        with open(path, 'r', encoding="utf-8") as file:
            dict_list =[]
            for line in file.readlines():
                dict_list.append(eval(line.replace(' null', ' None')))
        return dict_list


    def load(self, order = True):
        ### THIS METHOD IS NOT UPDATED IT HAS IMPORTANT CODE THAT ORDERS THE OUTPUTS OF THE API BASED ON THE API CALL ORDER THAT WAS SAVED IN THE SESSION BEFORE THE CALL
        ### LIKE OTHER METHODS YOU HAVE TO REWRITE THIS METHOD FOR THE SESSION MANAGER
        try:
            values_unordered = self.eval_file(self.path)
            self.type = self.what_type(values_unordered)
            prompts_unordered = self.extract_prompts(values_unordered)
            self.values = []
            if order:
                used_entries = []
                try:
                    log_file_path = os.path.abspath(self.path).replace('.txt', '_log.txt')
                    order = self.eval_file(log_file_path)
                    prompts_ordered = self.extract_prompts(order)
                    for prompt_ordered in prompts_ordered:
                        for i, (prompt_unoordered, v) in enumerate(zip(prompts_unordered, values_unordered)):
                            if prompt_ordered == prompt_unoordered and i not in used_entries:
                                self.values.append(v)
                                used_entries.append(i)
                                break
                    assert len(self.values) <= len(values_unordered)
                    self.status = "loaded,ordered" if len(self.values) <= len(values_unordered) else "partially_loaded,ordered"
                except:
                    # If this occurs, there most likely is no *_log.txt file
                    self.values = values_unordered
                    if len(values_unordered)>1:
                        self.status = "loaded,unordered"
                    else:
                        self.status = "loaded,ordered"

            else:
                self.values = values_unordered
                self.status = "loaded,ordered"  # If this occurs it is unordered but intentionally

        except FileNotFoundError:
            # raise Exception(f"Trying to restart or file not found: {self.path}"
            print("Failed to load file, returning a File object with a .load() method")
            self.values  = None
        except Exception as e:
            print(f"Error loading file: {e}")
        if self.garbage_collect and not self.status == "partially_loaded,ordered" and self.values is not None:
            try:
                os.remove(self.path)
                os.remove(log_file_path)
            except:
                pass
        return self.values

    def _load(self):
        self.load()
        return self

    def to_df(self):
        return pd.DataFrame({"text" if self.type == "embedding" else "prompt": self.input, "embedding" if self.type == "embedding" else "completion": self.completion})

    @property
    def _prompts(self):
        if self.values is None:
            self.load()
        return [entry[0] for entry in self.values] if self.values else []

    @property
    def _completions(self):
        if self.values is None:
            self.load()
        return [entry[1] for entry in self.values] if self.values else []

    @property
    def prompts(self):
        if self.values is None:
            self.load()
        return self.extract_prompts(self._prompts)

    @property
    def completions(self):
        if self.values is None:
            self.load()
        try:
            return [(entry["data"][0]["embedding"] if self.type == "embedding" else (entry["choices"][0]["message"]["content"] if len(entry["choices"]) == 1 else [m["message"]["content"] for m in entry["choices"]])) for entry in self._completions] if self._completions else []
        except TypeError: # Indicates an error api response
            return self._completions

    embedding = completions
    input = prompts
    embeddings = embedding
    inputs = input
    completion = completions
    prompt = prompts
    result = completions

    def __getitem__(self, index):
        if self.values is None:
            self.load()
        return self.values[index] if self.values else None

    def save(self, path):
        df = self.to_df()
        df.to_csv(path)

    def save_ordered(self, suffix = None, to_csv = True):
        # THIS CAN BE JUST A SAVE BUT YOU HAVE TO ORDER THE prompts and completions before saving

        if to_csv == False and self.status == "partially_loaded,ordered":
                print("The unordered file has more entries than our attempt at ordering")
                return
        if suffix is None:
            "_embeddings.csv" if self.status == "embeddings" else "_chat.csv"
        abs_filepath = os.path.abspath(self.path)  # Convert to absolute path
        dir_path = os.path.dirname(abs_filepath)  # Extract directory name
        base_filename = os.path.splitext(os.path.basename(abs_filepath))[0]
        file_path = os.path.join(dir_path, base_filename + suffix)
        if to_csv:
            self.save(file_path)
        else:
            with open(file_path, 'w') as file:
                file = "\n".join([str(line).replace(' None', ' null') for line in self.values])



if __name__ == "__main__":
    auth()
    # f = chat('a','a','test')
    # Example usage
    prompts = ["""You are taking part in a study, where you've been asked to solve the following puzzle:
    
    Peter is looking at Linda
    Linda is looking at Henry
    Peter is married
    Henry is not married
    Is someone who is married looking at someone who is not married?
    You have answered: We can't tell
    Your explanation: Based on the given information, we know that Peter is married and Henry is not married. However, we do not have any information about Linda's marital status. 
    
    A Message to you:
    
    Hi,
    Thank you for your well-thought-out response. I appreciate the clarity and critical thinking you’ve brought to the discussion. However, there seems to be a small misunderstanding which I'd like to address.
    
    Let’s reexamine the question: “Is someone who is married looking at someone who is not married?” The question does not require that it be the same married person in every scenario; rather, it asks if, in the given situation, there exists at least one instance of a married person looking at an unmarried person.
    
    Now let's revisit the scenarios I presented:
    
    1. If Linda is married, then she is looking at Henry, who is not married. In this scenario, Linda (married) is looking at Henry (not married), fulfilling the condition.
       
    2. If Linda is not married, then we have Peter (who is married) looking at Linda (not married). In this scenario, Peter (married) is looking at Linda (not married), again fulfilling the condition.
    
    Note that the question doesn't ask if the same married person is looking at an unmarried person in all cases. It asks whether, in the information provided, there is at least one instance of this happening. Since we have established that in either scenario, regardless of Linda’s marital status, there is at least one instance of a married person looking at an unmarried person, the answer must be “yes”.
    
    Your concern seems to stem from the idea that the “someone who is married” must remain constant across both scenarios. However, this is not a requirement of the question. It merely asks if such a situation exists within the information provided, not whether it’s consistently the same individual who is married.
    
    I hope this clears up the confusion and helps in understanding why the answer is indeed "yes".
    
    Best regards,
    
    """]
    system_messages = ["You are a participant in a psychology study, your behaviour has been encoded in function inputs"]


    def revise_your_answer(thought: str, new_answer: str, new_explanation: str):
        """Decide to revise your answer based on the message response.

        Parameters:
            thought (string): The internal thought process behind the decision.
            new_answer (string): The revised answer.
            new_explanation (string): The explanation for the revised answer.
        """
        pass



    json_schema = generate_schema_from_function(revise_your_answer)

    function_call = "auto"




