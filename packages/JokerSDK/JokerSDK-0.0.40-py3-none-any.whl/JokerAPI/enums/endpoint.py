from strenum import StrEnum

class Enums(StrEnum):
    BASE = "https://api.jokerapi.co/voice/v1/"
    
    DIAL = "https://api.jokerapi.co/voice/v1/dial"
    HANGUP = "https://api.jokerapi.co/voice/v1/hangup"
    PLAY_AUDIO = "https://api.jokerapi.co/voice/v1/play"
    PLAY_TEXT = "https://api.jokerapi.co/voice/v1/playtext"
    GATHER_DTMF_WITH_AUDIO = "https://api.jokerapi.co/voice/v1/gather"
    GATHER_DTMF_WITH_TEXT = "https://api.jokerapi.co/voice/v1/gathertext"
    SEND_DTMF = "https://api.jokerapi.co/voice/v1/senddtmf"