from finbourne_lab.lusid.base import BaseLusidLab
from finbourne_lab.lusid import LusidExperiment
from finbourne_lab.lusid.ensure import QutoesData, InstrumentData
import shortuuid


class LusidQuoteLab(BaseLusidLab):
    """Lab class for lusid qutes endpoint methods.

    """
    quotes_data = QutoesData(quiet=False)
    instrument_data = InstrumentData(quiet=False)

    def upsert_quotes_measurement(self, **kwargs) -> LusidExperiment:
        """Make an experiment object for lusid upsert quotes' performance.

        Keyword Args:
            x_rng (Union[int, List[int]]): the range to sample when upserting x-many quotes. Given as a list
                containing two integers or a const int value. Defaults to [1, 2000].
            scope: scope of the quotes, defaults to f"fbnlab-test-{str(shortuuid.uuid())}"
            id_prefix: prefix for naming the instruments, defaults to "fbnlab-test-instruments"

        Returns:
            LusidExperiment: the upsert quotes experiment object.
        """

        x_rng = kwargs.get('x_rng', [1, 2000])
        scope = kwargs.get('scope', f"fbnlab-test-{str(shortuuid.uuid())}")
        id_prefix = "fbnlab-test-instruments"

        self.instrument_data.ensure(n_insts=x_rng[1], id_prefix=id_prefix)

        method = self.lusid.quotes_api.upsert_quotes

        def build(x):
            instrument_ids = [f"{id_prefix}_{i}" for i in range(x)]
            request_key_pair = self.quotes_data.build_upsert_quote_request_key_pairs(instrument_ids)
            return lambda: method(scope, request_body=request_key_pair, _preload_content=False)

        return LusidExperiment('upsert_quotes', build, x_rng)
    