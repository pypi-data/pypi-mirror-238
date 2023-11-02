import unittest
import lumipy as lm
import os

import pandas as pd

from finbourne_lab import Convener, FileRecorder
from finbourne_lab.lusid import LusidQuoteLab, LusidClient
import shortuuid


class TestQuote(unittest.TestCase):

    lm_client = lm.get_client()
    lusid_quote_lab = LusidQuoteLab(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    def test_upsert_quotes_measurement(self):

        x_rng = [1, 5]
        scope = f"fbnlab-test-{str(shortuuid.uuid())}"
        id_prefix = "fbnlab-test-instruments"

        experiment = self.lusid_quote_lab.upsert_quotes_measurement(
            x_rng=x_rng,
            scope=scope,
            id_prefix=id_prefix)

        path = 'test_upsert_quotes'
        recorder = FileRecorder(path)
        convener = Convener(experiment, recorder)
        convener.go(10)

        df = pd.read_csv(f"{path}/upsert_quotes.csv")
        if len(df) == 0:
            raise Exception('There was no data recorded')
        else:
            df_errored = df.loc[df['errored'] == True]
            # check whether we have less than 5 percent error rate
            self.assertTrue(expr=(len(df_errored)/len(df)) < 0.05, msg="Error rate is higher than 5%")
