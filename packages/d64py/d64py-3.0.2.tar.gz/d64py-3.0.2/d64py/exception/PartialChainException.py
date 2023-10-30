#======================================================================
# PartialChainException.py
#======================================================================
from d64py.base.Chain import Chain

class PartialChainException(BaseException):
    partialChain: Chain

    def __init__(self, message, partialChain: Chain):
        super().__init__(message)
        self.partialChain = partialChain

    def getPartialChain(self) -> Chain:
        return self.partialChain

