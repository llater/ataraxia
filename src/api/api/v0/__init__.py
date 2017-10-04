import os
import logging
from flask import Flask

log = logging.getLogger('cueapi')
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

def create_app(cfg=None):
    log.info('Calling create_app()...')
    app = Flask(__name__)
    if cfg is not None:
        app.config.from_object(cfg)
    log.info('Beginning db setup...')
    from .database import db
    log.debug('Creating database tables...')
    db._setupdb()
    log.debug('Database tables created.')
    log.debug('Preparing statements...')
    db._prepare_statements()
    log.debug('Prepared statements.')
    if app.config['TESTING']:
        log.debug('TESTING is True -- populating the database with demo data...')
        db._populatedb()
        log.debug('Populated the database.')
    log.info('db setup complete.')

    log.debug('Registering routes...')
    from .endpoints import v0
    app.register_blueprint(v0)
    log.debug('Routes registered.')

    log.info('create_app() complete.') 
    return app