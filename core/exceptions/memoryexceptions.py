class Error(Exception):
    pass


class MemoryLocationError(Error):

    def __init__(self, address, message):
        self.address = address
        self.message = message
