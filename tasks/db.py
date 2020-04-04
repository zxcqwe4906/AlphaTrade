import os
import sys
from invoke import task

def get_project_root(path=__file__):
    directory = os.path.dirname(path)

    while directory != '/':
        p = os.path.join(directory, 'requirements.txt')
        if os.path.isfile(p):
            return directory
        else:
            directory = os.path.dirname(directory)

    return None

def _exec_db_task(ctx, cmd):
    config = ctx['config']
    password = ':' + config['MYSQL_PASSWORD'] if config['MYSQL_PASSWORD'] else ''

    url = 'mysql+pymysql://{}{}@{}:{}/{}?charset=utf8'.format(
        config['MYSQL_USERNAME'],
        password,
        config['ALEMBIC_MYSQL_HOST'],
        config['MYSQL_PORT'],
        config['MYSQL_DATABASE'])
    dir = os.path.join(get_project_root(__file__), 'migrations')
    ctx.run(f'cd {dir} && alembic -x dburl={url} {cmd}')

@task
def migrate(ctx):
    _exec_db_task(ctx, 'upgrade head')

@task
def upgrade(ctx, revision):
    _exec_db_task(ctx, 'upgrade {revision}')

@task
def downgrade(ctx, revision):
    _exec_db_task(ctx, f'downgrade {revision}')

@task
def reset(ctx):
    _exec_db_task(ctx, 'downgrade base')

@task
def version(ctx):
    _exec_db_task(ctx, 'current')

@task
def history(ctx):
    _exec_db_task(ctx, 'history')

@task
def sql(ctx):
    _exec_db_task(ctx, 'upgrade head --sql > init.sql')

@task
def revision(ctx, msg):
    _exec_db_task(ctx, f'revision --autogenerate -m "{msg}"')