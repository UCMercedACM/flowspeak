from flask import Flask

class MyApp(Flask):
    def __init__(self, **kwargs):
        super().__init__(
            import_name=__name__
        )