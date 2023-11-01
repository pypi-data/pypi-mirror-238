=======
jsphinx
=======
**Improve developer experience**:
Write better docs. Stay concise. Never miss a detail.

.. image:: https://img.shields.io/github/v/release/barseghyanartur/jsphinx?label=Version&color=blue
   :target: https://github.com/barseghyanartur/jsphinx/releases
   :alt: jsDelivr version

.. image:: https://data.jsdelivr.com/v1/package/gh/barseghyanartur/jsphinx/badge
   :target: https://github.com/barseghyanartur/jsphinx/releases
   :alt: jsDelivr stats

.. image:: https://img.shields.io/pypi/v/jssphinx.svg
   :target: https://pypi.python.org/pypi/jssphinx
   :alt: PyPI Version

.. image:: https://img.shields.io/pypi/pyversions/jssphinx.svg
    :target: https://pypi.python.org/pypi/jssphinx/
    :alt: Supported Python versions

.. image:: https://github.com/barseghyanartur/jsphinx/actions/workflows/test.yml/badge.svg?branch=main
   :target: https://github.com/barseghyanartur/jsphinx/actions
   :alt: Build Status

.. image:: https://readthedocs.org/projects/jsphinx/badge/?version=sphinx_rtd_theme
    :target: http://jsphinx.readthedocs.io/
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
   :target: https://github.com/barseghyanartur/jsphinx/#License
   :alt: MIT

.. Dependencies

.. _Sphinx: https://github.com/sphinx-doc/sphinx
.. _PrismJS: https://github.com/PrismJS/prism
.. _pytest: https://github.com/pytest-dev/pytest/

.. Themes

.. _alabaster: https://github.com/sphinx-doc/alabaster
.. _furo: https://github.com/pradyunsg/furo
.. _pydata-sphinx-theme: https://pypi.org/project/pydata-sphinx-theme/
.. _sphinx-book-theme: https://pypi.org/project/sphinx-book-theme/
.. _sphinx-bootstrap-theme: https://pypi.org/project/sphinx-bootstrap-theme/
.. _sphinx-material: https://github.com/bashtage/sphinx-material
.. _sphinx-rtd-theme: https://github.com/readthedocs/sphinx_rtd_theme

.. Project

.. _GitHub issues: https://github.com/barseghyanartur/jsphinx/issues

.. Demos

.. _alabaster demo: https://jsphinx.readthedocs.io/en/alabaster/examples.html
.. _furo demo: https://jsphinx.readthedocs.io/en/furo/examples.html
.. _pydata-sphinx-theme demo: https://jsphinx.readthedocs.io/en/pydata_sphinx_theme/examples.html
.. _sphinx-book-theme demo: https://jsphinx.readthedocs.io/en/sphinx_book_theme/examples.html
.. _sphinx-bootstrap demo: https://jsphinx.readthedocs.io/en/bootstrap/examples.html
.. _sphinx-material demo: https://jsphinx.readthedocs.io/en/sphinx_material/examples.html
.. _sphinx-rtd-theme demo: https://jsphinx.readthedocs.io/en/sphinx_rtd_theme/examples.html
.. _faker-file documentation: https://faker-file.readthedocs.io/en/latest/creating_pdf.html#building-pdfs-with-text-using-reportlab
.. _jsphinx-download demo: https://jsphinx.readthedocs.io/en/sphinx_rtd_theme/examples.html#jsphinx-download-directive-usage
.. _jsphinx-toggle-emphasis demo: https://jsphinx.readthedocs.io/en/sphinx_rtd_theme/examples.html#jsphinx-toggle-emphasis-directive-usage

----

``jsphinx`` helps you to achieve what's mentioned above.
You could see it as a mix of loosely coupled software components and
guidelines to make things perfect.

Let me ask you a couple of conceptually connected questions:

- Do you write documentation?
- If you do, do you provide code examples along?
- Are you able to test them? Do you want to?
- Do you struggle making examples compact, yet fully functional?
- And do you want to learn how?

What if I tell you that there's an easy, non-intrusive solution?
It doesn't reinvent the wheel; just leverages what's already there.

Move on to the `demos`_ section to see it in action.

Demos
=====

See the list of available demos below. Pick a demo and from within the example
page, click on any ``See the full example`` link to see how it works.

