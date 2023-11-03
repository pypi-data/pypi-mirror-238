from ..endpoints import outbound_calls

"""
# `create_outbound_call` class to initiate an outbound call.
------------------------------------------------------------
```
JokerObject = create_outbound_call(
    apiKey = "<APIKEY>": Default
    *arg, **kwargs: Required
    >   to: str ~ The phone number to dial.
        from_: str ~ The phone number to dial `to` from.
        callbackUrl: str ~ Any webserver to handle live callbacks to.
)
"""
class create_outbound_call(outbound_calls):
    """
    Main initiator for the `create_outbound_call` class.

    Parameters.
    ----------------------------------------------------
    `apiKey` > The API Key to use the SDK.

    *args > Not required key word arguments which may be used in the future.

    **kwargs > Required arguments to initiate a outbound call.


    `self.sid`: list[int] or list[int, str] 
        > Index 0 representing the status of the call (if it is live or not.): Static

        > Index 1 representing the SID of a channel if Index 0 is True (live).
    """
    def __init__(self, apiKey: str = "<API_KEY>", __retrieve__: bool = False, *args, **kwargs) -> None:
        self.sid: str = ""
        self.__retrieve__ = __retrieve__
        self._sid: list[bool] = [False if not __retrieve__ else True]
        super().__init__(apiKey)
        if not __retrieve__:
            self.__dial__(**kwargs)
    
    """
    'Private' `__dial__` function which is called whenever the class is initiated. 
    """
    def __dial__(self, to: str = "", from_: str = "", callbackUrl: str = "https://0.0.0.0/callbacks") -> str:
        self._sid[0], self.sid = self.create_call(to, from_, callbackUrl)
    
    """
    The `play_audio` function to play live audio into a live channel from a URL.
    """
    def play_audio(self, audioUrl: str = "http://0.0.0.0/audio.wav") -> None:
        return self.play_("audio", audioUrl_ = audioUrl)
    
    """
    The `play_text` function to play text into a live channel without the need of TTS.
    """
    def play_text(self, text: str = "This is an example phrase to play", voice: str = "ai3-en-US-Madison") -> None:
        return self.play_("text", text_ = text, voice_ = voice)
    
    """
    The `gather_dtmf_with_audio` function to play live audio into a live channel from a URL
        Whilst gathering DTMF inputs from the recipient.
    """
    def gather_dtmf_with_audio(self, audioUrl: str = "http://0.0.0.0/audio.wav", maxDigits: int = 0) -> None:
        return self.gather_dtmf_with("audio", audioUrl_ = audioUrl, maxDigits_ = maxDigits)
    
    """
    The `gather_dtmf_with_text` function to play text into a live channel without the need of TTS
        Whilst gathering DTMF inputs from the recipient.
    """
    def gather_dtmf_with_text(self, text: str = "This is an example phrase to play", voice: str = "ai3-en-US-Madison", maxDigits: int = 0) -> None:
        return self.gather_dtmf_with("text", text_ = text, voice_ = voice, maxDigits_ = maxDigits)
    
    """
    The `send_dtmf` function to send DTMF tones to a live channel.
    """
    def send_dtmf(self, input_: str = "123456789*#") -> None:
        return self.send_dtmf_(input_)
    
    """
    The `hangup` function to hangup a live channel.
    """
    def hangup(self) -> None:
        return self.hangup_call()

class retrieve(create_outbound_call):
    def __init__(self, apiKey: str = "<API_KEY>", sid: str = "callSID") -> None:
        super().__init__(apiKey=apiKey, __retrieve__ = True)
        self.sid = sid