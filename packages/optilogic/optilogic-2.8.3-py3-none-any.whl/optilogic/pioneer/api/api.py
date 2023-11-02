'''
Implementation of the Optilogic Pioneer Rest API.

API DOCUMENTATION
https://api-docs.optilogic.app/documentation

API AUTHENTICATION METHODS
User Pass: Legacy auth method with time to live key management.
App Key: Preferred auth method for API usage.

App Key Management
https://optilogic.app/#/user-account?tab=appkey

PIONEER PLATFORM & PRODUCT SUITE
Encompasses web applications such as Atlas, Andromeda, Rest API, Jobs Dashboard, Resource Library,
Account Management, Lightning Editor, SQL Editor, Cloud Storage, SCG Converter, Analytics Designer,
and more.

ATLAS
An Integrated Development Environment (IDE) designed specifically for Python programming.
It offers a terminal, debugger, along with cloud-based file storage, enabling you to conveniently
store and collaborate on your code with fellow users on the platform. Furthermore, ATLAS includes a
no-code automation capability for running extensive Python scripts via the job system. These scripts
operate in the background allowing you to carry out additional tasks concurrently.
https://optilogic.app/#/ide/{YOUR_USERNAME}/Studio

ANDROMEDA
The on-demand hyper-scaling system provisions a virtual machine software environment tailored to the
workspace's specifications. This environment is equipped with the necessary computational resources
to meet the demands of job management, concurrency, and the execution of Python modules.

STACK
Is a configuration of a Linux software environment consisting of multiple elements: kernel,
file system, system libraries, device drivers, utilities, package management, application software,
and beyond. This stack setup serves as the foundation for creating workspaces utilized in the
execution of tasks by Atlas and Andromeda.

WORKSPACE
A software environment is constructed using an stack instance which includes connected file storage
to save your code and projects. All users will have a default workspace named 'Studio' which is
created upon account creation. Workspace is accessible in the Atlas IDE, Lightning Editor, and
Andromeda. A multi-workspace feature may be available to paid users who need specific environments.
The term "Workspace" is also shortened to either WKSP or WS.

FILE STORAGE
A broad file storage reference that includes various types, such as workspace and account file
storage.

WORKSPACE FILE STORAGE
Standard file storage that is bound to specific workspace instance. Every workspace has a file
storage component.

ACCOUNT FILE STORAGE
In addition to the standard workspace file storage, exclusive to paid users, an enhanced premium SSD
file storage is connected to each user's workspace within the Atlas and Andromeda product. This
premium storage, offering high IOPS and significant capacity, allows you even more choice and
capability.

ANURA
Anura is a designated data schema, encompassing a set of tables, columns, and data types. This
schema serves as the framework for visualizing and populating your supply chain elements, policies,
and constraints.

MODEL
It encompasses either a PostgreSQL database or a set of delimited CSV files that adheres to the Anura
data schema with a hydrated data representation your supply chain.
'''

import os
import pickle
import time
from cachetools import cached, TTLCache
from datetime import datetime
from getpass import getpass
from json import dumps, loads
from os import getenv
from re import fullmatch, search
from requests import ConnectionError, delete, get, HTTPError, Response, request
from sys import platform
from tempfile import gettempdir
from types import FrameType
from typing import Any, cast, Dict, List, Literal, Optional, Set, Tuple, TypedDict, Union
from warnings import warn, warn_explicit

if platform == 'linux':
    from inspect import currentframe
    from signal import alarm, signal, SIGALRM
    from urllib.parse import unquote


class CacheEntry(TypedDict):
    '''Type annotations for cache entry to the cache store.'''

    value: Union[bool, float, int, str]
    updated: float


class DbTemplates(TypedDict):
    '''Type annotations for database templates.'''

    id: Literal[
        '2.1',
        '7.6',
        '7.11',
        '7.12',
        '9.20230925133401',
        '9.2023092508324',
        '12.20230925133401',
        '12.20230925083242',
        '15.202309251334',
        '15.20230925083242',
        '18.20230925133401',
        '18.20230925084416',
        '21.20230925133908',
        '21.20230925084431',
        '24.20230925133401',
        '24.20230925083847',
        '27.20230925084417',
        '27.20230925133955',
        '28.20230925083242',
        '28.202309251334',
        '29.20230925083241',
        '29.202309251334',
        '30.20230925083242',
        '30.20230925133401',
        '31.20230925084458',
        '31.20230925134019',
        '32.20230925083852',
        '32.20230925133401',
        '35.20230921133352',
        '35.20230925133401',
        '36.20230921130338',
        '36.20230925134017',
        '37.20230926142439',
        '37.20230927091221',
    ]
    name: Literal[
        'Empty Database',
        'Anura New Model',
        'Anura New Model v2.7.11',
        'Anura New Model v2.7.14',
        'Global Supply Chain Strategy (2.7.3)',
        'Global Supply Chain Strategy',
        'Tactical Capacity Optimization (2.7.3)',
        'Tactical Capacity Optimization',
        'Detailed Facility Selection (2.7.3)',
        'Detailed Facility Selection',
        'United States Greenfield Facility Selection (2.7.3)',
        'United States Greenfield Facility Selection',
        'China Exit Strategy in Asia (2.7.3)',
        'China Exit Strategy in Asia',
        'China Exit Risk Strategy (2.7.3)',
        'China Exit Risk Strategy',
        'Multi-Year Capacity Planning',
        'Multi-Year Capacity Planning (2.7.3)',
        'Fleet Size Optimization - EMEA Geo',
        'Fleet Size Optimization - EMEA Geo (2.7.3)',
        'Global Risk Analysis',
        'Global Risk Analysis (2.7.3)',
        'Fleet Size Optimization - US Geo',
        'Fleet Size Optimization - US Geo (2.7.3)',
        'Global Sustainability Analysis',
        'Global Sustainability Analysis (2.7.3)',
        'Global Sourcing - Cost To Serve',
        'Global Sourcing - Cost To Serve (2.7.3)',
        'Advanced United States Greenfield Facility Selection',
        'Advanced United States Greenfield Facility Selection (2.7.3)',
        'Outbound Distribution Simulation',
        'Outbound Distribution Simulation (2.7.3)',
        'Lookups example for Warehousing Policies',
        'Lookups example for Warehousing Policies (2.7.3)',
    ]


