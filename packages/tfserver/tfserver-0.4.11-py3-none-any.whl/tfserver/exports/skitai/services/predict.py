
import tensorflow as tf
import tfserver
from tfserver.pb2 import prediction_service_pb2, predict_pb2
from tensorflow.python.framework import tensor_util
import numpy as np

def serialize (result):
    resp = {}
    for k, v in result.items ():
        if isinstance (v, np.ndarray):
            resp [k] = v.tolist ()
        else:
            resp [k] = v
    return resp

def __mount__ (context):
    app = context.app

    # gRPC predict services ------------------------------------
    @app.route ("/tensorflow.serving.PredictionService/Predict")
    def Predict (context, request, timeout = 10):
        model = tfserver.get_model (request.model_spec.name)
        inputs = { k: tensor_util.MakeNdarray (v) for k, v in request.inputs.items () }

        result = getattr (model, request.model_spec.signature_name) (inputs, as_dict = True)
        response = predict_pb2.PredictResponse ()
        for k, v in result.items ():
            response.outputs [k].CopyFrom (tf.make_tensor_proto (v))
        return response

    # JSON predict service ---------------------------------------
    @app.route ("/models/<alias>/predict", methods = ['POST'])
    @app.argspec (reduce__in = ['mean', 'max', 'min'])
    def predict (context, alias, reduce = None, **inputs):
        model = tfserver.get_model (alias)
        inputs = { k: np.array (v) for k, v in inputs.items () }
        result = model.predict (inputs, as_dict = True, reducer = reduce)
        return context.API (result = serialize (result))

    # POST predict service ---------------------------------------
    @app.route ("/models/<alias>/media/predict", methods = ['POST'])
    @app.argspec (reduce__in = ['mean', 'max', 'min'])
    def predict_media (context, alias, media, reduce = None, **options):
        assert hasattr (media, 'path'), context.HttpError ('400 Bad Request', 'file stream is required')
        model = tfserver.get_model (alias)
        with media.as_flashfile ():
            xs = model.preprocess (media.path, **options)
        result = model.predict (xs, as_dict = True, reducer = reduce)
        return context.API (result = serialize (result))
