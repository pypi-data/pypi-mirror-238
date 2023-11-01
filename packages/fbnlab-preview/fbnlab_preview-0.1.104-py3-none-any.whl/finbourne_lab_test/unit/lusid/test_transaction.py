import unittest
import lumipy as lm
import os
from finbourne_lab import Convener, FileRecorder
from finbourne_lab.lusid import LusidTransactionLab, LusidClient
import shortuuid
import finbourne_lab.lusid.ensure as ensure
import pandas as pd


class TestTransaction(unittest.TestCase):

    lm_client = lm.get_client()
    lusid_transaction_lab = LusidTransactionLab(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    properties_data = ensure.PropertiesData(quiet=False)
    instrument_data = ensure.InstrumentData(quiet=False)
    transaction_data = ensure.TxnsData(quiet=False)

    domain = "Transaction"

    def test_upsert_transactions_measurement(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        code_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        x_rng = [1, 5]
        n_props = 1
        n_portfolios = 1

        experiment = self.lusid_transaction_lab.upsert_transactions_measurement(
            x_rng=x_rng,
            n_props=n_props,
            scope=scope,
            n_portfolios=n_portfolios,
            id_prefix=code_prefix)

        path = 'test_upsert_transactions'
        recorder = FileRecorder(path)
        convener = Convener(experiment, recorder)
        convener.go(10)

        df = pd.read_csv(f"{path}/upsert_transactions.csv")
        if len(df) == 0:
            raise Exception('There was no data recorded')
        else:
            df_errored = df.loc[df['errored'] == True]
            # check whether we have less than 5 percent error rate
            self.assertTrue(expr=(len(df_errored)/len(df)) < 0.05, msg="Error rate is higher than 5%")

    def test_get_transactions_measurement(self):

        scope = f"fbnlab-ut-get-txns"
        code_prefix = f"fbnlab-ut-get-txns"
        x_rng = [1, 5]
        n_props = 1
        n_portfolios = 1

        experiment = self.lusid_transaction_lab.get_transactions_measurement(
            x_rng=x_rng,
            n_props=n_props, 
            n_portfolios=n_portfolios,
            scope=scope,
            code_prefix=code_prefix)

        path = 'test_get_transactions'
        recorder = FileRecorder(path)
        convener = Convener(experiment, recorder)
        convener.go(10)

        df = pd.read_csv(f"{path}/get_transactions.csv")
        if len(df) == 0:
            raise Exception('There was no data recorded')
        else:
            df_errored = df.loc[df['errored'] == True]
            # check whether we have less than 5 percent error rate
            self.assertTrue(expr=(len(df_errored)/len(df)) < 0.05, msg="Error rate is higher than 5%")
