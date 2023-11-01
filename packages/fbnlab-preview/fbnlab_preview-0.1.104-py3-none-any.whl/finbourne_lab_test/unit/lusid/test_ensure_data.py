import json
import unittest
import lumipy as lm
import os
from finbourne_lab.lusid import LusidClient
import shortuuid
import finbourne_lab.lusid.ensure as ensure
import lusid.models as models
from datetime import datetime
import pytz
from lusid.exceptions import ApiException


class TestPortfoliosData(unittest.TestCase):

    portfolios_data = ensure.PortfolioData(quiet=False)

    def test_build_portfolio_codes(self):
        n_portfolios = 2
        code_prefix = "fbnlab-test"

        portfolio_codes_actual = self.portfolios_data.build_portfolio_codes(
            n_portfolios=n_portfolios,
            code_prefix=code_prefix
        )
        portfolio_codes_expected = ["portfolio-fbnlab-test-0", "portfolio-fbnlab-test-1"]
        self.assertEqual(portfolio_codes_actual, portfolio_codes_expected)

    def test_ensure_portfolios_creates_new_portfolios(self):

        from lusid.models.portfolio import Portfolio
        n_portfolios = 2
        scope = f"fbnlab-test-{str(shortuuid.uuid())}"
        code_prefix = f"fbnlab-test-{str(shortuuid.uuid())}"
        effective_date = datetime(2018, 1, 1, tzinfo=pytz.utc)

        portfolio_codes = self.portfolios_data.build_portfolio_codes(
            n_portfolios=n_portfolios,
            code_prefix=code_prefix)
        response = self.portfolios_data.ensure(
            scope=scope,
            portfolio_codes=portfolio_codes,
            effective_date=effective_date)
        [self.assertTrue(isinstance(r, Portfolio)) for r in response]

    def test_ensure_portfolios_does_not_create_already_existing_portfolios(self):

        n_portfolios = 2
        scope = f"fbnlab-test-{str(shortuuid.uuid())}"
        code_prefix = f"fbnlab-test-{str(shortuuid.uuid())}"
        effective_date = datetime(2018, 1, 1, tzinfo=pytz.utc)

        portfolio_codes = self.portfolios_data.build_portfolio_codes(
            n_portfolios=n_portfolios,
            code_prefix=code_prefix)

        for portfolio_code in portfolio_codes:
            transactions_portfolio_request = models.CreateTransactionPortfolioRequest(
                display_name="test portfolio",
                code=portfolio_code,
                base_currency="GBP",
                created=effective_date
            )

            self.portfolios_data.client.transaction_portfolios_api.create_portfolio(
                scope=scope,
                create_transaction_portfolio_request=transactions_portfolio_request
            )

        response_actual = self.portfolios_data.ensure(
            scope=scope,
            portfolio_codes=portfolio_codes,
            effective_date=effective_date)
        response_expected = True
        self.assertEqual(response_actual, response_expected)


class TestPropertiesData(unittest.TestCase):

    properties_data = ensure.PropertiesData(quiet=False)

    def test_ensure_property_definitions(self):

        from lusid.models.property_definition import PropertyDefinition
        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        domain = "Instrument"
        n_props = 50
        response = self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        type_expected = PropertyDefinition
        [self.assertTrue(isinstance(r, type_expected)) for r in response]

    def test_build_properties(self):
        scope = f"fbnlab-ut-prop"
        domain = "Instrument"
        n_props = 2
        properties_actual = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)

        from lusid import PropertyValue

        properties_expected = [
            models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop0',
                value=PropertyValue(metric_value=models.MetricValue(value=0))
            ),
            models.ModelProperty(
                key=f'Instrument/fbnlab-ut-prop/test_prop1',
                value=PropertyValue(metric_value=models.MetricValue(value=100))
            )
        ]

        self.assertEqual(properties_expected, properties_actual)

    def test_build_perpetual_properties(self):
        scope = f"fbnlab-ut-prop"
        domain = "Transaction"
        n_props = 2
        properties_actual = self.properties_data.build_perpetual_properties(
            n_props=n_props,
            scope=scope,
            domain=domain)

        from lusid import PropertyValue

        properties_expected = [
            models.PerpetualProperty(
                key=f'Transaction/fbnlab-ut-prop/test_prop0',
                value=PropertyValue(metric_value=models.MetricValue(value=0))
            ),
            models.PerpetualProperty(
                key=f'Transaction/fbnlab-ut-prop/test_prop1',
                value=PropertyValue(metric_value=models.MetricValue(value=100))
            )
        ]

        self.assertEqual(properties_expected, properties_actual)


