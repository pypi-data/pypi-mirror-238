
def __dial_format__(apiKey, baseUrl: str, to: str, from_: str, callbackUrl: str) -> str:
    return f"{baseUrl}?apikey={apiKey}&to={to}&from={from_}&webhookurl={callbackUrl}"

def __hangup_format__(apiKey, baseUrl: str, sid: str) -> str:
    return f"{baseUrl}?apikey={apiKey}&callsid={sid}"

def __play_audio_format__(apiKey, baseUrl: str, sid: str, audioUrl: str) -> str:
    return f"{baseUrl}?apikey{apiKey}&callsid={sid}&audiourl={audioUrl}"

def __play_text_format__(apiKey, baseUrl: str, sid: str, text: str, voice: str) -> str:
    return f"{baseUrl}?apikey={apiKey}&callsid={sid}&text={text}&voice={voice}"

def __play_audio_dtmf__(apiKey, baseUrl: str, sid: str, audioUrl: str, maxDigits: int) -> str:
    return f"{baseUrl}?apikey={apiKey}&callsid={sid}&audiourl={audioUrl}&maxdigits={maxDigits}"

def __play_text_dtmf__(apiKey, baseUrl: str, sid: str, text: str, voice: str, maxDigits: int) -> str:
    return f"{baseUrl}?apikey={apiKey}&callsid={sid}&text={text}&voice={voice}&maxdigits={maxDigits}"

def __send_dtmf_format__(apiKey, baseUrl: str, sid: str, input_) -> str:
    return f"{baseUrl}?apikey={apiKey}&callsid={sid}&input={input_}"