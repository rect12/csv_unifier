class BaseReaderError(Exception):
    def __init__(self, message=None):
        self.message = message


class ReaderConvertorError(BaseReaderError):
    pass


class UnknownBankType(BaseReaderError):
    pass


class BaseUnloaderError(Exception):
    def __init__(self, message=None):
        self.message = message


class UnloaderError(BaseUnloaderError):
    pass
