import logging
import socket
import subprocess
import time
import unittest
from subprocess import Popen

from get_chromedriver import run as get_chromedriver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

__author__ = "Artur Barseghyan <artur.barseghyan@gmail.com>"
__copyright__ = "2023 Artur Barseghyan"
__license__ = "MIT"
__all__ = (
    "DocumentationTest",
    "build_documentation",
    "is_valid_python_code",
)

LOGGER = logging.getLogger(__name__)
DOCS_DIR = "testdocs"


def build_documentation() -> None:
    """Build documentation."""
    try:
        # Invoke the sphinx-build command
        subprocess.check_call(
            ["sphinx-build", "-n", "-a", "-b", "html", "docs", DOCS_DIR],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as err:
        LOGGER.error(f"Error building documentation: {err}")
        raise err


def is_valid_python_code(text) -> bool:
    """Check if the given text is a valid Python code.

    Usage example:

    .. code-block:: python

        text = '''
        def my_function(x):
            print(x)
        '''

        print(is_valid_python_code(text))
    """
    try:
        compile(text, "<string>", "exec")
        return True
    except SyntaxError:
        return False


class DocumentationTest(unittest.TestCase):
    server_process: "Popen"
    driver: "WebDriver"
    port: int

    @classmethod
    def setUpClass(cls) -> None:
        build_documentation()
        get_chromedriver()
        # Find an available port dynamically
        cls.port = cls.find_available_port()

        # Start the HTTP server in the background
        cls.server_process = subprocess.Popen(
            ["python", "-m", "http.server", str(cls.port)],
            cwd=DOCS_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        time.sleep(2)  # Give the server some time to start

        # Configure Chrome to run in headless mode
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls) -> None:
        # Stop the HTTP server
        cls.server_process.terminate()
        cls.server_process.wait()

        # Quit the browser
        cls.driver.quit()

    @staticmethod
    def find_available_port() -> int:
        """Find available port by binding to a socket and then releasing it."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("localhost", 0))
            return s.getsockname()[1]

    def test_documentation_links(self) -> None:
        """Test documentation links."""
        # Use the dynamically determined port and local server URL
        documentation_url = f"http://localhost:{self.port}/examples.html"
        self.driver.get(documentation_url)

        # Find and click the links
        link_elements = self.driver.find_elements(
            By.CSS_SELECTOR,
            ".jsphinx-download a.reference.download.internal",
        )
        for link in link_elements:
            LOGGER.info(link.get_attribute("href"))
            # print(link.get_attribute("href"))
            link.click()

            wait = WebDriverWait(self.driver, 10)
            fetched_div = wait.until(
                EC.presence_of_element_located(
                    (
                        By.XPATH,
                        (
                            '//a[contains(@class, "reference download internal")]'
                            '/following-sibling::div[contains(@class, "fetched")]'
                        ),
                    )
                )
            )
            LOGGER.info(fetched_div.text)
            # print(fetched_div.text)
            self.assertTrue(fetched_div.is_displayed())
            # Check if the code is a valid Python code
            self.assertTrue(is_valid_python_code(fetched_div.text))
