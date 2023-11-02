Quickstart
----------

.. teaser-begin

A helper for jupyter(lab/notebook/console).

|python-support| |downloads| |license| |black| |openissues| |GHDiscussion|

.. teaser-end

Installation
------------

Install via pip:
  pip install jupyter-helper

Or you can use an editable install with:
  git clone https://github.com/lll9p/jupyter-helper.git
  cd  jupyter-helper
  pip install -e . --no-build-isolation


Usage
-----

to run:
  from helper import Helper
  helper = Helper(scope=globals())
  helper.set_global_values().import_libs().run_magics().done()

or
  helper.done()

.. |latest-version| image:: https://img.shields.io/pypi/v/jupyter-helper.svg
   :alt: Latest version on PyPI
   :target: https://pypi.org/project/jupyter-helper
.. |python-support| image:: https://img.shields.io/pypi/pyversions/jupyter-helper.svg
   :target: https://pypi.org/project/jupyter-helper
   :alt: Python versions
.. |downloads| image:: https://img.shields.io/pypi/dm/jupyter-helper.svg
   :alt: Monthly downloads from PyPI
   :target: https://pypi.org/project/jupyter-helper
.. |license| image:: https://img.shields.io/pypi/l/jupyter-helper.svg
   :alt: Software license
   :target: https://github.com/lll9p/jupyter-helper/blob/master/LICENSE
.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black
    :alt: Black Formatter
.. |openissues| image:: http://isitmaintained.com/badge/open/lll9p/jupyter-helper.svg
    :target: http://isitmaintained.com/project/lll9p/jupyter-helper
    :alt: Percentage of open issues
.. |GHAction| image:: https://github.com/lll9p/jupyter-helper/workflows/Python/badge.svg
    :alt: Python
.. |GHDiscussion| image:: https://shields.io/badge/GitHub-%20Discussions-green?logo=github
    :target: https://github.com/lll9p/jupyter-helper/discussions
    :alt: GitHub Discussion
