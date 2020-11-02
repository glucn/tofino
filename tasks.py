import os

from invoke import task

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


@task()
def run(ctx):
    os.environ['PYTHONPATH'] = os.path.join(BASE_DIR, 'src')
    os.environ['FLASK_APP'] = os.path.join(BASE_DIR, 'src', 'main.py')
    ctx.run('python -m flask run')


@task()
def test(ctx):
    os.environ['PYTHONPATH'] = os.path.join(BASE_DIR, 'src')
    ctx.run('python -m unittest discover -s tests -p *_test.py')


@task()
def pylint(ctx):
    ctx.run('flake8 . --count --select=E9,F4,F63,F7,F82 --show-source --statistics')
