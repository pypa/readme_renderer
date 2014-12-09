Then, you can create a *development environment* like this,
if you have **virtualenv** installed:

    $ virtualenv --no-site-packages .
    $ pip install -r requirements.txt

Then you can launch the server using the `pypi.wsgi` script:

    $ python pypi.wsgi
    Serving on port 8000...

PyPI will be available in your browser at http://localhost:8000
