class InvalidBetException(Exception):
    def __init__(self, msg='Invalid bet!'):
        super().__init__(msg)

class UnknownBetException(Exception):
    def __init__(self, msg='Unknown bet!'):
        super().__init__(msg)

class InvalidPlayerException(Exception):
    def __init__(self, msg='Invalid player!'):
        super().__init__(msg)

class IncompleteCommandException(Exception):
    def __init__(self, msg='Incomplete command!'):
        super().__init__(msg)

class InvalidCommandException(Exception):
    def __init__(self, msg='Invalid command!'):
        super().__init__(msg)
