# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import warnings, requests, os, pdb

from .version import __version__

#defaul_url = 'https://ultronsandbox.oss-cn-hangzhou.aliyuncs.com/version/seleya.json'
#default_url = 'https://seleya.blob.core.windows.net/nsark'
version_url = "https://pypi.org/pypi/Finance-Seleya/json"
#try:
from . import seleya
from .data.DataAPI.sqlatom.fetch_engine import FetchEngine as DBFetchEngine
from .data.DataAPI.sqlatom.db_factory import *

from .data.DataAPI import http as SeleyaAPI
from .data.DataAPI import sqlatom as DBAPI
from .data.SurfaceAPI import sqlatom as SurfaceDBAPI
from .data.SurfaceAPI import mongo as SurfaceMGAPI
from .mfc import alchemy as AlchemyAPI
#except ImportError as e:
#    print(e)
#    warnings.warn("pip install --upgrade  SeleyaSDK")

from .Toolset import *

try:
    from ultron.factor.data.standardize import standardize
    from ultron.factor.data.winsorize import winsorize_normal
    from ultron.factor.data.neutralize import neutralize
    from ultron.factor.data.processing import factor_processing
    from ultron import sentry
except ImportError:
    warnings.warn(
        "If you need high-performance computing，please install Finance-Ultron.First make sure that the C++ compilation environment has been installed"
    )

session = requests.Session()


def get_version():
    res = requests.get(version_url).json()
    if res.get('code') != 200:
        return '', ''

    remote_version = res['info']['version']
    content = res['info']['summary']

    return remote_version, content


def check_version():
    try:
        remote_version, content = get_version()
        if not remote_version or remote_version <= __version__:
            return
        if __version__ != remote_version:
            print(
                "New pypi version: {0} (current: {1}) | pip install -U Finance-Seleya"
                .format(remote_version, __version__))

    except Exception as e:
        print("Failed to check Finance-Seleya pypi version: {0}".format(e))


check_version()