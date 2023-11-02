from tm_sl.com import *

import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv
from urllib.parse import urlencode


class SnapLogicManager:
    """
    A class representing a SnapLogic Manager.

    Attributes:
        session (requests.Session): The session used for making API requests.
        base (str): The base URL for the API endpoint.
    """
    def __init__(self, user=None, password=None, env=None):
        self.session = self.login(user, password, env)
        self.base = "https://elastic.snaplogic.com/api/1/rest/"

    def __del__(self):
        self.session.close()

    def get_creds(self, user, password, env):
        """
        Get the user credentials.

        Args:
            user (str): The user's username.
            password (str): The user's password.
            env (str): The path to the .env file.

        Returns:
            tuple: The user's username and password.
        """
        if not env and not user and not password:
            # print("Trying to load the default .env file")
            load_dotenv(dotenv_path=".env", override=True)
        elif env:
            # print("Trying to load the .env file from the path provided, ignoring all other parameter inputs")
            load_dotenv(dotenv_path=env, override=True)
        elif not env and (user and password):
            if not user or not password:
                # print("Please provide both username and password")
                exit(1) 
            # print("Got manual username and password")
        # inspect(ctx.obj,all=True)
        ruser = os.getenv('SL_USER') if not user else user
        rpassword = os.getenv('SL_PASSWORD') if not password else password
        return ruser, rpassword

    def login(self, user, password, env):
        """
        Login to the SnapLogic Manager API.

        Args:
            user (str): The user's username.
            password (str): The user's password.
            env (str): The path to the .env file.

        Returns:
            requests.Session: The logged-in session.
        """
        s = requests.Session()
        s.auth = HTTPBasicAuth(*self.get_creds(user, password, env))
         # type: ignore
        return s

    def r(self, method, path, query = None, debug = False,  *args, **kwargs):
        """
        Make a request to the SnapLogic Manager API.

        Args:
            method (str): The HTTP method of the request.
            path (str): The path to the API endpoint.
            query (dict, optional): The query parameters of the request. Defaults to None.
            *args: Additional positional arguments passed to the request method.
            **kwargs: Additional keyword arguments passed to the request method.

        Returns:
            tuple: The response data and the response object.
        """
        response = None
        try:
            url = self.base + path

            if query:
                query_string = urlencode(query)
                url += '?' + query_string

            if method == 'GET': response = self.session.get(url, *args, **kwargs)
            elif method == 'PUT': response = self.session.put(url, *args, **kwargs)
            elif method == 'POST': response = self.session.post(url, *args, **kwargs)
            elif method == 'DELETE': response = self.session.delete(url, *args, **kwargs)
            else: raise Exception(f"Unknown method {method}")
            response.raise_for_status()
            data = response.json()['response_map']
            return data, response
        except Exception as e:
            if debug:
                print(f"[bold red] -- API FAIL {method} {path} --  [/bold red]")
                print(f"[gray]{e}[/gray]")
                if response != None:
                    print(f"Response status code: {response.status_code}")
                    # print(f"Request headers:")
                    # pprint(response.request.headers)
                    if response.request.body: 
                        print(f"Request body:\n{response.request.body}")
                    print(f"[bold red] -- API RESPONSE -- [/bold red]")
                    pprint(response.json())
                print(f"[bold red] -- TRACEBACK -- [/bold red]")
                console.print_exception()
            raise e
        
    def download_binary(self, path, save_path): 
        """
        Download a binary file from the SnapLogic Manager API.

        Args:
            path (str): The path to the binary file.
            save_path (str): The path to save the downloaded file.

        Raises:
            Exception: If the download fails.
        """
        try:
            response = self.session.get( path)
            response.raise_for_status()
            with open(save_path, 'wb') as file:
                file.write(response.content)
        except Exception as e:
            print(f"Failed to download binary file: {e}")
