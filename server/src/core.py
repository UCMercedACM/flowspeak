from flask import Flask

class VoiceApp(Flask):
    def __init__(self, **kwargs):
        super().__init__(
            import_name=__name__,
            **kwargs
        )
        
    