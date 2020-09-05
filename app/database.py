from flask_sqlalchemy import SQLAlchemy as _BaseSQLAlchemy
# from flask_redis import FlaskRedis


class SQLAlchemy(_BaseSQLAlchemy):
    def apply_pool_defaults(self, app, options):
        super(SQLAlchemy, self).apply_pool_defaults(app, options)
        options["pool_pre_ping"] = True

    def safe_commit(self, session=None, without_exception=False):  # pylint: disable=no-self-use
        ''' Safe commit. Auto-rollback when raise except. '''
        session = session or DB.session

        try:
            session.commit()
        except Exception:
            session.rollback()
            if not without_exception:
                raise
            return False
        return True

DB = SQLAlchemy()
# REDIS = FlaskRedis()
