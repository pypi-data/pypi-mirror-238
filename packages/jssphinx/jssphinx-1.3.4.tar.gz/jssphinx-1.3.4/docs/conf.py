# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os

# Check if we're running on Read the Docs' servers
on_rtd = os.environ.get("READTHEDOCS", None) == "True"
branch_name = os.environ.get("READTHEDOCS_VERSION", "sphinx_rtd_theme")
if branch_name in {"main", "dev", "latest"}:
    branch_name = "sphinx_rtd_theme"

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "jsphinx"
copyright = "2023, Artur Barseghyan"
author = "Artur Barseghyan"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
]
pygments_style = "sphinx"
templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = branch_name
# html_theme = "sphinx_rtd_theme"
# html_theme = "alabaster"
# html_theme = "sphinx_material"
# html_theme = "bootstrap"
# html_theme = "furo"
# html_theme = "sphinx_book_theme"
# html_theme = "pydata_sphinx_theme"

html_static_path = ["_static"]

prismjs_base = "https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0"

html_css_files = [
    f"{prismjs_base}/themes/prism.min.css",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.css",
    # f"https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/css/{html_theme}.css",
    f"themes/{html_theme}.css",
]

html_js_files = [
    f"{prismjs_base}/prism.min.js",
    f"{prismjs_base}/plugins/autoloader/prism-autoloader.min.js",
    f"{prismjs_base}/plugins/toolbar/prism-toolbar.min.js",
    f"{prismjs_base}/plugins/copy-to-clipboard/prism-copy-to-clipboard.min.js",
    # "//cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/src/js/download_adapter.js",
    "scripts/download_adapter.js",
]

# # For some themes, jQuery would need to be included in the conf.py:
# html_js_files.insert(
#     0,
#     "//cdnjs.cloudflare.com/ajax/libs/jquery/3.7.1/jquery.min.js",
# )
