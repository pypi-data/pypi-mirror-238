from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
import os
from prettytable import PrettyTable, ALL
from typing import Union, Optional, Any
import matplotlib.figure
from ._gql_cursor import _GqlCursor
from ._pg_cursor import _PgCursor
from ._plotter import _Plotter
from .citros_dict import CitrosDict
from .references import Ref

class CitrosDB(_PgCursor, _GqlCursor):
    '''
    CitrosDB object, that allows to get general information about the batch and make queries.

    Parameters
    ----------
    host : str
        Database host adress.
        If None, uses predefined ENV parameter "PG_HOST".
    user : str
        User name.
        If not specified, uses predefined ENV parameter "PG_USER" or try to define using 'auth' file.
    password : str
        Password.
        If not specified, uses predefined ENV parameter "PG_PASSWORD" or try to define using 'auth' file.
    database : str
        Database name.
        If not specified, uses predefined ENV parameter "PG_DATABASE" or try to define using 'auth' file.
    schema : str
        If None, uses predefined ENV parameter "PG_SCHEMA".
    repo : str or int, optional
        Repository name or id.
        If name is provided, searches for the exact match.
        If an integer value is provided, it determines the selection based on the order of repository creation (-1 for the last created, 0 for the first).
        If not specified, uses predefined ENV parameter "CITROS_REPO" or tries to set repo using 'name' field from '.citros/project.json'.
    batch : str or int, optional
        Batch name or id.
        If name is provided, searches for the exact match.
        If an integer value is provided, it determines the selection based on the order of batch creation (-1 for the last created, 0 for the first).
        If not specified, uses predefined ENV parameter "bid".
    simulation : str, optional
        Name of the simulation. If not specified, uses predefined ENV parameter "CITROS_SIMULATION".
    port : str
        If None, uses predefined ENV parameter "PG_PORT".
    sid : int, optional
        Default sid.
        If not specified, uses predefined ENV parameter "CITROS_SIMULATION_RUN_ID" if it exists or None.
    debug_flag : bool, default False
        If False, program will try to handle errors and only print error messages without code breaking.
        If True, this will cause the code to abort if an error occurs.
    '''

    def __init__(self, host = None, user = None, password = None, database = None, schema = None, 
                 repo = None, batch = None, simulation = None, port = None, sid = None, debug_flag = False):
        
        _PgCursor.__init__(self, host = host, user = user, password = password, database = database, 
                schema = schema, batch = batch, port = port, sid = sid, debug_flag = debug_flag)
        _GqlCursor.__init__(self, repo = repo, simulation = simulation)
        
        if self._user is None:
            try:
                self._user = self._get_current_user()
            except:
                if self._debug_flag:
                    raise NameError('`user` is not defined')
                else:
                    print('`user` is not defined')
        
        if self._password is None:
            if self._user is not None:
                self._password = self._user
            else:
                if self._debug_flag:
                    raise NameError('`password` is not provided')
                else:
                    print('`password` is not provided')

        if self._database is None:
            try:
                self._database = self._get_current_database()
            except:
                if self._debug_flag:
                    raise NameError('`database` is not defined')
                else:
                    print('`database` is not defined')

        self._set_batch(self._batch_id, exact_match = True)

    def _copy(self):
        '''
        Make a copy of the CitrosDB object.

        Returns
        -------
        CitrosDB
        '''
        ci = CitrosDB(host = self._host, 
                      user = self._user, 
                      password = self._password, 
                      database  = self._database, 
                      schema = self._schema,
                      port = self._port,
                      sid = self._sid,
                      debug_flag = self._debug_flag)
        
        if self._sid is None:
            if hasattr(self, '_sid_val'):
                ci._sid_val = self._sid_val.copy()
        if hasattr(self, 'error_flag'):
            ci.error_flag = self.error_flag
        if hasattr(self, '_rid_val'):
            ci._rid_val = self._rid_val.copy()
        if hasattr(self, '_time_val'):
            ci._time_val = self._time_val.copy()
        if hasattr(self, '_filter_by'):
            ci._filter_by = self._filter_by
        if hasattr(self, '_order_by'):
            ci._order_by = self._order_by
        
        ci._simulation = self._simulation
        ci._repo_id = self._repo_id
        ci._repo_name = self._repo_name
        ci._batch_id = self._batch_id
        if hasattr(self, '_batch_name'):
            ci._batch_name = self._batch_name
        if hasattr(self, '_test_mode'):
            ci._test_mode = self._test_mode

        if isinstance(self._topic, list):
            ci._topic = self._topic.copy()
        elif isinstance(self._topic, str):
            ci._topic = [self._topic]
        else:
            ci._topic = None
        
        if hasattr(self, 'method'):
            ci.method = self.method
        if hasattr(self, 'n_avg'):
            ci.n_avg = self.n_avg
        if hasattr(self, 'n_skip'):
            ci.n_skip = self.n_skip
        return ci
    
    def _is_batch_available(self):
        '''
        Check if the batch is set and in the database.
        '''
        if hasattr(self, '_test_mode'):
            return True
        
        # check if the batch is set.
        if not self._is_batch_set():
            return False
        else:
            # query for the batch status
            batch_status = self._get_batch_status(self._batch_id)

            if batch_status is None:
                # could not find the batch
                print(f"there is no batch with the id: '{self._batch_id}'")
                return False
            else:
                # write that user try to get batch
                self._set_data_access_time(self._batch_id)

                if batch_status == 'LOADED':
                    # chech if this table in postgres schema
                    if self._is_batch_in_database(self._batch_id):
                        # table is really downloaded, everything ok
                        Ref()._references.append(self._batch_id)
                        return True
                    else:
                        # table is not in postgres schema, mutate error
                        print(f"the batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' exists, but not loaded into the database. We are checking")
                        self._set_batch_status(self._batch_id, 'UNLOADED')
                        return False
                    
                elif batch_status == 'LOADING':
                    #batch is loading now
                    print(f"the batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' is loading. Please wait a few minutes and try again")
                    return False
                
                elif batch_status == 'UNLOADED':
                    #batch is not loaded
                    print(f"the batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' exists"
                          ", but not loaded into the database. Please wait a few minutes and try again")
                    return False

                elif batch_status == 'ERROR':
                    print(f"the batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' can not be loaded"
                          ", batch status is 'ERROR'")
                    return False
                
                elif batch_status == 'UNKNOWN':
                    # chech if this table is in postgres schema
                    if self._is_batch_in_database(self._batch_id):
                        self._set_batch_status(self._batch_id, 'LOADED')
                        Ref()._references.append(self._batch_id)
                        return True
                    else:
                        self._set_batch_status(self._batch_id, 'UNLOADED')
                        print(f"the batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' exists, but not loaded into the database."
                              " Please wait a few minutes and try again")
                        return False
                else:
                    print(f"batch '{self._batch_name if self._batch_name is not None else 'id'}': '{self._batch_id}' has unsupported status: '{batch_status}'")

    def repo_info(self, search: Optional[Union[int, str]] = None, search_by: Optional[str] = None, order_by: Optional[str] = None,
                  exact_match: bool = False, user: str = 'all') -> CitrosDict:
        '''
        Return information about repositories.

        The output is a dictionary, that contains repository names as dictionary keys 
        and repository ids, list of corresponding simulation ids and date of creation as dictionary values.

        Parameters
        ----------
        search : int or str
           - To search for the  repository with the exact id, provide the repository id as str.
           - To search by  repository name or by words that partially match the  repository name, provide the corresponding word as str.
           - To query the first created / second created / etc  repository, set `search` = 0, `search` = 1, etc.
           - To query the the last created / the second-to-last created / etc  repository, set `search` = -1, `search` = -2, etc.
           To use another field for search, set the appropriate `search_by` parameter

        search_by : str
            By default, the search is conducted based on name, repository id or ordinal number according to the creation time.
            To perform a search using an another field, set the `search_by` parameter to one of the following 
            and provide the appropriate format to `search` field:
            Provide `search` as a str for the following fields:
           - 'description'
           - 'git'<br />
            Provide `search` as str that may containes date, time and timezone information, like: 'dd-mm-yyyy hh:mm:ss +hh:mm',
            or only date and time without timezone: 'dd-mm-yyyy hh:mm:ss', or only date: 'dd-mm-yyyy' / 'dd-mm' / 'dd'
            or only time: 'hh:mm:ss' / 'hh:mm' with or without timezone. 
            Any missing date information is automatically set to today's date, and any missing time information is set to 0.
           - 'created_after'
           - 'created_before'
           - 'updated_after'
           - 'updated_before'

        order_by : str or list or dict
            To obtain the output in ascending order, provide one or more of the following options as either a single value as str or a as a list:
           - 'name'
           - 'repo_id' 
           - 'description'
           - 'created_at'
           - 'updated_at'
           - 'git'<br />
            To specify whether to use descending or ascending order, create a dictionary where the keys correspond to the options mentioned above, 
            and the values are either 'asc' for ascending or 'desc' for descending. For instance: {'name': 'asc', 'created_at': 'desc'}"

        exact_match : bool, default False
            If True and `search` is str, looks for an exact match in the field defined by the 'search_by' parameter.
            If `search_by` is not defined, search is perfomed by name.
            If set to False, searches for the occurrences of the provided string within the field defined by the 'search_by' parameter.

        user : str, default 'all'
            Set `user` as 'me' to filter and display only the repositories that belong to you.
            To get the repositories that were created by another user, provide the email.

        Returns
        -------
        citros_data_analysis.data_access.citros_dict.CitrosDict
            Information about the repositories.
        
        Examples
        --------
        Display the information about all repositories:

        >>> citros.repo_info().print()
        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         },
         'projects': {
           'repo_id': 'rrrrrrrr-1111-2222-aaaa-555555555555',
           'description': 'statistics',
           'created_at': '2023-05-18T12:55:41.144263+00:00',
           'updated_at': '2023-08-18T11:25:31.356987+00:00',
           'git': '...'
         },
         'citros': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444666666',
           'description': 'project repository',
           'created_at': '2023-05-16T13:52:44.523112+00:00',
           'updated_at': '2023-05-26T15:25:17.321432+00:00',
           'git': '...'
         }
        }

        Print information about all repositories that have word 'citros' in their name, order them in descending order by time of creation:

        >>> citros.repo_info('citros', order_by = {'created_at': 'desc'}).print()
        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         },
         'citros': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444666666',
           'description': 'project repository',
           'created_at': '2023-05-16T13:52:44.523112+00:00',
           'updated_at': '2023-05-26T15:25:17.321432+00:00',
           'git': '...'
         }
        }

        By default, the `repo_info` method searches for occurrences of the provided string in repository names rather than exact matches. 
        To select information for only 'citros' repository, set the `exact_match` parameter to True:

        >>> citros.repo_info('citros', exact_match = True).print()
        {
         'citros': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444666666',
           'description': 'project repository',
           'created_at': '2023-05-22T13:52:44.523112+00:00',
           'updated_at': '2023-05-26T15:25:17.321432+00:00',
           'git': '...'
         }
        }
        
        Display the repository that was created the last:

        >>> citros.repo_info(-1).print()
        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         }
        }

        Display the repository with the repository id = 'rrrrrrrr-1111-2222-aaaa-555555555555':

        >>> citros.repo_info('rrrrrrrr-1111-2222-aaaa-555555555555').print()
        {
        'projects': {
           'repo_id': 'rrrrrrrr-1111-2222-aaaa-555555555555',
           'description': 'statistics',
           'created_at': '2023-05-18T12:55:41.144263+00:00',
           'updated_at': '2023-08-18T11:25:31.356987+00:00',
           'git': '...'
         }
        }

        Show the repository with word 'citros' in the 'description' field:

        >>> citros.repo_info('citros', search_by = 'description').print()
        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         }
        }

        Display repositories that were updated earlier then 12:30 18 August 2023, timezone +0:00:

        >>> citros.repo_info('18-08-2023 12:30:00 +0:00', search_by = 'updated_before').print()

        {
        'projects': {
           'repo_id': 'rrrrrrrr-1111-2222-aaaa-555555555555',
           'description': 'statistics',
           'created_at': '2023-05-18T12:55:41.144263+00:00',
           'updated_at': '2023-08-18T11:25:31.356987+00:00',
           'git': '...'
         }
        }

        Show repositories that were created after 19 May:

        >>> citros.repo_info('19-05', search_by = 'created_after').print()
        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         }
        }

        Display repositories that were last updated before 8:00 AM today:

        >>> citros.repo_info('8:00', search_by = 'updated_before').print()

        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         },
         'projects': {
           'repo_id': 'rrrrrrrr-1111-2222-aaaa-555555555555',
           'description': 'statistics',
           'created_at': '2023-05-18T12:55:41.144263+00:00',
           'updated_at': '2023-08-18T11:25:31.356987+00:00',
           'git': '...'
         },
         'citros': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444666666',
           'description': 'project repository',
           'created_at': '2023-05-16T13:52:44.523112+00:00',
           'updated_at': '2023-05-26T15:25:17.321432+00:00',
           'git': '...'
         }
        }

        By default, all repositories are displayed, regardless of their creator. 
        To show only the repositories that belong to you, set `user` = 'me':

        >>> citros.batch_info(user = 'me').print()

        {
         'citros_project': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444444444',
           'description': 'citros runs',
           'created_at': '2023-05-20T09:57:44.632361+00:00',
           'updated_at': '2023-08-20T07:45:11.136632+00:00',
           'git': '...'
         }
        }

        To display repositories, that were created by another user, provide the email:

        >>> citros.batch_info(user = 'user@mail.com').print()

        {
        'citros': {
           'repo_id': 'rrrrrrrr-1111-2222-3333-444444666666',
           'description': 'project repository',
           'created_at': '2023-05-16T13:52:44.523112+00:00',
           'updated_at': '2023-05-26T15:25:17.321432+00:00',
           'git': '...'
         }
        }
        
        Get list of the all existing repositories names as a list:

        >>> repos_names = list(citros.repo_info().keys())
        >>> print(repo_names)
        ['projects', 'citros_project', 'citros']
        '''
        if user in ['all', None]:
            user_id = None
        elif not isinstance(user, str):
            print(f"repo_info(): `user` must be str ")
            return CitrosDict({})
        elif user == 'me':
            user_id = self._user
        else:
            user_id = self._get_user_by_email(user)
            if user_id is None:
                print(f'repo_info(): no user with email "{user}", try user_info() or get_users() methods')
                return CitrosDict({})
        
        return _GqlCursor.repo_info(self, search= search, search_by = search_by, order_by = order_by,
                  exact_match = exact_match, user_id = user_id)

    def batch_info(self, search: Optional[Union[str, int, float]] = None, search_by: Optional[str] = None, sid_status: Optional[str] = None, 
                   order_by: Optional[Union[str, list, dict]] = None, exact_match: bool = False, user: str = 'all') -> CitrosDict:
        '''
        Return information about batches.

        The output is a dictionary, that contains batch names as dictionary keys 
        and batch ids, list of corresponding simulation ids and date of creation as dictionary values.

        Parameters
        ----------
        search : str, int or float
           - To search for the batch with the exact id, provide the batch id as str.
           - To search by batch name or by words that occurred in the batch name, provide the corresponding word as str. For the exact match set `exact_match` = True.
           - To query the first created / second created / etc batch, set `search` = 0, `search` = 1, etc.
           - To query the the last created / the second-to-last created / etc batch, set `search` = -1, `search` = -2, etc.
           To use another field for search, set the appropriate `search_by` parameter

        search_by : str
            By default, the search is conducted based on name, batch id or ordinal number according to the creation time.
            To perform a search using an another field, set the `search_by` parameter to one of the following
            and provide the appropriate format to `search` field: <br />
            Provide `search` as a str for the following fields (looking for the accurance of `search`, for the exact match set `exact_match` = True):
           - 'simulation'
           - 'tag'
           - 'message'<br />
            Search by the batch status: set `search_by` = 'status' and 
            `search` = 'DONE', 'SCHEDULE', 'RUNNING', 'TERMINATING' or 'ERROR'<br />
            Provide `search` as str that may containes date, time and timezone information, like: 'dd-mm-yyyy hh:mm:ss +hh:mm', 
            or only date and time without timezone: 'dd-mm-yyyy hh:mm:ss', or only date: 'dd-mm-yyyy' / 'dd-mm' / 'dd'
            or only time: 'hh:mm:ss' / 'hh:mm' with or without timezone. 
            Any missing date information is automatically set to today's date, and any missing time information is set to 0:
           - 'created_after'
           - 'created_before'
           - 'updated_after'
           - 'updated_before'<br />
           Provide `search` as an int for:
           - 'parallelism'
           - 'completions'
           - 'memory'<br />
           Provide `search` as float for:
           - 'cpu'
           - 'gpu'
        
        sid_status : str, optional
            Select batches with the exact status of the simulation run: 'DONE', 'SCHEDULE', 'ERROR', 'CREATING', 'INIT', 'STARTING', 'RUNNING', 'TERMINATING' or 'STOPPING'.
            If the status is not specified, returns batches with sids with all statuses.

        order_by : str or list or dict
            To obtain the output in ascending order, provide one or more of the following options as either a single str or a as a list:
           - 'name'
           - 'batch_id' 
           - 'simulation'
           - 'status'
           - 'tag' 
           - 'message'
           - 'created_at'
           - 'updated_at'
           - 'parallelism'
           - 'completions'
           - 'cpu'
           - 'gpu'
           - 'memory'<br />           
            To specify whether to use descending or ascending order, create a dictionary where the keys correspond to the options mentioned above, 
            and the values are either 'asc' for ascending or 'desc' for descending. For instance: {'name': 'asc', 'created_at': 'desc'}"

        exact_match : bool, default False
            If True and `search` is str, looks for an exact match in the field defined by the 'search_by' parameter.
            If `search_by` is not defined, search is perfomed by name.
            If set to False, searches for the occurrences of the provided string within the field defined by the 'search_by' parameter.

        user : str, default 'all'
            Set `user` = 'me' to filter and display only the batches that belong to you. 
            To display batches that were created by another user, provide the user's email.

        Returns
        -------
        citros_data_analysis.data_access.citros_dict.CitrosDict
            Information about the batches.
        
        Examples
        --------
        Display the information about all batches:

        >>> citros.batch_info().print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           'updated_at': '2023-06-14T11:44:31.728585+00:00',
           'status': 'DONE',
           'tag': 'latest',
           'simulation': 'simulation_parameters',
           'message': 'launch_params',
           'parallelism': 1,
           'completions': 1,
           'cpu': 2,
           'gpu': 0,
           'memory': '265',
           'repo': 'citros_project'
         },
         'kinematics_2': {
           'batch_id': '00000000-bbbb-1111-2222-333333333333',
           'sid': [0, 1, 2, 3],
           'created_at': '2023-06-21T13:51:47.29987+00:00',
           'updated_at': '2023-06-21T13:51:47.29987+00:00',
           ...
         },
         'velocity': {
           'batch_id': '00000000-cccc-1111-2222-333333333333',
           'sid': [0, 2],
           'created_at': '2023-06-18T20:57:27.830134+00:00',
           'updated_at': '2023-06-18T20:57:27.830134+00:00',
           ...
         },
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           'updated_at': '2023-06-21T15:03:07.308498+00:00',
           ...
         }
        }

        Print information about all kinematics batches, order them in descending order by time of creation:

        >>> citros.batch_info('kinematics', order_by = {'created_at': 'desc'}).print()
        {
         'kinematics_2': {
           'batch_id': '00000000-bbbb-1111-2222-333333333333',
           'sid': [0, 1, 2, 3],
           'created_at': '2023-06-21T13:51:47.29987+00:00',
           ...
         },
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           ...
         }
        }

        If the information about only batch named exactly 'kinematics' is needed, `exact_match` = True:

        >>> citros.batch_info('kinematics', exact_match = True).print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           ...
         }
        }

        Display the batch that was created the last:

        >>> citros.batch_info(-1).print()
        {
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00'
           ...
         }
        }

        Display the batch with the batch id = '00000000-cccc-1111-2222-333333333333':

        >>> citros.batch_info('00000000-cccc-1111-2222-333333333333').print()
        {
         'velocity': {
           'batch_id': '00000000-cccc-1111-2222-333333333333',
           'sid': [0, 2],
           'created_at': '2023-06-18T20:57:27.830134+00:00'
           ...
         }
        }

        Show the batch with word 'test' in the 'tag' field:

        >>> citros.batch_info('test', search_by = 'tag').print()
        {
         'velocity': {
           'batch_id': '00000000-cccc-1111-2222-333333333333',
           'sid': [0, 2],
           'created_at': '2023-06-18T20:57:27.830134+00:00',
           'updated_at': '2023-06-18T20:57:27.830134+00:00',
           'status': 'DONE',
           'tag': 'test_1',
           ...
         }
        }

        Display batches that were created before 15:00 21 June 2023, timezone +0:00:

        >>> citros.batch_info('21-06-2023 15:00:00 +0:00', search_by = 'created_after').print()
        {
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           'updated_at': '2023-06-21T15:03:07.308498+00:00',
           ...
         }
        }
        
        Show batches that were created earlier then 15 June:

        >>> citros.batch_info('15-06', search_by = 'created_before').print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           ...
         }
        }

        Show batches that were last updated before 9:00 PM today:

        >>> citros.batch_info('21:00', search_by = 'updated_before').print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           'updated_at': '2023-06-14T11:44:31.728585+00:00',
           ...
         },
         'kinematics_2': {
           'batch_id': '00000000-bbbb-1111-2222-333333333333',
           'sid': [0, 1, 2, 3],
           'created_at': '2023-06-21T13:51:47.29987+00:00',
           'updated_at': '2023-06-21T13:51:47.29987+00:00',
           ...
         },
         'velocity': {
           'batch_id': '00000000-cccc-1111-2222-333333333333',
           'sid': [0, 2],
           'created_at': '2023-06-18T20:57:27.830134+00:00',
           'updated_at': '2023-06-18T20:57:27.830134+00:00',
           ...
         },
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           'updated_at': '2023-06-21T15:03:07.308498+00:00',
           ...
         }
        }

        By default, all batches are displayed, regardless of their creator. 
        To view only the batches that belong to you, set `user` = 'me':

        >>> citros.batch_info(user = 'me').print()

        {
        'velocity': {
           'batch_id': '00000000-cccc-1111-2222-333333333333',
           'sid': [0, 2],
           'created_at': '2023-06-18T20:57:27.830134+00:00',
           'updated_at': '2023-06-18T20:57:27.830134+00:00',
           ...
         }
        }

        To display bathces, that were created by another user, provide the email:

        >>> citros.batch_info(user = 'user@mail.com').print()

        {
        'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           'updated_at': '2023-06-21T15:03:07.308498+00:00',
           ...
         }
        }

        Get list of the all existing batches names as a list:

        >>> batches_names = list(citros.batch_info().keys())
        >>> print(batches_names)
        ['kinematics', 'kinematics_2', 'velocity', 'dynamics']
        '''
        if user in ['all', None]:
            user_id = None
        elif not isinstance(user, str):
            print(f"batch_info(): `user` must be str ")
            return CitrosDict({})
        elif user == 'me':
            user_id = self._user
        else:
            user_id = self._get_user_by_email(user)
            if user_id is None:
                print(f'batch_info(): no user with email "{user}", try user_info() or get_users() methods')
                return CitrosDict({})

        return _GqlCursor.batch_info(self, search = search, search_by = search_by, sid_status = sid_status, 
                   order_by = order_by, exact_match = exact_match, user_id = user_id)
    
    def get_users(self):
        '''
        Display a table that presents key user information, including their first names, last names, and email addresses.

        Examples
        --------
        Print information about users in a table:

        >>> citros.get_users()

        +--------+------------+-----------------------------+
        | name   | last name  | email                       |
        +--------+------------+-----------------------------+
        | alex   | blanc      | alex@mail.com               |
        | david  | gilbert    | david@mail.com              |
        | mary   | stevenson  | mary@mail.com               |
        +--------+------------+-----------------------------+
        '''
        users_dict = _GqlCursor.user_info(self, order_by = 'email')

        if users_dict is not None and len(users_dict) > 0:
            table_users = [[v['name'], v['last_name'], k] for k, v in users_dict.items()]
        else:
            table_users = None
        table = PrettyTable(field_names=['name', 'last name', 'email'], align='l')
        if table_users is not None:
            table.add_rows(table_users)
        print(table)

    def user_info(self, search: Optional[str] = None, search_by: Optional[str] = None, 
                  order_by: Optional[Union[str, list, dict]] = None):
        '''
        Retrieve information about users, including their first names, last names, emails and the lists of repositories 
        they have created, along with the repositories in which these users have created batches.
        
        If the repository is set using the `repo()` method, it displays information about both the user who created that repository 
        and users who have created batches within it. If the batch is set using the `batch()` method, it shows information 
        about the user who created that specific batch.

        Parameters
        ----------
        search : str, optional
           - By default, it displays information about all users within the organization.
           - Provide email to display information about the exact user.
           - To search user by their name, provide user's name and set `search_by` = 'name'
           - To search by the last name, provide user's last name and set `search_by` = 'last_name'

        search : str, optional
           - By default, if the `search` is provided, performs search by email.
           - To search by the name, set `search_by` = 'name'.
           - To search by the last name, set `search_by` = 'last_name'.

        order_by : str or list or dict
            To obtain the output in ascending order, provide one or more of the following options as either a single str or a as a list:
           - 'name'
           - 'last_name' 
           - 'email'<br />           
            To specify whether to use descending or ascending order, create a dictionary where the keys correspond to the options mentioned above, 
            and the values are either 'asc' for ascending or 'desc' for descending. For instance: {'name': 'asc', 'last_name': 'desc'}"

        Returns
        -------
        citros_data_analysis.data_access.citros_dict.CitrosDict
            Information about the users.

        Examples
        --------
        Display all users of your organization, order the output by names:

        >>> citros.user_info('order_by' = 'name').print()
        {
         {
         'david@mail.com': {
           'name': 'david',
           'last_name': 'gilbert',
           'create_repo': ['robot_master', 'automaton_lab'],
           'create_batch_in_repo': ['robot_master']
         },
         'mary@mail.com': {
           'name': 'mary',
           'last_name': 'stevenson',
           'create_repo': ['mech_craft'],
           'create_batch_in_repo': ['mech_craft', 'robot_master']
         },
         ...
        }

        Display information about the user with email 'mary@mail.com':
        
        >>> citros.user_info('mary@mail.com').print()
        {
         'mary@mail.com': {
           'name': 'mary',
           'last_name': 'stevenson',
           'create_repo': ['mech_craft'],
           'create_batch_in_repo': ['mech_craft', 'robot_master']
         }
        }

        Search for the user David:
        
        >>> citros.user_info('david', search_by = 'name').print()
        {
         'david@mail.com': {
           'name': 'david',
           'last_name': 'gilbert',
           'create_repo': ['robot_master', 'automaton_lab'],
           'create_batch_in_repo': ['robot_master']
         }
        }

        Show user, who created repository 'mech_craft' or created batches in this repository:

        >>> citros.repo('mech_craft').user_info().print()
        {
         'mary@mail.com': {
           'name': 'mary',
           'last_name': 'stevenson',
           'create_repo': ['mech_craft'],
           'create_batch_in_repo': ['mech_craft', 'robot_master']
         }
        }

        If there is a batch 'velocity' in 'robot_master' repository, to show who create it execute the following:

        >>> citros.batch('velocity').user_info().print()
        {
         'david@mail.com': {
           'name': 'david',
           'last_name': 'gilbert',
           'create_repo': ['robot_master'],
           'create_batch_in_repo': ['robot_master']
         }
        }
        '''
        return _GqlCursor.user_info(self, search = search, search_by = search_by, order_by = order_by)

    def repo(self, repo: Union[int, str] = None, inplace: bool = False, exact_match: bool = False) -> Optional[CitrosDB]:
        '''
        Set repository to the CitrosDB object.

        Parameters
        ----------
        repo : int or str
           - To set the repository with the exact id, provide the repository id as str.
           - To set a repository using its name, provide the name as a string. If the provided string matches multiple repository names, check the whole list by `repo_info()` method.
           - To query the first created / second created / etc repository, set `repo` = 0, `repo` = 1, etc.
           - To query the the last created / the second-to-last created / etc repository, set `repo` = -1, `repo` = -2, etc.
        inplace : bool, default False
            If True, set repository id to the current CitrosDB object, otherwise returns new CitrosDB object with
            set repository id.
        exact_match : bool, default False
            If True, search for the repository with exact match in name field.
            If False, searches for the occurance of the provided string within the name field.

        Returns
        -------
        CitrosDB
            CitrosDB with set repository id or None, if inplace = True.

        Examples
        --------
        Display information about all batches of the repository 'projects':

        >>> citros = da.CitrosDB()
        >>> citros.repo('projects').batch_info().print()
        {
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           ...
           'repo': 'projects'
         }
        }

        By default, the `repo` method searches for occurrences of the provided string in repository names rather than exact matches. 
        For instance, if there are multiple repositories with the word 'projects' in their names, such as 'projects' and 'projects_1', 
        the `repo` method will indicate this and not set the repository. To search for an exact repository name, 
        set the `exact_match` parameter to True.

        >>> citros.repo('projects', exact_name = True)

        Show information about all batches of the last created repository:

        >>> citros = da.CitrosDB()
        >>> citros.repo(-1).batch_info().print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           ...
           'repo': 'citros_project'
         },
         'kinematics_2': {
           'batch_id': '00000000-bbbb-1111-2222-333333333333',
           'sid': [0, 1, 2, 3],
           'created_at': '2023-06-21T13:51:47.29987+00:00',
           ...
           'repo': 'citros_project'
         }
        }

        Show information about all batches of the repository with id 'rrrrrrrr-1111-2222-3333-444444444444':

        >>> citros = da.CitrosDB()
        >>> citros.repo('rrrrrrrr-1111-2222-3333-444444444444').batch_info().print()
        {
         'kinematics': {
           'batch_id': '00000000-aaaa-1111-2222-333333333333',
           'sid': [1, 2, 3, 4, 5],
           'created_at': '2023-06-14T11:44:31.728585+00:00',
           ...
           'repo': 'citros_project'
         },
         'kinematics_2': {
           'batch_id': '00000000-bbbb-1111-2222-333333333333',
           'sid': [0, 1, 2, 3],
           'created_at': '2023-06-21T13:51:47.29987+00:00',
           ...
           'repo': 'citros_project'
         }
        }

        Assign the 'projects' repository to the existing CitrosDB object and show details for all its batches:

        >>> citros = da.CitrosDB()
        >>> citros.repo('projects', inplace = True)
        >>> citros.batch_info().print()
        {
         'dynamics': {
           'batch_id': '00000000-dddd-1111-2222-333333333333',
           'sid': [1, 3, 2],
           'created_at': '2023-06-21T15:03:07.308498+00:00',
           ...
           'repo': 'projects'
         }
        }
        '''
        if inplace:
            _GqlCursor._set_repo(self, repo, exact_match = exact_match)
            return None
        else:
            ci = self._copy()
            _GqlCursor._set_repo(ci, repo, exact_match = exact_match)
            return ci
        
    def get_repo(self):
        '''
        Get the current repository name if the repository is set.

        Returns
        -------
        str
            Name of the current repository. If the repository is not set, return None.

        Examples
        --------
        Get the name of the last created repository:

        >>> citros = da.CitrosDB()
        >>> df = citros.repo(-1).get_repo()
        'citros_project'
        '''
        return self._repo_name

    def get_repo_id(self):
        '''
        Get the current repository id if the repository is set.

        Returns
        -------
        str
            id of the current repository. If the repository is not set, return None.

        Examples
        --------
        Get id of the repository 'citros_project':

        >>> citros = da.CitrosDB()
        >>> df = citros.repo('citros_project').get_repo_id()
        'rrrrrrrr-1111-2222-3333-444444444444'
        '''
        return self._repo_id
        
    def batch(self, batch: Optional[Union[int, str]] = None, inplace: bool = False, exact_match: bool = False,
              user: str = 'all') -> Optional[CitrosDB]:
        '''
        Set batch to the CitrosDB object.

        Parameters
        ----------
        batch : int or str
           - To set the batch with the exact id, provide the batch id as str.
           - To set a batch using its name, provide the name as a string. If the provided string matches multiple batch names, check the whole list by `batch_info()` method.
           - To query the first created / second created / etc batch, set `batch` = 0, `batch` = 1, etc.
           - To query the the last created / the second-to-last created / etc batch, set `batch` = -1, `batch` = -2, etc.
        inplace : bool, default False
            If True, set batch id to the current CitrosDB object, otherwise returns new CitrosDB object with
            set batch id.
        exact_match : bool, default False
            If True, search for the batch with exact match in name field. 
            If False, searches for the occurance of the provided string within the name field.
        user : str, default 'all'
            Set `user` = 'me' to search only among batches that were created by you. 
            To display batches that were created by another user, provide the user's email.

        Returns
        -------
        CitrosDB
            CitrosDB with set batch id or None, if inplace = True.

        Examples
        --------
        Get data for topic 'A' from the batch '00000000-1111-2222-3333-444444aaaaaa':

        >>> citros = da.CitrosDB()
        >>> df = citros.batch('00000000-1111-2222-3333-444444aaaaaa').topic('A').data()

        Get data for topic 'B' from the batch last created batch:

        >>> citros = da.CitrosDB()
        >>> df = citros.batch(-1).topic('B').data()

        Get data for topic 'C' from the batch named 'dynamics':

        >>> citros = da.CitrosDB()
        >>> df = citros.batch('dynamics').topic('C').data()

        If there are several batches with word 'dynamics' in their name, for example 'dynamics' and 'aerodynamics', 
        the batch will not be set, since the `batch` method searches for the occurrences of the provided string within repository names.
        To force it to look for the exact match, set `exact_match` = True:

        >>> citros.batch('dynamics', exact_match = True)

        Set batch id '00000000-1111-2222-3333-444444444444' to the already existing `CitrosDB()` object and query data from topic 'A':

        >>> citros = da.CitrosDB()
        >>> citros.batch('00000000-1111-2222-3333-444444444444', inplace = True)
        >>> df = citros.topic('A').data()
        '''
        if user in ['all', None]:
            user_id = None
        elif not isinstance(user, str):
            print(f"batch(): `user` must be str, no filter by user is applied")
            user_id = None
        elif user == 'me':
            user_id = self._user
        else:
            user_id = self._get_user_by_email(user)
            if user_id is None:
                print(f'batch(): no user with email "{user}", try user_info() or get_users() methods; no filter by user is applied')
                user_id = None
            
        if inplace:
            self._set_batch(batch, exact_match = exact_match, user_id = user_id)
            return None
        else:
            ci = self._copy()
            ci._set_batch(batch, exact_match = exact_match, user_id = user_id)
            return ci

    def get_batch(self):
        '''
        Get the name of the current batch if the batch is set.

        Returns
        -------
        str
            Name of the current batch. If the batch is not set, return None.

        Examples
        --------
        Get name of the batch that was created the last:

        >>> citros = da.CitrosDB()
        >>> citros.batch(-1).get_batch()
        'dynamics'
        '''
        return _PgCursor.get_batch_name(self)

    def get_batch_id(self):
        '''
        Get the id of the current batch if the batch is set.

        Returns
        -------
        str
            id of the current batch. If the batch is not set, return None.

        Examples
        --------
        Get id of the batch 'dynamics':

        >>> citros = da.CitrosDB()
        >>> citros.batch('dynamics').get_batch_id()
        '00000000-dddd-1111-2222-333333333333'
        '''
        return _PgCursor.get_batch_id(self)

    def simulation(self, simulation: str = None, inplace: bool = False):
        '''
        Set batch to the CitrosDB object.

        Parameters
        ----------
        simulation : str
           Name of the simulation.
        inplace : bool, default False
            If True, set simulation name to the current CitrosDB object, otherwise returns new CitrosDB 
            object with set simulation.

        Examples
        --------
        Show information about the batch 'test' that was created in 'simulation_cannon_analytic' simulation:

        >>> citros = da.CitrosDB()
        >>> citros.simulation('simulation_cannon_analytic').batch_info('test').print()
        {
          'test': {
            'batch_id': '01318463-e2ce-4642-89db-0132f9ab49c2',
            'sid': [0],
            'created_at': '2023-05-16T20:20:13.932897+00:00',
            'updated_at': '2023-07-16T20:21:30.648711+00:00',
            'status': 'DONE',
            'tag': 'latest',
            'simulation': 'simulation_cannon_analytic',
         ...
        }
        '''
        if inplace:
            self._set_simulation(simulation)
            return None
        else:
            ci = self._copy()
            ci._set_simulation(simulation)
            return ci
        
    def get_simulation(self):
        '''
        Get the simulation name if the simulation is set.

        Returns
        -------
        str
            Name of the simulation. If the simulation is not set, return None.

        Examples
        --------
        Get the name of the imulation that was set in initialization:

        >>> citros = da.CitrosDB(simualtion = 'simulation_cannon_analytic')
        >>> citros.get_simulation()
        'simulation_cannon_analytic'
        '''
        return self._simulation

    def info(self) -> CitrosDict:
        '''
        Return information about the batch, based on the configurations set by topic(), rid(), sid() and time() methods.

        The output is a dictionary, that contains:
        ```python
        'size': size of the selected data,
        'sid_count': number of sids,
        'sid_list': list of the sids,
        'topic_count': number of topics,
        'topic_list': list of topics,
        'message_count': number of messages
        ```
        If specific sid is set, also appends dictionary 'sids', with the following structure:
        ```python
        'sids': {
          <sid, int>: {
            'topics': {
              <topic_name, str>: {
                'message_count': number of messages,
                'start_time': time when simulation started,
                'end_time': time when simulation ended,
                'duration': duration of the simalation process,
                'frequency': frequency of the simulation process (in Hz)}}}}
        ```
        If topic is specified, appends dictionary 'topics':
        ```python
        'topics': {
          <topic_name, str>: {
            'type': type,
            'data_structure': structure of the data,
            'message_count': number of messages}}
        ```
        If the topic has multiple types with the same data structure, they are presented in 
        'type' as a list. If the types have different data structures, they are grouped by 
        their data structure types and numbered as "type_group_0", "type_group_1", and so on:
        ```python
        'topics': {
          <topic_name, str>: {
            "type_group_0": {
              'type': type,
              'data_structure': structure of the data,
              'message_count': number of messages},
            "type_group_1": {
              'type': type,
              'data_structure': structure of the data,
              'message_count': number of messages}}}
        ```

        Returns
        -------
        citros_data_analysis.data_access.citros_dict.CitrosDict
            Information about the batch.

        Examples
        --------
        >>> citros = da.CitrosDB()
        >>> citros.info().print()
        {
         'size': '27 kB',
         'sid_count': 3,
         'sid_list': [1, 2, 3],
         'topic_count': 4,
         'topic_list': ['A', 'B', 'C', 'D'],
         'message_count': 100
        }

        >>> citros.topic('C').info().print()
        {
         'size': '6576 bytes',
         'sid_count': 3,
         'sid_list': [1, 2, 3],
         'topic_count': 1,
         'topic_list': ['C'],
         'message_count': 24,
         'topics': {
           'C': {
             'type': 'c',
             'data_structure': {
               'data': {
                 'x': {
                   'x_1': 'int', 
                   'x_2': 'float',
                   'x_3': 'float'
                 },
                 'note': 'list',
                 'time': 'float',
                 'height': 'float'
               }
             },
             'message_count': 24
           }
         }
        }

        >>> citros.sid([1,2]).info().print()
        {
         'size': '20 kB',
         'sid_count': 2,
         'sid_list': [1, 2],
         'topic_count': 4,
         'topic_list': ['A', 'B', 'C', 'D'],
         'message_count': 76,
         'sids': {
           1: {
             'topics': {
               'A': {
                  'message_count': 4,
                  'start_time': 2000000000,
                  'end_time': 17000000000,
                  'duration': 15000000000,
                  'frequency': 0.267
               },
               'B': {
                  'message_count': 9,
        ...
                  'duration': 150000000,
                  'frequency': 60.0
               }
             }
           }
         }
        }

        >>> citros.topic('C').sid(2).info().print()
        {
         'size': '2192 bytes',
         'sid_count': 1,
         'sid_list': [2],
         'topic_count': 1,
         'topic_list': ['C'],
         'message_count': 8,
         'sids': {
           2: {
             'topics': {
               'C': {
                 'message_count': 8,
                 'start_time': 7000000170,
                 'end_time': 19000000800,
                 'duration': 12000000630,
                 'frequency': 0.667
               }
             }
           }
         },
         'topics': {
           'C': {
             'type': 'c',
             'data_structure': {
               'data': {
                 'x': {
                   'x_1': 'int', 
                   'x_2': 'float',
                   'x_3': 'float'
                 },
                 'note': 'list',
                 'time': 'float',
                 'height': 'float'
                 }
               },
             'message_count': 8
           }
         }
        }
        '''
        if not self._is_batch_available():
            return CitrosDict({})
        return _PgCursor.info(self)

    def topic(self, topic_name: Optional[Union[str, list]] = None) -> CitrosDB:
        '''
        Select topic.

        Parameters
        ----------
        topic_name : str or list of str
            Name of the topic.

        Returns
        -------
        CitrosDB
            CitrosDB with set 'topic' parameter.

        Examples
        --------
        Get data for topic name 'A':

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data()

        Get maximum value of the 'sid' among topics 'A' and 'B':

        >>> citros = da.CitrosDB()
        >>> citros.topic(['A', 'B']).get_max_value('sid')
        3
        '''
        ci = self._copy()
        _PgCursor.topic(ci, topic_name = topic_name)
        return ci
        
    def sid(self, value: Optional[Union[int, list]] = None, start: int = 0, end: int = None, count: int = None) -> CitrosDB:
        '''
        Set constraints on sid.

        Parameters
        ----------
        value : int or list of ints, optional
            Exact values of sid.
            If nothing is passed, then the default value of sid is used (ENV parameter "CITROS_SIMULATION_RUN_ID").
            If the default value does not exist, no limits for sid are applied.
        start : int, default 0
            The lower limit for sid values.
        end : int, optional
            The higher limit for sid, the end is included.
        count : int, optional
            Used only if the `end` is not set.
            Number of sid to return in the query, starting form the `start`.

        Returns
        -------
        CitrosDB
            CitrosDB with set 'sid' parameter.

        Examples
        --------
        Get data for topic 'A' where sid values are 1 or 2:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').sid([1,2]).data()

        Get data for for topic 'A' where sid is in the range of 3 <= sid <= 8 :
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').sid(start = 3, end = 8).data()

        or the same with `count`:
        
        >>> df = citros.topic('A').sid(start = 3, count = 6).data()

        For sid >= 7:
        
        >>> df = citros.topic('A').sid(start = 7).data()
        '''
        ci = self._copy()
        _PgCursor.sid(ci, value = value, start = start, end = end, count = count)
        return ci
        
    def rid(self, value: Optional[Union[int, list]] = None, start: int = 0, end: int = None, count: int = None) -> CitrosDB:
        '''
        Set constraints on rid.

        Parameters
        ----------
        value : int or list of ints, optional
            Exact values of rid.
        start : int, default 0
            The lower limit for rid values.
        end : int, optional
            The higher limit for rid, the end is included.
        count : int, optional
            Used only if the `end` is not set.
            Number of rid to return in the query, starting form the `start`.

        Returns
        -------
        CitrosDB
            CitrosDB with set 'rid' parameter.

        Examples
        --------
        Get data for topic 'A' where rid values are 10 or 20:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').rid([10, 20]).data()

        Get data for for topic 'A' where rid is in the range of 0 <= rid <= 9 :
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').rid(start = 0, end = 9).data()

        or the same with `count`:
        
        >>> df = citros.topic('A').rid(start = 0, count = 10).data()

        For rid >= 5:
        
        >>> df = citros.topic('A').rid(start = 5).data()
        '''
        ci = self._copy()
        _PgCursor.rid(ci, value = value, start = start, end = end, count = count)
        return ci

    def time(self, start: int = 0, end: int = None, duration: int = None) -> CitrosDB:
        '''
        Set constraints on time.

        Parameters
        ----------
        start : int, default 0
            The lower limit for time values.
        end : int, optional
            The higher limit for time, the end is included.
        duration : int, optional
            Used only if the `end` is not set.
            Time interval to return in the query, starting form the `start`.

        Returns
        -------
        CitrosDB
            CitrosDB with set 'time' parameter.

        Examples
        --------
        Get data for for topic 'A' where time is in the range 10ns <= time <= 20ns:
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').time(start = 10, end = 20).data()

        To set time range 'first 10ns starting from 10th nanosecond', that means 10ns <= time < 20ns:
        
        >>> df = citros.topic('A').time(start = 10, duration = 10).data()

        For time >= 20:
        
        >>> df = citros.topic('A').time(start = 20).data()
        '''
        ci = self._copy()
        _PgCursor.time(ci, start = start, end = end, duration = duration)
        return ci
    
    def set_filter(self, filter_by: dict = None) -> CitrosDB:
        '''
        Set constraints on query.

        Allows to set constraints on json-data columns.

        Parameters
        ----------
        filter_by : dict
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values,<br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()` and `time()` and will override them.
            If sampling method is used, constraints on additional columns are applied BEFORE sampling while
            constraints on columns from json-data are applied AFTER sampling.

        Returns
        -------
        CitrosDB
            CitrosDB with set constraints.

        See Also
        --------
        topic() : set topic name to query
        sid() : set sid values to query
        rid() : set rid values to query
        time() : set time constraints

        Examples
        --------
        if the structure of the data column is the following:
        
        ```python
        {x: {x_1: 1}, note: [11, 34]}
        {x: {x_1: 2}, note: [11, 35]}
        ...
        ```
        to get data for topic 'A' where values of json-data column 10 < data.x.x_1 <= 20:
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').set_filter({'data.x.x_1': {'>': 10, '<=': 20}}).data()

        get data where the value on the first position in the json-array 'note' equals 11 or 12:
        
        >>> df = citros.topic('A').set_filter({'data.note[0]': [11, 12]}).data()
        '''
        ci = self._copy()
        _PgCursor.set_filter(ci, filter_by = filter_by)
        return ci

    def set_order(self, order_by: Optional[Union[str, list, dict]] = None) -> CitrosDB:
        '''
        Apply sorting to the result of the query.

        Sort the result of the query in ascending or descending order.

        Parameters
        ----------
        order_by : str, list of str or dict, optional
            If `order_by` is a single string or a list of strings, it represents the column label(s) by which the result is sorted in ascending order.
            For more control, use a dictionary with column labels as keys and values ('asc' for ascending, 'desc' for descending) to define the sorting order.

        Examples
        --------
        Get data for topic 'A' and sort the result by sid in ascending order and by rid in descending order.

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').set_order({'sid': 'asc', 'rid': 'desc'}).data()

        Sort the result by sid and rid in ascending order:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').set_order(['sid', 'rid']).data()
        '''
        ci = self._copy()
        _PgCursor.set_order(ci, order_by = order_by)
        return ci
    
    def skip(self, n_skip: int = None):
        '''
        Select each `n_skip`-th message.

        Messages with different sids are selected separately.

        Parameters
        ----------
        skip : int, optional
            Control number of the messages to skip.

        Returns
        -------
        CitrosDB
            CitrosDB with parameters set for sampling method 'skip'.

        Examples
        --------
        To get every 3th message of the topic 'A':
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').skip(3).data()
        
        the 1th, the 4th, the 7th ... messages will be selected
        '''
        ci = self._copy()
        _PgCursor.skip(ci, n_skip = n_skip)
        return ci
    
    def avg(self, n_avg: int = None) -> CitrosDB:
        '''
        Average `n_avg` number of messages.

        Messages with different sids are processed separately. 
        The value in 'rid' column is set as a minimum value among the 'rid' values of the averaged rows.

        Parameters
        ----------
        n_avg : int
            Number of messages to average.

        Returns
        -------
        CitrosDB
            CitrosDB with parameters set for sampling method 'avg'.

        Examples
        --------
        To average each 3 messages of the topic 'A' and get the result:
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').avg(3).data()
        '''
        ci = self._copy()
        _PgCursor.avg(ci, n_avg = n_avg)
        return ci
    
    def move_avg(self, n_avg: int = None, n_skip: int = 1):
        '''
        Compute moving average over `n_avg` massages and select each `n_skip`-th one.

        Messages with different sids are processed separately.
        The value in 'rid' column is set as a minimum value among the 'rid' values of the averaged rows.

        Parameters
        ----------
        n_avg : int, optional
            Number of messages to average.
        n_skip : int, default 1
            Number of the messages to skip.
            For example, if `skip` = 3, the 1th, the 4th, the 7th ... messages will be selected

        Returns
        -------
        CitrosDB
            CitrosDB with parameters set for sampling method 'move_avg'.

        Examples
        --------
        Calculate moving average over each 5 messages of the topic 'A' 
        and select every second row of the result:
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').move_avg(5,2).data()
        '''
        ci = self._copy()
        _PgCursor.move_avg(ci, n_avg = n_avg, n_skip = n_skip)
        return ci

    def data(self, data_names: list = None) -> pd.DataFrame:
        '''
        Return table with data.
         
        Query data according to the constraints set by topic(), rid(), sid() and time() methods
        and one of the aggrative method skip(), avg() or move_avg().

        Parameters
        ----------
        data_names : list, optional
            Labels of the columns from json data column.

        Returns
        -------
        pandas.DataFrame
            Table with selected data.

        Examples
        --------
        if the structure of the data column is the following:
        
        ```python
        {x: {x_1: 1}, note: ['a', 'b']}
        {x: {x_1: 2}, note: ['c', 'd']}
        ...
        ```
        to get the column with the values of json-object 'x_1'
        and the column with the values from the first position in the json-array 'note':
        
        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(["data.x.x_1", "data.note[0]"])

        To get all the whole 'data' column with json-objects divide into separate columns:
        
        >>> df = citros.topic('A').data()

        To get the whole 'data' column as a json-object:
        
        >>> df = citros.topic('A').data(["data"])
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.data(self, data_names = data_names)
        
    def get_current_batch_size(self):
        '''
        Print size of the current batch, if it is set.

        Print table with batch name, batch size and total batch size with indexes.

        Examples
        --------
        Print the table with information about batch sizes:

        >>> citros = da.CitrosDB(batch = 'galaxies')
        >>> citros.get_current_batch_size()
        +-----------+--------------------------------------+-------------+------------+
        | batch     | batch id                             | size        | total size |
        +-----------+--------------------------------------+-------------+------------+
        | galaxies  | 00000000-1111-2222-3333-444444444444 | 8192 bytes  | 16 kB      |
        +-----------+--------------------------------------+-------------+------------+
        '''
        if self._is_batch_available():
            table_to_display = self._get_batch_size(mode = 'current', names = True)
            table = PrettyTable(field_names=['batch', 'batch id', 'size', 'total size'], align='l')
            if table_to_display is not None:
                table.add_rows(table_to_display)
            print(table)

    def get_batch_size(self):
        '''
        Print sizes of the all batches in the current schema that are downloaded in the database.

        Print table with batch ids, batch size and total batch size with indexes.

        Examples
        --------
        Print the table with information about batch sizes:

        >>> citros = da.CitrosDB()
        >>> citros.get_batch_size()
        +-----------+--------------------------------------+-------------+------------+
        | batch     | batch id                             | size        | total size |
        +-----------+--------------------------------------+-------------+------------+
        | stars     | 00000000-1111-2222-3333-444444444444 | 32 kB       | 64 kB      |
        | galaxies  | 00000000-aaaa-2222-3333-444444444444 | 8192 bytes  | 16 kB      |
        +-----------+--------------------------------------+-------------+------------+
        '''
        table_to_display = self._get_batch_size(mode = 'all', names = True)
    
        table = PrettyTable(field_names=['batch', 'batch id', 'size', 'total size'], align='l')
        if table_to_display is not None:
            table.add_rows(table_to_display)
        print(table)

    def _get_batch_size(self, mode = 'all', names = False):
        '''
        Return sizes of the all tables in the current schema.

        Returns
        -------
        list of tuples
            Each tuple contains name of the table, table size and total size with indexes.
        '''
        table_size = _PgCursor._get_batch_size(self, mode = mode)
        if table_size is None:
            return None

        if names:
            batch_ids = [table_size[i][0] for i in range(len(table_size))]
            res = self._get_batch_names(batch_ids)
            if res is None:
                return None
            names_dict = {row['id']:row['name'] for row in res['batchRunsList']}
            keys = names_dict.keys()
            batch_names = []
            for row in table_size:
                if row[0] in keys:
                    batch_names.append(names_dict[row[0]])
                else:
                    batch_names.append('-')
            table_to_display = [[batch_names[i]] + list(table_size[i]) for i in range(len(table_size))]
            return table_to_display
        else:
            return table_size

    def get_data_structure(self, topic: str = None):
        '''
        Print structure of the json-data column for the specific topic(s).

        Each tuple conatains topic and type names, structure of the corresponding data and number of sids.

        Parameters
        ----------
        topic : list or list of str, optional
            list of the topics to show data structure for.
            Have higher priority, than those defined by `topic()` and `set_filter()` methods 
            and will override them.
            If not specified, shows data structure for all topics.

        Examples
        --------
        Print structure of the json-data column for topics 'A' and 'C':

        >>> citros = da.CitrosDB()
        >>> citros.topic(['A', 'C']).get_data_structure()
        
        or
        
        >>> citros.get_data_structure(['A', 'C'])
        +-------+------+-----------------+
        | topic | type | data            |
        +-------+------+-----------------+
        |     A |    a | {               |
        |       |      |   x: {          |
        |       |      |     x_1: float, |
        |       |      |     x_2: float, |
        |       |      |     x_3: float  |
        |       |      |   },            |
        |       |      |   note: list,   |
        |       |      |   time: float,  |
        |       |      |   height: float |
        |       |      | }               |
        +-------+------+-----------------+
        |     C |    c | {               |
        |       |      |   x: {          |
        |       |      |     x_1: float, |
        |       |      |     x_2: float, |
        |       |      |     x_3: float  |
        |       |      |   },            |
        |       |      |   note: list,   |
        |       |      |   time: float,  |
        |       |      |   height: float |
        |       |      | }               |
        +-------+------+-----------------+
        '''
        if not self._is_batch_available():
            return None
        _PgCursor.get_data_structure(self, topic = topic)

    def get_unique_values(self, column_names: Optional[Union[str, list]], filter_by: dict = None) -> list:
        '''
        Return unique values of the columns `column_names`.

        Parameters
        ----------
        column_names : str or list of str
            Columns for which the unique combinations of the values will be found.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values,<br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.

        Returns
        -------
        list or list of tuples
            Each tuple contains unique combinations of the values for `column_names`.

        Examples
        --------
        Get unique values of type for topics 'A' or 'B', where 10 <= 'time' <= 5000 and data.x.x_1 > 10:
        
        >>> citros = da.CitrosDB()
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_unique_values(['type'])
        >>> print(result)
        ['a', 'b']

        The same, but passing all constraintes by `filter_by` parameter:
        
        >>> result = citros.get_unique_values(['type'], filter_by = {'topic': ['A', 'B'], 
        ...                                       'time': {'>=': 10, '<=': 5000}, 
        ...                                       'data.x.x_1': {'>':10}})
        >>> print(result)
        ['a', 'b']
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_unique_values(self, column_names = column_names, filter_by = filter_by)
        
    def get_max_value(self, column_name: str, filter_by: dict = None, return_index: bool = False):
        '''
        Return maximum value of the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values,<br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        return_index : bool, default False
            If True, the pair of sid and rid corresponding to the obtained maximum value is also returned.

        Returns
        -------
        value : int, float, str or None
            Maximum value of the column `column_name`.
        sid : int or list
            Corresponding to the maximum value's sid. Returns only if `return_index` is set to True.
        rid : int or list
            Corresponding to the maximum value's rid. Returns only if `return_index` is set to True

        Examples
        --------
        Get max value of the column 'data.x.x_2' where topics are 'A' or 'B', 10 <= 'time' <= 5000 and data.x.x_1 > 10:
        
        >>> citros = da.CitrosDB()
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_max_value('data.x.x_2')
        >>> print(result)
        76.0

        Get also the sid and rid of the maximum value:

        >>> result, sid_max, rid_max = citros.topic(['A', 'B'])\\
        ...                            .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                            .time(start = 10, end = 5000)\\
        ...                            .get_max_value('data.x.x_2', return_index = True)
        >>> print(f"max = {result} at sid = {sid_max}, rid = {rid_max}")
        max = 76.0 at sid = 4, rid = 47

        The same as in the first example, but passing all constraintes by `filter_by` parameter:

        >>> result = citros.get_max_value('data.x.x_2',
        ...                               filter_by = {'topic': ['A', 'B'], 
        ...                                            'time': {'>=': 10, '<=': 5000}, 
        ...                                            'data.x.x_1' : {'>':10}})
        >>> print(result)
        76.0
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_min_max_value(self, column_name = column_name, filter_by = filter_by, 
                                           return_index = return_index, mode = 'MAX')

    def get_min_value(self, column_name: str, filter_by: dict = None, return_index: bool = False):
        '''
        Return minimum value of the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values, <br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        return_index : bool, default False
            If True, the pair of sid and rid corresponding to the obtained minimum value is also returned.
            If there are several cases when the maximum or minimum value is reached, the lists of corresponding 
            sids and rids are returned.

        Returns
        -------
        value : int, float, str or None
            Minimum value of the column `column_name`.
        sid : int or list
            Corresponding to the minimum value's sid. Returns only if `return_index` is set to True.
        rid : int or list
            Corresponding to the minimum value's rid. Returns only if `return_index` is set to True.

        Examples
        --------
        Get min value of the column 'data.x.x_2' where topics are 'A' or 'B', 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> citros = da.CitrosDB()
        >>> result = citros.topic(['A', 'B'])\\
        ...                .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                .time(start = 10, end = 5000)\\
        ...                .get_min_value('data.x.x_2')
        >>> print(result)
        -4.0

        Get also the sid and rid of the minimum value:

        >>> result, sid_min, rid_min = citros.topic(['A', 'B'])\\
        ...                            .set_filter({'data.x.x_1': {'>=': 10}})\\
        ...                            .time(start = 10, end = 5000)\\
        ...                            .get_min_value('data.x.x_2', return_index = True)
        >>> print(f"min = {result} at sid = {sid_min}, rid = {rid_min}")
        min = -4.0 at sid = 4, rid = 44

        The same as in the first example, but passing all constraintes by `filter_by` parameter:

        >>> result = citros.get_min_value('data.x.x_2',
        ...                               filter_by = {'topic': ['A', 'B'], 
        ...                                            'time': {'>=': 10, '<=': 5000}, 
        ...                                            'data.x.x_1' : {'>':10}})
        >>> print(result)
        -4.0
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_min_max_value(self, column_name = column_name, filter_by = filter_by, 
                                           return_index = return_index, mode = 'MIN')
        
    def get_counts(self, column_name: str = None, group_by: Optional[Union[str, list]] = None, filter_by: dict = None, 
                   nan_exclude: bool = False) -> list:
        '''
        Return number of the rows in the column `column_name`.

        Parameters
        ----------
        column_name : str
            Label of the column.
        group_by : list, optional
            Labels of the columns to group by. If blank, do not group.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values, <br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        nan_exclude : bool, default False
            If True, nan values are excluded from the count.

        Returns
        -------
        list of tuples or None
            Number of rows in `column_name`.

        Examples
        --------
        Calculate the total number of rows:

        >>> citros = da.CitrosDB()
        >>> citros.get_counts()
        [(300,)]

        Calculate the total number of rows in the topic 'A':

        >>> citros = da.CitrosDB()
        >>> citros.topic('A').get_counts()
        [(100,)]

        If the structure of the data column is the following:

        ```python
        {x: {x_1: 52}, note: ['b', 'e']}
        {x: {x_1: 11}, note: ['a', 'c']}
        {x: {x_1: 92}, note: ['b', 'd']}
        ...
        ```
        to find the number of values from the first position of the json-array 'note' for topics 'A' or 'B',
        where 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> citros = da.CitrosDB()
        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_counts('data.note[0]')
        [(30,)]

        To perform under the same conditions, but to get values grouped by topics:

        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_counts('data.note[0]', group_by = ['topic'])
        [('A', 17), ('B', 13)]

        The same, but passing all constraintes by `filter_by` parameter:
        
        >>> citros.get_counts('data.note[0]',
        ...                    group_by = ['topic'],
        ...                    filter_by = {'topic': ['A', 'B'], 
        ...                                 'time': {'>=': 10, '<=': 5000}, 
        ...                                 'data.x.x_1' : {'>':10}})
        [('A', 17), ('B', 13)]
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_counts(self, column_name = column_name, group_by = group_by, filter_by= filter_by, 
                   nan_exclude = nan_exclude)

    def get_unique_counts(self, column_name: str = None, group_by: list = None, filter_by: dict = None, 
                          nan_exclude: bool = False) -> list:
        '''
        Return number of the unique values in the column `column_name`.

        Parameters
        ----------
        column_name : str
            Column to count its unique values.
        group_by : list, optional
            Labels of the columns to group by. If blank, do not group.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values, <br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        nan_exclude : bool, default False
            If True, nan values are excluded from the count.

        Returns
        -------
        list of tuples or None
            Counts of the unique values in `column_name`.

        Examples
        --------
        If the structure of the data column is the following:

        ```python
        {x: {x_1: 52}, note: ['b', 'e']}
        {x: {x_1: 11}, note: ['a', 'c']}
        {x: {x_1: 92}, note: ['b', 'd']}
        ...
        ```
        to get the number of unique values from the first position of the json-array 'note' for topics 'A' or 'B',
        where 10 <= 'time' <= 5000 and data.x.x_1 > 10:

        >>> citros = da.CitrosDB()
        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_unique_counts('data.note[0]')
        [(2,)]

        To perform under the same conditions, but to get values grouped by topics:

        >>> citros.topic(['A', 'B'])\\
        ...       .set_filter({'data.x.x_1': {'>': 10}})\\
        ...       .time(start = 10, end = 5000)\\
        ...       .get_unique_counts('data.note[0]', group_by = ['topic'])
        [('A', 2), ('B', 2)]
        
        The same, but passing all constraintes by `filter_by` parameter:

        >>> citros.get_unique_counts('data.note[0]',
        ...                           group_by = ['topic'],
        ...                           filter_by = {'topic': ['A', 'B'], 
        ...                                        'time': {'>=': 10, '<=': 5000}, 
        ...                                        'data.x.x_1' : {'>':10}})
        [('A', 2), ('B', 2)]
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_unique_counts(self, column_name = column_name, group_by = group_by, filter_by = filter_by, 
                          nan_exclude = nan_exclude)
      
    def get_sid_tables(self, data_query: list = None, topic: Optional[Union[str, list]] = None, additional_columns: list = None, 
                       filter_by: dict = None, order_by: Optional[Union[str, list, dict]] = None, 
                       method: str = None, n_avg: int = 1, n_skip: int = 1):
        '''
        Return dict of tables, each of the tables corresponds to exact value of sid.

        Parameters
        ----------
        data_query : list, optional
            Labels of the data to download from the json-format column "data".
            If blank list, then all columns are are downloaded.
        topic : str or list of str
            Name of the topic.
            Have higher priority than defined by `topic()`.
            May be overrided by `filter_by` argument.
        additional_columns : list, optional
            Columns to download outside the json "data".
            If blank list, then all columns are are downloaded.
        filter_by : dict, optional
            Constraints to apply on columns: {key_1: value_1, key_2: value_2, ...}.<br />
            key_n - must match labels of the columns, <br />
            value_n  - in the case of equality: list of exact values<br />
                       in the case of inequality: dict with ">", ">=", "<" or "<=".<br />
            Conditions, passed here, have higher priority over those defined by `topic()`, `rid()`, `sid()`, `time()` and `set_filter()` and will override them.
        order_by : str or list of str or dict, optional
            If `order_by` is a single string or a list of strings, it represents the column label(s) by which the result is sorted in ascending order.
            For more control, use a dictionary with column labels as keys and values ('asc' for ascending, 'desc' for descending) to define the sorting order.
            Conditions, passed here, have higher priority over those defined by `set_order()` and will override them.
        method : {'', 'avg', 'move_avg', 'skip'}, optional
            Method of sampling:
            'avg' - average - average ``n_avg`` rows;
            'move_avg' - moving average - average ``n_avg`` rows and return every ``n_skip``-th row;
            'skip' - skiping ``n_skip`` rows;
            '' - no sampling.
            If not specified, no sampling is applied    
        n_avg : int
            Used only if ``method`` is 'move_avg' or 'avg'.
            Number of rows for averaging.
        n_skip : int
            Used only if ``method`` is 'move_avg' or 'skip'.
            Number of rows to skip in a result output. 
            For example, if skip = 2, only every second row will be returned.
        
        Returns
        -------
        dict of pandas.DataFrames
            dict with tables, key is a value of sid.

        Examples
        --------
        Download averaged data for each sid separately, setting ascending order by 'rid':

        >>> citros = da.CitrosDB()
        >>> dfs = citros.topic('A').set_order({'rid': 'asc'}).avg(2)\\
                        .get_sid_tables(data_query=['data.x.x_1'])

        Print sid value:

        >>> print(f'sid values are: {list(dfs.keys())}')
        sid values are: [1, 2, 3, 4]

        Get table corresponding to the sid = 2 and assign it to 'df':

        >>> df = dfs[2]

        The same, but setting constraints by parameters: 

        >>> dfs = citros.get_sid_tables(data_query = ['data.x.x_1'],
        ...                             topic = 'A', 
        ...                             additional_columns = [], 
        ...                             filter_by = {}, 
        ...                             order_by = {'rid': 'asc'}, 
        ...                             method = 'avg', 
        ...                             n_avg = 2)
        >>> print(f'sid values are: {list(dfs.keys())}')
        sid values are: [1, 2, 3, 4]
        '''
        if not self._is_batch_available():
            return None
        return _PgCursor.get_sid_tables(self, data_query, topic, additional_columns, filter_by, order_by, method, n_avg, n_skip)
    
    def plot_graph(self, df: pd.DataFrame, x_label: str, y_label: str, *args, ax: Optional[plt.Axes] = None, legend: bool = True, 
                   title: Optional[str] = None, set_x_label: Optional[str] = None, set_y_label: Optional[str] = None, 
                   remove_nan: bool = True, inf_vals: Optional[float] = 1e308, **kwargs):
        '''
        Plot graph '`y_label` vs. `x_label`' for each sid, where `x_label` and `y_label`
        are the labels of columns of the pandas.DataFrame `df`.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_label : str
            Label of the column to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, default None
            Label to set to the y-axis. If None, label is set according to `y_label`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : matplotlib.axes.Axes
            Created axis if `ax` is not passed.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        
        Examples
        --------
        Import matplotlib and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        From topic 'A' from json-data column download 'data.x.x_1' and 'data.x.x_2' columns:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(['data.x.x_1', 'data.x.x_2'])

        Plot `data.x.x_1` vs. `data.x.x_2`:

        >>> citros.plot_graph(df, 'data.x.x_1', 'data.x.x_2', ax = ax)
        
        Generate a new figure and plot the previous graph but using a dotted line:
        
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()
        >>> citros.plot_graph(df, 'data.x.x_1', 'data.x.x_2', '.', ax = ax)    
        '''
        plotter = _Plotter()
        return plotter.plot_graph(df, x_label, y_label, ax, legend, title , set_x_label, set_y_label, 
                                  remove_nan, inf_vals,  *args, **kwargs)

    def plot_3dgraph(self, df: pd.DataFrame, x_label: str, y_label: str, z_label: str, *args, ax: Optional[plt.Axes] = None, 
                     scale: bool = True, legend: bool = True, title: Optional[str] = None, 
                     set_x_label: Optional[str] = None, set_y_label: Optional[str] = None, set_z_label: Optional[str] = None, 
                     remove_nan: bool = True, inf_vals: Optional[float] = 1e308, **kwargs):
        '''
        Plot 3D graph '`z_label` vs. `x_label` and `y_label`' for each sid, where `x_label`, `y_label` and `z_label`
        are the labels of columns of the pandas.DataFrame `df`.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_label : str
            Label of the column to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created.
        scale : bool, default True
            Specify whether the axis range should be the same for all axes.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, default None
            Label to set to the y-axis. If None, label is set according to `y_label`.
        set_z_label : str, default None
            Label to set to the z-axis. If None, label is set according to `z_label`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : matplotlib.axes.Axes
            Created axis if `ax` is not passed.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        
        Examples
        --------
        Import matplotlib and mplot3d for 3D plots and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> from mpl_toolkits import mplot3d
        >>> fig = plt.figure(figsize=(6, 6))
        >>> ax = fig.add_subplot(111, projection = '3d')

        For topic 'A' from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' columns:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        Make 3D plot with dashed lines; `scale` = True aligns all axes to have the same range:

        >>> citros.plot_3dgraph(df, 'data.x.x_1', 'data.x.x_2', 'data.x.x_1', '--', ax = ax, scale = True)
        '''
        plotter = _Plotter()
        return plotter.plot_3dgraph(df, x_label, y_label, z_label, ax, scale, legend, title, 
                                    set_x_label, set_y_label, set_z_label, remove_nan, inf_vals, *args, **kwargs)
        
    def multiple_y_plot(self, df: pd.DataFrame, x_label: str, y_labels: str, *args, fig: Optional[matplotlib.figure.Figure] = None, 
                        legend: bool = True, title: Optional[str] = None, set_x_label: Optional[str] = None, 
                        set_y_label: Optional[str] = None, remove_nan: bool = True, inf_vals: Optional[float] = 1e308, **kwargs):
        '''
        Plot a series of vertically arranged graphs 'y vs. `x_label`', with the y-axis labels 
        specified in the `y_labels` parameter.

        Different colors correspond to different sids.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_labels : list of str
            Labels of the columns to plot along y-axis.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        fig : matplotlib.figure.Figure, optional
            If None, a new Figure will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : str, default None
            Label to set to the x-axis. If None, label is set according to `x_label`.
        set_y_label : list of str, default None
            Labels to set to the y-axis. If None, label is set according to `y_labels`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `fig` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `fig` is not passed.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        
        Examples
        --------
        For topic 'A' from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' and 'data.time' columns:

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3', 'data.time'])

        Plot three graphs: 'data.x.x_1' vs. 'data.time', 'data.x.x_2' vs. 'data.time' and 'data.x.x_3' vs. 'data.time':

        >>> fig, ax = citros.multiple_y_plot(df, 'data.time', ['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        Plot scatter graph:

        >>> fig, ax = citros.multiple_y_plot(df, 'data.time', ['data.x.x_1', 'data.x.x_2', 'data.x.x_3'], '.')
        '''
        plotter = _Plotter()
        return plotter.multiple_y_plot(df, x_label, y_labels,  fig, legend, title, set_x_label, set_y_label, remove_nan, inf_vals, *args, **kwargs)
        
    
    def multiplot(self, df: pd.DataFrame, labels: list, *args, scale: bool = True, fig: Optional[matplotlib.figure.Figure] = None, 
                  legend: bool = True, title: Optional[str] = None, set_x_label: Optional[str] = None, set_y_label: Optional[str] = None, 
                  remove_nan: bool = True, inf_vals: Optional[float] = 1e308, label_all_xaxis: bool = False, 
                  label_all_yaxis: bool = False, num: int = 5, **kwargs):
        '''
        Plot a matrix of N x N graphs, each displaying either the histogram with values distribution (for graphs on the diogonal) or
        the relationship between variables listed in `labels`, with N being the length of `labels` list.

        For non-diagonal graphs, colors are assigned to points according to sids.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        labels : list of str
            Labels of the columns to plot.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        scale : bool, default True
            Specify whether the axis range should be the same for x and y axes.
        fig : matplotlib.figure.Figure, optional
            If None, a new Figure will be created.
        legend : bool, default True
            If True, show the legend with sids.
        title : str
            Set title of the plot.
        set_x_label : list of str
            Labels to set to the x-axis. If None, label is set according to `labels`.
        set_y_label : list of str
            Labels to set to the y-axis. If None, label is set according to `labels`.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.
        label_all_xaxis : bool, default False
            If True, x labels are set to the x-axes of the all graphs, otherwise only to the graphs in the bottom row.
        label_all_yaxis : bool, default False
            If True, y labels are set to the y-axes of the all graphs, otherwise only to the graphs in the first column.
        num : int, default 5
            Number of bins in the histogram on the diogonal.
            
        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `fig` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `fig` is not passed.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        Examples
        --------
        For topic 'A' from json-data column download 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3':

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(['data.x.x_1', 'data.x.x_2', 'data.x.x_3'])

        Plot nine graphs: histograms for three graphs on the diogonal, that represent 
        distribution of the 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3' values, and six graphs that show 
        correlation between them; plot by dots and scale x and y axes ranges to oneintreval for each graph:

        >>> fig, ax = citros.multiplot(df, ['data.x.x_1'], '.' ,fig = fig, scale = True)
        '''
        plotter = _Plotter()
        return plotter.multiplot(df, labels, scale, fig, legend, title, set_x_label, set_y_label, remove_nan, inf_vals, label_all_xaxis, 
                  label_all_yaxis, num, *args, **kwargs)
        
    def plot_sigma_ellipse(self, df: pd.DataFrame, x_label: str, y_label: str, ax: plt.Axes = None, n_std: int = 3, 
                           plot_origin: bool = True, bounding_error: bool = False, inf_vals: Optional[float] = 1e308, 
                           legend: bool = True, title: Optional[str] = None, set_x_label: Optional[str] = None, 
                           set_y_label: Optional[str] = None, scale: bool = False, return_ellipse_param: bool = False):
        '''
        Plot sigma ellipses for the set of data.

        Parameters
        ----------
        df : pandas.DataFrame
            Data table.
        x_label : str
            Label of the column to plot along x-axis.
        y_labels : list of str
            Labels of the columns to plot along y-axis.
        ax : matplotlib.axes.Axes
            Figure axis to plot on. If not specified, the new pair of fig, ax will be created and returned.
        n_std : int or list of ints
            Radius of ellipses in sigmas.
        plot_origin: bool, default True
            If True, depicts origin (0, 0) with black cross.
        bounding_error : bool, default False
            If True, plots bounding error circle for each of the ellipses.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.
        legend : bool, default True
            If True, show the legend.
        title : str, optional
            Set title. If None, title is set as '`x_label` vs. `y_label`'.
        set_x_label : str, optional
            Set label of the x-axis. If None, label is set according to `x_label`.
        set_y_label : str, optional
            Set label of the y-axis. If None, label is set according to `y_label`.
        scale : bool, default False
            Specify whether the axis range should be the same for x and y axes.
        return_ellipse_param : bool, default False
            If True, returns ellipse parameters.

        Returns
        -------
        fig : matplotlib.figure.Figure
            Created figure if `ax` is not passed.
        ax : numpy.ndarray of matplotlib.axes.Axes
            Created axis if `ax` is not passed.
        ellipse_param : dict or list of dict
            Ellipse parameters if `return_ellipse_param` set True.<br />
            Parameters of the ellipse:
          - x : float
              x coordinate of the center.
          - y : float
              y coordinate of the center.
          - width : float
              Total ellipse width (diameter along the longer axis).
          - height : float
              Total ellipse height (diameter along the shorter axis).
          - alpha : float
              Angle of rotation, in degrees, anti-clockwise from the shorter axis.<br />
            If bounding_error set True:
          - bounding_error : float
              Radius of the error circle.

        Examples
        --------
        For topic 'A' from json-data column query 'data.x.x_1', 'data.x.x_2' and 'data.x.x_3':

        >>> citros = da.CitrosDB()
        >>> df = citros.topic('A').data(['data.x.x_1', 'data.x.x_2'])

        Plot 'data.x.x_1' vs. 'data.x.x_2', 1-$\sigma$ ellipse, origin point that has coordinates (0, 0) 
        and set the same range for x and y axis:

        >>> fig, ax = citros.plot_sigma_ellipse(df, x_label = 'data.x.x_1', y_label = 'data.x.x_2',
        ...                                      n_std = 1, plot_origin=True, scale = True)

        Plot the same but for 1-, 2- and 3-$\sigma$ ellipses, add bounding error circle (that indicates the maximum distance
        between the ellipse points and the origin), set custom labels and title to the plot:

        >>> fig, ax = citros.plot_sigma_ellipse(df, x_label = 'data.x.x_1', y_label = 'data.x.x_2', 
        ...                                     n_std = [1,2,3], plot_origin=True, bounding_error=True, 
        ...                                     set_x_label='x, [m]', set_y_label = 'y, [m]', 
        ...                                     title = 'Coordinates')
        '''
        plotter = _Plotter()
        return plotter.plot_sigma_ellipse(df, x_label, y_label, ax, n_std, plot_origin, bounding_error, inf_vals, 
                           legend, title, set_x_label, set_y_label, scale, return_ellipse_param)
        

    def time_plot(self, ax: plt.Axes, *args, topic_name: Optional[str] = None, var_name: Optional[str] = None, 
                  time_step: Optional[float] = 1.0, sids: list = None, y_label: Optional[str] = None, title_text: Optional[str] = None, 
                  legend: bool = True, remove_nan: bool = True, inf_vals: Optional[float] = 1e308, **kwargs):
        '''
        Plot `var_name` vs. `Time` for each of the sids, where `Time` = `time_step` * rid.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Figure axis to plot on.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        topic_name : str
            Input topic name. If specified, will override value that was set by `topic()` method.
        var_name : str
            Name of the variable to plot along y-axis.
        time_step : float or int, default 1.0
            Time step, `Time` = `time_step` * rid.
        sids : list
            List of the sids. If specified, will override values that were set by `sid()` method.
            If not specified, data for all sids is used.
        y_label : str
            Label to set to y-axis. Default `var_name`.
        title_text : str
            Title of the figure. Default '`var_y_name` vs. Time'.
        legend : bool
            If True, show the legend with sids.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        Examples
        --------
        Import matplotlib and create figure to plot on:

        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        For topic 'A' plot `data.x.x_1` vs. `Time` for all existing sids, `Time` = 0.5 * rid

        >>> citros = da.CitrosDB()
        >>> citros.time_plot(ax, topic_name = 'A', var_name = 'data.x.x_1', time_step = 0.5)

        It is possible to set topic by `topic()` method:

        >>> citros.topic('A').time_plot(ax, var_name = 'data.x.x_1', time_step = 0.5)

        Create a new figure and plot only part of the data, where 'data.x.x_1' <= 0; plot by dashed line:

        >>> fig, ax = plt.subplots()
        >>> citros.topic('A').set_filter({'data.x.x_1':{'<=': 0}})\\
                  .time_plot(ax, '--', var_name = 'data.x.x_1', time_step = 0.5)
        '''
        if not self._is_batch_available():
            return
        var_df, sids = _PgCursor.data_for_time_plot(self, topic_name, var_name, time_step, sids, remove_nan, inf_vals)
        if var_df is None:
            return
    
        plotter = _Plotter()
        plotter.time_plot(var_df, ax, var_name, sids, y_label, title_text, legend, *args, **kwargs)

    def xy_plot(self, ax: plt.Axes, *args, topic_name: Optional[str] = None, var_x_name: Optional[str] = None, 
                var_y_name: Optional[str] = None, sids: Optional[Union[int, list]] = None, x_label: Optional[str] = None, 
                y_label: Optional[str] = None, title_text: Optional[str] = None, legend: bool = True, remove_nan: bool = True, 
                inf_vals: Optional[float] = 1e308, **kwargs):
        '''
        Plot `var_y_name` vs. `var_x_name` for each of the sids.

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Figure axis to plot on.
        *args : Any
            Additional arguments to style lines, set color, etc, 
            see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.
        topic_name : str
            Input topic name. If specified, will override value that was set by `topic()` method.
        var_x_name : str
            Name of the variable to plot along x-axis.
        var_y_name : str
            Name of the variable to plot along y-axis.
        sids : int or list of int, optional
            List of the sids. If specified, will override values that were set by `sid()` method.
            If not specified, data for all sids is used.
        x_label : str, optional
            Label to set to x-axis. Default `var_x_name`.
        y_label : str, optional
            Label to set to y-axis. Default `var_y_name`.
        title_text : str, optional
            Title of the figure. Default '`var_y_name` vs. `var_x_name`'.
        legend : bool
            If True, show the legend with sids.
        remove_nan : bool, default True
            If True, NaN values will be removed before plotting.
        inf_vals : None or float, default 1e308
            If specified, all values that exceed the provided value in absolute terms will be removed before plotting.
            If this functionality is not required, set inf_vals = None.

        Other Parameters
        ----------------
        **kwargs
            Other keyword arguments, see **[matplotlib.axes.Axes.plot](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.plot.html)**.

        Examples
        --------
        >>> import matplotlib.pyplot as plt
        >>> fig, ax = plt.subplots()

        For topic 'A' plot 'data.x.x_1' vs. 'data.x.x_2' for all existing sids:

        >>> citros = da.CitrosDB()
        >>> citros.xy_plot(ax, topic_name = 'A', var_x_name = 'data.x.x_1', var_y_name = 'data.x.x_2')

        It is possible to set topic by `topic()` method:

        >>> citros.topic('A').xy_plot(ax, var_x_name = 'data.x.x_1', var_y_name = 'data.x.x_2')

        Create new figure and plot only part of the data, where 'data.x.x_1' <= 0, sid = 1 and 2; plot by dashed lines:

        >>> fig, ax = plt.subplots()
        >>> citros.topic('A').set_filter({'data.x.x_1':{'<=': 0}}).sid([1,2])\\
                  .xy_plot(ax, '--', var_x_name = 'data.x.x_1', var_y_name = 'data.x.x_2')
        '''
        if not self._is_batch_available():
            return None
        xy_df, sids = _PgCursor.data_for_xy_plot(self, topic_name, var_x_name, var_y_name, sids, remove_nan, inf_vals)
        if xy_df is None:
            return
        
        plotter = _Plotter()
        plotter.xy_plot(xy_df, ax,  var_x_name, var_y_name, sids, x_label, y_label, title_text, legend, *args, **kwargs)