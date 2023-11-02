import unittest
import lumipy as lm
import os
from finbourne_lab import Convener, FileRecorder
from finbourne_lab.lusid import LusidHoldingLab, LusidClient
import shortuuid
import finbourne_lab.lusid.ensure as ensure
import pandas as pd


class TestHolding(unittest.TestCase):

    lm_client = lm.get_client()
    lusid_holding_lab = LusidHoldingLab(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    properties_data = ensure.PropertiesData(quiet=False)
    instrument_data = ensure.InstrumentData(quiet=False)
    holding_data = ensure.TxnsData(quiet=False)

    domain = "Holding"

    def test_set_holdings_measurement(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        code_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        x_rng = [1, 5]
        n_props = 1
        n_portfolios = 1
        experiment = self.lusid_holding_lab.set_holdings_measurement(
            x_rng=x_rng,
            n_props=n_props,
            scope=scope,
            n_portfolios=n_portfolios,
            code_prefix=code_prefix)

        path = 'test_set_holdings'
        recorder = FileRecorder(path)
        convener = Convener(experiment, recorder)
        convener.go(10)

        df = pd.read_csv(f"{path}/set_holdings.csv")
        if len(df) == 0:
            raise Exception('There was no data recorded')
        else:
            df_errored = df.loc[df['errored'] == True]
            # check whether we have less than 5 percent error rate
            self.assertTrue(expr=(len(df_errored)/len(df)) < 0.05, msg="Error rate is higher than 5%")
