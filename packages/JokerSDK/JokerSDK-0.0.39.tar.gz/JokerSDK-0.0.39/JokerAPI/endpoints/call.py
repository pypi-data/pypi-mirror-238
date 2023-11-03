import re
from requests import get
from ..enums import *
from ..format import __dial_format__, __hangup_format__, __play_audio_format__, __play_text_format__, __play_audio_dtmf__, __play_text_dtmf__, __send_dtmf_format__
from typing import Any
from ..exceptions import exceptions

class outbound_calls:
    def __init__(self, apiKey: str) -> None:
        self.apiKey = apiKey
    
    def parse_request_response(self, requestResponse: str) -> Any | bool :
        exceptionEnum = {
            response.Enums.COUNTRY_NOT_WHITELISTED: exceptions.CountryNotWhitelistedException,
            response.Enums.INVALID_API_KEY: exceptions.InvalidAPIKeyException,
            response.Enums.INSUFFICIENT_FUNDS: exceptions.InsufficientBalanceException,
            response.Enums.MISSING_PARAMETERS: exceptions.MissingParametersException
        }

        if requestResponse.status_code == 403:
            raise exceptions.WAFTriggeredException()
        
        elif requestResponse.json()['status'] == response.Enums.STATUS_FAILED:
            raise exceptionEnum[requestResponse.json()['context']]()
        
        return False
    
    def create_call(self, to: str, from_: str, callbackUrl: str) -> list[bool, dict[Any]]:
        if self.__retrieve__:
            return
        
        apiResponse = get(__dial_format__(self.apiKey, endpoint.Enums.DIAL, to, from_, callbackUrl))
        
        if not self.parse_request_response(apiResponse):
            return True, apiResponse.json()['callsid']


    def hangup_call(self) -> Any:
        if not self._sid[0]:
            raise exceptions.NonExistentCallException()
        
        self._sid[0] = False
        return get(__hangup_format__(self.apiKey, endpoint.Enums.HANGUP, self.sid))

    def play_(self, _: str, audioUrl_: str = None, text_: str = None, voice_: str = None) -> str:
        if not self._sid[0]:
            raise exceptions.NonExistentCallException()

        formatEnum = {
            "audio": [__play_audio_format__, {"apiKey": self.apiKey, "baseUrl": endpoint.Enums.PLAY_AUDIO.value, "sid": self.sid, "audioUrl": audioUrl_}],
            "text": [__play_text_format__, {"apiKey": self.apiKey, "baseUrl": endpoint.Enums.PLAY_TEXT.value, "sid": self.sid, "text": text_, "voice": voice_}]
        }
        
        return get(formatEnum[_][0](**formatEnum[_][1]))
    
    def gather_dtmf_with(self, _: str, maxDigits_: int, audioUrl_: str = None, text_: str = None, voice_: str = None) -> str:
        if not self._sid[0]:
            raise exceptions.NonExistentCallException()
        
        elif not isinstance(maxDigits_, int):
            raise exceptions.InvalidDataTypeException("maxDigits", "int")
          
        formatEnum = {
            "audio": [__play_audio_dtmf__, {"apiKey": self.apiKey, "baseUrl": endpoint.Enums.GATHER_DTMF_WITH_AUDIO, "sid": self.sid, "audioUrl": audioUrl_, "maxDigits": maxDigits_}],
            "text": [__play_text_dtmf__, {"apiKey": self.apiKey, "baseUrl": endpoint.Enums.GATHER_DTMF_WITH_TEXT, "sid": self.sid, "text": text_, "voice": voice_, "maxDigits": maxDigits_}]
        }

        return get(formatEnum[_][0](**formatEnum[_][1]))

    def send_dtmf_(self, input: Any) -> str:
        if not self._sid[0]:
            raise exceptions.NonExistentCallException()
        
        elif not re.match(r"^[0-9*#]+$", input):
            raise exceptions.InvalidRegexResultException()
        
        return get(__send_dtmf_format__(self.apiKey, endpoint.Enums.SEND_DTMF, self.sid, input))