class TestInstrumentData(unittest.TestCase):

    properties_data = ensure.PropertiesData(quiet=False)
    instrument_data = ensure.InstrumentData(quiet=False)
    lm_client = lm.get_client()
    client = LusidClient(token=lm_client.get_token(), api_url=os.environ['FBN_LUSID_API_URL'])

    def test_ensure_instrument_data_ensure_does_upsert_new_instruments_without_properties(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5

        response = self.instrument_data.ensure(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        metadata_actions_type_expected = "CreatedInstruments"
        for r in response:
            metadata = r.json()
            metadata_actions_type_actual = metadata['metadata']['actions'][0]["type"]
            self.assertEqual(metadata_actions_type_expected, metadata_actions_type_actual)

    def test_ensure_instrument_data_ensure_does_not_upsert_already_existing_instruments_without_properties(self):

        scope = f"fbnlab-ut-test"
        id_prefix = f"fbnlab-ut-test"
        n_inst = 5

        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')}
            )
            for i in range(n_inst)
        }
        self.client.instruments_api.upsert_instruments(
            request_body=instruments,
            scope=scope,
            _preload_content=False)

        # attempt to recreate the already existing instruments
        response_actual = self.instrument_data.ensure(n_insts=n_inst, id_prefix=id_prefix, scope=scope)
        response_expected = True
        self.assertEqual(response_actual, response_expected)

    def test_ensure_instrument_data_ensure_does_upsert_new_instruments_with_properties(self):

        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        id_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_inst = 5
        n_props = 1
        domain = "Instrument"

        self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        properties = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)
        response = self.instrument_data.ensure(
            n_insts=n_inst,
            id_prefix=id_prefix,
            scope=scope,
            properties=properties
        )
        metadata_actions_type_expected = "CreatedInstruments"
        for r in response:
            metadata = r.json()
            metadata_actions_type_actual = metadata['metadata']['actions'][0]["type"]
            self.assertEqual(metadata_actions_type_expected, metadata_actions_type_actual)

    def test_ensure_instruments_does_not_upsert_already_existing_instruments(self):

        scope = f"fbnlab-ut-test"
        id_prefix = f"fbnlab-ut-test"
        n_inst = 5
        n_props = 1
        domain = "Instrument"

        self.properties_data.ensure(n_props=n_props, scope=scope, domain=domain)
        properties = self.properties_data.build_properties(n_props=n_props, scope=scope, domain=domain)

        instruments = {
            f'inst_{i}': models.InstrumentDefinition(
                name=f'Instrument{i}',
                identifiers={"ClientInternal": models.InstrumentIdValue(f'{id_prefix}_{i}')},
                properties=properties
            )
            for i in range(n_inst)
        }

        self.client.instruments_api.upsert_instruments(
            request_body=instruments,
            scope=scope,
            _preload_content=False)

        # attempt to recreate the already existing instruments
        response_actual = self.instrument_data.ensure(
            n_insts=n_inst,
            id_prefix=id_prefix,
            scope=scope,
            properties=properties
        )
        response_expected = True
        self.assertEqual(response_actual, response_expected)


class TestTxnsData(unittest.TestCase):

    txns_data = ensure.TxnsData(quiet=False)

    def test_ensure_transactions_does_upsert_new_transactions(self):
        scope = f"fbnlab-ut-{str(shortuuid.uuid())}"
        code_prefix = f"fbnlab-ut-{str(shortuuid.uuid())}"
        n_txns = 5
        n_portfolios = 2
        n_props = 1

        response = self.txns_data.ensure(
            n_txns=n_txns,
            code_prefix=code_prefix,
            scope=scope,
            n_portfolios=n_portfolios,
            n_props=n_props)
        warnings = []
        for r in response:
            response_data = r.json()
            if response_data['metadata'].get('warnings'):
                warnings.append(response_data['metadata']['warnings'])
                print(response_data['metadata']['warnings'])
            method_actual = response_data['links'][0]['method']
            method_expected = 'GET'
            self.assertEqual(method_expected, method_actual)
        self.assertTrue(len(warnings) == 0)

    def test_ensure_transactions_does_not_upsert_already_existing_transactions(self):
        scope = f"fbnlab-ut-test"
        code_prefix = f"fbnlab-ut-test"
        n_txns = 5
        n_portfolios = 1
        n_props = 0

        from datetime import datetime
        import pytz
        import numpy as np
        domain = "Transaction"

        properties_data = ensure.PropertiesData(quiet=False)
        portfolios_data = ensure.PortfolioData(quiet=False)
        instrument_data = ensure.InstrumentData(quiet=False)

        effective_date = datetime(2018, 1, 1, tzinfo=pytz.utc)
        # ensure transaction property definitions
        if n_props > 0:
            properties_data.ensure(n_props, scope, domain)
        # ensure portfolios
        portfolio_codes = portfolios_data.build_portfolio_codes(
            n_portfolios=n_portfolios,
            code_prefix=code_prefix)
        portfolios_data.ensure(
            scope=scope,
            portfolio_codes=portfolio_codes,
            effective_date=effective_date)
        # ensure instruments
        instrument_prefix = "fbnlab-test"
        instrument_data.ensure(n_insts=1, id_prefix=instrument_prefix)
        properties = []
        if n_props > 0:
            perpetual_properties = properties_data.build_perpetual_properties(
                n_props=n_props,
                scope=scope,
                domain=domain
            )
            properties = {_property.key: _property for _property in perpetual_properties}
        transactions = self.txns_data.build_transactions(
            n_transactions=n_txns,
            instrument_identifiers={f"Instrument/default/ClientInternal": f"{instrument_prefix}_0"},
            effective_date=effective_date,
            properties=properties)

        self.txns_data.client.transaction_portfolios_api.upsert_transactions(
            scope=scope,
            code=portfolio_codes[np.random.randint(n_portfolios)],
            transaction_request=transactions,
            _preload_content=False)

        response_actual = self.txns_data.ensure(
            n_txns=n_txns,
            code_prefix=code_prefix,
            scope=scope,
            n_portfolios=n_portfolios,
            n_props=n_props)
        response_expected = True

        self.assertEqual(response_actual, response_expected)
