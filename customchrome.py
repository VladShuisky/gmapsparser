import undetected_chromedriver
from config import config
from selenium.webdriver import ActionChains
from selenium.webdriver import DesiredCapabilities
from undetected_chromedriver import ChromeOptions
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeWithDebugMode:
    def __init__(self) -> None:
        self.driver = Chrome(
            service=Service(ChromeDriverManager().install()),
            # options=self._set_options(),
            # desired_capabilities=self._set_capabilities()
        )
        self.action_chains = ActionChains(self.driver)

    def _set_options(self):
        options = ChromeOptions()
        options.add_experimental_option("debuggerAddress", '127.0.0.1:9222')
        return options

    def _set_capabilities(self):
        capabilities = DesiredCapabilities.CHROME
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        return capabilities


class UndetectedChromeWithDebugMode(ChromeWithDebugMode):
    def __init__(self) -> None:
        self.driver = undetected_chromedriver.Chrome(
            driver_executable_path=config.DRIVER_EXEC_PATH,
            desired_capabilities=self._set_capabilities(),
            options=self._set_options()
        )
        self.action_chains = ActionChains(self.driver)
