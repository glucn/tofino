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
