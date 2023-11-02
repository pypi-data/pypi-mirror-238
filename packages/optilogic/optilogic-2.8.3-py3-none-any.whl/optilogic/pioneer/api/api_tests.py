'''
Performs unit tests on the Pioneer REST Client and API.

Usage:
  api_tests.py [--authlegacy=<bool>] [--user=<str>] [--pass=<str>] [--appkey=<str>] [--wksp=<str>]
  api_tests.py (-h | --help)

Examples:
  api_tests.py --user=username --pass=secret
  api_tests.py --user=username --appkey=op_guid --wksp=sqa

Options:
  -h, --help
  -a, --authlegacy=<bool>  true for legacy username password method [default: False]
  -u, --user=<str>         API user [default:]
  -p, --pass=<str>         API password [default:]
  -k, --appkey=<str>       non expiring auth key [default:]
  -w, --wksp=<str>         wksp to use [default: Studio]
'''

import api
import os
import time
import unittest
from collections import OrderedDict
from contextlib import redirect_stderr, redirect_stdout
from dateutil.parser import parse
from datetime import date, datetime, timedelta
from difflib import Differ
from docopt import docopt
from io import StringIO
from json import dumps, loads
from numbers import Number
from random import randint
from re import fullmatch, match
from sys import platform
from threading import Thread
from typing import Any, Dict, Final, List, Literal, Tuple, TypedDict, Optional, Union
from uuid import uuid4


class Templates(TypedDict):
    '''Typing database templates data structure.'''

    baseId: int
    baselineSchemaVersion: str
    id: float
    isDefault: bool
    longDescription: str
    media: list
    name: str
    pgTemplateName: str
    schema: str
    schemaReleaseStatus: str
    shortDescription: str
    tags: list
    templateType: str
    templateVersion: str


