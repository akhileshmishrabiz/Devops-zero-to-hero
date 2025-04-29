from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.middleware.proxy_fix import ProxyFix
import time
from app.logging_config import setup_logging
from app.metrics import http_requests_total, request_duration_seconds

db = SQLAlchemy()
login_manager = LoginManager()
logger = setup_logging()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'asdf45sfsdg777gsdg'
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Add Prometheus middleware
    app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
        '/metrics': make_wsgi_app()
    })
    app.wsgi_app = ProxyFix(app.wsgi_app)

    @app.before_request
    def before_request():
        request.start_time = time.time()

    @app.after_request
    def after_request(response):
        if request.path != '/metrics':
            duration = time.time() - request.start_time
            endpoint = request.endpoint or 'unknown'
            
            http_requests_total.labels(
                method=request.method,
                endpoint=endpoint,
                status=response.status_code
            ).inc()
            
            request_duration_seconds.labels(
                endpoint=endpoint
            ).observe(duration)

            logger.info('Request processed', extra={
                'method': request.method,
                'path': request.path,
                'status': response.status_code,
                'duration': duration
            })

        return response

    with app.app_context():
        from app.routes import routes, auth
        app.register_blueprint(routes.bp)
        app.register_blueprint(auth.auth_bp)
        
    return app