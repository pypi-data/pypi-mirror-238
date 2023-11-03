from atila import Atila
from rs4.termcolor import tc

def __config__ (pref):
    import tfserver

    if "TF_MODELS" in pref.config:
        for alias, model in pref.config.TF_MODELS.items ():
            config = {}
            if isinstance (model, (list, tuple)):
                model, config = model
            tfserver.add_model (alias, model, **config)

    if "GPU_LIMIT" not in pref.config:	# Mb or None
        pref.config.GPU_LIMIT = 'growth'

    if "GPU_DEVICES" not in pref.config:
        pref.config.GPU_DEVICES = []

    assert pref.config.GPU_LIMIT == 'growth' or isinstance (pref.config.GPU_LIMIT, (int, float)), 'GPU_LIMIT should be growth or Memory Mbytes'
    assert isinstance (pref.config.GPU_DEVICES, (list, tuple)), 'GPU_DEVICES should be GPU index list'

def __app__ ():
    return Atila (__name__)

def __mounted__ (context):
    import dnn
    import tfserver

    dnn.setup_gpus (context.app.config.GPU_LIMIT, context.app.config.GPU_DEVICES) # this call must be in a child process
    for alias, model_dir in tfserver.load_models ():
        context.logger ("app", "- loading tensorflow model '{}' from {}".format (tc.cyan (alias), tc.white (model_dir)), 'info')

def __umounted__ (context):
    import tfserver
    tfserver.close_models ()

def __setup__ (context):
    from . import services
    import tfserver
    assert context.mount_options ['point'] == '/', 'must be mounted on root for gRPC methods'
    context.app.mount ('/', services)