class TestApi(unittest.TestCase):
    '''A series of Pioneer REST API unit tests.

    OVERRIDE
    docopt configuration passed into the module will override the default static members

    STATIC MEMBERS
    USERNAME    required to be issued api key
    USERPASS    required to be issued api key
    WKSP        file storage to use for IO operations
    APPKEY      non expiring authentication key
    AUTH_LEGACY true for legacy username password authentication method
    '''

    USERNAME: Optional[str] = None
    USERPASS: Optional[str] = None
    WKSP: str = 'Studio'
    APPKEY: Optional[str] = None
    AUTH_LEGACY: bool = False
    TEST_SYSTEM: bool = False

    @classmethod
    def setUpClass(cls) -> None:
        '''Execute before test methods are ran.
        Ensure cache directories and test data inputs are available in target wksp.
        '''

        cls.API = api.Api(
            auth_legacy=cls.AUTH_LEGACY,
            appkey=cls.APPKEY,
            un=cls.USERNAME,
            pw=cls.USERPASS,
            test_system=cls.TEST_SYSTEM,
        )
        print(cls.API._domain)
        cls.__jobkey_quick: str = ''
        cls.API._log_active = True

        # directory references
        cls.dir_local_current: str = os.path.dirname(__file__)
        cls.dir_testdata_local: str = os.path.join(cls.dir_local_current, 'quick_tests')
        assert os.path.exists(cls.dir_testdata_local)
        assert len(os.listdir(cls.dir_testdata_local)) >= 1
        cls.dir_testdata_remote: str = 'quick_tests'
        cls.files_testdata_local: list[str] = []
        cls.files_testdata_remote: list[str] = []
        cls.py_sleep: str = ''
        cls.py_bash: str = ''
        cls.py_quick: str = ''
        cls.py_sidecar: str = ''

        # get all directories from wksp
        resp = cls.API.wksp_files(cls.WKSP, '/quick_tests/')
        files_remote: list[str] = [f['filePath'] for f in resp['files']]

        # comb over local test data and map to destination file structure
        for f in os.listdir(cls.dir_testdata_local):
            local: str = os.path.join(cls.dir_testdata_local, f)
            if os.path.isfile(local) is False:
                continue
            elif os.path.getsize(local) == 0:
                continue
            dest: str = os.path.join(cls.dir_testdata_remote, f)
            cls.files_testdata_local.append(local)
            cls.files_testdata_remote.append(dest)
            if dest.endswith('sleep.py'):
                cls.py_sleep = dest
            elif dest.endswith('quick.py'):
                cls.py_quick = dest
            elif dest.endswith('bash.py'):
                cls.py_bash = dest
            elif dest.endswith('sidecar.py'):
                cls.py_sidecar = dest

            # upload local test data to destination
            for idx, local in enumerate(cls.files_testdata_local):
                dest = cls.files_testdata_remote[idx]
            res: list[str] = [f for f in files_remote if dest in f]
            if len(res) == 0:
                print(f'uploading {dest}')
                resp = cls.API.wksp_file_upload(
                    cls.WKSP, file_path_dest=dest, file_path_local=local
                )

    @classmethod
    def tearDownClass(cls) -> None:
        '''Execute after all tests have ran.'''

        dbs: List[Dict[str, Any]] = cls.API._database_by_name(r'unittest.+\d{13}', wildcard=True)
        for d in dbs:
            print(f"Deleting database dust bunny {d['name']}")
            cls.API.database_delete(d['name'])

        cache_store = cls.API._cache_store()
        keys_to_delete: list[str] = [key for key in cache_store.keys() if 'cache_' in key]
        for key in keys_to_delete:
            cls.API._cache_entry_delete(key)

    def compare_words(self, str1: str, str2: str, echo: bool = False) -> List[str]:
        '''Identify any word differences between two strings.

        :param str1: The first string for comparison.
        :param str2: The second string for comparison.
        :param echo: True to print diffs to stdout.
        '''

        if not isinstance(str1, str):
            raise TypeError(f'str1 must be a string, but got {type(str1)}')
        if not isinstance(str2, str):
            raise TypeError(f'str2 must be a string, but got {type(str2)}')

        # Split the input strings by spaces to compare words
        words1: List[str] = str1.split()
        words2: List[str] = str2.split()

        # Compare the words
        differ = Differ()
        diff = list(differ.compare(words1, words2))
        diffs: List[str] = []
        char_position: int = 0

        for i, line in enumerate(diff):
            if line.startswith(('+', '-')):
                # Extract the plus and minus symbol from the word
                symbol, word = line[:1], line[2:]

                # Minus is unique to sequence 1, plus is unique to sequence 2
                word_list = words1 if symbol == '-' else words2

                # BUG OE-8786 index will return first match found
                word_index = word_list.index(word) if word in word_list else None
                if word_index is None:
                    continue

                # Get two words before and after the difference
                start_idx = max(0, word_index - 2)
                end_idx = min(len(word_list), word_index + 3)
                context_words = word_list[start_idx:end_idx]
                context = ' '.join(context_words)
                char_position = ' '.join(word_list).find(context)
                diffs.append(f'{symbol}{context} (position: {char_position})')
                if echo:
                    print(f'{symbol}{context} (position: {char_position})')

        return diffs

    def database_ensure_exist(self, name: str = 'pg_unittest') -> None:
        '''Database must exist for db unit tests.'''

        # cache is for 10 seconds
        exists: bool = self.API.storagename_database_exists(name)
        if exists:
            resp: Dict[str, Any] = self.API.storage(name)
            assert resp.get('crash') is None
        else:
            self.API.database_create(name, desc='common db for unit tests', backups=False)

    def databases_utilized_by_unittest(self, all: bool = False) -> List[Dict[str, Any]]:
        '''Which databases are used by unit tests.

        :param all: bool, False returns only temporary unittest databases
        '''

        dbs: List[Dict[str, Any]] = []
        if all is False:
            dbs = self.API._database_by_name(r'unittest.+\d{13}', wildcard=True)
        else:
            dbs = self.API._database_by_name('unittest', wildcard=True)
        return dbs

    def date_isoformat(self, date_str: str) -> bool:
        '''Verify date string isoformat.'''

        d: date
        try:
            d = date.fromisoformat(date_str)
            return isinstance(d, date)
        except ValueError:
            return False

    def deserialize_pip_output(self, std_out: str) -> List[Dict[str, Any]]:
        '''Deserialization of `pip list --format json` from standard output.'''

        if len(std_out) < 58:
            raise ValueError(f'len of std_out is {std_out}, too short')
        # remove cli earmarking from std_out
        m = match(r"(.|\n)+format\sjson'\}\n", std_out)
        if m is None:
            raise ValueError(f'could not match std_out')
        return loads(std_out.lstrip(m.group()))

    def job_prereq(self) -> None:
        '''For running test methods in isolation.'''

        resp = self.API.wksp_job_start(
            self.WKSP, self.py_quick, tags='unittest_prereq', resourceConfig='mini'
        )
        self.assertEqual(resp['result'], 'success')
        self.__jobkey_quick = resp['jobKey']
        # BUG ledger and metrics should be immediately available when job is running
        res: bool = self.API.util_job_monitor(self.WKSP, resp['jobKey'], stop_when='done')
        self.assertTrue(res)

    def storage_common(self, d: Dict[str, Any]) -> None:
        '''Device attributes expected across afs, wksp, onedrive, and postgres storage devices.'''

        self.assertIsInstance(d['annotations'], dict)
        self.assertIsInstance(d['bytesUsed'], int)
        self.assertGreater(d['bytesUsed'], -1)
        self.assertIsInstance(d['created'], int)
        self.assertTrue(d['description'] is None or isinstance(d['description'], str))
        self.assertIsInstance(d['id'], str)
        self.assertIsInstance(d['labels'], dict)
        self.assertTrue(d['lockoutReason'] is None or isinstance(d['lockoutReason'], str))
        self.assertIsInstance(d['name'], str)
        self.assertIsInstance(d['notes'], str)
        self.assertIsInstance(d['shortcuts'], list)
        if len(d['shortcuts']) >= 1:
            for s in d['shortcuts']:
                self.assertIsInstance(s['driveId'], str)
                self.assertIsInstance(s['driveName'], str)
                self.assertIsInstance(s['id'], str)
                self.assertIsInstance(s['name'], str)
                self.assertIsInstance(s['path'], str)
                self.assertIsInstance(s['type'], str)
        self.assertIsInstance(d['tags'], str)
        self.assertIsInstance(d['type'], str)
        self.assertIsInstance(d['updated'], int)

        # DEBUG ONLY remove common keys
        KEYS = (
            'annotations',
            'created',
            'description',
            'id',
            'labels',
            'lockoutReason',
            'name',
            'notes',
            'secureFields',
            'shortcuts',
            'tags',
            'updated',
            'userId',
        )

        # for k in tuple(d.keys()):
        #    if k in KEYS:
        #        d.pop(k)

    def storage_azure_afs(self, d: Dict[str, Any]) -> None:
        '''SSD device attributes for get device and devices.'''

        self.storage_common(d)
        self.assertIsInstance(d['capacity'], int)
        self.assertEqual(d['capacity'], 100)
        self.assertIsInstance(d['internal'], bool)
        self.assertTrue(d['internal'])
        self.assertIsInstance(d['tier'], str)
        self.assertEqual(d['tier'], 'Premium')

    def storage_azure_workspace(self, d: Dict[str, Any]) -> None:
        '''Workspace device attributes for get device and devices.'''

        self.storage_common(d)
        self.assertIsInstance(d['capacity'], int)
        self.assertTrue(4 <= d['capacity'] <= 512)  # default is 4 but some are custom
        self.assertIsInstance(d['internal'], bool)
        self.assertIsInstance(d['tier'], str)
        self.assertEqual(d['tier'], 'TransactionOptimized')
        self.assertIsInstance(d['workspaceKey'], str)
        self.assertEqual(len(d['workspaceKey']), 25)
        self.assertTrue(d['workspaceKey'].startswith('workspace'))

    def storage_database(self, d: Dict[str, Any]) -> None:
        '''Database attributes for get device and devices.'''

        self.storage_common(d)
        self.assertIsInstance(d['bytesUsedLastUpdated'], int)
        self.assertIsInstance(d['dbname'], str)
        self.assertIsInstance(d['defaultSchema'], str)
        self.assertIsInstance(d['host'], str)
        self.assertIsInstance(d['port'], int)
        self.assertIsInstance(d['schemaStatus'], str)
        self.assertTrue(d['schemaStatus'] in ('error', 'invalid', 'valid'))  # BUG OE-8954
        self.assertIsInstance(d['schemaStatusLastUpdated'], Number)
        self.assertIsInstance(d['schemaVersion'], str)
        self.assertIsInstance(d['user'], str)

        # empty pg database vs anura schema
        if d['defaultSchema'].startswith('anura_2_'):
            self.assertRegex(d['schemaVersion'], r'2\.[4-9]\.\d+')
            self.assertIsInstance(d['schemaReleaseStatus'], str)
            release_status: bool = (
                d['schemaReleaseStatus'].startswith('stable')
                or d['schemaReleaseStatus'].startswith('preview')
                or d['schemaReleaseStatus'].startswith('release candidate')
            )
            self.assertTrue(release_status)
            self.assertIsInstance(d['schemaStatusLastValidated'], Number)
        else:
            self.assertIn(d['defaultSchema'], ('"$user"', 'public'))
            self.assertTrue(len(d['schemaVersion']) == 0)

    def storage_onedrive(self, d: dict) -> None:
        '''Onedrive storage attributes for get device and devices.'''

        self.storage_common(d)

        self.assertIsInstance(d['authenticated'], int)
        dt: datetime = datetime.fromtimestamp(d['authenticated'] / 1000)
        self.assertGreaterEqual(dt.year, 2020)

        # connect is not in get devices call due to real time performance
        # self.assertIsInstance(d['connected'], bool)
        self.assertIsInstance(d['capacity'], int)

        self.assertIsInstance(d['homeAccountId'], str)
        self.assertIsInstance(d['internal'], bool)

        self.assertIsInstance(d['username'], str)

    def test_000_init_api_version_bad(self) -> None:
        '''Recover from a bad api version provided.'''

        bad_version: int = 99

        with redirect_stderr(StringIO()) as err:
            a = api.Api(auth_legacy=self.AUTH_LEGACY, version=bad_version, ut=True)
            output: str = err.getvalue().strip()

        self.assertGreater(output.find(f'API version {bad_version} not supported'), -1)
        self.assertRegex(a.api_version, r'app/v0/')

    def test_000_init_password_missing(self) -> None:
        '''Get password uses a secret stream and input will not echo.'''

        if platform != 'linux':
            self.skipTest('only linux has timed inputs')

        with redirect_stdout(StringIO()) as out:
            try:
                a = api.Api(auth_legacy=True, un=self.USERNAME, ut=True)
            except (EOFError, TimeoutError):
                pass
            output: str = out.getvalue().strip()

        self.assertEqual(output.find('REQUIRED API User Password'), -1)

    def test_000_prereq(self) -> None:
        '''Ensure job data is available to test against.'''

        resp = self.API.wksp_job_start(
            self.WKSP, self.py_quick, tags='unittest_preseed', resourceConfig='mini'
        )
        self.assertEqual(resp['result'], 'success')
        self.__jobkey_quick = resp['jobKey']
        stime: float = time.time()
        print('Pre-seeding by running a new job')
        res: bool = self.API.util_job_monitor(
            self.WKSP, resp['jobKey'], stop_when='done', secs_max=300
        )
        delta: float = time.time() - stime
        print(f'Job completed {res}, time spent {delta}')
        self.assertLessEqual(delta, 240.0)

    def test_auth_apikey(self) -> None:
        '''Api key is required for all api calls with legacy authentication.'''

        self.assertIsNotNone(
            self.API.auth_apikey
        ) if self.API.auth_method_legacy else self.assertIsNone(self.API.auth_apikey)

    def test_auth_apikey_expiration(self) -> None:
        '''Ensure api key is refreshed and not expired.'''

        if self.API.auth_method_legacy:
            self.assertGreater(self.API.auth_apikey_expiry, datetime.now().timestamp())
        else:
            self.assertEqual(self.API.auth_apikey_expiry, 0)

    def test_auth_header(self) -> None:
        '''Request header must have valid apikey or appkey.'''

        if self.API.auth_method_legacy:
            self.assertEqual(self.API.auth_req_header['x-api-key'], self.API.auth_apikey)
        else:
            self.assertEqual(self.API.auth_req_header['x-app-key'], self.API.auth_appkey)

    def test_account_info(self) -> None:
        '''Account properties.'''

        resp = self.API.account_info()
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 9)

        self.assertIsInstance(resp['created'], int)
        dt: datetime = datetime.fromtimestamp(resp['created'] / 1000)
        self.assertGreaterEqual(dt.year, 2019)
        now: datetime = datetime.utcnow()
        self.assertLessEqual(dt.year, now.year)

        self.assertIsInstance(resp['email'], str)
        self.assertIsInstance(resp['name'], str)
        self.assertGreaterEqual(len(resp['name']), 3)

        self.assertIsInstance(resp['subscriptionName'], str)
        self.assertIn(resp['subscriptionName'], ('Standard', 'Professional', 'empcustom'))

        self.assertIsInstance(resp['limits'], dict)
        self.assertEqual(len(resp['limits']), 3)
        self.assertIsInstance(resp['limits']['concurrentJobs'], int)
        self.assertIsInstance(resp['limits']['databaseCount'], int)
        self.assertIsInstance(resp['limits']['fileStorageGb'], int)
        self.assertEqual(resp['limits']['fileStorageGb'], 500)  # max possible

        self.assertIsInstance(resp['roles'], dict)
        self.assertEqual(len(resp['roles']), 1)
        self.assertIsInstance(resp['roles']['api'], list)
        roles = (
            'api-access',
            'api-internal',
            'api-beast',
            'api-share',
            'api-proxy',
            'user-initiated-db-upgrade',
            'preview-schema',
            'pioneer-team',
        )
        for r in resp['roles']['api']:
            self.assertIsInstance(r, str)
            self.assertIn(r, roles)

        self.assertIsInstance(resp['usage'], dict)
        self.assertEqual(len(resp['usage']), 5)
        self.assertIsInstance(resp['usage']['databaseCount'], int)
        self.assertIsInstance(resp['usage']['databaseStorageBytes'], int)
        dbs_total_bytes: int = resp['usage']['databaseStorageBytes']
        self.assertIsInstance(resp['usage']['fileStorageCount'], int)
        self.assertIsInstance(resp['usage']['fileStorageGb'], int)
        self.assertIsInstance(resp['usage']['workspaceCount'], int)
        self.assertGreaterEqual(resp['usage']['databaseCount'], 0)
        self.assertLessEqual(resp['usage']['databaseCount'], resp['limits']['databaseCount'])
        self.assertTrue(0 < resp['usage']['fileStorageCount'] < 10)
        self.assertTrue(0 < resp['usage']['workspaceCount'] < 10)
        self.assertLessEqual(
            resp['usage']['fileStorageGb'],
            resp['limits']['fileStorageGb'] * resp['usage']['fileStorageCount'],
        )

        self.assertIsInstance(resp['username'], str)
        if self.API.auth_username:
            self.assertEqual(resp['username'], self.API.auth_username)

        dbs: List[Dict[str, Any]] = self.API.databases()
        total: int = 0
        for db in dbs:
            total += db['bytesUsed']

        self.assertEqual(dbs_total_bytes, total)

        # limits per rate plan
        if resp['subscriptionName'] == 'Standard':
            self.assertEqual(resp['limits']['concurrentJobs'], 3)
            self.assertEqual(resp['limits']['databaseCount'], 25)
        elif resp['subscriptionName'] == 'Professional':
            self.assertEqual(resp['limits']['concurrentJobs'], 10)
            self.assertEqual(resp['limits']['databaseCount'], 100)
        elif resp['subscriptionName'] == 'empcustom':
            self.assertEqual(resp['limits']['concurrentJobs'], 50)
            self.assertEqual(resp['limits']['databaseCount'], 100)
            self.assertGreater(resp['email'].find('@optilogic.com'), -1)

    def test_account_jobs(self) -> None:
        '''User jobs from any workspace.'''

        job_count: int = 50
        resp = self.API._account_jobs(max_jobs=job_count)
        self.assertIsInstance(resp['jobs'], list)
        self.assertIsInstance(resp['result'], str)
        self.assertIsInstance(resp['subsetCount'], int)
        self.assertIsInstance(resp['totalCount'], int)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['subsetCount'], job_count)
        for job in resp['jobs']:
            self.assertIsInstance(job['canHaveResult'], bool)
            self.assertIsInstance(job['jobInfo'], dict)
            self.assertIsInstance(job['jobInfo']['command'], str)
            if job['jobInfo']['command'] != 'run_custom':
                self.assertIsInstance(job['jobInfo']['directoryPath'], str)
                self.assertIsInstance(job['jobInfo']['filename'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig'], dict)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['cpu'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['name'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['ram'], str)
            self.assertIsInstance(job['jobInfo']['resourceConfig']['run_rate'], Number)
            self.assertIsInstance(job['jobInfo']['tags'], str)
            self.assertIsInstance(int(job['jobInfo']['timeout']), int)  # BUG OE-6710 str or int
            self.assertIsInstance(job['jobInfo']['workspace'], str)
            self.assertIsInstance(job['jobKey'], str)
            self.assertIsInstance(job['runRate'], Number)
            self.assertIsInstance(job['status'], str)
            self.assertIsInstance(job['submittedDatetime'], str)
            self.assertIsInstance(job['submittedTimeStamp'], int)

            if job['status'] in self.API.JOBSTATES_TERMINAL_RUNTIME:
                self.assertTrue(job['canHaveResult'])
                self.assertIsInstance(job['billedTime'], str)
                self.assertIsInstance(job['billedTimeMs'], Number)
                self.assertIsInstance(job['endDatetime'], str)
                self.assertIsInstance(job['endTimeStamp'], int)
                self.assertIsInstance(job['runTime'], str)
                self.assertIsInstance(job['runTimeMs'], int)
                self.assertIsInstance(job['startDatetime'], str)
                self.assertIsInstance(job['startTimeStamp'], int)
            else:
                with self.subTest():
                    self.assertIsNone(job['startDatetime'])
                    self.assertIsNone(job['endDatetime'])
                    # self.assertFalse(job['canHaveResult'])  # BUG 6710

    def test_account_jobs_active(self) -> None:
        '''Compare active account jobs count to all active wksp jobs.'''

        start_new_job: bool = bool(randint(0, 1))
        if start_new_job:
            self.API.wksp_job_start(
                self.WKSP, self.py_sleep, tags='unittest_jobs_active', resourceConfig='mini'
            )

        active_account: int = 0
        resp = self.API._account_jobs(
            max_jobs=200
        )  # BUG submitted counts as active therefore must account for excessive submitted jobs
        for job in resp['jobs']:
            if job['status'] in self.API.JOBSTATES_ACTIVE:
                active_account += 1

        active_wksp: int = self.API._jobs_active
        self.assertEqual(active_account, active_wksp)
        if start_new_job:
            self.assertGreater(active_account, 0)
            self.assertGreater(active_wksp, 0)

    def test_account_storage_devices(self) -> None:
        '''Get a list of available storage devices in an account.'''

        resp = self.API.account_storage_devices()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storages'], list)
        with self.subTest():
            for device in resp['storages']:
                d = OrderedDict(sorted(device.items()))
                if d['type'] == 'azure_afs':
                    self.assertEqual(len(d), 16)
                    self.storage_azure_afs(d)
                if d['type'] == 'azure_workspace':
                    self.assertEqual(len(d), 17)
                    self.storage_azure_workspace(d)
                elif d['type'] == 'onedrive':
                    self.assertEqual(len(d), 18)
                    self.storage_onedrive(d)
                elif d['type'] == 'postgres_db':
                    self.assertEqual(len(d), 24)
                    self.storage_database(d)

    def test_account_usage(self) -> None:
        '''Atlas and andromeda information.'''

        resp = self.API._account_usage()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['andromeda'], dict)
        self.assertIsInstance(resp['atlas'], dict)
        self.assertEqual(len(resp), 3)

        self.assertIsInstance(resp['andromeda']['jobsLastThirty'], int)
        self.assertIsInstance(resp['andromeda']['jobsMostRecent'], int)
        self.assertIsInstance(resp['andromeda']['jobsTimeLastThirty'], float)
        self.assertIsInstance(resp['andromeda']['jobsTimeTotal'], float)
        self.assertIsInstance(resp['andromeda']['jobsTotal'], int)
        self.assertIsInstance(resp['andromeda']['periodHours'], Number)
        self.assertEqual(len(resp['andromeda']), 6)
        self.assertEqual(len(str(resp['andromeda']['jobsMostRecent'])), 13)
        dt: datetime = datetime.fromtimestamp(resp['andromeda']['jobsMostRecent'] / 1000)
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)

        self.assertIsInstance(resp['atlas'], dict)
        if (
            self.API._domain != 'https://api.optilogic.app'
            and resp['atlas'].get('lastLogin') is None
        ):
            # BUG OE-7432
            self.assertEqual(len(resp['atlas']), 3)
        else:
            self.assertEqual(len(resp['atlas']), 4)
            self.assertIsInstance(resp['atlas']['lastLogin'], int)
            self.assertEqual(len(str(resp['atlas']['lastLogin'])), 13)
            dt: datetime = datetime.fromtimestamp(resp['atlas']['lastLogin'] / 1000)
            self.assertIsInstance(dt, datetime)
        self.assertIsInstance(resp['atlas']['periodHours'], Number)
        self.assertIsInstance(resp['atlas']['task'], dict)
        self.assertIsInstance(resp['atlas']['workspaceCount'], int)
        self.assertIsInstance(resp['atlas']['task'], dict)
        self.assertIsInstance(resp['atlas']['task']['durationCurrentWeek'], Number)
        self.assertIsInstance(resp['atlas']['task']['durationLastThirty'], Number)
        self.assertIsInstance(resp['atlas']['task']['durationTotal'], float)
        self.assertIsInstance(resp['atlas']['task']['lastDuration'], float)
        self.assertIsInstance(resp['atlas']['task']['lastRunStart'], int)
        self.assertIsInstance(resp['atlas']['task']['runCurrentWeek'], int)
        self.assertIsInstance(resp['atlas']['task']['runlastThirty'], int)
        self.assertIsInstance(resp['atlas']['task']['runTotal'], int)
        self.assertEqual(len(resp['atlas']['task']), 8)
        self.assertEqual(len(str(resp['atlas']['task']['lastRunStart'])), 13)
        dt: datetime = datetime.fromtimestamp(resp['atlas']['task']['lastRunStart'] / 1000)
        self.assertIsInstance(dt, datetime)

    def test_account_workspaces(self) -> None:
        '''Check all workspaces properties.'''

        resp = self.API.account_workspaces()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)

        wksp_exists: bool = False
        for wksp in resp['workspaces']:
            self.assertRegex(wksp['name'], '^[\\w-]+$')
            self.assertEqual(len(wksp['key']), 25)
            self.assertIn(wksp['stack'], ['Optilogic', 'Gurobi'])
            self.assertIn(wksp['status'], ['STARTING', 'RUNNING', 'STOPPING', 'STOPPED'])
            self.assertRegex(wksp['status'], '\\w{3,}')

            # https://en.wikipedia.org/wiki/ISO_8601
            dt_wksp_creation: datetime = parse(wksp['createdon'])
            self.assertGreaterEqual(dt_wksp_creation.year, 2020)

            if wksp['name'] == self.WKSP:
                wksp_exists = True

        self.assertTrue(wksp_exists)

    def test_account_workspace_count(self) -> None:
        '''Account info and workspaces both return wksp count.'''

        resp = self.API.account_info()
        ws_count: int = self.API.account_workspace_count
        self.assertEqual(resp['usage']['workspaceCount'], ws_count)

    @unittest.skip('cant delete a wksp atm')
    def test_account_workspace_create(self) -> None:
        '''Creating a new workspace.'''

        resp = self.API.account_workspace_create('delete_me')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], 'delete_me')
        self.assertEqual(resp['stack'], 'Gurobi')

    def test_account_workspace_create_crash(self) -> None:
        '''Expected to not create the same workspace twice.'''

        resp = self.API.account_workspace_create('Studio')
        self.assertEqual(resp['crash'], True)
        self.assertEqual(resp['exception'].response.status_code, 400)

    def test_account_workspace_delete(self):
        '''Deleting a newly created workspace.'''

        with self.assertRaises(NotImplementedError):
            resp = self.API.account_workspace_delete('delete_me')

    def test_andromeda_configs(self) -> None:
        '''Memory and CPU configurations for Andromeda.'''

        NAMES = (
            'mini',
            '4XS',
            '3XS',
            '2XS',
            'XS',
            'S',
            'M',
            'L',
            'XL',
            '2XL',
            '3XL',
            '4XL',
            'overkill',
        )
        resp: Dict[str, Any] = self.API.andromeda_machine_configs()
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 4)
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['defaultConfigName'], str)
        self.assertIsInstance(resp['resourceConfigs'], list)

        self.assertEqual(resp['count'], 13)
        self.assertEqual(resp['defaultConfigName'], '3XS')
        self.assertEqual(len(resp['resourceConfigs']), 13)

        for rc in resp['resourceConfigs']:
            self.assertIsInstance(rc, dict)
            self.assertEqual(len(rc.keys()), 5)
            self.assertTrue(rc.get('name'))
            self.assertTrue(rc.get('description'))
            self.assertTrue(rc.get('cpu'))
            self.assertTrue(rc.get('ram'))
            self.assertTrue(rc.get('runRate'))

            self.assertIsInstance(rc['name'], str)
            self.assertIsInstance(rc['description'], str)
            self.assertIsInstance(rc['cpu'], Number)
            self.assertIsInstance(rc['ram'], Number)
            self.assertIsInstance(rc['runRate'], Number)

            self.assertIn(rc['name'], NAMES)
            self.assertRegex((rc['description']), r'(\d{1,2}\sCPU).+(\d{1,3}[GM]b RAM)')

    def test_andromeda_utilities(self) -> None:
        '''Get a list of all CLI utilities that can run in Andromeda.'''

        resp: Dict[str, Any] = self.API._andromeda_utilities()
        self.assertIsInstance(resp, dict)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        # TODO OE-8726 specific utilities are to be added
        self.assertGreater(resp['count'], 0)
        self.assertIsInstance(resp['utilities'], list)
        for d in resp['utilities']:
            self.assertIsInstance(d, dict)
            self.assertEqual(len(d.keys()), 5)
            self.assertIsInstance(d['name'], str)
            self.assertIsInstance(d['description'], str)
            self.assertIsInstance(d['version'], str)
            self.assertIsInstance(d['stable'], bool)
            self.assertIsInstance(d['hasParameters'], bool)

    def test_andromeda_utility(self) -> None:
        '''Get details of a CLI utility.'''

        utils: Dict[str, Any] = self.API._andromeda_utilities()
        item: int = randint(0, len(utils['utilities']) - 1)
        util_name: str = utils['utilities'][item]['name']
        util_preview: bool = True if utils['utilities'][item]['stable'] is False else False

        # TODO OE-8726 test a specific utility
        resp: Dict[str, Any] = self.API._andromeda_utility(util_name, util_preview)
        self.assertIsInstance(resp, dict)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 6)
        self.assertIsInstance(resp['name'], str)
        self.assertIsInstance(resp['description'], str)
        self.assertIsInstance(resp['version'], str)
        self.assertIsInstance(resp['stable'], bool)
        self.assertIsInstance(resp['parameters'], list)
        for d in resp['parameters']:
            # TODO OE-8726 a specific utility will have specific parameters
            self.assertIsInstance(d, dict)
            self.assertTrue(all(isinstance(k, str) for k in d.keys()))

    def test_andromeda_utility_run(self) -> None:
        '''Run a named CLI utility in Andromeda.'''

        utils: Dict[str, Any] = self.API._andromeda_utilities()
        item: int = randint(0, len(utils['utilities']) - 1)
        util_name: str = utils['utilities'][item]['name']
        util_preview: bool = True if utils['utilities'][item]['stable'] is False else False
        cmd = 'utility'
        tag = 'unittest_utility'
        size = '3xs'
        secs = 60

        # TODO OE-8726 commandArgs is CLI mechanism for input parameters to py module
        resp: Dict[str, Any] = self.API.wksp_job_start(
            wksp=self.WKSP,
            command=cmd,
            utility_name=util_name,
            utility_preview_version=util_preview,
            tags='unittest_utility',
            resourceConfig=size,  # TODO OE-8732 casing is inconsistent
            timeout=secs,
        )

        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(resp['jobInfo']['command'], cmd)
        self.assertTrue(tag in resp['jobInfo']['tags'])
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'].lower(), size)
        self.assertEqual(resp['jobInfo']['timeout'], secs)  # TODO OE-8733 not respected

    def test_andromeda_utility_run_bad_utility_name(self) -> None:
        '''Attempt to run a CLI utility that does not exist in Andromeda.'''

        resp: Dict[str, Any] = self.API.wksp_job_start(
            wksp=self.WKSP,
            command='utility',
            utility_name='does_not_exist',
        )
        self.assertIsInstance(resp, dict)
        self.assertEqual(resp['crash'], True)
        self.assertEqual(resp['resp'].status_code, 404)
        self.assertEqual(resp['exception'].response.reason, 'Not Found')
        err: Dict[str, str] = loads(resp['response_body'])
        self.assertEqual(err['error'], 'Utility name and/or version not found')

    def test_andromeda_utility_run_cant_finish(self) -> None:
        '''Run a CLI utility that is intentionally cut short.'''

        utils: Dict[str, Any] = self.API._andromeda_utilities()
        item: int = randint(0, len(utils['utilities']) - 1)
        util_name: str = utils['utilities'][item]['name']
        util_preview: bool = True if utils['utilities'][item]['stable'] is False else False
        cmd = 'utility'
        tag = 'unittest_utility'
        size = 'mini'
        secs = 1

        resp: Dict[str, Any] = self.API.wksp_job_start(
            wksp=self.WKSP,
            command=cmd,
            utility_name=util_name,
            utility_preview_version=util_preview,
            tags=tag,
            resourceConfig=size,
            timeout=secs,
        )

        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(resp['jobInfo']['command'], cmd)
        self.assertTrue(tag in resp['jobInfo']['tags'])
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], size)

        # add cache entry to be verified run results later
        k = 'utility_run_incomplete'
        added: bool = self.API._cache_entry_upsert(k, resp['jobKey'])
        self.assertTrue(added)

    def test_andromeda_utility_verify_cant_finish(self) -> None:
        '''Utility run was intentionally cut short or may not have enough memory.'''

        k = 'utility_run_incomplete'
        timestamp: float = self.API._cache_entry_get_updated(k)
        now: float = time.time()
        if now - timestamp > 300.0:
            self.skipTest('utility has not been run in the last 60 seconds')

        # TODO OE-8726 verify utility run was cut short
        # timeout cut it short or ran out of memory

    def test_api_server_online(self) -> None:
        '''Check if api service is up and running.'''

        self.assertTrue(self.API.api_server_online)

    def test_api_version(self) -> None:
        '''Only version zero is supported.'''

        self.assertTrue(self.API.api_version.endswith('v0/'))

    def test_cache_store_add(self) -> None:
        '''Add a cache entry to cache store.'''

        ns: int = time.perf_counter_ns()
        k = f'cache_{ns}'

        # assert cache entry does not exist
        timestamp: float = self.API._cache_entry_get_updated(k)
        self.assertIsInstance(timestamp, float)
        self.assertEqual(timestamp, -1.0)

        # add cache entry
        added: bool = self.API._cache_entry_upsert(k, ns)
        self.assertTrue(added)

        # assert key type is correct
        val = self.API._cache_entry_get_value(k)
        self.assertIsInstance(val, int)
        self.assertEqual(val, ns)

        # clean up and remove unit tests cache entries!
        self.API._cache_entry_delete(k)

    def test_cache_store_update(self) -> None:
        '''Update a cache entry in cache store.'''

        ns: int = time.perf_counter_ns()
        k = f'cache_{ns}'
        v = True

        # add cache entry
        added_time: float = time.time()
        added: bool = self.API._cache_entry_upsert(k, v)
        self.assertTrue(added)

        timestamp_add: float = self.API._cache_entry_get_updated(k)
        self.assertIsInstance(timestamp_add, float)
        self.assertGreater(timestamp_add, added_time)

        val = self.API._cache_entry_get_value(k)
        self.assertIsInstance(val, bool)
        self.assertEqual(val, v)

        # update cache entry
        updated_time: float = time.time()
        updated: bool = self.API._cache_entry_upsert(k, False)
        self.assertTrue(updated)
        timestamp_update: float = self.API._cache_entry_get_updated(k)
        self.assertGreater(timestamp_update, updated_time)
        self.assertGreater(updated_time, added_time)
        diff: float = timestamp_update - timestamp_add
        self.assertLess(diff, 1.0)

        # clean up and remove unit tests cache entries!
        self.API._cache_entry_delete(k)

    def test_cache_store_update_bad_type(self) -> None:
        '''Try to update a cache entry where its value type is not supported.'''

        ns: int = time.perf_counter_ns()
        k = f'cache_{ns}'

        updated: bool = self.API._cache_entry_upsert(k, time)  # type: ignore
        self.assertFalse(updated)
        timestamp: float = self.API._cache_entry_get_updated(k)
        self.assertIsInstance(timestamp, float)
        self.assertEqual(timestamp, -1.0)

    def test_cache_store_delete(self) -> None:
        '''Delete a cache entry from cache store.'''

        ns: int = time.perf_counter_ns()
        k = f'cache_{ns}'

        added: bool = self.API._cache_entry_upsert(k, ns)
        self.assertTrue(added)
        deleted: bool = self.API._cache_entry_delete(k)
        self.assertTrue(deleted)

    def test_cache_store_get_nonexistent(self) -> None:
        '''Try to get a non-existent cache entry.'''

        ns: int = time.perf_counter_ns()
        k = f'cache_{ns}'

        timestamp: float = self.API._cache_entry_get_updated(k)
        self.assertIsInstance(timestamp, float)
        self.assertEqual(timestamp, -1.0)

    def test_database_clone(self) -> None:
        '''Duplicate a postgres database.'''

        self.database_ensure_exist()
        name_new: str = f'pg_unittest_{time.perf_counter_ns()}'
        name: str = f'pg_unittest'
        resp: Dict[str, str] = self.API.database_clone(name, name_new)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 3)
        self.assertIsInstance(resp['jobKey'], str)
        self.assertIsInstance(resp['storageId'], str)
        self.assertTrue(bool(fullmatch(self.API.re_uuid4, resp['jobKey'], flags=2)))
        self.assertTrue(bool(fullmatch(self.API.re_uuid4, resp['storageId'], flags=2)))

        # TODO verify database was actually created and time to complete system jobs
        # 1) db_clone
        # 2) db_analyze
        db_src: Dict[str, Any] = self.API.database(name)
        db_clone: Dict[str, Any] = {}
        ready: bool = False
        while ready is False:
            db_clone = self.API.database(name_new)
            if db_clone.get('lockoutReason') is None:
                ready = True
                break
            time.sleep(10)

        # 3) db now exists
        # self.assertEqual(db_clone['annotations']['sharedByUserName'], self.API.auth_username)
        self.assertEqual(db_clone['description'], 'Duplicated via OptiPy')
        self.assertIsNone(db_clone['annotations'].get('shared'))
        dbc = OrderedDict(sorted(db_clone.items()))
        self.storage_database(dbc)

        bytes_diff: int = abs(db_src['bytesUsed'] - db_clone['bytesUsed'])
        bytes_diff_percent: float = bytes_diff / db_src['bytesUsed']
        self.assertLess(bytes_diff_percent, 1.0)

        self.assertEqual(db_src['defaultSchema'], db_clone['defaultSchema'])
        self.assertEqual(db_src['notes'], db_clone['notes'])
        self.assertEqual(db_src['schemaReleaseStatus'], db_clone['schemaReleaseStatus'])
        self.assertEqual(db_src['schemaStatus'], db_clone['schemaStatus'])
        self.assertEqual(db_src['schemaVersion'], db_clone['schemaVersion'])

        src_schema_update: datetime = datetime.fromtimestamp(db_src['schemaStatusLastUpdated'])
        clone_schema_update: datetime = datetime.fromtimestamp(db_clone['schemaStatusLastUpdated'])
        schema_update_diff: timedelta = clone_schema_update - src_schema_update
        self.assertLessEqual(schema_update_diff.seconds, 3600)

        src_schema_valid: datetime = datetime.fromtimestamp(db_src['schemaStatusLastValidated'])
        clone_schema_valid: datetime = datetime.fromtimestamp(db_clone['schemaStatusLastValidated'])
        schema_valid_diff: timedelta = src_schema_valid - clone_schema_valid
        self.assertLessEqual(schema_valid_diff.seconds, 0)

        self.assertEqual(db_src['tags'], db_clone['tags'])
        self.assertEqual(db_src['type'], db_clone['type'])

    def test_database_connections(self) -> None:
        '''Get a list of active database connections.'''

        nano_secs: str = str(time.perf_counter_ns())
        thread = Thread(
            target=lambda: self.API.sql_query('pg_unittest', f'/*{nano_secs}*/ SELECT pg_sleep(30)')
        )
        thread.start()  # fire and forget
        now: datetime = datetime.utcnow()
        time.sleep(2)

        resp: Dict[str, Any] = self.API.database_connections('pg_unittest')
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['rowCount'], int)
        self.assertGreaterEqual(resp['rowCount'], 1)
        self.assertIsInstance(resp['queryResults'], list)
        self.assertEqual(len(resp['queryResults']), resp['rowCount'])

        KEYS: Tuple[str, ...] = (
            'application',
            'Query Start',
            'query',
            'State Change',
            'state',
            'Transaction Start',
        )
        query_found: bool = False
        for row in resp['queryResults']:
            self.assertIsInstance(row, dict)
            self.assertEqual(len(row.keys()), 8)
            for k in KEYS:
                self.assertIn(k, row.keys())
            self.assertIsInstance(row['application'], str)
            self.assertIsInstance(row['Query Start'], str)
            self.assertIsInstance(row['query'], str)
            self.assertIsInstance(row['State Change'], str)
            self.assertIsInstance(row['state'], str)
            self.assertTrue(
                row['Transaction Start'] is None or isinstance(row['Transaction Start'], str)
            )
            self.assertTrue(row['Wait Event'] is None or isinstance(row['Wait Event'], str))
            self.assertTrue(row['Wait Type'] is None or isinstance(row['Wait Type'], str))

            if row['query'].find('SELECT pg_sleep(') > -1:
                query_found = True
                self.assertGreater(row['query'].find('OptiPy'), -1)
                self.assertEqual(row['Wait Event'], 'PgSleep')
                self.assertEqual(row['Wait Type'], 'Timeout')

                dt: datetime = parse(row['Query Start'])
                self.assertTrue(dt.tzname(), 'UTC')
                self.assertEqual(dt.year, now.year)
                self.assertEqual(dt.month, now.month)
                self.assertEqual(dt.day, now.day)

        self.assertTrue(query_found)

    def test_database_connections_terminate(self) -> None:
        '''Terminate a database connection.'''

        resp: Dict[str, Any] = self.API.database_connections_terminate('pg_unittest')
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['rowCount'], int)
        self.assertIsInstance(resp['queryResults'], list)
        self.assertEqual(resp['rowCount'], 0)
        self.assertEqual(len(resp['queryResults']), 0)

    def test_database_create_delete(self) -> None:
        '''Create a postgres database then delete.'''

        bots: List[str] = self.API._database_templates_legacy_by_name('Global', wildcard=True)
        self.assertGreaterEqual(len(bots), 1)
        db_name: str = f'pg_unittest_{time.perf_counter_ns()}'

        # create database
        label: dict[str, bool] = {'no-backup': True}
        resp: dict = self.API.database_create(
            db_name,
            desc=f'unittest {db_name}',
            template=bots[0],
            backups=False,
            labels=label,
        )
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['storageId'], str)
        self.assertEqual(len(resp['storageId']), 36)

        # verify database was created
        db: Dict[str, Any] = self.API.database(db_name)
        self.storage_database(db)
        self.assertGreater(db['tags'].find('no-backup'), -1)
        self.assertDictEqual(db['labels'], {'no-backup': True})

        # delete database
        resp = self.API.storage_delete(db_name)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')

    def test_database_create_delete_all(self) -> None:
        '''For each database template create a database, verify then delete it.'''

        k = 'db_create_delete_all'

        timestamp: float = self.API._cache_entry_get_updated(k)
        now: float = time.time()
        delta = timedelta(seconds=now - timestamp)
        if delta.total_seconds() < 604_800:  # skip if ran in last 7 days
            self.skipTest(f'test ran {str(delta)} ago, skipping less than 7 days')

        self.API._cache_entry_upsert(k, True)

        for template_name, tid in self.API.DATABASE_TEMPLATES_NAMEID.items():
            # create database
            db_name: str = f'pg_unittest_all_templates_{tid}_{time.perf_counter_ns()}'
            db_desc: str = f'unittest {db_name}'
            # TODO make tid always be friendly str instead of guid
            resp: dict = self.API.database_create(
                db_name, desc=db_desc, template=tid, backups=False, labels={'no-backup': True}
            )
            self.assertIsInstance(resp['result'], str)
            self.assertEqual(resp['result'], 'success')
            self.assertIsInstance(resp['storageId'], str)
            self.assertEqual(len(resp['storageId']), 36)

            # verify
            db: Dict[str, Any] = self.API.database(db_name)
            self.storage_database(db)
            self.assertEqual(db['id'], resp['storageId'])
            self.assertEqual(db['name'], db_name)
            self.assertEqual(db['description'], db_desc)
            self.assertEqual(db['schemaStatus'], 'valid')

            print(f'\n\n{tid}, {template_name},')
            print(f"  tags: {len(db['tags'])},\n  {db['labels']}\n  {db['annotations']}")
            self.assertGreater(db['tags'].find('no-backup'), -1)
            self.assertDictEqual(db['labels'], {'no-backup': True})

            if db['annotations'].get('sourceBaseTemplateId'):
                # 2023-10-30 anura_2_7_11_clean shows this still exists
                self.assertIsInstance(db['annotations']['sourceBaseTemplateId'], Number)
                self.assertEqual(db['annotations']['sourceBaseTemplateName'], template_name)
            if db['annotations'].get('sourceTemplateSetId'):
                self.assertIsInstance(db['annotations']['sourceTemplateSetId'], Number)
                self.assertEqual(db['annotations']['sourceTemplateSetName'], template_name)

            # delete database
            resp = self.API.storage_delete(db_name)
            self.assertIsInstance(resp['result'], str)
            self.assertEqual(resp['result'], 'success')

    def test_database_create_id_wrong(self) -> None:
        '''Create a postgres database with a template name instead of id.'''

        template_name: str = 'China Exit Risk Strategy'
        db_name: str = f'pg_unittest_{time.perf_counter_ns()}'

        # get template id
        ids: List[str] = self.API._database_templates_legacy_by_name(template_name)
        self.assertEqual(len(ids), 1)
        self.assertEqual(ids[0], self.API.DATABASE_TEMPLATES_NAMEID[template_name])

        # create database with template id derived from the template name
        resp: Dict[str, Any] = self.API.database_create(
            db_name, desc=f'unittest {db_name} {template_name}', template=ids[0], backups=False
        )
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['storageId'], str)
        self.assertEqual(len(resp['storageId']), 36)

        # verify database creation
        db: Dict[str, Any] = self.API.database(db_name)
        self.assertEqual(db['result'], 'success')
        self.assertEqual(db['name'], db_name)
        self.assertEqual(db['type'], 'postgres_db')
        self.assertEqual(db['id'], resp['storageId'])
        self.assertGreater(db['description'].find(template_name), -1)
        self.assertGreater(db['tags'].find('no-backup'), -1)

    def test_database_create_failure_already_exists(self) -> None:
        '''Attempt creating a postgres database but cannot db name is already used.'''

        db_name: str = 'cant'
        template: str = 'does_not_exist'

        if self.API.storagename_database_exists(db_name) is False:
            self.API.database_create(name=db_name, template=template)

        with self.assertRaises(AssertionError):
            self.API.database_create(name=db_name, template=template)

    def test_database_create_failure_template_bad(self) -> None:
        '''Attempt creating a postgres database with bad template id that does not exist.'''

        db_name: str = f'pg_unittest_{time.perf_counter_ns()}'
        resp = self.API.database_create(name=db_name, template='does_not_exist')

        self.assertEqual(resp['crash'], True)
        self.assertEqual(resp['exception'].response.status_code, 400)

    def test_database_customization(self) -> None:
        '''Perform customizations on a database and verify.'''

        CUSTOM: str = '''
        DO $$
        BEGIN
            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'analytics'
                AND column_name = 'custom'
            ) THEN
                ALTER TABLE analytics ADD COLUMN custom TEXT;
            END IF;

            IF NOT EXISTS (
                SELECT 1
                FROM information_schema.tables
                WHERE table_name = 'dirt_bikes'
            ) THEN
            CREATE TABLE dirt_bikes (
                manf TEXT,
                year INT,
                model TEXT,
                price INT,
                freight INT
            );
            INSERT INTO dirt_bikes (manf, year, model, price, freight)
            VALUES
                ('GasGas', 2023, 'MC 50', 4599, 410),
                ('KTM', 2023, '50sx', 4699, 385),
                ('Husqvarna', 2023, 'TC 50', 4799, 385);
            END IF;
        END $$;

        '''

        # apply customizations
        self.API.sql_query('pg_unittest', CUSTOM)

        # verify customizations
        resp: Dict[str, Any] = self.API.database_customizations('pg_unittest')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 2)
        self.assertIsInstance(resp['schemas'], list)
        self.assertGreaterEqual(len(resp['schemas']), 1)
        for s in resp['schemas']:
            self.assertIsInstance(s['name'], str)
            self.assertIsInstance(s['tables'], list)
            self.assertIsInstance(s['views'], list)
            for t in s['tables']:
                self.assertIsInstance(t['name'], str)
                self.assertIsInstance(t['columns'], list)
                self.assertIsInstance(t['isCustom'], bool)
                # TODO if custom table, assert table is truly from anura schema
                for c in t['columns']:
                    self.assertIsInstance(c['name'], str)
                    self.assertIsInstance(c['dataType'], str)
            for v in s['views']:
                self.assertIsInstance(v['name'], str)
                self.assertIsInstance(v['columns'], list)
                self.assertIsInstance(v['isCustom'], bool)
                for c in v['columns']:
                    self.assertIsInstance(c['name'], str)
                    self.assertIsInstance(c['dataType'], str)

        # clean up
        DELETE_CUSTOMIZATIONS = '''
        DO $$ 
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'analytics'
                AND column_name = 'custom'
                ) THEN
                    ALTER TABLE analytics DROP COLUMN custom;
            END IF;

            IF EXISTS (
                SELECT 1
                FROM information_schema.columns
                WHERE table_name = 'dirt_bikes'
                ) THEN
                    DROP TABLE dirt_bikes;
            END IF;
        END $$;
        '''
        self.API.sql_query('pg_unittest', DELETE_CUSTOMIZATIONS)

    def test_database_customization_none(self) -> None:
        '''Database has no customizations.'''

        CUSTOM_COLUMN = '''
        SELECT
        EXISTS (
            SELECT 1
            FROM information_schema.columns
            WHERE table_name = 'analytics'
            AND column_name = 'custom'
        );
        '''
        resp = self.API.sql_query('pg_unittest', CUSTOM_COLUMN)
        self.assertFalse(resp['queryResults'][0]['exists'])

        CUSTOM_TABLE = '''
        SELECT
        EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_name = 'dirt_bikes'
        );
        '''
        resp = self.API.sql_query('pg_unittest', CUSTOM_TABLE)
        self.assertFalse(resp['queryResults'][0]['exists'])

        resp: Dict[str, Any] = self.API.database_customizations('pg_unittest')
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 2)
        self.assertIsInstance(resp['schemas'], list)
        self.assertEqual(len(resp['schemas']), 0)

    def test_database_export(self) -> None:
        '''Initiate job to export database named empty table, nonEmptyTables, and custom sql query.'''

        DB: Final[str] = 'pg_unittest'
        G: Final[str] = 'nonEmptyTables'
        Q: Final[str] = 'SELECT datname FROM pg_database'
        TBL: Final[List[str]] = ['advancedqueueingdetails']

        with self.assertRaises(ValueError):
            self.API.database_export(DB, named=[])

        with self.assertRaises(ValueError):
            self.API.database_export(DB, group='does_not_exist')  # type: ignore

        with self.assertRaises(AssertionError):
            self.API.database_export(DB, query='ha')

        # xls format mirrors csv and includes two extra files: .xls, readme.txt
        resp: Dict[str, Any] = self.API.database_export(
            DB, named=TBL, group=G, query=Q, format='xls'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 10)
        self.assertIsInstance(resp['format'], str)
        self.assertIsInstance(resp['jobKey'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['sourceGroup'], str)
        self.assertIsInstance(resp['sourceList'], list)
        self.assertIsInstance(resp['sourceQuery'], str)
        self.assertIsInstance(resp['sourceSchema'], str)
        self.assertIsInstance(resp['storageId'], str)
        self.assertIsInstance(resp['storageName'], str)
        self.assertTrue(bool(fullmatch(self.API.re_uuid4, resp['jobKey'])))
        self.assertEqual(
            resp['message'], 'DB Data Export job submitted. Poll job info for current job status.'
        )
        self.assertIsNone(resp.get('multipleFiles'))
        self.assertEqual(resp['sourceGroup'], G)
        self.assertEqual(resp['sourceList'], TBL)
        self.assertEqual(resp['sourceQuery'], Q)
        self.assertTrue(bool(fullmatch(self.API.re_uuid4, resp['storageId'])))
        self.assertEqual(resp['storageName'], DB)

        # TODO
        # 1) poll job key status
        # 2) download zip
        # 3) unpack zip
        # 4) verify csv output folder: csv, source_query, metadata
        # 5) if xls format, verify xls output file and readme.txt

    def test_database_no_backups(self) -> None:
        '''Unittest databases should not be eligible for system backups.'''

        dbs: List[Dict[str, Any]] = self.databases_utilized_by_unittest(all=True)
        for db in dbs:
            self.assertGreater(db['tags'].find('no-backup'), -1)

    def test_database_objects(self) -> None:
        '''Tables and views with stats.'''

        self.database_ensure_exist()
        resp: Dict[str, Any] = self.API.database_objects('pg_unittest')
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['schemas'], list)
        for schema in resp['schemas']:
            self.assertEqual(len(schema.keys()), 6)
            self.assertIsInstance(schema['isDefault'], bool)
            self.assertIsInstance(schema['name'], str)
            self.assertIsInstance(schema['tableCount'], int)
            self.assertIsInstance(schema['tables'], list)
            self.assertIsInstance(schema['viewCount'], int)
            self.assertIsInstance(schema['views'], list)
            self.assertEqual(len(schema['tables']), schema['tableCount'])
            self.assertEqual(len(schema['views']), schema['viewCount'])
            for t in schema['tables']:
                self.assertIsInstance(t['name'], str)
                self.assertIsInstance(t['rows'], int)
                self.assertGreaterEqual(len(t['name']), 1)
                self.assertGreaterEqual(t['rows'], 0)

        # tables only
        resp: Dict[str, Any] = self.API.database_objects('pg_unittest', views=False)
        self.assertEqual(resp['result'], 'success')
        for schema in resp['schemas']:
            self.assertIsNone(schema.get('views'))

        # views only
        resp: Dict[str, Any] = self.API.database_objects('pg_unittest', tables=False)
        self.assertEqual(resp['result'], 'success')
        for schema in resp['schemas']:
            self.assertIsNone(schema.get('tables'))

    def test_database_schemas(self) -> None:
        '''Currently only anura schemas.'''

        ANURA_STATUS: Tuple[str, ...] = (
            'current',
            'deprecated',
            'preview',
            'release candidate',
            'retired',
            'stable',
        )
        resp = self.API.database_schemas_anura()
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['schemas'], dict)
        self.assertEqual(len(resp), 2)
        self.assertEqual(len(resp['schemas']), 1)
        self.assertTrue(resp['schemas'].get('anura', False))
        for schema_type in resp['schemas'].keys():
            for v in resp['schemas'][schema_type]:
                self.assertEqual(len(v), 10)
                self.assertIsInstance(v['generalAvailabilityDate'], str)
                self.assertIsInstance(v['description'], str)
                self.assertIsInstance(v['notes'], str)
                self.assertIsInstance(v['schemaName'], str)
                self.assertRegex(v['schemaName'], r'anura_2_[4-9]')
                self.assertIsInstance(v['schemaVersion'], str)
                self.assertRegex(v['schemaVersion'], r'2\.[4-9]\.\d+')
                self.assertIsInstance(v['status'], str)
                self.assertIn(v['status'], ANURA_STATUS)
                self.assertTrue(self.date_isoformat(v['generalAvailabilityDate']))
                if v.get('defaultMigrationDate'):
                    self.assertIsInstance(v['defaultMigrationDate'], str)
                    self.assertTrue(self.date_isoformat(v['defaultMigrationDate']))
                if v.get('endOfLifeDate'):
                    self.assertIsInstance(v['endOfLifeDate'], str)
                    self.assertTrue(self.date_isoformat(v['endOfLifeDate']))
                if v.get('limitedAvailabilityDate'):
                    self.assertIsInstance(v['limitedAvailabilityDate'], str)
                    self.assertTrue(self.date_isoformat(v['limitedAvailabilityDate']))
                if v.get('techPreviewDate'):
                    self.assertIsInstance(v['techPreviewDate'], str)
                    self.assertTrue(self.date_isoformat(v['techPreviewDate']))

    def test_database_tables(self) -> None:
        '''List of schemas and tables.'''

        self.database_ensure_exist()
        db = self.API.account_storage_device(type='postgres_db')
        resp = self.API.database_tables(db['name'])
        self.assertIsInstance(resp['result'], str)
        for schema in resp['schemas']:
            self.assertIsInstance(schema['name'], str)
            self.assertIsInstance(schema['tables'], int)
            self.assertIsInstance(schema['is_default_schema'], bool)
        self.assertIsInstance(resp['tables'], list)

        if len(resp['tables']) >= 1:
            self.assertIsInstance(resp['tables'][0]['name'], str)
            self.assertIsInstance(resp['tables'][0]['rows'], int)
            self.assertIsInstance(resp['tables'][0]['schema'], str)

    def test_database_tables_empty(self) -> None:
        '''Clear the data in specified tables.'''

        db: str = 'pg_unittest_empty_bom_table'
        tbl: str = 'billsofmaterials'
        anura_versions: list[str] = sorted(
            {t for t in self.API.DATABASE_TEMPLATES if t.find('anura') > -1}, reverse=True
        )
        tid: str = anura_versions[0]
        schema: str = tid[0:9]

        # assert db exists
        exists: bool = self.API.storagename_database_exists(db)
        if exists:
            resp: Dict[str, Any] = self.API.storage(db)
            schema = resp['defaultSchema']
        else:
            self.API.database_create(name=db, template=tid, backups=False)

        # assert db has data
        QUERY_ROWS: str = f'SELECT COUNT(*) FROM {schema}.{tbl}'
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows: int = int(resp['queryResults'][0]['count'])
        if rows == 0:
            query_insert = f'INSERT INTO {schema}.{tbl}\n'
            query_insert += (
                '(bomname, productname, producttype, quantity, quantityuom, status, notes)\n'
            )
            query_insert += f"VALUES\n('Unittest', 'RM1', 'Component', '1', 'EA', 'Exclude', 'unittest{time.time()}')"
            self.API.sql_query(db, query_insert)
            rows = 1

        # remove table data dry run
        resp = self.API.database_tables_empty(db, tables=[tbl], dry_run=True)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 4)
        self.assertTrue(resp['dryRun'])
        self.assertIsInstance(resp['emptied'], list)
        self.assertEqual(len(resp['emptied']), 1)
        self.assertEqual(resp['emptied'][0], f'{schema}.{tbl}')
        self.assertIsInstance(resp['failed'], list)
        self.assertEqual(len(resp['failed']), 0)
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows_dry_run: int = int(resp['queryResults'][0]['count'])
        self.assertEqual(rows, rows_dry_run)

        # remove table data
        resp = self.API.database_tables_empty(db, tables=[tbl])
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 4)
        self.assertFalse(resp['dryRun'])
        self.assertIsInstance(resp['emptied'], list)
        self.assertEqual(len(resp['emptied']), 1)
        self.assertEqual(resp['emptied'][0], f'{schema}.{tbl}')
        self.assertIsInstance(resp['failed'], list)
        self.assertEqual(len(resp['failed']), 0)
        resp = self.API.sql_query(db, QUERY_ROWS)
        rows_cleared: int = int(resp['queryResults'][0]['count'])
        self.assertEqual(rows_cleared, 0)

    def test_database_templates(self) -> None:
        '''Empty db or anura schemas.'''

        # 2023-06-02
        templates: Dict[float, Any] = {
            2.1: {
                "id": 2.1,
                "name": "Empty Database",
                "templateType": "baseline",
                "pgTemplateName": "template1",
                "schema": "none",
                "baselineSchemaVersion": "1.0",
                "baseId": 2,
                "templateVersion": "1.0",
                "shortDescription": "Database with no tables or schemas other than public.",
                "longDescription": "Database with no tables or schemas other than public.",
                "isDefault": True,
                "tags": [],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            7.6: {
                "id": 7.6,
                "name": "Anura New Model",
                "templateType": "baseline",
                "pgTemplateName": "anura_2_6_31_3_1_clean",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3.1",
                "baseId": 7,
                "templateVersion": "2.6.31.3.1",
                "shortDescription": "Optilogic standard supply chain schema.",
                "longDescription": "Optilogic standard supply chain schema.",
                "isDefault": True,
                "tags": ["Cosmic Frog"],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            7.11: {
                "id": 7.11,
                "name": "Anura New Model v2.7.11",
                "templateType": "baseline",
                "pgTemplateName": "anura_2_7_11_clean",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.11",
                "baseId": 33,
                "templateVersion": "2.7.11",
                "shortDescription": "Optilogic standard supply chain schema.",
                "longDescription": "Optilogic standard supply chain schema.",
                "isDefault": True,
                "tags": ["Cosmic Frog"],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.11",
            },
            9.20230925133401: {
                "id": 9.20230925133401,
                "name": "Global Supply Chain Strategy (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "640d2e66-ec81-4822-a509-be4b0b0797be",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 9,
                "templateVersion": "20230925133401",
                "shortDescription": "Global network strategy that includes inbound raw material sourcing and outbound finished goods distribution.",
                "longDescription": "Use this database to answer global network strategy questions. Database Structure: Raw material suppliers located in Asia and Europe, production plants located in Mexico and USA, and outbound distribution to 1000+ customers in USA. Questions answered: What is our baseline as-is network? What if we increase production volume in Mexico? What if we close the Detroit DC? What if demand increases 10%? What are the financial tradeoffs between production cost, transportation cost, and fixed operating cost? What are tradeoffs between financials, service level, and risk?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                    "Risk & Resiliency",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/IGDxhMO1zeA"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            9.2023092508324: {
                "id": 9.2023092508324,
                "name": "Global Supply Chain Strategy",
                "templateType": "templateSet",
                "pgTemplateName": "93517785-3447-43c7-abf1-3f4545a41c83",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 9,
                "templateVersion": "2023092508324",
                "shortDescription": "Global network strategy that includes inbound raw material sourcing and outbound finished goods distribution.",
                "longDescription": "Use this database to answer global network strategy questions. Database Structure: Raw material suppliers located in Asia and Europe, production plants located in Mexico and USA, and outbound distribution to 1000+ customers in USA. Questions answered: What is our baseline as-is network? What if we increase production volume in Mexico? What if we close the Detroit DC? What if demand increases 10%? What are the financial tradeoffs between production cost, transportation cost, and fixed operating cost? What are tradeoffs between financials, service level, and risk?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                    "Risk & Resiliency",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/IGDxhMO1zeA"}],
                "schemaReleaseStatus": "stable",
            },
            12.20230925133401: {
                "id": 12.20230925133401,
                "name": "Tactical Capacity Optimization (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "ac53b629-08e8-4aa0-b16f-d96f2043bacb",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 12,
                "templateVersion": "20230925133401",
                "shortDescription": "Pharmaceutical manufacturer uses strategic network databaseing to support tactical daily capacity planning. Tactical capacity planning for a pharmaceutical manufacturer. Optimizing the daily storage and manufacturing plan to support vaccine production.",
                "longDescription": "Optimizing daily storage and manufacturing plan to support vaccine production. Pharmaceutical raw materials have unique temperature requirements and finite capacities for onsite storage. If the plant runs out of storage capacity, then offsite 3rd party storage is needed. Questions answered: If, when, and how much 3PL space will be required? How do we balance the transportation costs and external storage costs? What is the detailed storage and shipment plan? What is the optimized plan at the daily level for 180 days? What happens if a supplier fails? Can we use an alternate supplier?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Capacity Planning",
                    "Production Planning",
                    "Risk & Resiliency",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/G0LZnkfyYlI"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            12.20230925083242: {
                "id": 12.20230925083242,
                "name": "Tactical Capacity Optimization",
                "templateType": "templateSet",
                "pgTemplateName": "19d1aeff-6870-4809-a433-23ef855f3dea",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 12,
                "templateVersion": "20230925083242",
                "shortDescription": "Pharmaceutical manufacturer uses strategic network databaseing to support tactical daily capacity planning. Tactical capacity planning for a pharmaceutical manufacturer. Optimizing the daily storage and manufacturing plan to support vaccine production.",
                "longDescription": "Optimizing daily storage and manufacturing plan to support vaccine production. Pharmaceutical raw materials have unique temperature requirements and finite capacities for onsite storage. If the plant runs out of storage capacity, then offsite 3rd party storage is needed. Questions answered: If, when, and how much 3PL space will be required? How do we balance the transportation costs and external storage costs? What is the detailed storage and shipment plan? What is the optimized plan at the daily level for 180 days? What happens if a supplier fails? Can we use an alternate supplier?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Capacity Planning",
                    "Production Planning",
                    "Risk & Resiliency",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/G0LZnkfyYlI"}],
                "schemaReleaseStatus": "stable",
            },
            15.202309251334: {
                "id": 15.202309251334,
                "name": "Detailed Facility Selection (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "a6160d9b-c5e7-421b-b860-62eacab77d31",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 15,
                "templateVersion": "202309251334",
                "shortDescription": "Use this database for facility selection, where detailed cost and capacities are important.",
                "longDescription": "Detailed Facility Selection uses network optimization to determine which facilities to open and close as well as how products should flow from those facilities to the customers.  Feed the database with pre-identified candidate sites, which could be generated by Triad (Intelligent Greenfield engine) and the solver will select optimal locations from this pool of candidates.  This database is appropriate where detailed cost and capacities are important beyond what is supported in Triad.  Questions answered (used in conjunction with Triad): What is the optimal DC footprint to serve our existing customer demand? We want to open X# of short listed DCs. What are the optimal locations? I have a list of possible candidate facility locations. How many facilities should I choose? Where should they be located? Can I create a sensitivity analysis by running dozens of scenarios? What are the cost, service level, and risk tradeoffs? What is the break point where the incremental benefits of adding a new DC are outweighed by the costs?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Risk",
                    "Network Strategy",
                    "Capacity Planning",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/S1XCLtmTqeY"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            15.20230925083242: {
                "id": 15.20230925083242,
                "name": "Detailed Facility Selection",
                "templateType": "templateSet",
                "pgTemplateName": "2f070371-5850-46b9-9227-327a19f3f7bb",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 15,
                "templateVersion": "20230925083242",
                "shortDescription": "Use this database for facility selection, where detailed cost and capacities are important.",
                "longDescription": "Detailed Facility Selection uses network optimization to determine which facilities to open and close as well as how products should flow from those facilities to the customers.  Feed the database with pre-identified candidate sites, which could be generated by Triad (Intelligent Greenfield engine) and the solver will select optimal locations from this pool of candidates.  This database is appropriate where detailed cost and capacities are important beyond what is supported in Triad.  Questions answered (used in conjunction with Triad): What is the optimal DC footprint to serve our existing customer demand? We want to open X# of short listed DCs. What are the optimal locations? I have a list of possible candidate facility locations. How many facilities should I choose? Where should they be located? Can I create a sensitivity analysis by running dozens of scenarios? What are the cost, service level, and risk tradeoffs? What is the break point where the incremental benefits of adding a new DC are outweighed by the costs?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Risk",
                    "Network Strategy",
                    "Capacity Planning",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/S1XCLtmTqeY"}],
                "schemaReleaseStatus": "stable",
            },
            18.20230925133401: {
                "id": 18.20230925133401,
                "name": "United States Greenfield Facility Selection (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "170f109a-c155-4029-9e6a-ff40f42a4160",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 18,
                "templateVersion": "20230925133401",
                "shortDescription": "Use this database for facility selection from many automatically generated candidates, considering basic capacities, costs and service levels.",
                "longDescription": "The database uses the Intelligent Greenfield engine. Simply provide the database with Customers and Demand to be able to find the optimum facilities from many automatically generated candidates. You are also able to include existing facilities, basic fixed and variables costs, capacities as well as service level bands. This database is appropriate where considering high-level greenfield networks to narrow down facility selection for more detailed analysis in Neo (network optimization). Questions answered: \u201c# cost optimized Facilities that meet a defined service level\u201d, \u201c# of Facilities that meet a defined service level, minimizing weighting.",
                "isDefault": True,
                "tags": [
                    "Intelligent Greenfield",
                    "Triad",
                    "Cosmic Frog",
                    "Greenfield",
                    "Network Strategy",
                    "Facility Selection",
                    "CAPEX Planning",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/IC2cmYYHR8s"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            18.20230925084416: {
                "id": 18.20230925084416,
                "name": "United States Greenfield Facility Selection",
                "templateType": "templateSet",
                "pgTemplateName": "69fc6c70-9d94-497c-8dfb-0db1e4340ecb",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 18,
                "templateVersion": "20230925084416",
                "shortDescription": "Use this database for facility selection from many automatically generated candidates, considering basic capacities, costs and service levels.",
                "longDescription": "The database uses the Intelligent Greenfield engine. Simply provide the database with Customers and Demand to be able to find the optimum facilities from many automatically generated candidates. You are also able to include existing facilities, basic fixed and variables costs, capacities as well as service level bands. This database is appropriate where considering high-level greenfield networks to narrow down facility selection for more detailed analysis in Neo (network optimization). Questions answered: \u201c# cost optimized Facilities that meet a defined service level\u201d, \u201c# of Facilities that meet a defined service level, minimizing weighting.",
                "isDefault": True,
                "tags": [
                    "Intelligent Greenfield",
                    "Triad",
                    "Cosmic Frog",
                    "Greenfield",
                    "Network Strategy",
                    "Facility Selection",
                    "CAPEX Planning",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/IC2cmYYHR8s"}],
                "schemaReleaseStatus": "stable",
            },
            21.20230925133908: {
                "id": 21.20230925133908,
                "name": "China Exit Strategy in Asia (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "1b5bf8d9-48ea-4a64-954e-985d591819e5",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 21,
                "templateVersion": "20230925133908",
                "shortDescription": "Japan network strategy that includes inbound raw material sourcing and outbound finished goods distribution. This database focuses on overseas suppliers and potentially shifting the supply base from China to Thailand, Vietnam and local Japanese suppliers.",
                "longDescription": "Use this database to answer Japanese network strategy questions related to supply base. How do we adjust and respond to a supplier bottleneck? What if capacity drops at our Chinese suppliers due to COVID restrictions, port congestion, factory shutdown, or other factors? What if our Chinese suppliers go offline entirely? How does the supply base shift if we bring Thailand and Vietnam suppliers online? What are the financial, service and risk tradeoffs? Risk is a very important consideration because as we migrate from China to other countries in Asia, we reduce cost but increase risk due to political and economic stability in the other countries. Should we Exit China?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Risk",
                    "Network Strategy",
                    "Risk & Resiliency",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                    "Japan",
                    "Asia",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/P8oHfujEx2Y"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            21.20230925084431: {
                "id": 21.20230925084431,
                "name": "China Exit Strategy in Asia",
                "templateType": "templateSet",
                "pgTemplateName": "48275960-5448-4aed-b5e4-2f852bf8f985",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 21,
                "templateVersion": "20230925084431",
                "shortDescription": "Japan network strategy that includes inbound raw material sourcing and outbound finished goods distribution. This database focuses on overseas suppliers and potentially shifting the supply base from China to Thailand, Vietnam and local Japanese suppliers.",
                "longDescription": "Use this database to answer Japanese network strategy questions related to supply base. How do we adjust and respond to a supplier bottleneck? What if capacity drops at our Chinese suppliers due to COVID restrictions, port congestion, factory shutdown, or other factors? What if our Chinese suppliers go offline entirely? How does the supply base shift if we bring Thailand and Vietnam suppliers online? What are the financial, service and risk tradeoffs? Risk is a very important consideration because as we migrate from China to other countries in Asia, we reduce cost but increase risk due to political and economic stability in the other countries. Should we Exit China?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Risk",
                    "Network Strategy",
                    "Risk & Resiliency",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                    "Japan",
                    "Asia",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/P8oHfujEx2Y"}],
                "schemaReleaseStatus": "stable",
            },
            24.20230925133401: {
                "id": 24.20230925133401,
                "name": "China Exit Risk Strategy (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "d2a22c9d-bb5c-44bf-a014-ada3de1092b0",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 24,
                "templateVersion": "20230925133401",
                "shortDescription": "Global network strategy that includes inbound raw material sourcing and outbound finished goods distribution. This database focuses on overseas suppliers and potentially shifting the supply base from APAC to LATAM and EMEA.",
                "longDescription": "Use this database to answer global network strategy questions related to supply base. How do we adjust and respond to a supplier bottleneck? What if capacity drops at our Chinese suppliers due to COVID restrictions, port congestion, factory shutdown, or other factors? What if our Chinese suppliers go offline entirely? How does the supply base shift if we bring EMEA and LATAM suppliers online? What are the financial, service and risk tradeoffs? Risk is a very important consideration because as we migrate from China to LATAM, we reduce cost but increase risk due to political and economic stability in the LATAM region. Should we Exit China?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Risk & Resiliency",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/EpplSGcHbEE"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            24.20230925083847: {
                "id": 24.20230925083847,
                "name": "China Exit Risk Strategy",
                "templateType": "templateSet",
                "pgTemplateName": "29de0d54-ee83-43da-a284-04170475e7e6",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 24,
                "templateVersion": "20230925083847",
                "shortDescription": "Global network strategy that includes inbound raw material sourcing and outbound finished goods distribution. This database focuses on overseas suppliers and potentially shifting the supply base from APAC to LATAM and EMEA.",
                "longDescription": "Use this database to answer global network strategy questions related to supply base. How do we adjust and respond to a supplier bottleneck? What if capacity drops at our Chinese suppliers due to COVID restrictions, port congestion, factory shutdown, or other factors? What if our Chinese suppliers go offline entirely? How does the supply base shift if we bring EMEA and LATAM suppliers online? What are the financial, service and risk tradeoffs? Risk is a very important consideration because as we migrate from China to LATAM, we reduce cost but increase risk due to political and economic stability in the LATAM region. Should we Exit China?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Risk",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Risk & Resiliency",
                    "Sourcing Optimization",
                    "Distribution",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/EpplSGcHbEE"}],
                "schemaReleaseStatus": "stable",
            },
            27.20230925084417: {
                "id": 27.20230925084417,
                "name": "Multi-Year Capacity Planning",
                "templateType": "templateSet",
                "pgTemplateName": "8acfc863-1dde-4924-8480-12f02eec41e1",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 27,
                "templateVersion": "20230925084417",
                "shortDescription": "Designing the network to expand over the next 5 years in support of future demand growth. Determining the timing and location of capital expenditure (CAPEX) investments in production and distribution capacity.",
                "longDescription": "Use this database to answer questions about where and when to invest in additional production and distribution capacity. A European cheese manufacturer has enough capacity to serve the mature market in Western Europe today. However, the next 5 years show growth in the Eastern Europe market and inadequate capacity to support this. Questions answered: Is our current network sufficient to meet demand in the next 5 years? When and where will we run out of capacity? Where should we invest in additional Production Capacity? When should we time these investments? Where should we invest in additional Distribution Capacity? When should we bring the new DCs online? Should we close existing DC(s)? Where should we open additional DC(s)?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Capacity Planning",
                    "CAPEX Planning",
                    "Distribution",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/SESKKVbcoGk"}],
                "schemaReleaseStatus": "stable",
            },
            27.20230925133955: {
                "id": 27.20230925133955,
                "name": "Multi-Year Capacity Planning (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "5667340d-f6a3-435e-99f3-36efab90cd8b",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 27,
                "templateVersion": "20230925133955",
                "shortDescription": "Designing the network to expand over the next 5 years in support of future demand growth. Determining the timing and location of capital expenditure (CAPEX) investments in production and distribution capacity.",
                "longDescription": "Use this database to answer questions about where and when to invest in additional production and distribution capacity. A European cheese manufacturer has enough capacity to serve the mature market in Western Europe today. However, the next 5 years show growth in the Eastern Europe market and inadequate capacity to support this. Questions answered: Is our current network sufficient to meet demand in the next 5 years? When and where will we run out of capacity? Where should we invest in additional Production Capacity? When should we time these investments? Where should we invest in additional Distribution Capacity? When should we bring the new DCs online? Should we close existing DC(s)? Where should we open additional DC(s)?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Capacity Planning",
                    "CAPEX Planning",
                    "Distribution",
                    "Product Flow",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/SESKKVbcoGk"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            28.20230925083242: {
                "id": 28.20230925083242,
                "name": "Fleet Size Optimization - EMEA Geo",
                "templateType": "templateSet",
                "pgTemplateName": "af9630ce-fe0a-4e9b-ba6d-0d05944d8ef5",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 28,
                "templateVersion": "20230925083242",
                "shortDescription": "Use this database to answer fleet sizing questions. This database leverages network optimization to solve the fleet size problem \u2013 how many and what type of assets are needed. Include factors such as fixed & variable transportation cost, transit time, service level, and asset capacity.",
                "longDescription": "Use this database to solve fleet size and asset mix questions. Find out if your current fleet is optimal. Define your own asset types like 24' truck, 48' truck, 53' truck, and 3PL. What is the optimal number and mix of assets needed to fulfill demand across multiple echelons in your network? Do you need to add capacity by investing in new assets for your private fleet or use a 3rd party carrier? What is the ROI of investing in additional assets for your private fleet? If your network footprint changes - like a DC closure or addition - what is the impact to your fleet? How does seasonal demand affect fleet and costs?",
                "isDefault": True,
                "tags": [
                    "Fleet Sizing",
                    "Mode Selection",
                    "Network Strategy",
                    "MIP",
                    "Cosmic Frog",
                ],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            28.202309251334: {
                "id": 28.202309251334,
                "name": "Fleet Size Optimization - EMEA Geo (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "8437b526-b15f-4a8c-84ff-d1413a69ee9b",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 28,
                "templateVersion": "202309251334",
                "shortDescription": "Use this database to answer fleet sizing questions. This database leverages network optimization to solve the fleet size problem \u2013 how many and what type of assets are needed. Include factors such as fixed & variable transportation cost, transit time, service level, and asset capacity.",
                "longDescription": "Use this database to solve fleet size and asset mix questions. Find out if your current fleet is optimal. Define your own asset types like 24' truck, 48' truck, 53' truck, and 3PL. What is the optimal number and mix of assets needed to fulfill demand across multiple echelons in your network? Do you need to add capacity by investing in new assets for your private fleet or use a 3rd party carrier? What is the ROI of investing in additional assets for your private fleet? If your network footprint changes - like a DC closure or addition - what is the impact to your fleet? How does seasonal demand affect fleet and costs?",
                "isDefault": True,
                "tags": [
                    "Fleet Sizing",
                    "Mode Selection",
                    "Network Strategy",
                    "MIP",
                    "Cosmic Frog",
                ],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            29.20230925083241: {
                "id": 29.20230925083241,
                "name": "Global Risk Analysis",
                "templateType": "templateSet",
                "pgTemplateName": "5d4bd0fc-1da8-4807-a560-528cb841659e",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 29,
                "templateVersion": "20230925083241",
                "shortDescription": "Use this global risk database to learn how the Risk engine works in Cosmic Frog. Run 80+ network optimization scenarios that automatically calculate Opti Risk Scores. Evaluate the impact of disruptions at key nodes in the network and develop risk mitigation strategies to make the supply chain more resilient.",
                "longDescription": "This global risk model features a retail supply chain with a network of production plants, packaging plants and tier 1&2 suppliers in Europe and Asia. The dense and complex flow of materials, coupled with a wide geographical distribution, presents a challenging task in terms of risk estimation. For each supplier, facility and customer, Cosmic Frog provides a set of risk score (ex: geographical, economic resiliency, political, and natural disaster) that identify risk and the potential for disruption that may impact the supply chain. Evaluate the impact of city-level disruption across the network by running 80+ what if scenarios that exclude a given city due to events such as COVID-19 or natural disasters. Compute the performance impact of each city in the event of a disruption and develop risk mitigation strategies. In situations where both spend and performance impact are high, consider utilizing multiple sites and implementing risk-sharing partnerships and performance tracking mechanisms.",
                "isDefault": True,
                "tags": ["Risk & Resiliency", "Network Optimization", "MIP", "Risk", "Cosmic Frog"],
                "media": [{"type": "yt", "url": "https://youtu.be/dmzaZP1-lm8"}],
                "schemaReleaseStatus": "stable",
            },
            29.202309251334: {
                "id": 29.202309251334,
                "name": "Global Risk Analysis (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "a18f9694-db59-49ef-92f0-ad211e2533c9",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 29,
                "templateVersion": "202309251334",
                "shortDescription": "Use this global risk database to learn how the Risk engine works in Cosmic Frog. Run 80+ network optimization scenarios that automatically calculate Opti Risk Scores. Evaluate the impact of disruptions at key nodes in the network and develop risk mitigation strategies to make the supply chain more resilient.",
                "longDescription": "This global risk model features a retail supply chain with a network of production plants, packaging plants and tier 1&2 suppliers in Europe and Asia. The dense and complex flow of materials, coupled with a wide geographical distribution, presents a challenging task in terms of risk estimation. For each supplier, facility and customer, Cosmic Frog provides a set of risk score (ex: geographical, economic resiliency, political, and natural disaster) that identify risk and the potential for disruption that may impact the supply chain. Evaluate the impact of city-level disruption across the network by running 80+ what if scenarios that exclude a given city due to events such as COVID-19 or natural disasters. Compute the performance impact of each city in the event of a disruption and develop risk mitigation strategies. In situations where both spend and performance impact are high, consider utilizing multiple sites and implementing risk-sharing partnerships and performance tracking mechanisms.",
                "isDefault": True,
                "tags": ["Risk & Resiliency", "Network Optimization", "MIP", "Risk", "Cosmic Frog"],
                "media": [{"type": "yt", "url": "https://youtu.be/dmzaZP1-lm8"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            30.20230925083242: {
                "id": 30.20230925083242,
                "name": "Fleet Size Optimization - US Geo",
                "templateType": "templateSet",
                "pgTemplateName": "e0a12e51-d00c-43f6-abf6-07b328d4f270",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 30,
                "templateVersion": "20230925083242",
                "shortDescription": "Use this database to answer fleet sizing questions. This database leverages network optimization to solve the fleet size problem \u2013 how many and what type of assets are needed. Include factors such as fixed & variable transportation cost, transit time, service level, and asset capacity.",
                "longDescription": "Use this USA-centric database to solve fleet size and asset mix questions. Find out if your current fleet is optimal. Define your own asset types like 24' truck, 48' truck, 53' truck, and 3PL. What is the optimal number and mix of assets needed to fulfill demand across multiple echelons in your network? Do you need to add capacity by investing in new assets for your private fleet or use a 3rd party carrier? What is the ROI of investing in additional assets for your private fleet? If your network footprint changes - like a DC closure or addition - what is the impact to your fleet? How does seasonal demand affect fleet and costs?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Fleet Sizing",
                    "Mode Selection",
                    "Network Strategy",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/BrUJQjhcVTQ"}],
                "schemaReleaseStatus": "stable",
            },
            30.20230925133401: {
                "id": 30.20230925133401,
                "name": "Fleet Size Optimization - US Geo (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "da9087a1-cce9-4598-93b4-acf96ac8bf4c",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 30,
                "templateVersion": "20230925133401",
                "shortDescription": "Use this database to answer fleet sizing questions. This database leverages network optimization to solve the fleet size problem \u2013 how many and what type of assets are needed. Include factors such as fixed & variable transportation cost, transit time, service level, and asset capacity.",
                "longDescription": "Use this USA-centric database to solve fleet size and asset mix questions. Find out if your current fleet is optimal. Define your own asset types like 24' truck, 48' truck, 53' truck, and 3PL. What is the optimal number and mix of assets needed to fulfill demand across multiple echelons in your network? Do you need to add capacity by investing in new assets for your private fleet or use a 3rd party carrier? What is the ROI of investing in additional assets for your private fleet? If your network footprint changes - like a DC closure or addition - what is the impact to your fleet? How does seasonal demand affect fleet and costs?",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Fleet Sizing",
                    "Mode Selection",
                    "Network Strategy",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/BrUJQjhcVTQ"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            31.20230925084458: {
                "id": 31.20230925084458,
                "name": "Global Sustainability Analysis",
                "templateType": "templateSet",
                "pgTemplateName": "71f9da77-edb9-4fad-b18e-684065109cac",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 31,
                "templateVersion": "20230925084458",
                "shortDescription": "This sustainability model optimizes a global supply chain for a manufacturer operating production plants in China, Vietnam, and Brazil, with distribution in the USA. It focuses on achieving sustainability while considering financials, service, and risk. The model also includes recycling and landfill flows to simulate a circular supply chain.",
                "longDescription": "This global sustainability model features a manufacturer\u2019s supply chain with a network of production plants in China, Vietnam, and Brazil, and outbound distribution in USA. The manufactured products could be textiles (retail) or consumer goods (CPG). In addition to balancing financials, service, and risk, the goal for this analysis is to find the most sustainable supply chain. As a next step, add recycling flows and landfill flows to model the circular supply chain.",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Sustainability",
                    "Sourcing Optimization",
                    "Risk",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/Ivr1j1u_xuU"}],
                "schemaReleaseStatus": "stable",
            },
            31.20230925134019: {
                "id": 31.20230925134019,
                "name": "Global Sustainability Analysis (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "47a4f9c0-f09a-4b16-83b4-d2dc1c29f6c9",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 31,
                "templateVersion": "20230925134019",
                "shortDescription": "This sustainability model optimizes a global supply chain for a manufacturer operating production plants in China, Vietnam, and Brazil, with distribution in the USA. It focuses on achieving sustainability while considering financials, service, and risk. The model also includes recycling and landfill flows to simulate a circular supply chain.",
                "longDescription": "This global sustainability model features a manufacturer\u2019s supply chain with a network of production plants in China, Vietnam, and Brazil, and outbound distribution in USA. The manufactured products could be textiles (retail) or consumer goods (CPG). In addition to balancing financials, service, and risk, the goal for this analysis is to find the most sustainable supply chain. As a next step, add recycling flows and landfill flows to model the circular supply chain.",
                "isDefault": True,
                "tags": [
                    "MIP",
                    "Cosmic Frog",
                    "Network Strategy",
                    "Sustainability",
                    "Sourcing Optimization",
                    "Risk",
                ],
                "media": [{"type": "yt", "url": "https://youtu.be/Ivr1j1u_xuU"}],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            32.20230925083852: {
                "id": 32.20230925083852,
                "name": "Global Sourcing - Cost To Serve",
                "templateType": "templateSet",
                "pgTemplateName": "23462acf-f6b2-43a5-bc45-78c3e29bf752",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 32,
                "templateVersion": "20230925083852",
                "shortDescription": "This model is a variation of Global Sourcing model focused on showing capabilities of Cost To Serve. This model also includes three scenarios that are added as a result of additional insight gained by running cost to serve. Additionally, you can find custom built dashboards to show profitable/non-profitable customers as well as report cost to serve data for various customer segments.",
                "longDescription": "The Cost-to-Serve Optimization Framework is a refined approach that builds upon the Global Sourcing model. Its main objective is to fully utilize the potential of Cost-to-Serve analysis in order to streamline operations and drive profitable growth. This framework integrates the principles of global sourcing with advanced insights derived from cost-to-serve evaluations, resulting in improved decision-making capabilities.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "Optimization", "User Contribution"],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            32.20230925133401: {
                "id": 32.20230925133401,
                "name": "Global Sourcing - Cost To Serve (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "42a30fb6-8f3a-41a7-a1cb-df5a80c33933",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 32,
                "templateVersion": "20230925133401",
                "shortDescription": "This model is a variation of Global Sourcing model focused on showing capabilities of Cost To Serve. This model also includes three scenarios that are added as a result of additional insight gained by running cost to serve. Additionally, you can find custom built dashboards to show profitable/non-profitable customers as well as report cost to serve data for various customer segments.",
                "longDescription": "The Cost-to-Serve Optimization Framework is a refined approach that builds upon the Global Sourcing model. Its main objective is to fully utilize the potential of Cost-to-Serve analysis in order to streamline operations and drive profitable growth. This framework integrates the principles of global sourcing with advanced insights derived from cost-to-serve evaluations, resulting in improved decision-making capabilities.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "Optimization", "User Contribution"],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            35.20230921133352: {
                "id": 35.20230921133352,
                "name": "Advanced United States Greenfield Facility Selection",
                "templateType": "templateSet",
                "pgTemplateName": "0c294262-394e-402c-80c2-cbdc2fba1cbc",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 35,
                "templateVersion": "20230921133352",
                "shortDescription": "US Greenfield Model with Throughput Constraints, Suppliers and Candidates",
                "longDescription": "This model demonstrates the ability to add additional detail to our Greenfield model. This detail further refines the locations suggested by the engine. We begin with scenarios 1a,b,c,d which examine the trade offs between fixed and transportation cost when adding greenfield sites, as well as ignoring vs including an existing location. After deciding to focus on our 01b results, we further refine our model by adding throughput constraints to our greenfield sites (02b). We then add suppliers into consideration (03b). The last scenario demonstrates evaluating candidate locations provided by the business after reviewing previous scenarios internally.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution", "Greenfield"],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            35.20230925133401: {
                "id": 35.20230925133401,
                "name": "Advanced United States Greenfield Facility Selection (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "fa3f223f-8d16-4220-aa4d-a78dd82886a0",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 35,
                "templateVersion": "20230925133401",
                "shortDescription": "US Greenfield Model with Throughput Constraints, Suppliers and Candidates",
                "longDescription": "This model demonstrates the ability to add additional detail to our Greenfield model. This detail further refines the locations suggested by the engine. We begin with scenarios 1a,b,c,d which examine the trade offs between fixed and transportation cost when adding greenfield sites, as well as ignoring vs including an existing location. After deciding to focus on our 01b results, we further refine our model by adding throughput constraints to our greenfield sites (02b). We then add suppliers into consideration (03b). The last scenario demonstrates evaluating candidate locations provided by the business after reviewing previous scenarios internally.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution", "Greenfield"],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            36.20230921130338: {
                "id": 36.20230921130338,
                "name": "Outbound Distribution Simulation",
                "templateType": "templateSet",
                "pgTemplateName": "f0dfdfff-85cd-4b13-a485-2ff61856234e",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 36,
                "templateVersion": "20230921130338",
                "shortDescription": "Simple supply chain simulation model focused on outbound distribution.",
                "longDescription": "Simple supply chain simulation model focused on outbound distribution.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution", "Simulation"],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            36.20230925134017: {
                "id": 36.20230925134017,
                "name": "Outbound Distribution Simulation (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "8c43a95f-fdab-4645-845a-2643052829d4",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 36,
                "templateVersion": "20230925134017",
                "shortDescription": "Simple supply chain simulation model focused on outbound distribution.",
                "longDescription": "Simple supply chain simulation model focused on outbound distribution.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution", "Simulation"],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
            37.20230926142439: {
                "id": 37.20230926142439,
                "name": "Lookups example for Warehousing Policies",
                "templateType": "templateSet",
                "pgTemplateName": "753501e5-395f-4411-8015-eb178484f356",
                "schema": "anura",
                "baselineSchemaVersion": "2.6.31.3",
                "baseId": 37,
                "templateVersion": "20230926142439",
                "shortDescription": "This template provides an example of how to build and use Lookups.",
                "longDescription": "Often when building models, we want to dynamically Lookup data at run time when data is expanded.  See how Cosmic Frog supports Lookups across all input tables. In this example we will look at warehousing policies that have been defined at an aggregate Products level.  Inbound handling costs are different depending upon the product, so these need to be dynamically looked up when the data is expanded.  This template provides an example of how to build and use Lookups.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution"],
                "media": [],
                "schemaReleaseStatus": "stable",
            },
            37.20230927091221: {
                "id": 37.20230927091221,
                "name": "Lookups example for Warehousing Policies (2.7.3)",
                "templateType": "templateSet",
                "pgTemplateName": "7956f551-6022-4dda-b3c9-dcd3551e3344",
                "schema": "anura",
                "baselineSchemaVersion": "2.7.3",
                "baseId": 37,
                "templateVersion": "20230927091221",
                "shortDescription": "This template provides an example of how to build and use Lookups.",
                "longDescription": "Often when building models, we want to dynamically Lookup data at run time when data is expanded.  See how Cosmic Frog supports Lookups across all input tables. In this example we will look at warehousing policies that have been defined at an aggregate Products level.  Inbound handling costs are different depending upon the product, so these need to be dynamically looked up when the data is expanded.  This template provides an example of how to build and use Lookups.",
                "isDefault": True,
                "tags": ["Cosmic Frog", "User Contribution"],
                "media": [],
                "schemaReleaseStatus": "release candidate 2.7.3",
            },
        }

        resp: Dict[str, Any] = self.API.database_templates()
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 3)
        self.assertIsInstance(resp['count'], int)
        # self.assertEqual(resp['count'], 40)
        self.assertIsInstance(resp['templates'], list)
        template_count: int = len(resp['templates'])
        # self.assertEqual(template_count, 40)
        self.assertEqual(template_count, resp['count'])
        for t in resp['templates']:
            self.assertIsInstance(t, dict)
            self.assertTrue(issubclass(type(templates[t['id']]['baseId']), type(t['baseId'])))
            self.assertTrue(
                issubclass(
                    type(templates[t['id']]['baselineSchemaVersion']),
                    type(t['baselineSchemaVersion']),
                )
            )
            self.assertTrue(issubclass(type(templates[t['id']]['id']), type(t['id'])))
            self.assertTrue(issubclass(type(templates[t['id']]['isDefault']), type(t['isDefault'])))
            self.assertTrue(
                issubclass(type(templates[t['id']]['longDescription']), type(t['longDescription']))
            )
            self.assertTrue(issubclass(type(templates[t['id']]['media']), type(t['media'])))
            self.assertTrue(issubclass(type(templates[t['id']]['name']), type(t['name'])))
            self.assertTrue(
                issubclass(type(templates[t['id']]['pgTemplateName']), type(t['pgTemplateName']))
            )
            self.assertTrue(issubclass(type(templates[t['id']]['schema']), type(t['schema'])))
            self.assertTrue(
                issubclass(
                    type(templates[t['id']]['shortDescription']), type(t['shortDescription'])
                )
            )
            self.assertTrue(issubclass(type(templates[t['id']]['tags']), type(t['tags'])))
            self.assertTrue(
                issubclass(type(templates[t['id']]['templateType']), type(t['templateType']))
            )
            self.assertTrue(issubclass(type(templates[t['id']]['baseId']), type(t['baseId'])))
            self.assertEqual(templates[t['id']]['baseId'], t['baseId'])
            self.assertEqual(
                templates[t['id']]['baselineSchemaVersion'], t['baselineSchemaVersion']
            )
            self.assertEqual(templates[t['id']]['id'], t['id'])
            self.assertEqual(templates[t['id']]['isDefault'], t['isDefault'])
            if templates[t['id']]['longDescription'] != t['longDescription']:
                diff: List[str] = self.compare_words(
                    t['longDescription'], templates[t['id']]['longDescription']
                )
                formatted_diff: str = '\n'.join(diff)
                self.fail(f"{t['name']} longDescription mismatch: \n{formatted_diff}")

            self.assertEqual(templates[t['id']]['longDescription'], t['longDescription'])
            self.assertEqual(templates[t['id']]['media'], t['media'])
            self.assertEqual(templates[t['id']]['name'], t['name'])
            self.assertEqual(templates[t['id']]['pgTemplateName'], t['pgTemplateName'])
            self.assertEqual(templates[t['id']]['schema'], t['schema'])
            self.assertEqual(templates[t['id']]['shortDescription'], t['shortDescription'])
            self.assertEqual(templates[t['id']]['tags'], t['tags'])
            self.assertEqual(templates[t['id']]['templateType'], t['templateType'])
            self.assertEqual(templates[t['id']]['baseId'], t['baseId'])

    def test_database_templates_by_name(self) -> None:
        '''Look up the database template id by case-insensitive template name.'''

        template_names: List[str] = [t['name'] for t in self.API.DATABASE_TEMPLATES_NEW]

        for name in template_names:
            ids: List[str] = self.API._database_templates_by_name(name)
            self.assertEqual(len(ids), 1)
            ids = self.API._database_templates_by_name(name[5:], wildcard=True)
            self.assertGreaterEqual(len(ids), 1)

    def test_database_templates_legacy(self) -> None:
        '''Legacy empty db or anura schemas.'''

        resp: Dict[str, Any] = self.API._database_templates_legacy()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], 33)
        self.assertIsInstance(resp['templates'], list)
        template_count: int = len(resp['templates'])
        self.assertEqual(template_count, 33)
        self.assertEqual(template_count, resp['count'])
        self.assertEqual(template_count, len(self.API.DATABASE_TEMPLATES))

        TEMPLATE_KEYS: Tuple[str, ...] = ('id', 'is_default', 'name', 'role', 'schema')
        for t in resp['templates']:
            self.assertIsInstance(t, dict)
            for k in t.keys():
                self.assertIsInstance(k, str)
                self.assertIn(t['id'], self.API.DATABASE_TEMPLATES)

    def test_database_templates_legacy_by_name(self) -> None:
        '''Look up the database template id by case-insensitive template name.'''

        template_names: List[str] = [k for k in self.API.DATABASE_TEMPLATES_NAMEID.keys()]

        for name in template_names:
            ids: List[str] = self.API._database_templates_legacy_by_name(name)
            self.assertEqual(len(ids), 1)
            self.assertEqual(ids[0], self.API.DATABASE_TEMPLATES_NAMEID[name])
            ids = self.API._database_templates_legacy_by_name(name[5:], wildcard=True)
            if name == 'Anura New Model v2.6':
                self.assertEqual(len(ids), 2)
            else:
                self.assertGreaterEqual(len(ids), 1)

    def test_database_templates_names_legacy_diff_modern(self) -> None:
        '''Diff Legacy Templates call to Modern.'''

        # TODO future state will be to remove legacy template calls in which this would go away

        legacy: Dict[str, Any] = self.API._database_templates_legacy()
        modern: Dict[str, Any] = self.API.database_templates()

        # Old call id attribute used to be friendly name with underscores, then changed to guids
        old = {t['id'] for t in legacy['templates']}

        # New call pgTemplateName maps to old id attribute
        new = {t['pgTemplateName'] for t in modern['templates']}
        diff = old ^ new

        # Canary warning if templates are added or removed but legacy call does not mirror changes
        self.assertEqual(len(diff), 0)

        # Canary warning if the known list of legacy template ids diffs from legacy api call
        static_ids = {t for t in self.API.DATABASE_TEMPLATES_NAMEID.values()}
        diff = static_ids ^ old
        self.assertEqual(len(diff), 0)

    def test_ip_address_allow(self) -> None:
        '''Whitelist ip address.'''

        self.database_ensure_exist()
        db: Dict[str, Any] = self.API.account_storage_device(type='postgres_db')
        resp: Dict[str, str] = self.API.ip_address_allow(database_name=db['name'], ip='127.0.0.0')

        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'accepted')
        self.assertIn('five-minute delay', resp['message'])

    def test_ip_address_allow_invalid(self) -> None:
        '''Unable to whitelist, ip address is invalid.'''

        self.database_ensure_exist()
        db: Dict[str, Any] = self.API.account_storage_device(type='postgres_db')
        r: Dict[str, Any] = self.API.ip_address_allow(database_name=db['name'], ip='alpha.0.0.0')
        resp: dict = r['resp'].json()
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')
        self.assertEqual(resp['result'], 'error')

    def test_ip_address_allowed(self) -> None:
        '''Ip address is whitelisted.'''

        self.database_ensure_exist()
        db: Dict[str, Any] = self.API.account_storage_device(type='postgres_db')
        resp: Dict[str, Any] = self.API.ip_address_allowed(database_name=db['name'], ip='127.0.0.0')
        self.assertIsInstance(resp['allowed'], bool)
        self.assertIsInstance(resp['ip'], str)
        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['allowed'], True)
        self.assertEqual(resp['ip'], '127.0.0.0')
        self.assertEqual(resp['result'], 'success')
        self.assertIn('is in the firewall', resp['message'])

    def test_ip_address_allowed_invalid(self) -> None:
        '''Ip address is invalid.'''

        self.database_ensure_exist()
        db: Dict[str, Any] = self.API.account_storage_device(type='postgres_db')
        r: Dict[str, Any] = self.API.ip_address_allowed(database_name=db['name'], ip='alpha.0.0.0')
        resp: dict = r['resp'].json()

        self.assertIsInstance(resp['message'], str)
        self.assertIsInstance(resp['result'], str)
        self.assertEqual(resp['message'], 'ipAddress is missing or invalid')

    def test_ip_address_is(self) -> None:
        '''Identify external IP4 address.'''

        ip: str = self.API.ip_address_is()
        pat = r'^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$'
        valid_ip4 = bool(fullmatch(pat, ip))
        self.assertTrue(valid_ip4)
        ipq: str = self.API._ip_address_is_quick()
        self.assertEqual(ip, ipq)

    def test_onedrive_push(self) -> None:
        '''Push optilogic files to onedrive.'''

        with self.assertRaises(NotImplementedError):
            self.API.onedrive_push('fakeFilePath')

        return  # OE-7039 API: OneDrive Push Broke

        # does account even have onedrive storage?
        if self.API.storagetype_onedrive_exists is False:
            self.skipTest('OneDrive device not available')

        # storage device info cached, grab the first onedrive device name
        all_storage_devices: Dict[str, Any] = self.API.account_storage_devices()
        onedrive_devices = [d for d in all_storage_devices['storages'] if d['type'] == 'onedrive']

        # upload a file to onedrive device
        file_contents: str = f'{datetime.now()} unittest test_onedrive_push {time.time()}'
        file_path: str = f"/{onedrive_devices[0]['name']}/unittest.txt"
        self.API.wksp_file_upload('Studio', file_path, overwrite=True, filestr=file_contents)

        # initiate push to onedrive
        resp = self.API.onedrive_push(file_path)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['storageId'], str)
        self.assertIsInstance(resp['storageName'], str)
        self.assertTrue(resp['storageId'], onedrive_devices[0]['id'])
        self.assertTrue(resp['storageName'], onedrive_devices[0]['name'])

    def test_secret_add(self) -> None:
        '''Create a new secret.'''

        nano_secs: str = str(time.perf_counter_ns())
        cat: str = 'geocode'
        desc: str = f'unittest {nano_secs}'
        for provider in self.API.GEO_PROVIDERS:
            meta_dict: dict = {'isDefault': False, 'provider': provider}
            meta_str: str = dumps(meta_dict)
            name: str = f'ut_{provider}_{nano_secs}'
            value: str = str(uuid4())

            resp = self.API.secret_add(name, value, cat, desc, meta=meta_str)
            self.assertIsInstance(resp['created'], str)
            self.assertIsInstance(resp['description'], str)
            self.assertIsInstance(resp['id'], str)
            self.assertIsInstance(resp['meta'], str)
            self.assertIsInstance(resp['name'], str)
            self.assertIsInstance(resp['result'], str)
            self.assertIsInstance(resp['type'], str)
            self.assertIsInstance(resp['value'], str)
            self.assertEqual(resp['description'], desc)
            self.assertEqual(resp['meta'], meta_str)
            self.assertEqual(resp['name'], name)
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['type'], cat)
            self.assertEqual(resp['value'], value)
            self.assertTrue(resp['created'].endswith('Z'))
            dt: datetime = parse(resp['created'])
            self.assertTrue(dt.tzname(), 'UTC')
            now: datetime = datetime.utcnow()
            self.assertEqual(dt.year, now.year)
            self.assertEqual(dt.month, now.month)
            self.assertEqual(dt.day, now.day)

    def test_secret_alter(self) -> None:
        '''Modify a secret.'''

        secrets = self.API._secret_select_all(desc='unittest')  # no values returned, too sensitive
        if len(secrets) < 4:
            self.skipTest('must first run method test_secret_add')

        sec: dict = {}
        name: str = ''
        for secret in secrets:
            if secret['name'].find('bing') > -1:
                sec = secret
                name = secret['name']
                break

        secret = self.API.secret(name)
        newname: str = 'ut_altered'

        resp = self.API.secret_update(name, new_name=newname)
        self.assertEqual(resp['created'], sec['created'])
        self.assertEqual(resp['id'], sec['id'])
        self.assertEqual(resp['description'], sec['description'])
        self.assertEqual(resp['meta'], sec['meta'])
        self.assertEqual(resp['name'], newname)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['type'], sec['type'])

        old = self.API.secret(name)
        self.assertTrue(old['crash'])
        d: dict = loads(old['response_body'])
        self.assertIsInstance(d, dict)
        self.assertEqual(d['result'], 'error')
        self.assertGreater(d['message'].find('no secret found'), -1)
        self.assertEqual(secret['value'], resp['value'])

        new = self.API.secret('ut_altered')
        self.assertEqual(resp['id'], new['id'])
        self.assertEqual(resp['name'], newname)

    def test_secrets(self) -> None:
        '''Check all secrets.'''

        resp = self.API.secrets()
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['secrets'], list)
        self.assertGreaterEqual(len(resp['secrets']), 1)

        for s in resp['secrets']:
            self.assertIsInstance(s['created'], str)
            self.assertEqual(len(s['created']), 24)
            self.assertIsInstance(s['id'], str)
            self.assertEqual(len(s['id']), 36)
            self.assertTrue(bool(fullmatch(self.API.re_uuid4, s['id'], flags=2)))
            self.assertIsInstance(s['name'], str)
            self.assertGreater(len(s['name']), 0)

            if s.get('description'):
                self.assertIsInstance(s['description'], str)
            if s.get('meta'):
                self.assertIsInstance(s['meta'], str)
            if s.get('type'):
                self.assertIsInstance(s['type'], str)

            dt: datetime = parse(s['created'])
            self.assertTrue(dt.tzname(), 'UTC')

    def test_secrets_exist(self) -> None:
        '''Check newly created unittest secrets.'''

        nil = 'does_not_exist'
        ut = 'unittest'
        geo = 'geocode'

        secrets: List[Dict[str, Any]] = self.API._secret_select_all(category=geo, desc=ut)
        if len(secrets) < 4:
            self.skipTest('must first run method test_secret_add')

        self.assertGreaterEqual(len(secrets), 4)
        for s in secrets:
            d: Dict[str, Any] = loads(s['meta'])
            self.assertIsInstance(d, dict)
            self.assertEqual(len(d.keys()), 2)
            self.assertIsInstance(d['isDefault'], bool)
            self.assertFalse(d['isDefault'])
            self.assertIsInstance(d['provider'], str)
            self.assertIn(d['provider'], self.API.GEO_PROVIDERS)

            dt: datetime = parse(s['created'])
            self.assertLess(time.time() - dt.timestamp(), 3600)

            self.assertGreater(s['name'].find('ut'), -1)
            self.assertGreater(s['description'].find(ut), -1)

        self.assertFalse(self.API._secret_exist(name=nil, category=geo, desc=ut))
        self.assertFalse(self.API._secret_exist(name=nil, category=geo))
        self.assertFalse(self.API._secret_exist(name=nil, desc=ut))
        self.assertFalse(self.API._secret_exist(name=nil))
        self.assertFalse(self.API._secret_exist(category=nil))
        self.assertFalse(self.API._secret_exist(desc=nil))

        self.assertTrue(self.API._secret_exist(category=geo, desc=ut))
        self.assertTrue(self.API._secret_exist(category=geo))
        self.assertTrue(self.API._secret_exist(desc=ut))

    def test_secrets_remove(self) -> None:
        '''Remove all unittest secrets.'''

        secrets: List[Dict[str, Any]] = self.API._secret_select_all(desc='unittest')
        # BUG Caching and secret alter is causing this to fail
        for s in secrets:
            resp = self.API.secret_delete(s['name'])
            self.assertEqual(resp['result'], 'success')
            self.assertEqual(resp['id'], s['id'])
            self.assertEqual(resp['name'], s['name'])

    def test_sql_connect_info(self) -> None:
        '''Get the connection information for a sql storage item.'''

        self.database_ensure_exist()
        pg = self.API.account_storage_device('postgres_db')
        resp = self.API.sql_connection_info(pg['name'])
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['raw']), 6)
        self.assertIsInstance(resp['raw']['host'], str)
        self.assertTrue(
            resp['raw']['host'].endswith('postgres.database.azure.com')
            or resp['raw']['host'].endswith('database.optilogic.app')
        )
        self.assertIsInstance(resp['raw']['dbname'], str)
        self.assertIsInstance(resp['raw']['password'], str)
        self.assertIsInstance(resp['raw']['port'], int)
        self.assertIsInstance(resp['raw']['sslmode'], str)
        self.assertIsInstance(resp['raw']['user'], str)
        self.assertIsInstance(resp['connectionStrings'], dict)
        self.assertEqual(len(resp['connectionStrings']), 5)
        self.assertTrue(resp['connectionStrings']['jdbc'].startswith('jdbc:postgresql://'))
        self.assertTrue(resp['connectionStrings']['libpq'].startswith('host='))
        self.assertTrue(resp['connectionStrings']['net'].startswith('Server='))
        self.assertTrue(resp['connectionStrings']['psql'].startswith('psql \'host='))
        self.assertTrue(resp['connectionStrings']['url'].startswith('postgresql://'))

    def test_storage(self) -> None:
        '''Perform storage device info on every device from storage device list.'''

        devices = self.API.account_storage_devices()
        self.assertEqual(devices['result'], 'success')
        with self.subTest():
            for device in devices['storages']:
                resp: Dict[str, Any] = self.API.storage(device['name'])
                d = OrderedDict(sorted(resp.items()))
                self.assertEqual(d['result'], 'success')
                if d['type'] == 'azure_afs':
                    self.assertEqual(len(d), 17)
                    self.storage_azure_afs(d)
                if d['type'] == 'azure_workspace':
                    self.assertEqual(len(d), 18)
                    self.storage_azure_workspace(d)
                elif d['type'] == 'onedrive':
                    self.assertEqual(len(d), 20)
                    self.storage_onedrive(d)
                    self.assertIsInstance(d['connected'], bool)
                elif d['type'] == 'postgres_db':
                    # storage item contains an additional result key
                    self.assertEqual(len(d), 25)
                    self.storage_database(d)

    def test_storage_attr(self) -> None:
        '''Device attributes: annotations, label, and tag.'''

        attrs: Tuple[Literal['annotations'], Literal['labels'], Literal['tags']] = (
            'annotations',
            'labels',
            'tags',
        )
        devices: Dict[str, Any] = self.API.account_storage_devices()
        self.assertEqual(devices['result'], 'success')
        with self.subTest():
            for d in devices['storages']:
                for a in attrs:
                    resp: Dict[str, Any] = self.API._storage_attr(d['name'], a)
                    self.assertEqual(resp['result'], 'success')
                    self.assertEqual(len(resp.keys()), 2)
                    self.assertTrue(a in resp.keys())
                    if a == 'tags':
                        self.assertIsInstance(resp[a], str)
                    else:
                        self.assertIsInstance(resp[a], dict)

    @unittest.skip('api has not implemented')
    def test_storage_disk_create(self):
        '''Create a new file storage device.'''

        raise NotImplementedError

    @unittest.skip('api is incomplete')
    def test_storage_delete(self):
        '''Delete storage device.'''

        raise NotImplementedError

    def test_sql_query(self) -> None:
        '''Test sql statement execution.'''

        self.database_ensure_exist()
        pg = self.API.account_storage_device(type='postgres_db')
        resp = self.API.sql_query(
            database_name=pg['name'], query='SELECT datname FROM pg_database;'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['rowCount'], int)
        self.assertGreaterEqual(resp['rowCount'], 1)
        self.assertIsInstance(resp['queryResults'], list)
        self.assertGreaterEqual(len(resp['queryResults']), 1)

    def test_util_env(self) -> None:
        '''Atlas and andromeda common environment variables.'''

        keys: Tuple[str, ...] = (
            'job_cmd',
            'job_dir',
            'job_key',
            'job_api',
            'job_img',
            'pip_ver',
            'py_ver',
        )
        d = self.API.util_environment()
        for k in d.keys():
            self.assertTrue(k in keys)
            self.assertIsInstance(d[k], str)

    def test_util_job_monitor_bad(self) -> None:
        '''Job monitor check invalid job key or job state.'''

        # invalid job state
        with self.assertRaises(ValueError):
            self.API.util_job_monitor(self.WKSP, '5633e372-337a-454c-aae4-10084ea5bac6', 'invalid')  # type: ignore
        # invalid job key
        with self.assertRaises(ValueError):
            self.API.util_job_monitor(self.WKSP, '')
        with self.assertRaises(ValueError):
            self.API.util_job_monitor(self.WKSP, 'invalid')
        with self.assertRaises(ValueError):
            self.API.util_job_monitor(self.WKSP, '633e372-337a-454c-aae4-10084ea5bac6')
        # valid but job key does not exist
        resp: bool = self.API.util_job_monitor(self.WKSP, '00000000-0000-0000-0000-000000000000')
        self.assertFalse(resp)

    def test_wksp_file_copy(self) -> None:
        '''Make a copy of a file within a workspace.'''

        src: str = self.py_sleep
        dest: str = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_copy(
            self.WKSP, file_path_src=src, file_path_dest=dest, overwrite=True
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['copyStatus'], 'success')
        self.assertEqual(resp['message'], 'Copy complete')
        src_result: str = (
            f"{resp['sourceFileInfo']['directoryPath']}/{resp['sourceFileInfo']['filename']}"
        )
        dest_result: str = (
            f"{resp['targetFileInfo']['directoryPath']}/{resp['targetFileInfo']['filename']}"
        )
        self.assertEqual(src, src_result)
        self.assertEqual(dest, dest_result)

    def test_wksp_file_delete(self) -> None:
        '''Delete a copied file with a workspace.'''

        f: str = f'{self.dir_testdata_remote}/cp_test.txt'
        resp = self.API.wksp_file_delete(self.WKSP, file_path=f)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'File deleted')
        file_result = f"{resp['fileInfo']['directoryPath']}/{resp['fileInfo']['filename']}"
        self.assertEqual(f, file_result)

    def test_wksp_file_download(self) -> None:
        '''Download a file from a given workspace.'''

        download = self.API.wksp_file_download(self.WKSP, file_path=self.py_sleep)
        self.assertGreaterEqual(len(download), 1)
        self.assertIsInstance(download, str)

    def test_wksp_file_download_crash(self) -> None:
        '''Download a file from a given workspace.'''

        resp: str = self.API.wksp_file_download(self.WKSP, file_path='does_not_exist')
        self.assertIsInstance(resp, str)
        r: dict = loads(resp)
        self.assertEqual(r['result'], 'error')
        self.assertIsInstance(r['error'], str)
        self.assertEqual(len(r['correlationId']), 36)

    def test_wksp_file_download_meta(self) -> None:
        '''File metadata.'''

        resp = self.API.wksp_file_download_status(self.WKSP, file_path=self.py_sleep)
        self.assertEqual(resp['result'], 'success')
        keys: Tuple[str, ...] = (
            'result',
            'workspace',
            'filename',
            'directoryPath',
            'filePath',
            'lastModified',
            'contentLength',
            'date',
            'fileCreatedOn',
            'fileLastWriteOn',
            'fileChangeOn',
        )
        for key in resp.keys():
            self.assertIn(key, keys)
        self.assertEqual(resp['filePath'], self.py_sleep)
        self.assertEqual(resp['workspace'], self.WKSP)
        self.assertIsInstance(resp['contentLength'], int)
        dt: datetime = parse(resp['lastModified'])
        self.assertEqual(dt.tzname(), 'UTC')

    def test_wksp_file_upload(self) -> None:
        '''Upload a file to a workspace.'''

        dest: str = f'{self.dir_testdata_remote}/str2file.txt'
        resp = self.API.wksp_file_upload(
            self.WKSP, file_path_dest=dest, overwrite=True, filestr='test'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertIn(resp['message'], ['File created', 'File replaced'])

    def test_wksp_files(self) -> None:
        '''File structure from a given workspace and must have at least one file.'''

        resp = self.API.wksp_files(self.WKSP)
        self.assertEqual(resp['result'], 'success')
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['files'], list)
        self.assertGreaterEqual(len(resp['files']), 1)
        self.assertTrue(resp['files'][0].get('filename'))
        self.assertTrue(resp['files'][0].get('directoryPath'))
        self.assertTrue(resp['files'][0].get('filePath'))
        self.assertTrue(resp['files'][0].get('contentLength'))

    def test_wksp_folder_delete(self) -> None:
        '''Delete a folder from a workspace.'''

        folder: str = 'delete_me_now'
        fp: str = os.path.join(folder, 'delete_me.txt')
        self.API.wksp_file_upload(self.WKSP, fp, filestr='first file line')
        resp = self.API.wksp_folder_delete(self.WKSP, dir_path=folder, force=True)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Directory and all contents deleted')
        self.assertEqual(resp['directoryPath'], folder)

    def test_wksp_info(self) -> None:
        '''Properties of a given workspace.'''

        resp = self.API.wksp_info(self.WKSP)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['name'], self.WKSP)
        self.assertEqual(len(resp['key']), 25)
        self.assertRegex(resp['key'], '^workspace')
        self.assertIn(resp['stack'], ['Optilogic', 'Simulation', 'Gurobi'])
        self.assertTrue(resp['status'].isupper())

    def test_wksp_job_back2back(self) -> None:
        '''One job to run many python modules in a row.'''

        item_one: dict = {
            'pyModulePath': '/projects/quick_tests/sleep.py',
            'commandArgs': 'not_used',
            'timeout': 90,
        }
        item_two: dict = {
            'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py',
            'timeout': 30,
        }
        batch = {'batchItems': [item_one, item_two]}

        tag: str = 'unittest_batch_back2back'
        resp = self.API.wksp_job_back2back(self.WKSP, batch=batch, verboseOutput=True, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 1)

        # batchItems
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pyModulePath'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])

        # jobInfo
        andromeda_configs: Dict[str, Any] = self.API.andromeda_machine_configs()
        cfg_name: str = andromeda_configs['defaultConfigName']
        cfg_run_rate: Number = next(
            cfg['runRate']
            for cfg in andromeda_configs['resourceConfigs']
            if cfg['name'] == cfg_name
        )

        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WKSP)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], cfg_name)
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], cfg_run_rate)

        # verify new batch job
        job = self.API.wksp_job_status(self.WKSP, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WKSP)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pyModulePath'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pyModulePath'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], cfg_name)
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], cfg_run_rate)

    def test_wksp_job_back2back_findnrun(self) -> None:
        '''Search file paths yields one job to run many python modules in a row.'''

        item_one: dict = {
            'pySearchTerm': '/projects/quick_tests/sleep.py',
            'commandArgs': 'not_used',
            'timeout': 90,
        }
        item_two: dict = {
            'pySearchTerm': '/projects/quick_tests/airline_hub_location_cbc.py',
            'timeout': 30,
        }
        batch = {'batchItems': [item_one, item_two]}

        tag: str = 'unittest_batch_back2back_find'
        resp = self.API.wksp_job_back2back_findnrun(
            self.WKSP, batch=batch, verboseOutput=True, tags=tag
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp), 5)
        self.assertEqual(resp['message'], 'Job submitted')
        self.assertIsInstance(resp['jobKey'], str)
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['batch'], dict)
        self.assertEqual(len(resp['batch']), 2)
        self.assertTrue(resp['batch']['search'])

        # batchItems
        self.assertIsInstance(batch['batchItems'], list)
        self.assertEqual(len(batch['batchItems']), 2)
        # item_one
        self.assertIsInstance(resp['batch']['batchItems'][0], list)
        self.assertEqual(len(resp['batch']['batchItems'][0]), 3)
        self.assertEqual(resp['batch']['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(resp['batch']['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(resp['batch']['batchItems'][0][2], item_one['timeout'])
        # item_two
        self.assertIsInstance(resp['batch']['batchItems'][1], list)
        self.assertEqual(len(resp['batch']['batchItems'][1]), 3)
        self.assertEqual(resp['batch']['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertIsNone(resp['batch']['batchItems'][1][1])
        self.assertEqual(resp['batch']['batchItems'][1][2], item_two['timeout'])

        # jobInfo
        andromeda_configs: Dict[str, Any] = self.API.andromeda_machine_configs()
        cfg_name: str = andromeda_configs['defaultConfigName']
        cfg_run_rate: Number = next(
            cfg['runRate']
            for cfg in andromeda_configs['resourceConfigs']
            if cfg['name'] == cfg_name
        )

        self.assertIsInstance(resp['jobInfo'], dict)
        self.assertEqual(len(resp['jobInfo']), 4)
        self.assertEqual(resp['jobInfo']['workspace'], self.WKSP)
        self.assertEqual(resp['jobInfo']['tags'], tag)
        self.assertEqual(resp['jobInfo']['timeout'], -1)
        self.assertIsInstance(resp['jobInfo']['resourceConfig'], dict)
        self.assertEqual(len(resp['jobInfo']['resourceConfig']), 4)
        self.assertEqual(resp['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(resp['jobInfo']['resourceConfig']['name'], cfg_name)
        self.assertEqual(resp['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(resp['jobInfo']['resourceConfig']['run_rate'], cfg_run_rate)

        # verify new batch job
        job = self.API.wksp_job_status(self.WKSP, resp['jobKey'])
        self.assertEqual(job['jobInfo']['workspace'], self.WKSP)
        self.assertEqual(job['jobInfo']['directoryPath'], '/usr/bin')
        self.assertEqual(job['jobInfo']['filename'], 'batch_search_n_run.py')
        self.assertEqual(job['jobInfo']['command'], 'run')
        self.assertIsInstance(job['jobInfo']['commandArgs'], str)
        args: dict = loads(job['jobInfo']['commandArgs'][1:-1])
        self.assertIsInstance(args, dict)
        self.assertIsInstance(args['batchItems'], list)
        self.assertEqual(args['batchItems'][0][0], item_one['pySearchTerm'])
        self.assertEqual(args['batchItems'][0][1], item_one['commandArgs'])
        self.assertEqual(args['batchItems'][0][2], item_one['timeout'])
        self.assertEqual(args['batchItems'][1][0], item_two['pySearchTerm'])
        self.assertEqual(args['batchItems'][1][1], item_two.get('commandArgs'))
        self.assertEqual(args['batchItems'][1][2], item_two['timeout'])
        self.assertEqual(job['jobInfo']['resourceConfig']['cpu'], '1vCore')
        self.assertEqual(job['jobInfo']['resourceConfig']['name'], cfg_name)
        self.assertEqual(job['jobInfo']['resourceConfig']['ram'], '2Gb')
        self.assertEqual(job['jobInfo']['resourceConfig']['run_rate'], cfg_run_rate)

    def test_wksp_job_file_error(self) -> None:
        '''Get job error file.'''

        resp: str = self.API.wksp_job_file_error(self.WKSP, self.API._job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err: dict = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_file_result(self) -> None:
        '''Get job result file.'''

        resp: str = self.API.wksp_job_file_result(self.WKSP, self.API._job_start_recent_key)
        self.assertIsInstance(resp, str)
        if resp.startswith('{\"result\":\"error\"'):
            err: dict = loads(resp)
            self.assertEqual(err['result'], 'error')
            self.assertIsInstance(err['error'], str)
            self.assertIsInstance(err['correlationId'], str)
            self.assertEqual(len(err['correlationId']), 36)
        else:
            self.assertGreater(len(resp), 0)

    def test_wksp_job_ledger(self) -> None:
        '''Get job ledger that has realtime messages.'''

        # Job.add_record method expects param message of type str
        # sidecar.py during job runtime emits messages that are not type str to test
        type_tup = (
            bool(1),
            int(1),
            float(1),
            [1],
            (1, 2),
            {1: 2},
            {1, 2},
            b'101',
        )
        # str version of object, ie int(1) == '1'
        type_strs: List[str] = sorted([t.__str__() for t in type_tup])

        job = self.API.wksp_job_start(
            self.WKSP,
            self.py_sidecar,
            resourceConfig='mini',
            tags='unittest',
            preview_image=True,  # TODO drop preview_image
        )
        res: bool = self.API.util_job_monitor(self.WKSP, job['jobKey'], stop_when='done')
        self.assertTrue(res)

        resp = self.API.wksp_job_ledger(self.WKSP, job['jobKey'])
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)

        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)

        # assert non str types messages cast to str by verifying the job ledger
        type_msgs: List[str] = sorted([r['message'] for r in resp['records'] if r['key'] == 'type'])
        self.assertEqual(len(type_strs), len(type_msgs))

        for r in resp['records']:
            self.assertIsInstance(r['timestamp'], int)
            self.assertIsInstance(r['datetime'], str)

            # job was created during init, assert same day
            self.assertTrue(r['datetime'].endswith('Z'))
            dt: datetime = parse(r['datetime'])
            self.assertTrue(dt.tzname(), 'UTC')
            now: datetime = datetime.utcnow()
            self.assertEqual(dt.year, now.year)
            self.assertEqual(dt.month, now.month)
            self.assertEqual(dt.day, now.day)

            self.assertIsInstance(r['key'], str)
            self.assertIsInstance(r['message'], str)
            self.assertIn(r['key'], ('eta', 'type', '96k'))
            if r['key'] == '96k':
                self.assertEqual(len(r['message']), 32_000)  # OE-8083 truncate

    def test_wksp_job_metrics(self) -> None:
        '''Get one second cpu and memory sampling of a job.'''

        if len(self.__jobkey_quick) == 0:
            self.job_prereq()
        resp = self.API.wksp_job_metrics(self.WKSP, self.__jobkey_quick)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertGreaterEqual(resp['count'], 1)
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], Number)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], float)
        self.assertIsInstance(resp['max']['cpuAvailable'], Number)
        self.assertIsInstance(resp['max']['processCount'], int)
        self.assertIsInstance(resp['records'], list)
        self.assertGreaterEqual(len(resp['records']), 1)
        self.assertIsInstance(resp['records'][0]['timestamp'], int)
        self.assertIsInstance(resp['records'][0]['datetime'], str)
        self.assertTrue(resp['records'][0]['datetime'].endswith('Z'))
        dt: datetime = parse(resp['records'][0]['datetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIsInstance(resp['records'][0], dict)
        self.assertIsInstance(resp['records'][0]['cpuAvailable'], Number)
        self.assertIsInstance(resp['records'][0]['cpuPercent'], float)
        self.assertIsInstance(resp['records'][0]['cpuUsed'], float)
        self.assertIsInstance(resp['records'][0]['memoryAvailable'], int)
        self.assertIsInstance(resp['records'][0]['memoryPercent'], float)
        self.assertIsInstance(resp['records'][0]['memoryResident'], float)
        self.assertIsInstance(resp['records'][0]['processCount'], int)

    def test_wksp_job_metrics_max(self) -> None:
        '''Get peak cpu and memory stats of a job.'''

        if len(self.__jobkey_quick) == 0:
            self.job_prereq()
        resp = self.API.wksp_job_metrics_max(self.WKSP, self.__jobkey_quick)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['max'], dict)
        self.assertEqual(len(resp['max']), 7)
        self.assertIsInstance(resp['max']['memoryPercent'], float)
        self.assertIsInstance(resp['max']['memoryResident'], float)
        self.assertIsInstance(resp['max']['memoryAvailable'], int)
        self.assertIsInstance(resp['max']['cpuPercent'], float)
        self.assertIsInstance(resp['max']['cpuUsed'], Number)
        self.assertIsInstance(resp['max']['cpuAvailable'], Number)
        self.assertIsInstance(resp['max']['processCount'], int)

    def test_wksp_job_metrics_mia(self) -> None:
        '''OE-5276 Job Metrics are Missing Sometimes.
        OE-5369 Job Metrics Missing v3.
        '''

        # spin up a few jobs to create load and evaluate all
        jobs_max: int = 9
        tag_time: float = time.time()
        tag: str = f'metrics_{tag_time}'
        secs: int = 20
        d: dict = {}  # store job key and elapsed time without metrics
        for job in range(jobs_max):
            resp = self.API.wksp_job_start(
                self.WKSP, self.py_sleep, tags=tag, timeout=secs, resourceConfig='mini'
            )
            if resp.get('crash'):
                print(resp)
                jobs_max -= 1
                continue
            d[resp['jobKey']] = {'seen_first': None, 'missing_last': None}

        # check the jobs that are about to run
        metrics_missing = False
        check: bool = True
        while check:
            # stop if all jobs finished
            jobs: Dict[str, Any] = self.API.wksp_jobs(self.WKSP, tags=tag)
            terminal: int = 0
            for t in self.API.JOBSTATES_TERMINAL:
                terminal += jobs['statusCounts'].get(t)
            if terminal == jobs_max:
                check = False
                break

            # check running jobs for metrics
            active: Dict[str, Any] = self.API.wksp_jobs(self.WKSP, status='running', tags=tag)
            for job in active['jobs']:
                # elapsed run time
                st: str = str(job['startDatetime'])
                st = st.replace('T', ' ')
                st = st.replace('Z', '')
                job_start: datetime = datetime.fromisoformat(st)
                now: datetime = datetime.utcnow()
                delta: timedelta = now - job_start

                # first time observed the job was running
                if d[job['jobKey']].get('seen_first') is None:
                    d[job['jobKey']]['seen_first'] = str(delta)

                # check for metrics
                resp: Dict[str, Any] = self.API.wksp_job_metrics(self.WKSP, job['jobKey'])
                self.assertEqual(resp['result'], 'success')
                self.assertIsInstance(resp['count'], int)

                # missing metrics?
                if resp['count'] == 0:
                    metrics_missing = True
                    d[job['jobKey']]['missing_last'] = str(delta)
                    print(f"{str(delta)} secs elapsed, metrics missing for job {job['jobKey']}")
                    with self.subTest():
                        self.assertLess(delta.total_seconds(), 10)

        if metrics_missing:
            print('\n\nTEST_WKSP_JOB_METRICS_MIA')
            print(f"\n\nJob Submitted: {jobs_max}, Job Duration: {secs}, Job Tag: {tag}")
            for item in d.items():
                print(item)

    def test_wksp_job_start(self) -> None:
        '''Creating a job.'''

        resp = self.API.wksp_job_start(
            self.WKSP, file_path=self.py_sleep, tags='unittest_start', resourceConfig='mini'
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        job_info_keys: Tuple[str, ...] = (
            'workspace',
            'directoryPath',
            'filename',
            'command',
            'resourceConfig',
            'tags',
            'timeout',
        )
        for key in resp['jobInfo'].keys():
            self.assertIn(key, job_info_keys)

    def test_wksp_job_start_preview(self) -> None:
        '''Create a job using andromeda preview image and compare to stable.'''

        job_preview: Dict[str, Any] = self.API.wksp_job_start(
            self.WKSP,
            file_path=self.py_bash,
            commandArgs="'pip list -v --format json'",
            resourceConfig='mini',
            tags='unittest',
            preview_image=True,
        )
        self.assertEqual(job_preview['result'], 'success')

        job_stable: Dict[str, Any] = self.API.wksp_job_start(
            self.WKSP,
            file_path=self.py_bash,
            commandArgs="'pip list -v --format json'",
            resourceConfig='mini',
            tags='unittest',
            preview_image=False,
        )
        self.assertEqual(job_stable['result'], 'success')

        done: bool = self.API.util_job_monitor(
            self.WKSP, job_key=job_preview['jobKey'], stop_when='done'
        )
        self.assertTrue(done)

        # preview image
        std_out: str = self.API.wksp_job_file_result(self.WKSP, job_preview['jobKey'])
        self.assertIsInstance(std_out, str)
        jsn: List[Dict[str, str]] = self.deserialize_pip_output(std_out)
        pkgs_preview: Dict[str, Dict[str, str]] = {d['name']: d for d in jsn}
        self.assertRegex(pkgs_preview['anura']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['costtoserve']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['dendro']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['frogspawn']['version'], r'2\.[6-7]\.\d+')
        self.assertRegex(pkgs_preview['hopper']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['neo']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['optiengines']['version'], r'0\.\d\.\d+')
        self.assertRegex(pkgs_preview['optilogic']['version'], r'2\.[8-9]\.\d')
        self.assertRegex(pkgs_preview['riskrating']['version'], r'2\.7\.\d+')
        self.assertRegex(pkgs_preview['scenarioexecution']['version'], r'1\.1\.([6-9]|1\d)')
        self.assertRegex(pkgs_preview['throg']['version'], r'2\.7\.\d+')

        # stable image
        done: bool = self.API.util_job_monitor(
            self.WKSP, job_key=job_stable['jobKey'], stop_when='done'
        )
        self.assertTrue(done)
        std_out: str = self.API.wksp_job_file_result(self.WKSP, job_stable['jobKey'])
        self.assertIsInstance(std_out, str)
        jsn = self.deserialize_pip_output(std_out)
        pkgs_stable: Dict[str, Dict[str, str]] = {d['name']: d for d in jsn}
        self.assertRegex(pkgs_stable['anura']['version'], r'2\.6\.([3][6-9]|4\d)')
        self.assertRegex(pkgs_stable['costtoserve']['version'], r'2\.6\.([2][4-9]|4\d)')
        self.assertRegex(pkgs_stable['dendro']['version'], r'2\.6\.([6-9]|1\d)')
        self.assertRegex(pkgs_stable['frogspawn']['version'], r'2\.6\.(\d|1\d)')
        self.assertRegex(pkgs_stable['neo']['version'], r'2\.6\.(1[8-9]|2\d)')
        self.assertRegex(pkgs_stable['optiengines']['version'], r'0\.\d\.\d+')
        self.assertRegex(pkgs_stable['optilogic']['version'], r'2\.[8-9]\.\d')
        self.assertRegex(pkgs_stable['riskrating']['version'], r'2\.6\.(9|1\d)')
        self.assertRegex(pkgs_stable['scenarioexecution']['version'], r'1\.1\.([3-9]|1\d)')
        self.assertRegex(pkgs_stable['throg']['version'], r'2\.6\.(9|1\d)')

        diff: Dict[str, str] = {}
        for pkg in pkgs_stable:
            if pkgs_preview.get(pkg) is None:
                diff[pkg] = 'not found in preview image'
            elif pkgs_stable[pkg]['version'] != pkgs_preview[pkg]['version']:
                diff[pkg] = f"{pkgs_stable[pkg]['version']} != {pkgs_preview[pkg]['version']}"
        if diff:
            # diffs are expecting when preview image contains release candidates
            print(f'stable vs preview\n{dumps(diff, indent=2, sort_keys=True)}')

    def test_wksp_job_start_sample(self) -> None:
        '''Create job api call. The response time is the slow and fails often with 504s.'''

        max: int = int(self.API.account_info()['limits']['concurrentJobs'] * 0.5)
        min: int = 10
        job_count: int = max if max > min else min
        jobs: List[str] = []
        tag: str = 'unittest_job_speed'

        # start jobs
        for j in range(job_count):
            with self.subTest():
                resp = self.API.wksp_job_start(
                    self.WKSP, self.py_quick, tags=tag, resourceConfig='mini'
                )
                self.assertEqual(resp['result'], 'success')
            # d = {}
            # d['key'] = resp['jobKey']
            # jobs.append(d)
            # spin up a few jobs to create load and evaluate all

        return
        # what is current job count
        jobs_active: int = self.API._jobs_active
        jobs_max: int = self.API.account_info()['limits']['concurrentJobs']
        max: int = jobs_max - jobs_active if jobs_max > jobs_active else 0

        jobs_max: int = 9
        tag_time: float = time.time()
        tag: str = f'unittest_job_sample_{tag_time}'

        for job in range(jobs_max):
            self.API.wksp_job_start(self.WKSP, self.py_sleep, tags=tag)

        # check the jobs that are about to run
        d: dict = {}
        check: bool = True
        while check:
            jobs = self.API.wksp_jobs(self.WKSP, tags=tag)

            # jobs all finished?
            terminal: int = 0
            for t in self.API.JOBSTATES_TERMINAL:
                terminal += jobs['statusCounts'].get(t)

            if terminal == jobs_max:
                check = False
                break

            # check running jobs for metrics
            active = self.API.wksp_jobs(self.WKSP, status='running', tags=tag)

            if active['statusCounts']['running'] >= 1:
                for job in active['jobs']:
                    resp = self.API.wksp_job_metrics(self.WKSP, job['jobKey'])
                    self.assertEqual(resp['result'], 'success')
                    self.assertIsInstance(resp['count'], int)
                    # self.assertGreaterEqual(resp['count'], 1)

                    # missing metrics!
                    if resp['count'] == 0:
                        st: str = str(job['startDatetime'])
                        st = st.replace('T', ' ')
                        st = st.replace('Z', '')
                        job_start: datetime = datetime.fromisoformat(st)
                        now: datetime = datetime.utcnow()
                        delta: timedelta = now - job_start
                        d[job['jobKey']] = str(
                            delta
                        )  # store job key and elapsed time without metrics

                        print(
                            f"{str(delta)} secs elapsed and metrics missing for job {job['jobKey']}"
                        )
                        with self.subTest():
                            self.assertLess(delta.total_seconds(), 5)

            time.sleep(1)

        # were there any jobs that failed metric check?
        secs = 0
        if len(d) >= 1:
            print(f"\n\nJob Submitted: {jobs_max}, Job Duration: {secs}, Job Tag: {tag}")
            print('\n JobKey, LastSeenWithMissingMetricCount_RunDuration')
            for k in d.items():
                print(k[1], k[0])

    def test_wksp_job_status(self) -> None:
        '''Get job status for explicit state.'''

        resp = self.API.wksp_job_status(self.WKSP, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp['jobKey']), 36)
        self.assertIsInstance(resp['submittedDatetime'], str)
        self.assertTrue(resp['submittedDatetime'].endswith('Z'))
        dt: datetime = parse(resp['submittedDatetime'])
        self.assertTrue(dt.tzname(), 'UTC')
        now: datetime = datetime.utcnow()
        self.assertEqual(dt.year, now.year)
        self.assertEqual(dt.month, now.month)
        self.assertEqual(dt.day, now.day)
        self.assertIn(resp['status'], self.API.JOBSTATES)
        job_info_keys: Tuple[str, ...] = (
            'workspace',
            'directoryPath',
            'filename',
            'command',
            'errorFile',
            'resultFile',
            'resourceConfig',
            'tags',
            'timeout',
        )
        for key in resp['jobInfo'].keys():
            self.assertIn(key, job_info_keys)
        self.assertEqual(resp['jobInfo']['command'], 'run')
        self.assertIsInstance(resp['jobInfo']['errorFile'], bool)
        self.assertIsInstance(resp['jobInfo']['resultFile'], bool)
        resource_keys: Tuple[str, ...] = ('name', 'cpu', 'ram', 'run_rate')
        for key in resp['jobInfo']['resourceConfig']:
            self.assertIn(key, resource_keys)

    def test_wksp_job_stop(self) -> None:
        '''Stop a most recently created job.'''

        # guarantee a job is currently running
        resp = self.API.wksp_job_status(self.WKSP, self.API._job_start_recent_key)
        if resp['status'] in self.API.JOBSTATES_TERMINAL:
            resp = self.API.wksp_job_start(self.WKSP, self.py_sleep, resourceConfig='mini')
            success: bool = self.API.util_job_monitor(self.WKSP, resp['jobKey'])
            if success is False:
                self.skipTest('failed to start job within two minutes')

        # stop running job
        resp = self.API.wksp_job_stop(self.WKSP, self.API._job_start_recent_key)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['jobKey'], self.API._job_start_recent_key)
        keys: Tuple[str, ...] = ('result', 'message', 'jobKey', 'status', 'jobInfo')
        for key in resp.keys():
            self.assertIn(key, keys)

    def test_wksp_jobify(self) -> None:
        '''Batch queue many jobs.'''

        batch = {
            'batchItems': [
                {'pyModulePath': '/projects/quick_tests/sleep.py', 'timeout': 90},
                {
                    'pyModulePath': '/projects/quick_tests/airline_hub_location_cbc.py',
                    'timeout': 30,
                },
            ]
        }

        tag: str = 'unittest_batch_jobify'
        resp = self.API.wksp_jobify(self.WKSP, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobify_findnrun(self) -> None:
        '''Search file paths yields many jobs to run each python module found.'''

        batch = {
            'batchItems': [
                {'pySearchTerm': '^/quick_tests/sleep.py', 'timeout': 90},
                {'pySearchTerm': '^/quick_tests/airline_hub_location_cbc.py', 'timeout': 30},
            ]
        }

        tag: str = 'unittest_batch_jobify_find'
        resp = self.API.wksp_jobify_findnrun(self.WKSP, batch=batch, tags=tag)
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(resp['message'], 'Jobs submitted')
        self.assertIsInstance(resp['count'], int)
        self.assertEqual(len(batch['batchItems']), resp['count'])
        self.assertEqual(resp['count'], len(resp['jobKeys']))
        for key in resp['jobKeys']:
            self.assertIsInstance(key, str)
            self.assertEqual(len(key), 36)

    def test_wksp_jobs(self) -> None:
        '''List the jobs for a specific workspace.'''

        resp = self.API.wksp_jobs(self.WKSP)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys: Tuple[str, ...] = self.API.JOBSTATES
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys: Tuple[str, ...] = (
            'command',
            'history',
            'runSecsMax',
            'runSecsMin',
            'status',
            'tags',
        )
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

        self.assertGreaterEqual(len(resp['jobs']), 1)
        job_keys: Tuple[str, ...] = (
            'jobKey',
            'submittedDatetime',
            'startDatetime',
            'endDatetime',
            'runTime',
            'runRate',
            'billedTime',
            'status',
            'jobInfo',
            'waitTime',
        )
        for job in resp['jobs']:
            for key, value in job.items():
                self.assertIn(key, job_keys)
                if key.lower().find('datetime') > -1 and value:
                    with self.subTest():
                        dt: datetime = parse(value)
                        self.assertEqual(dt.tzname(), 'UTC')
                if key == 'jobInfo':
                    if job[key]['command'] == 'run':
                        self.assertIsInstance(job[key]['directoryPath'], str)
                        self.assertIsInstance(job[key]['filename'], str)
                    self.assertIsInstance(job[key]['resourceConfig'], dict)
                    self.assertIsInstance(job[key]['workspace'], str)

    def test_wksp_jobs_stats(self) -> None:
        '''Get the stats for jobs for a specific workspace.'''

        resp = self.API.wksp_jobs(self.WKSP)
        self.assertEqual(resp['result'], 'success')
        self.assertIsInstance(resp['count'], int)
        self.assertIsInstance(resp['statusCounts'], dict)

        status_keys: Tuple[str, ...] = self.API.JOBSTATES
        for status in resp['statusCounts']:
            self.assertIn(status, status_keys)
            self.assertGreaterEqual(resp['statusCounts'][status], 0)

        self.assertIsInstance(resp['tagCounts'], dict)
        self.assertIsInstance(resp['filters'], dict)

        filter_keys: Tuple[str, ...] = (
            'command',
            'history',
            'runSecsMax',
            'runSecsMin',
            'status',
            'tags',
        )
        for filter in resp['filters']:
            self.assertIn(filter, filter_keys)

    def test_wksp_share_file(self) -> None:
        '''Share a file from a workspace to all other workspaces of a user/self.'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')

        resp = self.API.wksp_share_file(
            self.WKSP, file_path=self.py_sleep, targetUsers=self.API.auth_username
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 8)
        self.assertIsInstance(resp['errored'], list)
        self.assertEqual(len(resp['errored']), 0)
        self.assertIsInstance(resp['erroredCount'], int)
        self.assertIsInstance(resp['jobs'], list)
        self.assertEqual(len(resp['jobs']), self.API.account_workspace_count - 1)
        for j in resp['jobs']:
            self.assertIsInstance(j['jobKey'], str)
            self.assertIsInstance(j['result'], str)
            self.assertEqual(j['result'], 'success')
        self.assertEqual(resp['jobsCount'], self.API.account_workspace_count - 1)
        self.assertIsInstance(resp['message'], str)
        self.assertEqual(resp['message'], 'Share Accepted')
        self.assertIsInstance(resp['sourceFileInfo'], dict)
        self.assertEqual(len(resp['sourceFileInfo'].keys()), 2)
        self.assertIsInstance(resp['sourceFileInfo']['directoryPath'], str)
        self.assertEqual(resp['sourceFileInfo']['directoryPath'], os.path.split(self.py_sleep)[0])
        self.assertIsInstance(resp['sourceFileInfo']['filename'], str)
        self.assertEqual(resp['sourceFileInfo']['filename'], os.path.split(self.py_sleep)[1])
        self.assertEqual(resp['targetUsers'], self.API.auth_username)

    def test_wksp_share_file_sample(self) -> None:
        '''OE-5840 API Share File/Folder Results in 500 Internal Server Error.'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')

        if self.API.account_workspace_count < 2:
            self.skipTest('account does not have required multi-workspaces needed for sharing')

        test_result: bool = False

        # get all not Studio workspaces
        resp: dict = self.API.account_workspaces()
        wksp_names: list[str] = [w['name'] for w in resp['workspaces'] if w['name'] != 'Studio']
        wksp_not_studio: str = wksp_names[0]

        # upload files to share
        filenames: list[str] = []
        filepaths: list[str] = []
        tag: int = time.perf_counter_ns()
        for x in range(10):
            filename: str = f'{tag}_{x}.txt'
            file_path: str = f'/My Files/{tag}/{filename}'
            file_contents: str = f'{datetime.now()} {tag}_{x} unittest test_wksp_share_file_sample'
            resp = self.API.wksp_file_upload('Studio', file_path, filestr=file_contents)
            if resp.get('crash'):
                print(f'{x} {filename} upload attempt failed')
                continue
            filenames.append(filename)
            filepaths.append(file_path)

        # verify uploaded files arrived
        up_arrived: bool = False
        up_count_verified: int = 0
        up_start: float = time.perf_counter()
        while up_arrived is False and time.perf_counter() - up_start < 30:
            resp = self.API.wksp_files('Studio', str(tag))
            if resp.get('crash'):
                continue

            up_count_verified = resp.get('count', 0)
            print(
                f'{tag} {up_count_verified}/{len(filepaths)} confirmed files uploaded {time.perf_counter() - up_start} secs'
            )
            if resp.get('count') == len(filepaths):
                up_arrived = True
                break
            time.sleep(2)

        if up_arrived is False:
            print(f'verify upload failed {len(filepaths)} - {up_count_verified} files missing')
            print('30 seconds not enough time to verify?')

        # share files to other workspaces
        files_failed_sharing: int = 0
        for fp in filepaths:
            resp = self.API.wksp_share_file('Studio', fp, targetUsers=self.API.auth_username)
            if resp.get('crash'):
                print(f'share crash skipping {fp}')
                files_failed_sharing += 1

        # verify shared files arrived to determine test case can pass
        share_arrived: bool = False
        start_share: float = time.perf_counter()
        # TODO verify file share arrived to all non studio workspaces
        diffs = set()
        while share_arrived is False and time.perf_counter() - start_share < 180:
            resp = self.API.wksp_files(wksp_not_studio, str(tag))
            filenames_verified: set[str] = {f['filename'] for f in resp['files']}
            diffs: set[str] = set(filenames).symmetric_difference(filenames_verified)
            if resp.get('count') == up_count_verified and len(diffs) == 0:
                share_arrived = True
                break
            elif resp.get('count', 0) > up_count_verified:
                # BUG there might be file share retry logic
                # 1156398951931738_1.txt failed to share due to 500/504 issue but it showed up 5mins later
                # 1156398951931738_1_2022-10-15T021756Z.txt server tried more than once and created a duplicate!
                break
            time.sleep(2)

        if share_arrived:
            test_result = True
        else:
            print(f'verify share file diff: {len(diffs)}\n{sorted(diffs)}')

        # cleanup: remove files used to share out
        self.API.wksp_folder_delete('Studio', f'My Files/{tag}', force=True)

        # cleanup: remove files shared to other workspaces
        share_folders: list[str] = ['Sent to Me', 'sent_to_me']
        for ws in wksp_names:
            for share_folder in share_folders:
                resp = self.API.wksp_files(ws, share_folder)
                if resp.get('count') == 0:
                    continue
                for fn in filenames:
                    self.API.wksp_file_delete(ws, f'{share_folder}/{self.API.auth_username}/{fn}')

        self.assertTrue(test_result)

    def test_wksp_share_folder(self) -> None:
        '''Share a subtree from a workspace to all other workspaces of a user/self.'''

        if self.API.auth_username is None:
            self.skipTest('test_wksp_share_folder requires a username')

        resp = self.API.wksp_share_folder(
            self.WKSP, dir_path=self.dir_testdata_remote, targetUsers=self.API.auth_username
        )
        self.assertEqual(resp['result'], 'success')
        self.assertEqual(len(resp.keys()), 8)
        self.assertIsInstance(resp['errored'], list)
        self.assertEqual(len(resp['errored']), 0)
        self.assertIsInstance(resp['erroredCount'], int)
        self.assertIsInstance(resp['jobs'], list)
        self.assertEqual(len(resp['jobs']), self.API.account_workspace_count - 1)
        for j in resp['jobs']:
            self.assertIsInstance(j['jobKey'], str)
            self.assertIsInstance(j['result'], str)
            self.assertEqual(j['result'], 'success')
        self.assertEqual(resp['jobsCount'], self.API.account_workspace_count - 1)
        self.assertIsInstance(resp['message'], str)
        self.assertEqual(resp['message'], 'Share Accepted')
        self.assertIsInstance(resp['sourceFileInfo'], dict)
        self.assertEqual(len(resp['sourceFileInfo'].keys()), 1)
        self.assertIsInstance(resp['sourceFileInfo']['directoryPath'], str)
        self.assertEqual(resp['sourceFileInfo']['directoryPath'], self.dir_testdata_remote)
        self.assertEqual(resp['targetUsers'], self.API.auth_username)


if __name__ == '__main__':
    # !! TODO update module docstring to set your user defaults !!
    # apikey replace YOUR_USERNAME, YOUR_PASSWORD
    # appkey replace YOUR_USERNAME, YOUR_APPLICATION_KEY, and set auth_legacy to False

    args: dict = docopt(__doc__)
    TestApi.APPKEY = args.get('--appkey')
    TestApi.AUTH_LEGACY = args.get('--authlegacy', '').lower() == 'true'
    TestApi.USERNAME = args.get('--user')
    TestApi.USERPASS = args.get('--pass')
    TestApi.WKSP = args.get('--wksp', 'Studio')
    unittest.main(__name__, argv=['main'])