- `alabaster demo`_
- `furo demo`_
- `pydata-sphinx-theme demo`_
- `sphinx-book-theme demo`_
- `sphinx-bootstrap demo`_
- `sphinx-material demo`_
- `sphinx-rtd-theme demo`_
- `faker-file documentation`_

Impressed? Want to know how it works?

Under the hood
==============
``jsphinx-download`` directive
------------------------------
`Sphinx`_ is a documentation generator. It has many directives, among which
the ``.. literalinclude::``, which allows us to include content of a file
directly into your documentation.

``.. literalinclude::`` itself has a ``:lines:`` option, which allows us to
specify which parts of the code to show. That's what we use to keep the
primary focus on the most important parts of the code, reducing cognitive
load for the reader.

Consider the following code example stored in a
file ``_static/py/faker_file_docx_1.py``:

.. code-block:: python

   import os

   # Required imports
   from faker import Faker
   from faker_file.providers.docx_file import DocxFileProvider

   FAKER = Faker()  # Initialize Faker
   FAKER.add_provider(DocxFileProvider)  # Register DocxFileProvider

   # Generate DOCX file
   docx_file = FAKER.docx_file()

   # Test things out
   print(docx_file)
   print(docx_file.data["filename"])
   assert os.path.exists(docx_file.data["filename"])

See the following snippet:

.. code-block:: rst

    .. literalinclude:: _static/py/faker_file_docx_1.py
       :language: python
       :lines: 3-11

The above mentioned snippet will be rendered as follows:

.. code-block:: python

    # Required imports
    from faker import Faker
    from faker_file.providers.docx_file import DocxFileProvider

    FAKER = Faker()  # Initialize Faker
    FAKER.add_provider(DocxFileProvider)  # Register DocxFileProvider

    # Generate DOCX file
    docx_file = FAKER.docx_file()

However, we also understand the importance of the broader context. For that
we use the ``:download:`` directive, which allows us to create a downloadable
link to a file (the same file we already included into the documentation
using ``.. literalinclude::``). By that we ensure that those interested in the
complete code can easily access it.

See the following snippet:

.. code-block:: rst

    .. container:: jsphinx-download

        *See the full example*
        :download:`here <_static/py/faker_file_docx_1.py>`

The above mentioned snippet will be produce the following HTML:

.. code-block:: html

   <p class="jsphinx-download">
     <em>See the full example</em>
     <a class="reference download internal" href="_static/py/faker_file_docx_1.py">
       <span class="pre">here</span>
     </a>
   </p>

*See the* `jsphinx-download demo`_ *to see how it's rendered.*

This is where ``jsphinx`` steps in. Using provided JavaScript,
we hook to the links generated by the ``:download:`` directive and instead
of downloading the content, show it in-line, right in place.

Note, that although ``.. container:: jsphinx-download`` technically
isn't strictly required, it wraps our link into an element with
``jsphinx-download`` class so that we can safely hook to all underlying
download links without a risk to cause unwanted behavior for other places
where you might have used ``:download:`` directive for other purposes.

Finally, `PrismJS`_ syntax highlighter is used to beautify the code and make
it look close to the code highlighting of your `Sphinx`_ theme of choice.

``jsphinx-toggle-emphasis`` directive
-------------------------------------
Another popular `Sphinx`_ directive is the ``.. code-block::``, which enables
us to display code blocks within your documentation.

The ``.. code-block::`` directive itself has a ``:emphasize-lines:`` option,
which is particularly useful for highlighting specific lines of code within
the code block. This helps to draw attention to most important  parts of the
code and helps the reader to understand the code.

Consider the following example:

.. code-block:: rst

    .. container:: jsphinx-toggle-emphasis

        .. code-block:: python
            :emphasize-lines: 3,6,8

            from faker import Faker
            # Import the file provider we want to use
            from faker_file.providers.txt_file import TxtFileProvider

            FAKER = Faker()  # Initialise Faker instance
            FAKER.add_provider(TxtFileProvider)  # Register the file provider

            txt_file = FAKER.txt_file()  # Generate a TXT file

*See the* `jsphinx-toggle-emphasis demo`_ *to see how it's rendered.*

``jsphinx`` will add a link to each ``.. container:: jsphinx-toggle-emphasis``
block for toggling the visibility of non-emphasized elements.

Themes
======

