from celery import Celery
from config import app
from flask_restful import Api

from vistas.vistas import VistaDownloadTask, VistaLogin, VistaSignUp, VistaTask

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

api = Api(app)
api.add_resource(VistaSignUp, '/api/auth/signup')
api.add_resource(VistaLogin, '/api/auth/login')
api.add_resource(VistaTask, '/api/tasks', '/api/tasks/<int:task_id>')
api.add_resource(VistaDownloadTask, '/api/tasks/<int:task_id>/download')

if __name__ == '__main__':
    app.run()