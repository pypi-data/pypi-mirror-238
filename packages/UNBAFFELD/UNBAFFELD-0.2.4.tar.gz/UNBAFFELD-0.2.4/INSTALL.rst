Basic Installation
------------------

UNBAFFELD is available on PyPI and Conda-Forge. To install, you need python >=3.6.  Then do::

    pip install unbaffeld
or::

    conda install unbaffeld

After this, within python the package can be used by standard import statements::

    import unbaffeld

or::

    from unbaffeld.gpr.gpfit import GPTSFit

Advanced Local Installation
---------------------------

UNBAFFELD can also be used directly from the repository, or from the
standard python setuptools build system.   The documentation is designed with
both workflows in mind, but here we discuss the standard setuptools system.

To build and install UNBAFFELD, the steps are::

    python setup.py build
    python setup.py install

The installation directory by default is the site-packages directory for the
python used in the above command.  To specify a different location::

    python setup.py --prefix=<path to installation> install

Running tests
-------------

We use pyest for testing.  It automatically runs all `test_*.py` files in the
given directory and subdirectories::

    pytest unbaffeld

Running linter
--------------

We use mypy for testing types::

    mypy -v --ignore-missing-imports --html-report mypy_log-html unbaffeld/database

We also excpect that flake8 should pass.  Eventually we will move to having
black as a pre-hook.

Making documentation
--------------------

We use `sphinx` for our documentation::

    cd docs
    make html
