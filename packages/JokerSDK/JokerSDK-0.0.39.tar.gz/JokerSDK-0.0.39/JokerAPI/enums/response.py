from strenum import StrEnum

class Enums(StrEnum):
    
    STATUS_FAILED = "failed"
    COUNTRY_NOT_WHITELISTED = "this country is not whitelisted"
    INVALID_API_KEY = "invalid api key"
    INSUFFICIENT_FUNDS = "you have no balance"
    MISSING_PARAMETERS = "you are missing parameters"