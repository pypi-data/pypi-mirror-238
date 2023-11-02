from finbourne_lab.luminesce.base import BaseLumiLab
from finbourne_lab.luminesce.ensure import LumiPortfolioData, LumiInstrumentData, LumiHoldingsData, LumiTxnsData


class LusidLumiLabBase(BaseLumiLab):
    """The lusid lumi lab encapsulates standard measurements for lusid luminesce providers.

    """

    def __init__(self, atlas, verbose):
        """Creator for the LusidLumiLab class.

        Args:
            atlas (Atlas): the lumipy atlas to run luminesce queries with.
            verbose (bool): whether to run in verbose mode. This will give feedback on ensure (entity) steps
            during running.

        """

        self.pf_gen = LumiPortfolioData(atlas, not verbose)
        self.in_gen = LumiInstrumentData(atlas, not verbose)
        self.hl_gen = LumiHoldingsData(atlas, not verbose)
        self.tx_gen = LumiTxnsData(atlas, not verbose)

        super().__init__(atlas, verbose)