`PrismJS`_ themes based on `Sphinx`_'s aesthetics:

- `alabaster`_ (key: ``alabaster``, `alabaster demo`_)
- `furo`_ (key: ``furo``, `furo demo`_)
- `pydata-sphinx-theme`_ (key: ``pydata_sphinx_theme``,
  `pydata-sphinx-theme demo`_)
- `sphinx-book-theme`_ (key: ``sphinx_book_theme``, `sphinx-book-theme demo`_)
- `sphinx-bootstrap-theme`_ (key: ``bootstrap``, `sphinx-bootstrap demo`_)
- `sphinx-material`_ (key: ``sphinx_material``, `sphinx-material demo`_)
- `sphinx-rtd-theme`_ (key: ``sphinx_rtd_theme``, `sphinx-rtd-theme demo`_)

Installation
============

Via CDN (jsDelivr)
------------------

To use both the theme and adapter in your HTML:

.. code-block:: html

   <!-- CSS for PrismJS Sphinx RTD theme -->
   <link href="https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/sphinx_rtd_theme.css"
         rel="stylesheet">

   <!-- JS for PrismJS Sphinx Adapter -->
   <script src="https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js">
   </script>

Sphinx integration
==================

Configuration
-------------

To integrate both into your `Sphinx`_ project, add the following in
your ``conf.py``:

.. code-block:: python

   # ************************************************************
   # ************************** The theme ***********************
   # ************************************************************
   html_theme = "sphinx_rtd_theme"

   # ************************************************************
   # ***************** Additional JS/CSS files ******************
   # ************************************************************
   html_css_files = [
       # ...
       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/sphinx_rtd_theme.css",
       # ...
   ]

   html_js_files = [
       # ...
       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js",
       # ...
   ]

A complete configuration example, together with loaded `PrismJS`_ and the
toolbar with plugins, would look as follows:

.. code-block:: python

   prismjs_base = "//cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"

   html_css_files = [
       f"{prismjs_base}/themes/prism.min.css",
       f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.css",
       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/sphinx_rtd_theme.css",
   ]

   html_js_files = [
       f"{prismjs_base}/prism.min.js",
       f"{prismjs_base}/plugins/autoloader/prism-autoloader.min.js",
       f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.js",
       f"{prismjs_base}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
       "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js",
   ]

----

You can also use other `Sphinx`_ themes, such as `alabaster`_, `furo`_,
`pydata-sphinx-theme`_, `sphinx-book-theme`_, `sphinx-bootstrap-theme`_,
`sphinx-material`_ or `sphinx-rtd-theme`_.

Make sure to specify appropriate value (theme key) in ``html_theme``,
as follows (pick one):

.. code-block:: python

   html_theme = "alabaster"
   html_theme = "bootstrap"
   html_theme = "furo"
   html_theme = "pydata_sphinx_theme"
   html_theme = "sphinx_book_theme"
   html_theme = "sphinx_material"
   html_theme = "sphinx_rtd_theme"

Finally, make sure to specify correct path to the desired theme:

.. code-block:: python

   html_css_files = [
       # ...
       f"https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/{html_theme}.css",
   ]

Testing your documentation
==========================

All code snippets of this repository can be tested with `pytest`_ as follows:

.. code-block:: sh

    pytest

The `pytest`_ test-runner finds tests in the ``docs/test_docs.py`` module,
which is responsible for dynamical execution of Python files located in the
``docs/_static/py/`` directory.

This is how ``docs/test_docs.py`` could look:

.. code-block:: python

    from pathlib import Path
    import pytest

    # Walk through the directory and all subdirectories for .py files
    example_dir = Path("docs/_static/py")
    py_files = sorted([str(p) for p in example_dir.rglob("*.py")])

    def execute_file(file_path):
        """Dynamic test function."""
        global_vars = {}
        with open(file_path, "r") as f:
            code = f.read()
        exec(code, global_vars)

    @pytest.mark.parametrize("file_path", py_files)
    def test_dynamic_files(file_path):
        execute_file(file_path)

License
=======

MIT

Support
=======

For security issues contact me at the e-mail given in the `Author`_ section.

For overall issues, go to `GitHub issues`_.

Author
======

Artur Barseghyan
`artur.barseghyan@gmail.com <artur.barseghyan@gmail.com>`__.
