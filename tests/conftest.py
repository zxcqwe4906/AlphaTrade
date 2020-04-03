import os
import sys

sys.path.append(os.getcwd())

import pytest
from AlphaTrade.client.ftx_client import FtxClient

@pytest.fixture()
def ftx_client():
    api_key = ''
    api_secret = ''
    subaccount_name = ''

    return FtxClient(api_key, api_secret, subaccount_name)