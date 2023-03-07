from flask import Flask, request, abort
from pymongo import MongoClient
import threading
from bson.json_util import dumps
from .repository import LimitsRepository
from .memory_consumer import MemoryConsumer
from .config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class())

    uri = app.config['MONGODB_URI']
    username = app.config['MONGODB_USERNAME']
    password = app.config['MONGODB_PASSWORD']
    db_client = MongoClient(uri, username=username, password=password)
    try:
        db_client.admin.command('ping')
    except:
        app.logger.fatal('Mongo server is not available')
        exit(1)
    db = LimitsRepository(db_client)

    mc = MemoryConsumer()
    threading.Thread(target=mc.run, daemon=True).start()

    @app.route('/limits', methods=['GET'])
    def getLimit():
        category = request.args['category']
        try:
            limit = db.get_by_category(category)
        except Exception as err:
            abort(500, description=err.message)
        return dumps(limit)

    @app.route('/limits', methods=['POST'])
    def setLimit():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            limit = request.get_json()
            try:
                result = db.add(limit)
            except Exception as err:
                abort(500, description=err.message)
            return dumps({ 'inserted_id': result.inserted_id })
        abort(400)


    @app.route('/limits', methods=['PUT'])
    def changeLimit():
        content_type = request.headers.get('Content-Type')
        if content_type == 'application/json':
            new_limit = request.get_json()
            try:
                result = db.modify(new_limit)
            except Exception as err:
                abort(500, description=err.message)
            return dumps({ 'modified_count': result.modified_count })
        abort(400)

    @app.route('/alarm')
    def alarm():
        app.logger.warning('Too much memory used')
        mc.free()
        return '', 204

    return app
