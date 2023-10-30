import os
from gql import Client, gql
from gql.transport.exceptions import TransportQueryError
from gql.transport.requests import RequestsHTTPTransport
from pathlib import Path
import jwt
from datetime import datetime, timezone, timedelta

class _GqlBase:
    '''
    Basis methods for communication with graph ql database
    '''

    def __init__(self):

        self.CITROS_ENVIRONMENT = os.getenv("CITROS_ENVIRONMENT", "LOCAL")
        url_prefix = "http" if self.CITROS_ENVIRONMENT == "CLUSTER" else "https"
        self.CITROS_DOMAIN = os.getenv("CITROS_DOMAIN", "citros.io")
        self.CITROS_URL = f"{url_prefix}://{self.CITROS_DOMAIN}"
        self.CITROS_ENTRYPOINT = f"{self.CITROS_URL}/api/graphql"

        self._jwt_token = os.getenv("KERNEL_CITROS_ACCESS_KEY", None)

        self.CITROS_HOME_DIR = Path.home() / ".citros"

        self.alternate_auth_paths = [self.CITROS_HOME_DIR / "auth", 
                                    Path("/var/lib/citros/auth")]
        self._gql_client = None
        self._token_changed = False
    
    def _find_citros_in_ancestors(self, proj_dir=""):
        current_dir = Path.cwd() if not proj_dir else Path(proj_dir).expanduser().resolve()

        # Ensure we don't go into an infinite loop at the root directory
        while current_dir != current_dir.parent:
            citros_dir = current_dir / ".citros"
            if citros_dir.exists():
                return citros_dir.expanduser().resolve()
            current_dir = current_dir.parent

        return None
    
    def _find_auth_key(self, proj_dir=""):
        # option 1: Start from current directory and traverse upwards
        citros_dir = self._find_citros_in_ancestors(proj_dir)
        if citros_dir is not None and Path(citros_dir, "auth").exists():
            return Path(citros_dir, "auth")

        # option 2: Look in alternate locations, e.g. the user's home folder.
        for auth_path in self.alternate_auth_paths:
            if auth_path.exists():
                return auth_path.expanduser().resolve()
        
        return None

    def _isAuthenticated(self):
        """
        returns the authentication status

        Returns:
            boolean: True if the user is logged in. 
        """        
        return self._get_token() is not None

    def _get_token(self):
        """
        Gets the JWT token.
        """
        try:
            if self._jwt_token:
                # assuming token is valid
                return self._jwt_token
            
            auth_path = self._find_auth_key()
            if auth_path is None:
                raise FileNotFoundError
            
            if auth_path not in self.alternate_auth_paths:
                auth_paths = [auth_path] + self.alternate_auth_paths
            else:
                idx = self.alternate_auth_paths.index(auth_path)
                auth_paths = self.alternate_auth_paths[idx:]

            for path in auth_paths:
                with open(path, mode='r') as file:            
                    self._jwt_token = file.read()
                    self._token_changed = True
                    if not self._validate_token(self._jwt_token):
                        # self.log.info(f"JWT token stored at {path} is invalid, removing.")
                        print(f"JWT token stored at {path} is invalid")
                        self._remove_token()
                    else:
                        break # valid token found
                    
        except FileNotFoundError as e:
            # Key file wasn't found. assuming the user is not logged in...
            self._jwt_token = None
            return None
        except Exception as e:
            self.handle_exceptions(e)
            print(e)

        return self._jwt_token
    
    def _validate_token(self, token : str):
        """
        Validates the JWT token.

        Args:
        token: JWT token to validate.

        Returns:
        Boolean indicating if the token is valid.
        """
        try:
            dictionary = jwt.decode(token, options={"verify_signature": False})

            expiration_timestamp = dictionary.get('exp', None)
            if not expiration_timestamp:
                return False
            
            date = datetime.fromtimestamp(expiration_timestamp)
            current_timestamp = datetime.now().timestamp()

            if expiration_timestamp < current_timestamp:
                # self.print(f"your login token has expired on {date}", color='yellow', only_verbose=True)
                print(f"your login token has expired on {date}", color='yellow', only_verbose=True)
                return False

            return True
        
        except Exception as ex:
            self.handle_exceptions(ex)
            return False
        
    def _remove_token(self):
        '''
        Removes the JWT token.
        '''
        self._set_token(None)

    def _set_token(self, jwt_token):
        """
        Sets the JWT token.

        Args:
        jwt_token: JWT token to set.
        """
        if not jwt_token or jwt_token.strip() == '':
            self._jwt_token = None
            self._token_changed = True
            try:
                auth_path = self._find_auth_key()
                if auth_path is None:
                    raise FileNotFoundError
                # os.remove(auth_path)
            except FileNotFoundError as e:
                pass # its ok that there is no file.                
            except Exception as e:
                self.handle_exceptions(e, exit=True)
                # print(e)
            return    
        
        if not self._validate_token(jwt_token):
            # self.log.error("Invalid JWT token.")
            print("Invalid JWT token.")
            return
            
        # if not self.CITROS_HOME_DIR.is_dir():
        #     self.CITROS_HOME_DIR.mkdir()

        # auth_dir = self.CITROS_REPO_DIR if self.is_initialized else self.CITROS_HOME_DIR
            
        # try:
        #     with open(f"{auth_dir}/auth", mode='w') as file:            
        #         file.write(jwt_token)      
        # except Exception as e:
        #     self.handle_exceptions(e, exit=True)
        # finally:
        #     self._jwt_token = jwt_token
        #     self._token_changed = True                        
        
        # return self._jwt_token
    
    def handle_exceptions(self, e, exit=False):
        import traceback
        from os import linesep
        print(f"An exception was raised")
        stack_trace = traceback.format_exception(type(e), e, e.__traceback__)
        stack_trace_str = "".join(stack_trace)
        print(f"Exception details:{linesep}{stack_trace_str}")

    def _get_transport(self):
        '''
        Obtain transport with authorization if user is authenticated.
        '''                      
        transport = RequestsHTTPTransport(
            url=self.CITROS_ENTRYPOINT,
            verify=True,
            retries=3            
        )     
        # create GQL client for user or for anonymous user. 
        if self._isAuthenticated():
            transport.headers = {
                "Authorization": f"Bearer {self._get_token()}",
                # "app" : "citros_cli",
                # "version" : citros_meta.__version__
            }
        return transport

    def _get_gql_client(self):
        '''
        Obtain GraphQL client.
        '''
        if self._gql_client and not self._token_changed:
            return self._gql_client
        # https://gql.readthedocs.io/en/v3.0.0a6/intro.html
        transport = self._get_transport()
        self._gql_client = Client(transport=transport, fetch_schema_from_transport=False)
        self._token_changed = False
        return self._gql_client

    def _gql_execute(self, query, variable_values=None):
        '''
        Execute a GraphQL query.

        Parameters
        ----------
        query : gql
            gql query
        variable_values : dict, default None
            variables for the gql query

        Returns
        -------
        dict: 
            Result of the executed query
        '''
        gql_query = gql(query)
        try:
            return self._get_gql_client().execute(gql_query, variable_values=variable_values)
        except TransportQueryError as ex:
            if variable_values is not None:
                safe_variable_values = dict(variable_values)
            else:
                safe_variable_values = {}
            if "password" in safe_variable_values:
                safe_variable_values["password"] = "REDACTED"
            # self.log.error(f"Error while querying: query={query} variable_values={safe_variable_values}")
            # print(f"Error while querying: query={query} variable_values={safe_variable_values}") #!
            # print(ex)

            self.handle_exceptions(ex)

            # if ex.errors[0].get('errcode', '') == "23514":
            #     self.print("The email you provided is not valid.", color='red')
            # if ex.errors[0].get('errcode', '') == "23503":
            #     self.logout()
        except Exception as ex:    
            # self.log.error(f"Error while querying: query={query} variable_values={variable_values}")
            # print(f"Error while querying: query={query} variable_values={variable_values}") #!
            # print(ex)
            self.handle_exceptions(ex)                           
        return None
