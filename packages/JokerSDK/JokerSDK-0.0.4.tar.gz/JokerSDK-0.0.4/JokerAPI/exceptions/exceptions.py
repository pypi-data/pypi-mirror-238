class CountryNotWhitelistedException(Exception):
    def __init__(self):
        super().__init__("The country you are trying to dial `from` or `to` is not whitelisted.")

class NonExistentCallException(Exception):
    def __init__(self, debug = False, callSid = ""):
        super().__init__(f"You cannot control a non-existent call or channel.{callSid if debug else ''}")

class WAFTriggeredException(Exception):
    def __init__(self):
        super().__init__("WAF triggered due to suspicious activity from IP address.")

class InvalidAPIKeyException(Exception):
    def __init__(self):
        super().__init__("Invalid API Key")

class InsufficientBalanceException(Exception):
    def __init__(self):
        super().__init__("API key has insufficient balance.")

class MissingParametersException(Exception):
    def __init__(self):
        super().__init__("API Request is malformed, re-check function parameters.")
    
class InvalidDataTypeException(Exception):
    def __init__(self, varName, type):
        super().__init__(f"Var[{varName}] must be data type of {type}.")

class InvalidRegexResultException(Exception):
    def __init__(self):
        super().__init__(f"Value must consist of: digits, '*' or '#'.")