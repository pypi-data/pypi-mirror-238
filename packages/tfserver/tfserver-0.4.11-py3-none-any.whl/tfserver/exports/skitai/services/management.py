import tfserver

def __mount__ (context):
    app = context.app

    @app.route ("/models")
    def models (context):
        return context.API (models = tfserver.models ())

    @app.route ("/models/<alias>", methods = ['GET', 'PATCH', 'DELETE'])
    def model (context, alias):
        if context.request.method == 'GET':
            model = tfserver.get_model (alias)
            return context.API (
                path = model.model_root,
                version = model.version,
                labels = {lb.name: lb.items () for lb in model.labels or []}
            )

        if context.request.method == 'PATCH': # reload model
            tfserver.refresh_model (alias)
            app.emit ('tfserver:model-reloaded', alias)
            return context.API ('204 No Content')

        tfserver.delete_model (alias)
        app.emit ('tfserver:model-unloaded', alias)
        return context.API ('204 No Content')

    @app.route ("/models/<alias>/versions/<int:version>", methods = ['PUT', 'POST'])
    @app.argspec (booleans = ['refresh', 'overwrite'])
    def put_model (context, alias, version, model, refresh = True, overwrite = False, config = None):
        with model.flashfile () as zfile:
            try:
                tfserver.add_version (alias, version, zfile, refresh, overwrite, config)
            except AssertionError:
                raise context.HttpError ('409 Conflict')
        app.emit ('tfserver:model-reloaded', alias)
        return context.API ('201 Created')

    @app.route ("/models/<alias>/version", methods = ['GET'])
    @app.route ("/model/<alias>/version", methods = ['GET']) # lower versoion compat
    def version (context, alias):
        sess = tfserver.tfsess.get (alias)
        if sess is None:
            return context.response ("404 Not Found")
        return context.API (version = sess.get_version ())

    @app.route ("/models/<alias>/versions/<int:version>", methods = ['DELETE'])
    def delete_model_version (context, alias, version):
        tfserver.delete_versions (alias, version)
        app.emit ('tfserver:model-reloaded', alias)
        return context.API ('204 No Content')

    @app.route ("/models/<alias>/versions", methods = ['DELETE'])
    @app.argspec (lists = ['versions'])
    def delete_model_versions (context, alias, versions):
        tfserver.delete_versions (alias, versions)
        return context.API ('204 No Content')

