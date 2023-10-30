#======================================================================
# PartialDataException.py
#======================================================================
class PartialDataException(BaseException):
    """
    Exception type for a text file whose chain contains an invalid track and
    sector or a circular reference. The partial data are contained within
    the exception.
    """
    def __init__(self, message: str, partialData: list):
        super(message)
        self.partialData = partialData