class Api:
    '''Optilogic API is to pilot Andromeda system.

    EXAMPLE CONFIG
    :{'un': 'username', 'pw': 'password', 'auth_legacy': True}
    :{'un': 'username', 'app_key': 'base64str'}

    :param un: username that has the API role
    :param pw: password of the user to authenticate and generate api key
    :param auth_legacy: true for conventional username password or false for appkey
    :param cfg: addition config to unpack and setup for api use
    :param apikey: username password authentication with one hour time to live
    :param appkey: authentication key generated in product without time to live restrictions
    '''

    DATABASE_TEMPLATES_NEW: Tuple[DbTemplates, ...] = (
        {'id': '2.1', 'name': 'Empty Database'},
        {'id': '7.6', 'name': 'Anura New Model'},
        {'id': '7.11', 'name': 'Anura New Model v2.7.11'},
        {'id': '7.12', 'name': 'Anura New Model v2.7.14'},
        {'id': '9.20230925133401', 'name': 'Global Supply Chain Strategy (2.7.3)'},
        {'id': '9.2023092508324', 'name': 'Global Supply Chain Strategy'},
        {'id': '12.20230925133401', 'name': 'Tactical Capacity Optimization (2.7.3)'},
        {'id': '12.20230925083242', 'name': 'Tactical Capacity Optimization'},
        {'id': '15.202309251334', 'name': 'Detailed Facility Selection (2.7.3)'},
        {'id': '15.20230925083242', 'name': 'Detailed Facility Selection'},
        {'id': '18.20230925133401', 'name': 'United States Greenfield Facility Selection (2.7.3)'},
        {'id': '18.20230925084416', 'name': 'United States Greenfield Facility Selection'},
        {'id': '21.20230925133908', 'name': 'China Exit Strategy in Asia (2.7.3)'},
        {'id': '21.20230925084431', 'name': 'China Exit Strategy in Asia'},
        {'id': '24.20230925133401', 'name': 'China Exit Risk Strategy (2.7.3)'},
        {'id': '24.20230925083847', 'name': 'China Exit Risk Strategy'},
        {'id': '27.20230925084417', 'name': 'Multi-Year Capacity Planning'},
        {'id': '27.20230925133955', 'name': 'Multi-Year Capacity Planning (2.7.3)'},
        {'id': '28.20230925083242', 'name': 'Fleet Size Optimization - EMEA Geo'},
        {'id': '28.202309251334', 'name': 'Fleet Size Optimization - EMEA Geo (2.7.3)'},
        {'id': '29.20230925083241', 'name': 'Global Risk Analysis'},
        {'id': '29.202309251334', 'name': 'Global Risk Analysis (2.7.3)'},
        {'id': '30.20230925083242', 'name': 'Fleet Size Optimization - US Geo'},
        {'id': '30.20230925133401', 'name': 'Fleet Size Optimization - US Geo (2.7.3)'},
        {'id': '31.20230925084458', 'name': 'Global Sustainability Analysis'},
        {'id': '31.20230925134019', 'name': 'Global Sustainability Analysis (2.7.3)'},
        {'id': '32.20230925083852', 'name': 'Global Sourcing - Cost To Serve'},
        {'id': '32.20230925133401', 'name': 'Global Sourcing - Cost To Serve (2.7.3)'},
        {'id': '35.20230921133352', 'name': 'Advanced United States Greenfield Facility Selection'},
        {
            'id': '35.20230925133401',
            'name': 'Advanced United States Greenfield Facility Selection (2.7.3)',
        },
        {'id': '36.20230921130338', 'name': 'Outbound Distribution Simulation'},
        {'id': '36.20230925134017', 'name': 'Outbound Distribution Simulation (2.7.3)'},
        {'id': '37.20230926142439', 'name': 'Lookups example for Warehousing Policies'},
        {'id': '37.20230927091221', 'name': 'Lookups example for Warehousing Policies (2.7.3)'},
    )
    DATABASE_TEMPLATES_NAMEID: Dict[str, str] = {
        'Advanced United States Greenfield Facility Selection (2.7.3)': 'fa3f223f-8d16-4220-aa4d-a78dd82886a0',
        'Advanced United States Greenfield Facility Selection': '0c294262-394e-402c-80c2-cbdc2fba1cbc',
        'Anura New Model v2.7.11': 'anura_2_7_11_clean',
        'Anura New Model v2.7.14': 'anura_2_7_14_clean',
        'Anura New Model': 'anura_2_6_31_3_1_clean',
        'China Exit Risk Strategy (2.7.3)': 'd2a22c9d-bb5c-44bf-a014-ada3de1092b0',
        'China Exit Risk Strategy': '29de0d54-ee83-43da-a284-04170475e7e6',
        'China Exit Strategy in Asia (2.7.3)': '1b5bf8d9-48ea-4a64-954e-985d591819e5',
        'China Exit Strategy in Asia': '48275960-5448-4aed-b5e4-2f852bf8f985',
        'Detailed Facility Selection (2.7.3)': 'a6160d9b-c5e7-421b-b860-62eacab77d31',
        'Detailed Facility Selection': '2f070371-5850-46b9-9227-327a19f3f7bb',
        'Empty Database': 'template1',
        'Fleet Size Optimization - EMEA Geo (2.7.3)': '8437b526-b15f-4a8c-84ff-d1413a69ee9b',
        'Fleet Size Optimization - EMEA Geo': 'af9630ce-fe0a-4e9b-ba6d-0d05944d8ef5',
        'Fleet Size Optimization - US Geo (2.7.3)': 'da9087a1-cce9-4598-93b4-acf96ac8bf4c',
        'Fleet Size Optimization - US Geo': 'e0a12e51-d00c-43f6-abf6-07b328d4f270',
        'Global Risk Analysis (2.7.3)': 'a18f9694-db59-49ef-92f0-ad211e2533c9',
        'Global Risk Analysis': '5d4bd0fc-1da8-4807-a560-528cb841659e',
        'Global Sourcing - Cost To Serve (2.7.3)': '42a30fb6-8f3a-41a7-a1cb-df5a80c33933',
        'Global Sourcing - Cost To Serve': '23462acf-f6b2-43a5-bc45-78c3e29bf752',
        'Global Supply Chain Strategy (2.7.3)': '640d2e66-ec81-4822-a509-be4b0b0797be',
        'Global Supply Chain Strategy': '93517785-3447-43c7-abf1-3f4545a41c83',
        'Global Sustainability Analysis (2.7.3)': '47a4f9c0-f09a-4b16-83b4-d2dc1c29f6c9',
        'Global Sustainability Analysis': '71f9da77-edb9-4fad-b18e-684065109cac',
        'Lookups example for Warehousing Policies (2.7.3)': '7956f551-6022-4dda-b3c9-dcd3551e3344',
        'Lookups example for Warehousing Policies': '753501e5-395f-4411-8015-eb178484f356',
        'Multi-Year Capacity Planning (2.7.3)': '5667340d-f6a3-435e-99f3-36efab90cd8b',
        'Multi-Year Capacity Planning': '8acfc863-1dde-4924-8480-12f02eec41e1',
        'Outbound Distribution Simulation (2.7.3)': '8c43a95f-fdab-4645-845a-2643052829d4',
        'Outbound Distribution Simulation': 'f0dfdfff-85cd-4b13-a485-2ff61856234e',
        'Tactical Capacity Optimization (2.7.3)': 'ac53b629-08e8-4aa0-b16f-d96f2043bacb',
        'Tactical Capacity Optimization': '19d1aeff-6870-4809-a433-23ef855f3dea',
        'United States Greenfield Facility Selection (2.7.3)': '170f109a-c155-4029-9e6a-ff40f42a4160',
        'United States Greenfield Facility Selection': '69fc6c70-9d94-497c-8dfb-0db1e4340ecb',
    }
    DATABASE_TEMPLATES: List[str] = [v for v in DATABASE_TEMPLATES_NAMEID.values()]
    GEO_PROVIDERS: Tuple[str, ...] = ('bing', 'google', 'mapbox', 'ptv')
    JOBSTATES: Tuple[str, ...] = (
        'submitted',
        'starting',
        'started',
        'running',
        'done',
        'stopping',
        'stopped',
        'canceling',
        'cancelled',
        'error',
    )
    JOBSTATES_ACTIVE: Tuple[str, ...] = (
        'submitted',
        'starting',
        'started',
        'running',
        'stopping',
        'canceling',
    )
    JOBSTATES_TERMINAL: Tuple[str, ...] = ('done', 'stopped', 'cancelled', 'error')
    JOBSTATES_TERMINAL_RUNTIME: Tuple[str, ...] = ('done', 'cancelled', 'error')
    SCHEMA_ANURA_VERSIONS: Tuple[str, ...] = ('2.4.0', '2.5.9', '2.5.10', '2.5.12', '2.5.13')
    STORAGE_DEVICE_TYPES: Tuple[str, ...] = (
        'azure_afs',
        'azure_workspace',
        'onedrive',
        'postgres_db',
    )

    def __init__(
        self,
        auth_legacy=True,
        version: int = 0,
        appkey: Optional[str] = None,
        un: Optional[str] = None,
        pw: Optional[str] = None,
        ut=False,
        **cfg,
    ):
        env_domain: Optional[str] = getenv('OPTILOGIC_API_URL')
        env_username: Optional[str] = getenv('OPTILOGIC_USERNAME')
        self._domain: str = 'https://api.optilogic.app'
        self.api_crash_count: int = 0
        self.auth_apikey_expiry: int = 0
        self.auth_apikey_mins_left: float = 0.0
        self.auth_apikey: Optional[str] = None
        self.auth_appkey: Optional[str] = appkey
        self.auth_method_legacy: bool = auth_legacy
        self.auth_req_header: dict = {
            'x-api-key': self.auth_apikey,
            'x-app-key': self.auth_appkey,
            'optilogic-client': 'optipy',
        }
        self.auth_username: Optional[str] = un

        if env_domain and env_domain != self._domain:
            self._domain = env_domain
        elif cfg.get('test_system'):
            self._domain = 'https://dev-api.optilogic.app'

        if version > 0:
            warn(
                f'API version {version} not supported. Defaulting to version zero',
                UserWarning,
                stacklevel=1,
            )
            version = 0

        self.api_version: str = f'{self._domain}/v{version}/'
        self.unit_test: bool = ut
        if self.auth_method_legacy:
            self.auth_req_header.pop('x-app-key')
            warn_explicit(
                'legacy userpass authentication, please use modern appkey auth https://optilogic.app/#/user-account?tab=appkey',
                FutureWarning,
                __file__,
                153,
            )

            if self.auth_username is None:
                self.auth_username = (
                    env_username if env_username else self.__input_timed('REQUIRED API Username')
                )
            assert len(self.auth_username) > 0

            self.auth_userpass: str = (
                pw if pw else self.__input_timed('REQUIRED API User Password', pw=True)
            )
            assert len(self.auth_userpass) > 0
        else:
            self.auth_req_header.pop('x-api-key')  # auth legacy header does not apply

            if appkey:
                self.auth_appkey = appkey
            else:
                env_appkey: Optional[str] = getenv('OPTILOGIC_JOB_APPKEY')
                self.auth_appkey = (
                    env_appkey if env_appkey else self.__input_timed('REQUIRED API AppKey')
                )

            if len(self.auth_appkey) != 51 or self.auth_appkey.startswith('op_') is False:
                raise ValueError(
                    'Valid appkey is required: https://optilogic.app/#/user-account?tab=appkey'
                )

            self.auth_req_header['x-app-key'] = self.auth_appkey

        self.system: Literal['prod', 'test'] = (
            'test' if self._domain.find('dev-api') > -1 else 'prod'
        )
        self.__cache: Dict[str, CacheEntry] = {}
        self.dir_tmp: str = os.path.join(gettempdir(), 'optilogic')
        self.file_cache_auth: str = os.path.join(self.dir_tmp, f'auth_{self.auth_username}.pkl')
        self.file_cache_store: str = os.path.join(
            self.dir_tmp, f'cache_{self.system}_{self.auth_username}.pkl'
        )
        self.file_log_http: str = os.path.join(self.dir_tmp, f'calls_{self.system}.csv')
        self._log_active: bool = False

        if os.path.exists(self.dir_tmp) is False:
            os.makedirs(self.dir_tmp)
        if os.path.exists(self.file_cache_auth) is False and self.auth_method_legacy:
            self.authenticate_legacy()
        if os.path.exists(self.file_cache_store):
            self.__cache_load_from_file()

        self.re_uuid4 = '(?:[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}|00000000-0000-0000-0000-000000000000)'
        self._job_start_recent_key: str = self.__job_key_recent()

        if cfg.get('user_info'):
            self.__account_summary_info()

    def __account_summary_info(self) -> None:
        '''Display account information.'''

        print('\nDATETIME'.ljust(25), datetime.now())
        resp = self.account_info()
        print(dumps(resp, sort_keys=True, indent=2))

    def __alarm_handler(self, signum: int, frame: Optional[FrameType]) -> None:
        '''Timeout expired.'''
        raise TimeoutError('timeout expired waiting for user input')

    def __batch_input_validation(self, batch: dict, find=False) -> None:
        '''Assert batch input structure.'''

        if batch.get('batchItems') is None:
            raise KeyError('batchItems key is missing')

        if len(batch['batchItems']) == 0:
            raise IndexError('batchItems list is empty')

        for item in batch['batchItems']:
            if find and item.get('pySearchTerm') is None:
                raise KeyError('pySearchTerm key is missing')
            if find is False and item.get('pyModulePath') is None:
                raise KeyError('pyModulePath key is missing')

    def __cache_entry_get(self, key: str) -> CacheEntry:
        '''Get a cache entry from the cache store.

        :param key: cache key name to retrieve
        :return: dict where key names are value and updated
        '''

        entry: Optional[CacheEntry] = self.__cache.get(key)
        if entry is None:
            warn(f'key {key} does not exist, return empty dict instead', stacklevel=2)
            return {'value': -1.0, 'updated': -1.0}
        return entry

    def __cache_load_from_file(self) -> bool:
        '''Read cache store from disk on startup and hydrate memory cache instance.

        :return: True if cache store exists and loaded, False if not loaded
        '''

        if os.path.exists(self.file_cache_store) is False:
            return False

        # hydrate cache store
        try:
            with open(self.file_cache_store, 'rb') as f:
                cache: Dict[str, CacheEntry] = pickle.load(f)
            self.__cache = cache
            return True
        except (FileNotFoundError, PermissionError, IOError, pickle.UnpicklingError):
            return False

    def __cache_save_to_file(self) -> bool:
        '''Save cache store to disk.

        :return: True if cache store saved, False if not saved
        '''

        try:
            with open(self.file_cache_store, 'wb') as f:
                pickle.dump(self.__cache, f)
            return True
        except (FileNotFoundError, PermissionError, IOError, pickle.PicklingError):
            return False

    def __does_storage_exist(
        self,
        type: Literal['azure_afs', 'azure_workspace', 'onedrive', 'postgres_db', None],
        name: Optional[str] = None,
    ) -> bool:
        '''Verify the account have a specific storage type and or storage name.

        :param type: storage type
        :param name: storage name of type, defaults to None
        '''

        if type is None and name is None:
            return False

        exists: List[bool] = []
        devices: Dict[str, Any] = self.account_storage_devices()

        if type and name:
            exists = [True for d in devices['storages'] if d['type'] == type and d['name'] == name]
        elif type:
            assert type in self.STORAGE_DEVICE_TYPES
            exists = [True for d in devices['storages'] if d['type'] == type]
        elif name:
            assert len(name) > 0
            exists = [True for d in devices['storages'] if d['name'] == name]

        return True if len(exists) >= 1 else False

    def __env(
        self,
    ) -> Dict[
        Literal['job_cmd', 'job_dir', 'job_key', 'job_api', 'job_img', 'pip_ver', 'py_ver'], str
    ]:
        '''Atlas and andromeda common environment variables.'''

        cmd: str = getenv('JOB_COMMAND', '')
        cmd = cmd.strip()
        d: Dict[
            Literal['job_cmd', 'job_dir', 'job_key', 'job_api', 'job_img', 'pip_ver', 'py_ver'], str
        ] = {
            'job_cmd': cmd,
            'job_dir': getenv('JOB_FILEPATH', ''),
            'job_key': getenv('JOB_KEY', ''),
            'job_api': getenv('OPTILOGIC_API_URL', ''),
            'job_img': getenv('RELEASE_LIFECYCLE', ''),
            'pip_ver': getenv('PYTHON_PIP_VERSION', ''),
            'py_ver': getenv('PYTHON_VERSION', ''),
        }
        return d

    def __job_key_recent(self) -> str:
        '''Most recent job key submitted.'''

        resp = self._account_jobs(1)  # TODO assert is latest and not stale
        return '' if len(resp.get('jobs', [])) == 0 else resp['jobs'][0]['jobKey']

    def __input_timed(self, question: str, max_secs: int = 30, pw: bool = False) -> str:
        '''Linux only user input prompt with max time in seconds to complete.'''

        answer: str = ''
        question = f'\n{question.strip()} -> '

        if platform == 'linux':
            if self.unit_test:
                max_secs = 1
            signal(SIGALRM, self.__alarm_handler)
            alarm(max_secs)
            try:
                answer = getpass(question) if pw else input(question)
            finally:
                alarm(0)
        else:
            answer = getpass(question) if pw else input(question)

        return answer

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def __ip_address_is(self) -> str:
        '''Hack - identify external ip4 address if a database pre-exists.'''

        # TODO future state granular db per db server ips
        db: Dict[str, Any] = self.account_storage_device('postgres_db')
        resp: Dict[str, Any] = self.ip_address_allowed(db['name'])
        return resp['ip']

    def __log_http_request(self, rsp: Response) -> None:
        '''Log http requests to disk.

        :param: resp Response: result from a http request
        '''

        if platform != 'linux':
            # stack frame is not guaranteed
            return

        # linter friendly even though we guarded against stack frame being None
        fn: str = cast(
            FrameType, cast(FrameType, cast(FrameType, currentframe()).f_back).f_back
        ).f_code.co_name

        secs: float = round(rsp.elapsed.total_seconds(), 4)
        verb: str = rsp.request.method.upper() if rsp.request.method else ''
        now: datetime = datetime.utcnow()
        url: str = unquote(rsp.url)
        url = url.replace(',', '')
        log: str = f'{now},{secs},{fn.upper()},{rsp.status_code},{verb},{url},'
        if rsp.request.body and isinstance(rsp.request.body, bytes):
            body: str = rsp.request.body.decode('utf-8', 'ignore')
            body = body.replace(',', '')
            log += f'{body},'
        else:
            log += ','
        if 500 <= rsp.status_code < 600:
            try:
                d: dict = rsp.json()
                log += f"{rsp.reason} {d.get('error')} {d.get('correlationId')}"
            except ValueError:
                log += f'{rsp.text}'
        with open(self.file_log_http, 'a+') as f:
            f.write(f'{log}\n')

    def __schema_anura_versions(self) -> List[str]:
        '''List of anura schemas tha major.minor.build.'''

        resp = self.database_schemas_anura()
        versions: List[str] = [s['schemaVersion'] for s in resp['schemas']['anura']]
        return sorted(versions, reverse=True)

    def __storage_type(
        self, type: Literal['azure_afs', 'azure_workspace', 'onedrive', 'postgres_db']
    ) -> List[Dict[str, Any]]:
        '''Specific storage type list.

        :param type: storage type
        '''

        assert type in self.STORAGE_DEVICE_TYPES
        resp: Dict[str, Any] = self.account_storage_devices()
        devices: List[Dict[str, Any]] = [d for d in resp['storages'] if d['type'] == type]
        return devices

    @cached(cache=TTLCache(maxsize=5, ttl=10))
    def _account_jobs(self, max_jobs: int = 100) -> Dict[str, Any]:
        '''Any user job from any workspace.'''

        url: str = f'{self.api_version}jobs-dashboard/jobs?maxResults={max_jobs}'
        resp = self._fetch_json('get', url)
        return resp

    @property
    def _account_jobs_count(self) -> int:
        '''All-time user jobs ran.'''

        resp = self._account_jobs(1)
        return resp.get('totalCount', 0)

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def _account_usage(self):
        '''Atlas and Andromeda information.'''

        warn('account_usage_stats method is experimental', UserWarning, stacklevel=2)
        url = f'{self.api_version}usage/stats'
        resp = self._fetch_json('get', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def _andromeda_utility(self, utility_name: str, preview: bool = False) -> Dict[str, Any]:
        '''Get the details of a CLI utility.
        Utility details may help a user determine which utility to run in Andromeda.
        The queuing a utility type job is a separate API call.


        :param utility_name: utility name
        :param preview: return preview version of utility, defaults to False
        '''

        url: str = f'{self.api_version}utility/{utility_name}?preview={preview}'  # TODO OE-8726
        resp = self._fetch_json('get', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=300))
    def _andromeda_utilities(
        self, version: Literal['both', 'preview', 'stable'] = 'both'
    ) -> Dict[str, Any]:
        '''Get a list of all CLI utilities that can run in Andromeda.
        The queuing a utility type job is a separate API call.

        :param version: utility version, defaults to both
        '''

        url: str = f'{self.api_version}utilities?version={version}'  # TODO OE-8726
        resp = self._fetch_json('get', url)
        return resp

    def _cache_apikey(self) -> dict:
        '''Read auth api from cache.'''

        with open(self.file_cache_auth, 'rb') as f:
            cache_auth_pickle: dict = pickle.load(f)

        return cache_auth_pickle

    def _cache_apikey_bad(self) -> bool:
        '''Check if api cache is incomplete or expired.'''

        bad: bool = False
        cache: dict = self._cache_apikey()

        # error on safety refresh before last two minutes
        now_time: float = datetime.now().timestamp() + 120

        if (
            cache.get('apikey') is None
            or cache.get('user') is None
            or cache.get('user') != self.auth_username
            or now_time > cache.get('expiration_time', 0)
        ):
            bad = True

        return bad

    def _cache_entry_delete(self, key: str) -> bool:
        '''Delete a cache entry from the cache store.

        :param key: cache key name to delete
        :return: True if deleted, False if not found
        '''

        if self.__cache.get(key) is None:
            return False

        del self.__cache[key]
        result: bool = self.__cache_save_to_file()
        return result

    def _cache_entry_get_value(self, key: str) -> Union[bool, float, int, str]:
        '''Value of cache entry.

        :param key: cache key name to retrieve
        '''

        entry: CacheEntry = self.__cache_entry_get(key)
        return entry['value']

    def _cache_entry_get_updated(self, key: str) -> float:
        '''Timestamp of when cache entry was last updated.

        :param key: cache key name to retrieve
        '''

        entry: CacheEntry = self.__cache_entry_get(key)
        return entry['updated']

    def _cache_entry_upsert(self, key: str, value: Union[bool, float, int, str]) -> bool:
        '''Add or update a cache entry to the cache store.

        :param key: cache key name to add or update
        :param value: bool, float, int, str: value to store
        :return: True if saved, False if not saved
        '''

        if type(key) != str:
            warn(f'expected key {key} of type str, but got {type(key)}', stacklevel=2)
            return False
        elif len(key) == 0:
            warn(f'key {key} cannot be an empty str', stacklevel=2)
            return False
        if type(value) not in [bool, float, int, str]:
            warn(f'value must be of type bool|float|int|str, but got {type(key)}', stacklevel=2)
            return False

        now: float = time.time()
        self.__cache[key] = {'value': value, 'updated': now}
        result: bool = self.__cache_save_to_file()
        return result

    def _cache_store(self) -> Dict[str, CacheEntry]:
        '''Return the entire cache store.'''

        return self.__cache

    def _check_apikey_expiration_time(self) -> None:
        '''Userpass key is only valid for 1 hour, ensure it is refreshed.'''

        key_bad: bool = self._cache_apikey_bad()
        if key_bad:
            self.authenticate_legacy()
        else:
            # if cache has time left on the clock, reuse cached apikey
            cache: dict = self._cache_apikey()
            now_time: float = datetime.now().timestamp() + 120
            mins_left: float = round((cache['expiration_time'] - now_time) / 60, 2)
            self.auth_apikey_mins_left = mins_left
            self.auth_apikey = cache['apikey']
            self.auth_apikey_expiry = cache['expiration_time']
            self.auth_req_header.update({'x-api-key': cache['apikey']})

    def _database_by_name(self, name: str, wildcard=False) -> List[Dict[str, Any]]:
        '''Find all database by name.

        :param name: database name
        :param wildcard: allow name to use regex case-insensitive matching, default to False
        '''

        devices: List[Dict[str, Any]] = self.__storage_type('postgres_db')
        dbs: List[Dict[str, Any]] = []

        for d in devices:
            if wildcard is True and search(name, d['name'].lower()):
                dbs.append(d)
            elif wildcard is False and name == d['name']:
                dbs.append(d)

        return dbs

    def _database_templates_by_name(self, name: str, wildcard=False) -> List[str]:
        '''Find all database template ids by case-insensitive template name.

        :param name: template name
        :param wildcard: allow name to use substr matching, default to False
        '''

        # template[name, id]
        template_map: Dict[str, str] = {t['name']: t['id'] for t in self.DATABASE_TEMPLATES_NEW}

        matches: List[str] = []
        name = name.lower()

        for t in template_map.items():
            if wildcard is False:
                # case-insensitive
                if name == t[0].lower():
                    matches.append(t[1])
            else:
                # substring case-insensitive
                if t[0].lower().find(name) > -1:
                    matches.append(t[1])

        return matches

    def _database_templates_legacy(self) -> Dict[str, Any]:
        '''Legacy available postgres schemas.'''

        warn('Deprecated, please use database_templates method', FutureWarning, stacklevel=2)
        url: str = f'{self.api_version}storage-templates'
        resp = self._fetch_json('get', url)
        return resp

    def _database_templates_legacy_by_name(self, name: str, wildcard=False) -> List[str]:
        '''Find all database template ids by case-insensitive template name.

        :param name: template name
        :param wildcard: substr matching, default to False
        '''

        matches: List[str] = []
        name = name.lower()

        for t in self.DATABASE_TEMPLATES_NAMEID.items():
            if wildcard is False:
                # case-insensitive
                if name == t[0].lower():
                    matches.append(t[1])
            else:
                # substring case-insensitive
                if t[0].lower().find(name) > -1:
                    matches.append(t[1])

        return matches

    def _fetch_json(
        self,
        method: str,
        url: str,
        json: Optional[Dict[str, Any]] = None,
        data=None,
        extra_headers: Optional[Dict[str, str]] = None,
        no_header: bool = False,
    ) -> dict:
        '''HTTP Requests to Pioneer REST API that returns a JSON response.

        :param method: http request methods
        :param url: api server endpoint
        :param json: payload in body of post call
        :param data: dictionary or list of tuples or bytes, or file-like object, defaults to None
        :param extra_headers: extend the request headers, defaults to None
        '''

        if self.auth_method_legacy is True:
            self._check_apikey_expiration_time()

        headers: Optional[Dict[str, str]] = self.auth_req_header
        if extra_headers:
            extra_headers.update(self.auth_req_header)
            headers = extra_headers
        elif no_header:
            headers = None

        resp: Response = Response()
        ret: dict = {}
        try:
            resp = request(method, url, headers=headers, json=json, data=data)
            if self._log_active:
                self.__log_http_request(resp)
            resp.raise_for_status()
            ret = resp.json()
        except HTTPError as he:
            self.api_crash_count += 1
            ret = {
                'crash': True,
                'url': url,
                'resp': resp,
                'response_body': resp.text,
                'exception': he,
            }
        except ConnectionError as ce:
            if self._domain != 'https://api.optilogic.app':
                print(f'{self._domain} != https://api.optilogic.app')
                ret = {'crash': True, 'url': url, 'exception': ce}
        except ValueError as ve:
            # JSONDecodeError
            ret = {'crash': True, 'url': url, 'exception': ve, 'text': resp.text}

        return ret

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def _ip_address_is_quick(self) -> str:
        '''Identify external ip4 address which is not as robust as ip_address_is method.'''

        url: str = 'https://api.ipify.org?format=json'
        resp: Dict[Literal['ip'], str] = self._fetch_json('get', url, no_header=True)
        return resp['ip']

    @property
    def _jobs_active(self) -> int:
        '''Total sum of jobs currently in an active state across all workspaces.'''

        active: int = 0
        states: Dict[str, int] = self._jobs_active_states()

        for s in states.values():
            active += s

        return active

    def _jobs_active_states(self) -> dict:
        '''All workspace's active job states.

        :return: {'submitted': 0, 'starting': 0, 'started': 0, 'running': 0, 'stopping': 0, 'canceling': 0}
        :rtype: dict
        '''

        active_job_status: Dict[str, int] = {}
        for s in self.JOBSTATES_ACTIVE:
            active_job_status[s] = 0

        wksp = self.account_workspaces()

        for ws in wksp['workspaces']:
            stats = self.wksp_jobs_stats(ws['name'])
            for s in active_job_status:
                active_job_status[s] += stats['statusCounts'][s]

        return active_job_status

    def _secret_exist(
        self, name: Optional[str] = None, category: Optional[str] = None, desc: Optional[str] = None
    ) -> bool:
        '''Verify secret store contain any matches.

        :param name: name of secret, defaults to None
        :param category: type of secret such as geocode, ssh, custom, defaults to None
        :param desc: substring to match a secret description, defaults to None
        :return: true if param(s) provided match any secret.
        '''

        if name is None and category is None and desc is None:
            warn(f'Must provide at least one param for name, category, or desc', stacklevel=2)
            return False

        secret_list: list = self._secret_select_all(name, category, desc)
        return True if len(secret_list) >= 1 else False

    def _secret_select_all(
        self, name: Optional[str] = None, category: Optional[str] = None, desc: Optional[str] = None
    ) -> list:
        '''Return all secrets that match criteria provided.

        :param name: name of secret, defaults to None
        :param category: type of secret such as geocode, ssh, custom, defaults to None
        :param desc: substring to match a secret description, defaults to None
        :return: list of secrets that match criteria.
        '''

        resp = self.secrets()
        params: int = 0
        params += 1 if name and len(name) > 0 else 0
        params += 1 if category and len(category) > 0 else 0
        params += 1 if desc and len(desc) > 0 else 0
        matches: list = []

        if params == 0:
            return resp['secrets'][0] if resp['count'] >= 1 else matches

        for s in resp['secrets']:
            n: str = s['name']
            t = s.get('type')
            d = s.get('description')
            if (params == 3) and (n == name) and (t == category) and (d and d.find(desc) > -1):
                matches.append(s)
            elif params == 2:
                if (name and category) and (n == name) and (t and t == category):
                    matches.append(s)
                if (name and desc) and (n == name) and (d and desc and d.find(desc) > -1):
                    matches.append(s)
                if (category and desc) and (t and t == category) and (d and d.find(desc) > -1):
                    matches.append(s)
            elif params == 1:
                if (n == name) or (t and t == category) or (d and desc and d.find(desc) > -1):
                    matches.append(s)

        return matches

    def _storage_attr(
        self, name: str, attr: Literal['annotations', 'labels', 'tags'] = 'tags'
    ) -> Dict[str, Any]:
        '''Get a attribute from a storage device.

        :param name: storage device name
        :param attr: specific storage device attribute, defaults to tags
        '''

        url: str = f'{self.api_version}storage/{name}/{attr}'
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=86400))
    def account_info(self) -> Dict[str, Any]:
        '''Get wksp and user information about the account.'''

        url: str = self.api_version + 'account'
        resp = self._fetch_json('get', url)
        if self.auth_username is None:
            self.auth_username = resp['username']
        return resp

    def account_storage_device(
        self,
        type: Literal['azure_afs', 'azure_workspace', 'onedrive', 'postgres_db'],
        name: Optional[str] = None,
    ) -> Dict[str, Any]:
        '''Get the first storage device by type or with optional name.

        :param type: storage device type
        :param name: storage device name, defaults to None
        '''

        device: dict = {}
        if self.__does_storage_exist(type=type, name=name) is True:
            devices = self.account_storage_devices()
            for d in devices['storages']:
                if d['type'] == type and name is None:
                    device = d
                    break
                elif d['type'] == type and d['name'] == name:
                    device = d
                    break

        return device

    @cached(cache=TTLCache(maxsize=1, ttl=10))
    def account_storage_devices(self) -> Dict[str, Any]:
        '''Get a list of available storage devices in an account.'''

        url: str = self.api_version + 'storage'
        resp = self._fetch_json('get', url)
        return resp

    def account_workspace_create(self, name: str, stack: str = 'Gurobi') -> dict:
        '''Create a new workspace.'''

        url: str = self.api_version + f'workspace?name={name}&stack={stack}'
        resp = self._fetch_json('post', url)
        return resp

    def account_workspace_delete(self, wksp: str) -> dict:
        '''Delete a workspace.'''

        raise NotImplementedError
        url = self.api_version + f'{wksp}/runtime'
        resp = self._fetch_json('delete', url)
        return resp

    @property
    def account_workspace_count(self) -> int:
        '''Total number of workspaces.'''

        resp = self.account_workspaces()
        return resp['count']

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def account_workspaces(self) -> dict:
        '''Get a list of available workspaces in an account.'''

        url: str = self.api_version + 'workspaces'
        resp = self._fetch_json('get', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=86400))
    def andromeda_machine_configs(self) -> Dict[str, Any]:
        '''Resource configurations and associated run rates.'''

        url: str = f'{self.api_version}jobs/resource-configs'
        resp = self._fetch_json('get', url)
        return resp

    @property
    def api_server_online(self) -> bool:
        '''Check if API service is up and running.'''

        response: Response = request('get', f'{self.api_version}ping')
        if self._log_active:
            self.__log_http_request(response)
        return True if response.status_code == 200 else False

    def authenticate_legacy(self) -> None:
        '''Legacy auth method that will create an Api Key via username and password.

        App Key is the preferred auth method for API usage
        https://optilogic.app/dashboard/#/user-account?tab=appkey

        '''

        # do a fetch, process response, then set
        url: str = self.api_version + 'refreshApiKey'
        headers: dict = {'x-user-id': self.auth_username, 'x-user-password': self.auth_userpass}

        response: Response = request('post', url, headers=headers)
        if self._log_active:
            self.__log_http_request(response)
        response.raise_for_status()
        resp: dict = response.json()

        # set instance members
        self.auth_apikey = resp['apiKey']
        self.auth_apikey_expiry = int(resp['expirationTime'])
        self.auth_apikey_mins_left = round(
            (self.auth_apikey_expiry - datetime.now().timestamp()) / 60, 2
        )
        self.auth_req_header.update({'x-api-key': resp['apiKey']})

        # cache to disk to avoid unnecessary calls to api server
        auth_pickle: Dict[str, Any] = {
            'apikey': self.auth_apikey,
            'expiration_time': self.auth_apikey_expiry,
            'user': self.auth_username,
        }

        with open(self.file_cache_auth, 'wb') as f:
            pickle.dump(auth_pickle, f)

    def database(self, name: str) -> Dict[str, Any]:
        '''User-friendly method wrapper for get storage device call.

        :param name: postgres database name
        '''

        return self.storage(name)

    @property
    def database_count(self) -> int:
        '''Quantity of a postgres databases in account.'''
        return self.storagetype_count('postgres_db')

    def database_clone(self, name: str, new_name: str) -> Dict[str, str]:
        '''Duplicate a postgres database.

        :param name: postgres database name
        :param new_name: change the db name that is to be duplicated to a new name
        '''

        url: str = f'{self.api_version}storage/{name}/clone?name={new_name}&description=Duplicated via OptiPy'
        resp: Dict[str, Any] = self._fetch_json('post', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=10))
    def database_connections(self, database_name: str) -> Dict[str, Any]:
        '''Active sessions and associated activities within a database.

        :param database_name: postgres database friendly name
        '''

        url: str = f'{self.api_version}storage/{database_name}/connections'
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def database_connections_terminate(self, database_name: str) -> Dict[str, Any]:
        '''Forcibly terminating all sessions can result in data loss or other unexpected.
        consequences if not done carefully.

        :param database_name: postgres database friendly name
        '''

        url: str = f'{self.api_version}storage/{database_name}/connections'
        time.sleep(1)
        resp: Dict[str, Any] = self._fetch_json('delete', url)
        return resp

    def database_create(
        self,
        name: str,
        desc: Optional[str] = None,
        template='anura_2_6_31_3_1_clean',
        backups=True,
        labels: Optional[Dict[str, Any]] = None,
        tags: Optional[str] = None,
    ) -> Dict[str, Any]:
        '''Create a postgres database.

        :param name: name of postgres database to create
        :param desc: describe the purpose, defaults to None
        :param template: database template id, defaults to anura_2_6_31_3_1_clean
            call `database_templates` method to list all templates available. Common template ids are:
            `empty`,
            `anura_2_6_31_3_1_clean`,
            `anura_2_7_14_clean`(For Tech Preview Users)
        :param backups: system will perform routine backups of the database, defaults to True
        :param labels: dict[str, Any]: key/value pairs, defaults to None
        :param tags: comma separated list of tags, defaults to None
        '''

        if template == 'empty':
            template = 'template1'
        if template not in self.DATABASE_TEMPLATES:
            # try to get db id by db template name
            template_ids: List[str] = self._database_templates_legacy_by_name(template)
            if len(template_ids) == 1:
                template = template_ids[0]
            # TODO OE-8737

        if self.storagename_database_exists(name):
            raise AssertionError(f'storage of name {name} already exists')

        # TODO warn per each subscription level limit
        db_count: int = self.database_count
        emp: bool = True if self.account_info()['email'].find('@optilogic.com') > 0 else False
        if emp and db_count > 90:
            warn(f'{db_count} databases, approaching limit of 100', UserWarning, stacklevel=2)

        if backups is False:
            if tags is None or len(tags) == 0:
                tags = 'no-backup'
            elif tags.endswith(',') is False:
                tags += ',no-backup'
            else:
                tags += 'no-backup'

        payload: Dict[str, Union[Dict[str, Any], None, str]] = {
            'type': 'sql',
            'template': template,
            'description': desc,
            'labels': labels,
            'tags': tags,
        }
        d: Dict[str, Union[Dict[str, Any], str]] = {k: v for k, v in payload.items() if v}

        url: str = f'{self.api_version}storage/{name}'
        resp: Dict[str, Any] = self._fetch_json('post', url, json=d)
        return resp

    def database_customizations(self, name: str, table: Optional[str] = None) -> Dict[str, Any]:
        '''List of schemas where tables and views are customized.

        :param name: postgres database name
        :param table: table name for targeted customizations or omit to retrieve all customized tables, defaults to None
        '''

        url: str = f'{self.api_version}storage/{name}/customizations'
        if table:
            url += f'?table={table}'

        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def database_delete(self, name: str) -> Dict[str, str]:
        '''User-friendly method wrapper for storage_delete call.'''
        return self.storage_delete(name)

    def database_objects(
        self, name: str, tables: bool = True, views: bool = True
    ) -> Dict[str, Any]:
        '''List of schemas with relative tables and views.

        :param name: postgres database name
        :param tables: include list of tables, defaults to True
        :param views: include list views tables, defaults to True
        '''

        url: str = f'{self.api_version}storage/{name}/db-objects'
        if not (tables and views) or (tables is False and views is False):
            query: str = '?type='
            query += 'tables,' if tables else ''
            query += 'views' if views else ''
            query = query.rstrip(',')
            url += query

        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def database_export(
        self,
        name: str,
        named: Optional[List[str]] = None,
        group: Optional[
            Literal['all', 'nonEmptyAll', 'nonEmptyTables', 'nonEmptyViews', 'tables', 'views']
        ] = None,
        query: Optional[str] = None,
        format: Literal['csv', 'xls'] = 'csv',
    ) -> Dict[str, Any]:
        '''Start a system job to perform export operation.

        set group, named, or query param to dictate what is exported to a zip csv/xls download

        :param name: postgres database name
        :param named: list[str]: table or view name(s), defaults to None
        :param group: all, nonEmptyAll, tables, views, nonEmptyTables, nonEmptyViews, defaults to None
        :param query: sql query to execute, defaults to None
        :param format: output file format csv or xls, defaults to csv
        '''

        g: Set[str] = {'all', 'nonEmptyAll', 'nonEmptyTables', 'nonEmptyViews', 'tables', 'views'}
        d: Dict[str, Any] = {}

        if named is not None:
            if len(named) == 0:
                raise ValueError(f'must provide a table/view name to export from {name} database')
            d['sourceList'] = named
        if group is not None:
            if group not in g:
                raise ValueError(f'invalid export group {group}, expecting: {g}')
            d['sourceGroup'] = group
        if query is not None:
            if len(query) < 5:
                raise AssertionError('sql query too short to be valid')
            d['sourceQuery'] = query

        url: str = f'{self.api_version}storage/{name}/db-data-export?format={format}'
        resp: Dict[str, Any] = self._fetch_json('post', url, json=d)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=86400))
    def database_schemas_anura(self) -> Dict[str, Any]:
        '''Anura data schemas and versions available for db creation.'''

        url: str = f'{self.api_version}storage/db-versions'
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def database_tables(self, name: str) -> Dict[str, Any]:
        '''List of schemas and tables.

        :param name: postgres database name
        '''

        warn('Deprecated, please use database_objects method', FutureWarning, stacklevel=2)
        url: str = f'{self.api_version}storage/{name}/tables'
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def database_tables_empty(self, name: str, tables: List[str], dry_run: bool = False) -> dict:
        '''Remove all data from specified tables.

        :param name: postgres database name
        :param tables: list[str]: tables to remove all data from
        :param dry_run: preview changes
        '''

        d: Dict[str, List[str]] = {'tables': tables}
        url: str = f'{self.api_version}storage/{name}/empty-tables?dryRun={dry_run}'
        resp: Dict[str, Any] = self._fetch_json('post', url, json=d)
        return resp

    def database_templates(self) -> Dict[str, Any]:
        '''Built db templates available for db creation.'''

        url: str = f'{self.api_version}storages/db-templates'
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def databases(self) -> List[Dict[str, Any]]:
        '''List of databases in account.'''

        dbs: List[Dict[str, Any]] = self.__storage_type('postgres_db')
        return dbs

    def ip_address_allow(self, database_name: str, ip: Optional[str] = None) -> Dict[str, str]:
        '''Grant an ip address to be whitelisted.

        :param database_name: postgres database name
        :param ip: ip address to allow through the firewall, defaults to None

        omitted ip address will use the client's ip address that is making the request
        '''

        if self.storagename_database_exists(database_name) is False:
            raise AssertionError(f'postgres database {database_name} does not exist')

        url: str = f'{self.api_version}storage/{database_name}/ip-in-firewall'
        if ip:
            url += f'?ipAddress={ip}'

        time.sleep(1)
        resp: Dict[str, str] = self._fetch_json('put', url)
        return resp

    def ip_address_allowed(self, database_name: str, ip: Optional[str] = None) -> Dict[str, Any]:
        '''Is this ip address whitelisted.

        :param database_name: postgres database name
        :param ip: ip address to allow through the firewall, defaults to None

        omitted ip address will use the client's ip address that is making the request
        '''

        if self.storagename_database_exists(database_name) is False:
            raise AssertionError(f'postgres database {database_name} does not exist')

        url: str = f'{self.api_version}storage/{database_name}/ip-in-firewall'
        if ip:
            url += f'?ipAddress={ip}'

        time.sleep(1)
        resp: Dict[str, Any] = self._fetch_json('get', url)
        return resp

    def ip_address_is(self) -> str:
        '''Identify external IP4 address if a database pre-exists.'''

        if self.storagetype_database_exists is False:
            raise AssertionError('a postgres database must pre-exist')

        return self.__ip_address_is()

    def onedrive_push(self, path: str) -> dict:
        '''Push Optilogic files to OneDrive.

        :param path: file or subtree path
        '''

        raise NotImplementedError
        url = f'{self.api_version}Studio/onedrive/push?path={path}'
        resp = self._fetch_json('post', url)
        return resp

    def secret(self, name: str) -> dict:
        '''Get confidential value.'''

        url: str = f'{self.api_version}secret/{name}'
        resp = self._fetch_json('get', url)
        return resp

    def secret_add(
        self,
        name: str,
        value: str,
        category: str = 'custom',
        desc: Optional[str] = None,
        meta: Optional[str] = None,
    ) -> dict:
        '''Set confidential key value.

        :param name: name of secret
        :param value: value of secret
        :param type: category ie geocode, ssh, custom, defaults to custom
        :param desc: description of secret, defaults to None
        :param meta: serialized dict of additional custom data, defaults to None
        '''

        if category == 'geocode':
            assert meta
            meta_dict: dict = loads(meta)
            if isinstance(meta_dict, dict) is False:
                raise TypeError(
                    "system secret type geocode expects {'isDefault': False,'provider': 'mapbox'}"
                )
            assert isinstance(meta_dict.get('isDefault'), bool)
            assert meta_dict.get('provider')
            assert isinstance(meta_dict.get('provider'), str)
            assert meta_dict.get('provider') in self.GEO_PROVIDERS

        url: str = f'{self.api_version}secret/{name}?value={value}&type={category}'
        url += f'&description={desc}' if desc else ''
        url += f'&meta={meta}' if meta else ''
        resp = self._fetch_json('post', url)
        return resp

    def secret_delete(self, name: str) -> dict:
        '''Set confidential key value.

        :param name: name of secret
        '''

        url: str = f'{self.api_version}secret/{name}'
        resp = self._fetch_json('delete', url)
        return resp

    def secret_update(
        self,
        name: str,
        new_name: Optional[str] = None,
        value: Optional[str] = None,
        type: Optional[str] = None,
        desc: Optional[str] = None,
        meta: Optional[str] = None,
    ) -> dict:
        '''Update confidential key value.

        :param name: name of secret
        :param new_name: change secret name to a new name, defaults to None
        :param value: value of secret, defaults to None
        :param type: category geocode, ssh, custom, defaults to custom
        :param desc: description of secret, defaults to None
        :param meta: serialized dict of additional custom data, defaults to None
        '''

        url: str = f'{self.api_version}secret/{name}'
        query: str = ''
        query += f'&name={new_name}' if new_name else ''
        query += f'&value={value}' if value else ''
        query += f'&type={type}' if type else ''
        query += f'&description={desc}' if desc else ''
        query += f'&meta={meta}' if meta else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('put', url)
        return resp

    @cached(cache=TTLCache(maxsize=1, ttl=60))
    def secrets(self, category: Optional[str] = None) -> dict:
        '''List of confidential key value store.

        :param type: category type ie geocode, ssh, custom, defaults to None
        '''

        url: str = (
            f'{self.api_version}secrets?type={category}'
            if category
            else f'{self.api_version}secrets'
        )
        resp = self._fetch_json('get', url)
        return resp

    def storage(self, name: str) -> Dict[str, Any]:
        '''Storage device info.

        :param name: storage device name
        '''

        url: str = f'{self.api_version}storage/{name}'
        resp = self._fetch_json('get', url)
        return resp

    def storage_delete(self, name: str) -> Dict[str, str]:
        '''Delete a storage device by name.

        :param name: storage device name
        '''

        url: str = f'{self.api_version}storage/{name}'
        response: Response = delete(url=url, headers=self.auth_req_header)
        if self._log_active:
            self.__log_http_request(response)
        response.raise_for_status()
        # returns 204 status code which has no content
        return {'result': 'success'}

    def storage_disk_create(self, name: str, type: str = 'hdd', size_gb: int = 10) -> dict:
        '''Create a new file storage device.

        :param name: name of new file storage device
        :param type: hdd or ssd
        :param size_gb: storage capacity in gigabytes, defaults to 10
        '''

        raise NotImplementedError
        # TODO check if storagename is already taken
        type = 'transaction-optimized' if type == 'hdd' else 'premium'
        url = f'{self.api_version}storage/{name}?type={type}&size={size_gb}'
        resp = self._fetch_json('post', url)
        return resp

    def storagename_exists(self, name: str) -> bool:
        '''Verify the account have any storage by name.'''
        return self.__does_storage_exist(None, name)

    def storagename_accountfiles_exists(self, name: str) -> bool:
        '''Verify the account have account file storage by name.'''
        return self.__does_storage_exist('azure_afs', name)

    def storagename_database_exists(self, name: str) -> bool:
        '''Verify the account have postgres database by name.'''
        return self.__does_storage_exist('postgres_db', name)

    def storagename_onedrive_exists(self, name: str) -> bool:
        '''Verify the account have OneDrive file storage by name.'''
        return self.__does_storage_exist('onedrive', name)

    def storagename_wkspfiles_exists(self, name: str) -> bool:
        '''Verify the account have workspace file storage by name.'''
        return self.__does_storage_exist('azure_workspace', name)

    def storagetype_count(
        self, type: Literal['azure_afs', 'azure_workspace', 'onedrive', 'postgres_db']
    ) -> int:
        '''Quantity of a storage type.'''
        count: int = len(self.__storage_type(type))
        return count

    @property
    def storagetype_accountfiles_exists(self) -> bool:
        '''Verify the account have account file storage.'''
        return self.__does_storage_exist('azure_afs')

    @property
    def storagetype_database_exists(self) -> bool:
        '''Verify the account have postgres database.'''
        return self.__does_storage_exist('postgres_db')

    @property
    def storagetype_onedrive_exists(self) -> bool:
        '''Verify the account have OneDrive file storage.'''
        return self.__does_storage_exist('onedrive')

    @property
    def storagetype_wkspfiles_exists(self) -> bool:
        '''Verify the account have workspace file storage.'''
        return self.__does_storage_exist('azure_workspace')

    @cached(cache=TTLCache(maxsize=25, ttl=300))
    def sql_connection_info(self, storage_name: str) -> dict:
        '''Get the connection information for a SQL storage item.

        :param storage_name: postgres database friendly name
        '''

        assert self.storagename_database_exists(storage_name)
        url: str = f'{self.api_version}storage/{storage_name}/connection-string'
        resp = self._fetch_json('get', url)
        return resp

    def sql_query(self, database_name: str, query: str) -> dict:
        '''Retrieve data from one or more tables.

        :param database_name: postgres database friendly name
        :param query: sql statement
        '''

        assert self.storagename_database_exists(database_name)
        query = f'/*OptiPy*/ {query}'
        d: Dict[str, str] = {'query': query}

        url: str = f'{self.api_version}storage/{database_name}/query-sql'
        resp = self._fetch_json('post', url, json=d)
        return resp

    def util_environment(
        self,
    ) -> Dict[
        Literal['job_cmd', 'job_dir', 'job_key', 'job_api', 'job_img', 'pip_ver', 'py_ver'], str
    ]:
        '''Atlas and andromeda common environment variables.'''
        return self.__env()

    def util_job_monitor(
        self,
        wksp: str,
        job_key: str,
        stop_when: Literal[
            'submitted',
            'starting',
            'started',
            'running',
            'done',
            'stopping',
            'stopped',
            'canceling',
            'cancelled',
            'error',
        ] = 'running',
        secs_max: int = 180,
    ) -> bool:
        '''Poll a job for status.

        :param wksp: workspace where relevant jobs belong to
        :param job_key: which job to monitor
        :param stop_when: return when job state matches, defaults to running
        :param secs_max: hard stop when wait time is exhausted, defaults to 180

        STOP WHEN STATES
        'submitted','starting','started','running','done','stopping','stopped','canceling','cancelled','error'

        fail-safe stop will occur when job is in a terminal state
        '''

        if stop_when not in self.JOBSTATES:
            raise ValueError(f'expecting job state in {str(self.JOBSTATES)}')

        # validate uuid4 job key case-insensitive
        valid_job_key = bool(fullmatch(self.re_uuid4, job_key, flags=2))
        if valid_job_key is False:
            raise ValueError(f'job_key is invalid uuid4 {job_key}')

        time_start: float = time.time()
        secs: float = 2.5
        retry: bool = True
        while True:
            time.sleep(secs)
            resp = self.wksp_job_status(wksp, job_key)
            if retry and resp.get('crash'):
                retry = False
                continue
            elif retry is False and resp.get('crash'):
                return False
            time_delta: float = time.time() - time_start
            if 17 < time_delta < 200:
                secs = round(time_delta * 0.15, 2)
            elif time_delta > 200:
                secs = 30
            if time_delta >= secs_max:
                return False
            elif resp['status'] in self.JOBSTATES_TERMINAL or resp['status'] == stop_when:
                return True

    def wksp_file_copy(
        self, wksp: str, file_path_src: str, file_path_dest: str, overwrite: bool = False
    ) -> dict:
        '''Copy a file within a workspace.

        :param wksp: workspace to download from
        :param file_path_src: file to copy from
        :param file_path_dest: where to copy to
        :param overwrite: overwrite existing file if exists, defaults to False
        '''

        src_path, src_filename = os.path.split(file_path_src)
        dest_path, dest_filename = os.path.split(file_path_dest)

        # if targetDirectoryPath is not provided, path will be defaulted to src directory
        url: str = f'{self.api_version }{wksp}/file/copy?sourceDirectoryPath={src_path}&sourceFilename={src_filename}'
        url += (
            f'&targetDirectoryPath={dest_path}&targetFilename={dest_filename}&overwrite={overwrite}'
        )
        resp = self._fetch_json('post', url)
        return resp

    def wksp_file_delete(self, wksp: str, file_path: str) -> dict:
        '''Delete a specific file from a workspace.

        :param wksp: workspace to delete from
        :param file_path: file to delete in wksp
        '''

        dir_path, file_name = os.path.split(file_path)
        url: str = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_file_download(self, wksp: str, file_path: str) -> str:
        '''Get a file from a specific workspace.

        :param wksp: workspace to download from
        :param file_path: file to download
        '''

        dir_path, file_name = os.path.split(file_path)
        url: str = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?op=download'
        response: Response = get(url=url, headers=self.auth_req_header)
        if self._log_active:
            self.__log_http_request(response)
        return response.text

    def wksp_file_download_status(self, wksp: str, file_path: str) -> dict:
        '''Get metadata of a file from a workspace.

        :param wksp: workspace to download from
        :param file_path: file to download
        '''

        dir_path, file_name = os.path.split(file_path)
        url: str = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?op=status'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_file_upload(
        self,
        wksp: str,
        file_path_dest: str,
        file_path_local: Optional[str] = None,
        overwrite: bool = False,
        filestr: Optional[str] = None,
    ) -> dict:
        '''Upload a file to a workspace.

        :param wksp: workspace to upload to
        :param file_path_dest: where to write file on optilogic file storage
        :param file_path_local: file to read from on local machine, defaults to None
        :param overwrite: change existing file, defaults to False
        :param filestr: alternative file contents, defaults to None
        '''

        dir_path, file_name = os.path.split(file_path_dest)
        url: str = f'{self.api_version}{wksp}/file/{dir_path}/{file_name}?overwrite={overwrite}'
        data: str = ''

        if filestr:
            data = filestr
        elif file_path_local:
            assert os.path.exists(file_path_local)
            with open(file_path_local) as file:
                data = file.read()
        elif filestr is None and file_path_local is None:
            raise ValueError('must provide a file_path_local or filestr')

        headers: Dict[str, str] = {
            'content-type': 'application/octet-stream',
            'content-length': f'{len(data)}',
        }

        if len(data) == 0:
            raise ValueError('file_path_local or filestr cannot be zero length str')

        resp = self._fetch_json('post', url, data=data, extra_headers=headers)
        return resp

    def wksp_files(self, wksp: str, filter: Optional[str] = None) -> dict:
        '''List all user files in the workspace.

        :param wksp: where your files live
        :param filter: regex str on full file path, defaults to None
        '''

        url: str = self.api_version + f'{wksp}/files'
        url += f'?filter={filter}' if filter else ''
        resp = self._fetch_json('get', url)
        return resp

    def wksp_folder_delete(self, wksp: str, dir_path: str, force: bool = False) -> dict:
        '''Delete a folder from a workspace.

        :param dir_path: folder to delete
        '''

        url: str = f'{self.api_version}{wksp}/folder/{dir_path}?recursive={str(force).lower()}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_info(self, wksp: str) -> dict:
        '''Get information about a workspace.

        :param wksp: where your files live
        '''

        url: str = self.api_version + wksp
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_back2back(
        self,
        wksp: str,
        batch: dict,
        verboseOutput: bool = False,
        resourceConfig: Optional[str] = None,
        tags: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        '''Queue one job to run many python modules in a row.

        :param batch: payload in body of post call
        :param resourceConfig: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: earmark the job record, defaults to None
        :param timeout: max job runtime in secs
        :param verboseOutput: emit python module info to stdout, defaults to False
        :param wksp: workspace scope

        INPUT DIRECTIVE
        :batch: payload to send in body of the request
        :batchItems: find python modules to execute
        :pyModulePath: absolute file path of the python module to execute
        :commandArgs: arguments to pass to associated python module
        :timeout: max run time of the associated python module
        {"batchItems":[
            {
                "pyModulePath":"/projects/My Models/Transportation/France.py",
                "commandArgs":"diesel",
                "timeout": 100
            }]
        }
        '''

        self.__batch_input_validation(batch)
        url: str = f'{self.api_version}{wksp}/jobBatch/backToBack'
        query: str = ''
        query += '&verboseOutput' if verboseOutput else ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        query += f'&timeout={timeout}' if timeout else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_job_back2back_findnrun(
        self,
        wksp: str,
        batch: dict,
        verboseOutput: bool = False,
        resourceConfig: Optional[str] = None,
        tags: Optional[str] = None,
        timeout: Optional[int] = None,
    ) -> dict:
        r'''Run many python modules back to back.

        :param batch: list of py regex search terms to discover py modules to run
        :param resourceConfig: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: earmark the job record, defaults to None
        :param timeout: max job runtime in secs, defaults to None
        :param verboseOutput: emit python module info to stdout, defaults to False
        :param wksp: workspace scope

        INPUT DIRECTIVE
        :batch: payload to send in body of the request
        :batchItems: find python modules to execute
        :pySearchTerm: regex search file paths yields python modules to execute
        :commandArgs: arguments to pass into matching python modules
        :timeout: max run time for matching python modules
        {"batchItems":[
            {"pySearchTerm":"My Models/Transportation", "commandArgs":"", "timeout": 0},
            {"pySearchTerm":"network-\d{3,}", "commandArgs":"", "timeout": 0}
        ]}
        '''

        self.__batch_input_validation(batch, find=True)
        url: str = f'{self.api_version}{wksp}/jobBatch/backToBack/searchNRun'
        query: str = ''
        query += '&verboseOutput' if verboseOutput else ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        query += f'&timeout={timeout}' if timeout else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_job_file_error(self, wksp: str, jobkey: str) -> str:
        '''Get job error file.

        :param wksp: workspace where job exists
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}?op=error'
        resp: Response = request('get', url, headers=self.auth_req_header)
        return resp.content.decode('utf-8')

    def wksp_job_file_result(self, wksp: str, jobkey: str) -> str:
        '''Get job result file.

        :param wksp: workspace where job exists
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version }{wksp}/job/{jobkey}?op=result'
        resp: Response = request('get', url, headers=self.auth_req_header)
        return resp.content.decode('utf-8')

    def wksp_job_ledger(self, wksp: str, jobkey: str, keys: Optional[str] = None) -> dict:
        '''Get records from a specified job.

        :param wksp: workspace scope
        :param jobkey: unique id
        :param keys: return only ledger records that match csv string, defaults to None
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}/ledger'
        if keys:
            url += f'?keys={keys}'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_metrics(self, wksp: str, jobkey: str) -> Dict[str, Any]:
        '''Get cpu and memory sampling of a job. The sampling frequency is one second.

        :param wksp: workspace scope
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}/metrics'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_metrics_max(self, wksp: str, jobkey: str) -> dict:
        '''Get peak cpu and memory stats of a job.

        :param wksp: workspace scope
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}/metrics/stats'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_start(
        self,
        wksp: str,
        file_path: Optional[str] = None,
        commandArgs: Optional[str] = None,
        tags: Optional[str] = None,
        timeout: Optional[int] = None,
        resourceConfig: Optional[
            Literal[
                'mini',
                '4xs',
                '3xs',
                '2xs',
                'xs',
                's',
                'm',
                'l',
                'xl',
                '2xl',
                '3xl',
                '4xl',
                'overkill',
            ]
        ] = None,
        command: Literal['run', 'run_model', 'tadpole', 'presolve', 'utility'] = 'run',
        preview_image: bool = False,
        utility_name: Optional[str] = None,
        utility_preview_version: Optional[bool] = False,
    ) -> Dict[str, Any]:
        '''Queue a job to run.

        :param wksp: workspace scope
        :param command: run, run_model, tadpole, presolve, utility, defaults to run
        :param commandArgs: positional args for py module, defaults to None
        :param file_path: python module to run
        :param preview_image: latest andromeda executable package candidate, defaults to False
        :param tags: earmark the job record, defaults to None
        :param timeout: kill job if still running after duration, defaults to None
        :param resourceConfig: mini, 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl defaults to None
        :param utility_name: name of utility to run, defaults to None
        :param utility_preview_version: use preview version of utility, defaults to False
        '''

        url: str = f'{self.api_version}{wksp}/job'
        params: Dict[str, Union[str, int, bool]] = {'command': command}

        if file_path:
            dir_path, file_name = os.path.split(file_path)
            assert file_name
            file_ext: str = os.path.splitext(file_name)[1]
            assert file_ext
            if command == 'run':
                assert file_ext == '.py'
            elif command == 'presolve':
                assert file_ext in ['.lp', '.mps']

            params['directoryPath'] = dir_path
            params['filename'] = file_name

        if commandArgs:
            params['commandArgs'] = commandArgs
        if tags:
            params['tags'] = tags
        if timeout:
            params['timeout'] = timeout
        if resourceConfig:
            params['resourceConfig'] = resourceConfig
        if preview_image:
            params['preview'] = preview_image

        if command == 'utility' and utility_name:
            params['utilityName'] = utility_name

            if utility_preview_version:
                params['utilityPreview'] = utility_preview_version

        resp = self._fetch_json('post', url, json=params)
        self._job_start_recent_key = resp['jobKey'] if resp.get('jobKey') else ''

        return resp

    def wksp_job_status(self, wksp: str, jobkey: str) -> dict:
        '''Get job status.

        :param wksp: workspace where job exists
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}?op=status'
        resp = self._fetch_json('get', url)
        return resp

    def wksp_job_stop(self, wksp: str, jobkey: str) -> dict:
        '''Stop a queued or running job.

        :param wksp: workspace where job exists
        :param jobkey: unique id
        '''

        url: str = f'{self.api_version}{wksp}/job/{jobkey}'
        resp = self._fetch_json('delete', url)
        return resp

    def wksp_jobify(
        self,
        wksp: str,
        batch: dict,
        resourceConfig: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> dict:
        '''Batch queue many jobs.

        Will create a job for each python module provided.

        :param batch: list of py modules to run and their config
        :param resourceConfig: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: earmark the job record, defaults to None
        :param wksp: workspace scope

        INPUT DIRECTIVE
        :batch: payload to send in body of the request
        :batchItems: find python modules to execute
        :pyModulePath: absolute file path of the python module to execute
        :commandArgs: arguments to pass to associated python module
        :timeout: max run time of the associated python module
        {"batchItems":[
            {
                "pyModulePath":"/projects/My Models/Transportation/France.py",
                "commandArgs":"diesel",
                "timeout": 100
            }]
        }
        '''

        self.__batch_input_validation(batch)
        url: str = f'{self.api_version}{wksp}/jobBatch/jobify'
        query: str = ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_jobify_findnrun(
        self,
        wksp: str,
        batch: dict,
        resourceConfig: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> dict:
        r'''Batch queue many jobs per search results.

        :param batch: list of py regex search terms to discover py modules to run
        :param resourceConfig: 4xs, 3xs, 2xs, xs, s, m, l, xl, 2xl, 3xl, 4xl, defaults to None
        :param tags: earmark the job record, defaults to None
        :param wksp: workspace scope

        INPUT DIRECTIVE
        :batch: payload to send in body of the request
        :batchItems: find python modules to execute
        :pySearchTerm: regex search file paths yields python modules to execute
        :commandArgs: arguments to pass into matching python modules
        :timeout: max run time for matching python modules
        {"batchItems":[
            {"pySearchTerm":"My Models/Transportation", "commandArgs":"", "timeout": 0},
            {"pySearchTerm":"network-\d{3,}", "commandArgs":"", "timeout": 0}
        ]}
        '''

        self.__batch_input_validation(batch, find=True)
        url: str = f'{self.api_version}{wksp}/jobBatch/jobify/searchNRun'
        query: str = ''
        query += f'&resourceConfig={resourceConfig}' if resourceConfig else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('post', url, json=batch)
        return resp

    def wksp_jobs(
        self,
        wksp: str,
        command: Optional[Literal['run', 'run_model', 'tadpole', 'presolve']] = None,
        history: Optional[str] = None,
        status: Optional[
            Literal[
                'submitted',
                'starting',
                'started',
                'running',
                'canceling',
                'cancelled',
                'stopping',
                'stopped',
                'done',
                'error',
            ]
        ] = None,
        runSecsMin: Optional[int] = None,
        runSecsMax: Optional[int] = None,
        tags: Optional[str] = None,
    ) -> Dict[str, Any]:
        '''List the jobs for a specific workspace.

        :param wksp: where your files live

        QUERYSTRING PARAMETERS
        :param command: run, run_model, tadpole, presolve, defaults to None
        :param history: all, or n days ago, defaults to None
        :param runSecsMax: maximum runtime in secs, defaults to None
        :param runSecsMin: minimum runtime in secs, defaults to None
        :param status: done, error, submitted, starting, running, cancelled, stopped, canceling, stopping, defaults to None
        :param tags: filter jobs where csv string matches, defaults to None
        '''

        url: str = f'{self.api_version}{wksp}/jobs'
        query: str = ''
        query += f'&command={command}' if command else ''
        query += f'&history={history}' if history else ''
        query += f'&status={status}' if status else ''
        query += f'&tags={runSecsMin}' if runSecsMin else ''
        query += f'&tags={runSecsMax}' if runSecsMax else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('get', url)
        return resp

    def wksp_jobs_stats(
        self,
        wksp: str,
        command: Optional[str] = None,
        history: Optional[str] = None,
        status: Optional[
            Literal[
                'submitted',
                'starting',
                'started',
                'running',
                'done',
                'stopping',
                'stopped',
                'canceling',
                'cancelled',
                'error',
            ]
        ] = None,
        runSecsMin: Optional[int] = None,
        runSecsMax: Optional[str] = None,
        tags: Optional[str] = None,
    ) -> dict:
        '''Get the stats for jobs for a specific workspace.

        :param wksp: where your files live

        QUERYSTRING PARAMETERS
        :param command: run, presolve, run_custom, run_default, supplychain-3echelon, estimate, accelerate, supplychain-2echelon, defaults to None
        :param history: all, n days ago, None is 7 days ago, defaults to None
        :param runSecsMax: maximum runtime in secs, defaults to None
        :param runSecsMin: minimum runtime in secs, defaults to None
        :param status: done, error, submitted, starting, running, cancelled, stopped, canceling, stopping, defaults to None
        :param tags: filter jobs where csv string matches, defaults to None
        '''

        url: str = f'{self.api_version}{wksp}/jobs'
        query: str = ''
        query += f'&command={command}' if command else ''
        query += f'&history={history}' if history else ''
        query += f'&status={status}' if status else ''
        query += f'&tags={runSecsMin}' if runSecsMin else ''
        query += f'&tags={runSecsMax}' if runSecsMax else ''
        query += f'&tags={tags}' if tags else ''
        if len(query) > 0:
            url = f"{url}?{query.lstrip('&')}"

        resp = self._fetch_json('get', url)
        return resp

    def wksp_share_file(self, wksp: str, file_path: str, targetUsers: str) -> dict:
        '''Share a specific file from a workspace to other users.

        :param wksp: workspace to copy from
        :param file_path: file to share
        :param targetUsers: csv string of usernames or email
        '''

        dir_path, file_name = os.path.split(file_path)
        url: str = f'{self.api_version}{wksp}/file/share?sourceDirectoryPath={dir_path}&sourceFilename={file_name}&targetUsers={targetUsers}'
        resp = self._fetch_json('post', url)
        return resp

    def wksp_share_folder(
        self, wksp: str, dir_path: str, targetUsers: str, includeHidden: bool = False
    ) -> dict:
        '''Share a specific subtree from a workspace to other users.

        :param wksp: workspace to copy from
        :param dir_path: subtree to share
        :param targetUsers: csv list of usernames or email
        :param includeHidden: include hidden files in folder, defaults to False
        '''

        url: str = f'{self.api_version}{wksp}/folder/share?sourceDirectoryPath={dir_path}&targetUsers={targetUsers}&includeHidden={includeHidden}'
        resp = self._fetch_json('post', url)
        return resp


if __name__ == '__main__':
    api = Api(auth_legacy=False)
    pass  # set a breakpoint here
