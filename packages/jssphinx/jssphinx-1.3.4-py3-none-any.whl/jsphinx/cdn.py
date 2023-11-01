__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "ALABASTER_URL",
    "BOOTSTRAP_URL",
    "CDN_URL_BASE",
    "DOWNLOAD_ADAPTER_URL",
    "FURO_URL",
    "PYDATA_SPHINX_THEME_URL",
    "SPHINX_MATERIAL_URL",
    "SPHINX_RTD_THEME_URL",
)

CDN_URL_BASE = "https://cdn.jsdelivr.net/gh/barseghyanartur/jsphinx/"

DOWNLOAD_ADAPTER_URL = f"{CDN_URL_BASE}src/js/download_adapter.js"

ALABASTER_URL = f"{CDN_URL_BASE}css/alabaster.css"
FURO_URL = f"{CDN_URL_BASE}css/furo.css"
PYDATA_SPHINX_THEME_URL = f"{CDN_URL_BASE}css/pydata_sphinx_theme.css"
BOOTSTRAP_URL = f"{CDN_URL_BASE}css/bootstrap.css"
SPHINX_MATERIAL_URL = f"{CDN_URL_BASE}css/sphinx_material.css"
SPHINX_RTD_THEME_URL = f"{CDN_URL_BASE}css/sphinx_rtd_theme.css"
