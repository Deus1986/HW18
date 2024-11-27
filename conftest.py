import pytest
from dotenv import load_dotenv
from selene import browser
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="function", autouse=True)
def setup_browser(request):
    browser.config.base_url = "https://demowebshop.tricentis.com/"
    options = Options()
    options.add_argument("window-size=1920,1080")

    yield browser
    browser.quit()
