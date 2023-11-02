from finbourne_lab.lusid.base import BaseLusidLab
from finbourne_lab.lusid import LusidExperiment
import numpy as np
import finbourne_lab.lusid.ensure as ensure
import shortuuid
from datetime import datetime
import pytz


class LusidHoldingLab(BaseLusidLab):
    """Lab class for lusid holding endpoint methods.

    """
    properties_data = ensure.PropertiesData(quiet=False)
    portfolios_data = ensure.PortfolioData(quiet=False)
    instrument_data = ensure.InstrumentData(quiet=False)
    holding_data = ensure.HoldingsData(quiet=False)
    domain = 'Holding'

    def set_holdings_measurement(self, **kwargs) -> LusidExperiment:
        """Make an experiment object for lusid set holdings' performance.

        Keyword Args:
            x_rng (Union[int, List[int]]): the range to sample when setting x-many holdings. Given as a list
                containing two integers or a const int value. Defaults to [1, 2000].
            n_props: number of properties to create on each holding, defaults to 0
            n_portfolios: number of portfolios to upsert the holdings to, defaults to 1
            scope: scope of the holdings, defaults to f"fbnlab-test-{str(shortuuid.uuid())}"
            code_prefix: prefix for naming the holdings, defaults to "fbnlab-test-{str(shortuuid.uuid())}"

        Returns:
            LusidExperiment: the upsert holdings experiment object.
        """

        x_rng = kwargs.get('x_rng', [1, 2000])
        n_props = kwargs.get('n_props', 0)
        n_portfolios = kwargs.get('n_portfolios', 1)
        scope = kwargs.get('scope', f"fbnlab-test-{str(shortuuid.uuid())}")
        code_prefix = kwargs.get('code_prefix', f"fbnlab-test-{str(shortuuid.uuid())}")

        effective_date = datetime(2018, 1, 1, tzinfo=pytz.utc)
        # ensure holding property definitions
        if n_props > 0:
            self.properties_data.ensure(n_props, scope, self.domain)
        # ensure portfolios
        portfolio_codes = self.portfolios_data.build_portfolio_codes(
            n_portfolios=n_portfolios,
            code_prefix=code_prefix)
        self.portfolios_data.ensure(
            scope=scope,
            portfolio_codes=portfolio_codes,
            effective_date=effective_date)
        # ensure instruments
        instrument_prefix = "fbnlab-test"
        self.instrument_data.ensure(n_insts=x_rng[1], id_prefix=instrument_prefix)
        instrument_identifiers = [{f"Instrument/default/ClientInternal": f"{instrument_prefix}_{i}"}
                                  for i in range(x_rng[1])]

        method = self.lusid.transaction_portfolios_api.set_holdings

        def build(x, _n_props):
            properties = []
            if n_props > 0:
                properties = self.properties_data.build_properties(
                    n_props=_n_props,
                    scope=scope,
                    domain=self.domain
                )
                properties = {_property.key: _property for _property in properties}
            adjust_holding_request = self.holding_data.build_holdings_adjustments_request(
                n_transactions=x,
                instrument_identifiers=instrument_identifiers,
                properties=properties
            )

            return lambda: method(
                scope=scope,
                code=portfolio_codes[np.random.randint(n_portfolios)],
                adjust_holding_request=adjust_holding_request,
                effective_at=effective_date,
                _preload_content=False
            )

        return LusidExperiment('set_holdings', build, x_rng, n_props)
