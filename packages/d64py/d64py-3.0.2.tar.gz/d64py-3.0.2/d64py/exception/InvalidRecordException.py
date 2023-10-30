#======================================================================
# InvalidRecordException.py
#======================================================================
class InvalidRecordException(Exception):

    def __init__(self, message):
        super("Invalid or deleted VLIR record requested.")
