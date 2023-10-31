import requests
import logging
import json

class AskSageClient:
    """
    A Python client for interacting with the Ask Sage APIs.
    """

    def __init__(self, email, api_key, user_base_url='https://api.asksage.ai/user', server_base_url='https://api.asksage.ai/server'):
        """
        Initialize the client with the base URLs of the services and the access token.
        """
        self.user_base_url = user_base_url
        self.server_base_url = server_base_url

        # get the token
        token = self.get_token(email, api_key)

        self.headers = {'x-access-tokens': token}

        # Initialize logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def _request(self, method, endpoint, json=None, files=None, base_url=None, skip_headers=False, data=None):
        """
        Helper method to perform HTTP requests.
        Handles error checking and raises exceptions for HTTP errors.
        """
        if base_url == None:
            base_url = self.server_base_url

        url = f"{base_url}/{endpoint}"
        headers = None if skip_headers else self.headers

        try:
            response = requests.post(url, headers=headers, json=json, files=files, data=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as errh:
            self.logger.error("Http Error:", exc_info=True)
            raise
        except requests.exceptions.ConnectionError as errc:
            self.logger.error("Error Connecting:", exc_info=True)
            raise
        except requests.exceptions.Timeout as errt:
            self.logger.error("Timeout Error:", exc_info=True)
            raise
        except requests.exceptions.RequestException as err:
            self.logger.error("Something went wrong", exc_info=True)
            raise

    def get_token(self, email, api_key):
        """
    Get the short lived token for the user (required for all other Server and User API calls).

    Parameters:
    email (str): Your user email
    api_key (str): Your api key.

    Returns:
    dict: The response from the service with the token.
    """
        response = self._request('POST', 'get-token-with-api-key', json = {
            'email': email,
            'api_key': api_key
        }, base_url=self.user_base_url, skip_headers=True)

        if int(response["status"]) != 200:
            raise Exception("Error getting access token")
     
        return response["response"]["access_token"]

    def add_dataset(self, dataset):
        """
    Adds a dataset

    Parameters:
    dataset (str): The dataset to be used. Must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.

    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'add-dataset', json={'dataset': dataset}, base_url=self.user_base_url)

    def delete_dataset(self, dataset):
        """
    Deletes a dataset

    Parameters:
    dataset (str): The dataset to be used. Must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.

    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'delete-dataset', json={'dataset': dataset}, base_url=self.user_base_url)

    def assign_dataset(self, dataset, email):
        """
    Assign a dataset

    Parameters:
    dataset (str): The dataset to be used. Must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.
    email (str): Email of the user to assign the dataset to. Must be in the same organization. Reach out to support if need be.

    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'assign-dataset', json={'dataset': dataset, 'email': email}, base_url=self.user_base_url)

    def get_user_logs(self):
        """
    Get all user logs

    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'get-user-logs', base_url=self.user_base_url)

    def get_user_logins(self, limit=5):
        """
    Get all user logins

    Parameters:
    limit (int): The number of logins returns. Default is 5.

    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'get-user-logins', json={'limit': limit}, base_url=self.user_base_url)

    def query(self, message, persona='default', dataset='all', limit_references=None, temperature=0.0, live=0, model='openai_gpt'):
        """
    Interact with the /query endpoint of the Ask Sage API.

    Parameters:
    message (str): The message to be processed by the service. Message can be a single message or an array of messages following this JSON format: [{ user: "me", message: "Who is Nic Chaillan?"}, { user: "gpt", message: "Nic Chaillan is..."}]
    persona (str, optional): The persona to be used. Default is 'default'. Get the list of available personas using get_personas.
    dataset (str, optional): The dataset to be used. Default is 'all'. Other options include 'none' or your custom dataset, must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.
    limit_references (int, optional): The maximum number of references (embeddings) to be used. Default is None, meaning all references will be used. Use 1 to limit to 1 reference or 0 to remove embeddings. You can also set dataset to "none"
    temperature (float, optional): The temperature to be used for the generation. Default is 0.0. Higher values (up to 1.0) make the output more random.
    live (int, optional): Whether to use live mode. Default is 0. Live = 1 will pull 10 results from Bing and 2 will also pull the top 2 web pages summaries using our Web crawler.
    model (str, optional): The model to be used. Default is 'openai_gpt'. Other options include cohere, google-bison, gpt4, gpt4-32k, gpt35-16k, claude2, openai_gpt (gpt3.5), davinci, llma2.

    Returns:
    dict: The response from the service.
    """
        return self._request('POST', 'query', json = {
            'message': message,
            'persona': persona,
            'dataset': dataset,
            'limit_references': limit_references,
            'temperature': temperature,
            'live': live,
            'model': model
        })

    def query_plugin(self, plugin_tag, dataset='all', limit_references=None, model='openai_gpt', **params):
        """
    Interact with the /query endpoint of the Ask Sage API.

    Parameters:
    plugin_tag (str): The plugin tag to be used. Get the list of available plugins using get_plugins (shown in the prompt_template).
    dataset (str, optional): The dataset to be used. Default is 'all'. Other options include 'none' or your custom dataset, must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.
    limit_references (int, optional): The maximum number of references (embeddings) to be used. Default is None, meaning all references will be used. Use 1 to limit to 1 reference or 0 to remove embeddings. You can also set dataset to "none"
    model (str, optional): The model to be used. Default is 'openai_gpt'. Other options include cohere, google-bison, gpt4, gpt4-32k, gpt35-16k, claude2, openai_gpt (gpt3.5), davinci, llma2.
    params (optional): The parameters to be used for the plugin. The number of parameters depends on the plugin. Get the list of available plugins using get_plugins.

    Returns:
    dict: The response from the service.
    """
        if '[[' not in plugin_tag:
            plugin_tag = '[[' + plugin_tag + ']]'

        prompt_template = None
        plugins = self.get_plugins()
        for plugin in plugins["response"]:
            if plugin_tag in plugin["prompt_template"]:
                prompt_template = plugin["prompt_template"]
                break

        if not prompt_template:
            print(f"Plugin not found: {plugin_tag}")
            return None
        
        message = prompt_template.format(**params)

        return self._request('POST', 'query', json = {
            'message': message,
            'persona': 'default',
            'dataset': dataset,
            'limit_references': limit_references,
            'temperature': 0.0,
            'live': 0,
            'model': model
        })

    def query_with_file(self, message, file=None, persona='default', dataset='all', limit_references=None, temperature=0.0, live=0, model='openai_gpt'):
        """
    Interact with the /query_with_file endpoint of the Ask Sage API.

    Parameters:
    message (str): The message to be processed by the service. Message can be a single message or an array of messages following this JSON format: [{ user: "me", message: "Who is Nic Chaillan?"}, { user: "gpt", message: "Nic Chaillan is..."}]
    file (str, optional): File path of a file to add to the prompt.
    persona (str, optional): The persona to be used. Default is 'default'. Get the list of available personas using get_personas.
    dataset (str, optional): The dataset to be used. Default is 'all'. Other options include 'none' or your custom dataset, must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.
    limit_references (int, optional): The maximum number of references (embeddings) to be used. Default is None, meaning all references will be used. Use 1 to limit to 1 reference or 0 to remove embeddings. You can also set dataset to "none"
    temperature (float, optional): The temperature to be used for the generation. Default is 0.0. Higher values (up to 1.0) make the output more random.
    live (int, optional): Whether to use live mode. Default is 0. Live = 1 will pull 10 results from Bing and 2 will also pull the top 2 web pages summaries using our Web crawler.
    model (str, optional): The model to be used. Default is 'openai_gpt'. Other options include cohere, google-bison, gpt4, gpt4-32k, gpt35-16k, claude2, openai_gpt (gpt3.5), davinci, llma2.

    Returns:
    dict: The response from the service.
    """
        file_obj = None
        files = {}
        if file != None:
            file_obj = open(file, 'rb')
            files = {'file': file_obj}

        data = {
            'message': json.dumps(message),
            'model': model,
            'temperature': temperature,
            'persona': persona,
            'dataset': dataset,
            'live': live
        }

        ret = self._request('POST', 'query_with_file', files = files, data=data)        
        if file_obj != None:
            file_obj.close()
        return ret

    def follow_up_questions(self, message):
        """
    Interact with the /follow-up-questions endpoint of the Ask Sage API.

    Parameters:
    message (str): The single message to be processed by the service. 

    Returns:
    dict: The response from the service with follow up questions.
        """
        return self._request('POST', 'follow-up-questions', json={'message': message})

    def tokenizer(self, content):
        """
    Interact with the /tokenizer endpoint of the Ask Sage API.

    Parameters:
    content (str): The text to be processed by the service. 

    Returns:
    dict: The response from the service with token count of the content.
        """
        return self._request('POST', 'tokenizer', json={'content': content})

    def get_personas(self):
        """
    Get the available personas from the Ask Sage service.

    Returns:
    dict: The response from the service with personas.
        """
        return self._request('POST', 'get-personas')

    def get_datasets(self):
        """
    Get the available datasets from the Ask Sage service.

    Returns:
    dict: The response from the service with datasets.
        """
        return self._request('POST', 'get-datasets')

    def get_plugins(self):
        """
    Get the available plugins from the Ask Sage service.

    Returns:
    dict: The response from the service with plugins.
        """
        return self._request('POST', 'get-plugins')

    def count_monthly_tokens(self):
        """
    Get the count of monthly querying tokens spent for this user from the Ask Sage service.

    Returns:
    dict: The response from the service with the count.
        """
        return self._request('POST', 'count-monthly-tokens')

    def count_monthly_teach_tokens(self):
        """
    Get the count of monthly training tokens spent for this user from the Ask Sage service.

    Returns:
    dict: The response from the service with the count.
        """
        return self._request('POST', 'count-monthly-teach-tokens')

    def train(self, content, force_dataset=None, context=''):
        """
    Train the model based on the provided content.

    Parameters:
    content (str): The message to be processed by the service. Ensure it is under 500 tokens.
    force_dataset (str, optional): The dataset to be used. Enter your custom dataset, must follow the following format: user_content_USERID_DATASET-NAME_content. Replace USERID by user ID and DATASET-NAME by the name of your dataset.
    context (str): Short context about the content (metadata). Under 20 tokens.
    
    Returns:
    dict: The response from the service.
        """
        return self._request('POST', 'train', json= {
            'content': content,
            'force_dataset': force_dataset,
            'context': context
        })

    def file(self, file_path, strategy='auto'):
        """
    Upload a file to the Ask Sage service.

    Parameters:
    file_path (str): The file to upload to the service.
    strategy (str): The type of parser. Default "auto". Use "fast" for faster parsing but less accurate. and "hi_res" for OCR recognition (slow).
    
    Returns:
    dict: The response from the service with the text/plain.
        """
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self._request('POST', 'file', files=files, json={'strategy': strategy})
