from . import management
from . import predict

def __setup__ (context):
    context.app.mount ('/', predict)
    context.app.mount ('/', management)
