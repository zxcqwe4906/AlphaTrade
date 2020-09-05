import os
import sys

sys.path.append(os.getcwd())

import pytest
from app import create_app
from AlphaTrade.client.ftx_client import FtxClient

@pytest.fixture()
def ftx_client():
    api_key = 'gxcoCUxTeVemcWXpjVvSM7xZKJL7_ub1c3-VTgaa'
    api_secret = 'rqurkdbed462X_Cf_a_i30EOCDpp-0gLt_Z_mxKd'
    subaccount_name = 'CodeTest'

    return FtxClient(api_key, api_secret, subaccount_name)

@pytest.fixture()
def get_app():
    return create_app()
