#======================================================================
# TextLine.py
#======================================================================
class TextLine():
    def __init__(self, text: str, errorLine: bool):
        self.text = text
        self.errorLine = errorLine

    def text(self):
        return self.text

    def isErrorLine(self) -> bool:
        return self.errorLine
