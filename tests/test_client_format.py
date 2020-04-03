class TestFtxClient():
    def test_pass(self):
        assert 1 == 1

    def test_get_balance(self, ftx_client):
        balances = ftx_client.get_balances()
        assert len(balances) > 0
        for balance in balances:
            assert 'coin' in balance
            assert 'free' in balance
            assert 'total' in balance
            assert 'usdValue' in balance
