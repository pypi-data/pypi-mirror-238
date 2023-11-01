"""
This file contains the Manifest class,
which is used to download and extract the manifest from Bungie's servers.

Note:
    Most of the code is taken from:
        https://github.com/jgayfer/pydest/blob/master/pydest/dbase.py
"""
import json
import os
import sqlite3
import zipfile

import aiohttp
import async_timeout

from .dbase import DBase
from .utils.error import DestipyException

MANIFEST_ZIP = 'manifest_zip'

class Manifest:
    """
    This class downloads and extracts the manifest from Bungie's servers into a .content file.
    It also contains methods to decode hash ids into json objects but this should not be used directly.
    Instead, use the decode_hash method form the DestinyClient class.
    """
    def __init__(self, destiny2):
        self.manifest_files = {'en': '', 'fr': '', 'es': '', 'de': '', 'it': '', 'ja': '', 'pt-br': '', 'es-mx': '',
                               'ru': '', 'pl': '', 'zh-cht': '', 'ko': '', 'zh-chs': ''}
        self.session = None
        self.destiny2 = destiny2

    async def init(self):
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def decode_hash(self, hash_id: int, definition: str, language: str):
        """Decodes a hash id into a json object.

        Args:
            hash_id (int): The hash id to be decoded.
            definition (str): The type of entity to be decoded (ex. 'DestinyClassDefinition')
            language (str): The language to use when retrieving results from the Manifest.

        Returns:
            dict: Json object corresponding to the given hash_id and definition.
        """
        if language not in self.manifest_files.keys():
            raise DestipyException("Unsupported language: {language}")

        if self.manifest_files.get(language) == '':
            await self.update_manifest(language)

        if definition == 'DestinyHistoricalStatsDefinition':
            hash_id = f'"{hash_id}"'
            identifier = 'key'
        else:
            hash_id = self._twos_comp_32(hash_id)
            identifier = "id"

        with DBase(self.manifest_files.get(language)) as database:
            try:
                res = database.query(hash_id, definition, identifier)
            except sqlite3.OperationalError as ex:
                if ex.args[0].startswith('no such table'):
                    raise DestipyException(f"Invalid definition: {definition}")
                else:
                    raise ex

            if len(res) > 0:
                return json.loads(res[0][0])
            else:
                raise DestipyException(f"No entry found with id: {hash_id}")

    async def update_manifest(self, language):
        """
        Downloads and extracts the manifest from Bungie's servers.
        """
        if language not in self.manifest_files.keys():
            raise DestipyException(f"Unsupported language: {language}")

        response = await self.destiny2.GetDestinyManifest()
        if response['ErrorCode'] != 1:
            raise DestipyException("Could not retrieve Manifest from Bungie.net")

        manifest_url = 'https://www.bungie.net' + response['Response']['mobileWorldContentPaths'][language]
        manifest_file_name = manifest_url.split('/')[-1]

        if not os.path.isfile(manifest_file_name):
            # Manifest doesn't exist, or isn't up to date
            # Download and extract the current manifest
            # Remove the zip file once finished
            filename = await self._download_file(manifest_url, MANIFEST_ZIP)
            if os.path.isfile(f'./{MANIFEST_ZIP}'):
                zip_ref = zipfile.ZipFile(f'./{MANIFEST_ZIP}', 'r')
                zip_ref.extractall('./')
                zip_ref.close()
                os.remove(MANIFEST_ZIP)
            else:
                raise DestipyException("Could not retrieve Manifest from Bungie.net")

        self.manifest_files[language] = manifest_file_name

    async def _download_file(self, url, name):
        await self.init()
        with async_timeout.timeout(10):
            async with self.session.get(url) as response:
                filename = os.path.basename(name)
                with open(f"{filename}", 'wb') as f_handle:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f_handle.write(chunk)
                return await response.release()

    def _twos_comp_32(self, val):
        val = int(val)
        if (val & (1 << (32 - 1))) != 0:
            val = val - (1 << 32)
        return val
    