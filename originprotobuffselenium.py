import json
import time
from typing import Optional

from undetected_chromedriver import Chrome
from undetected_chromedriver import By
from selenium.webdriver import ActionChains

from originprotobufgetterbase import OriginProtobufGetterBase
from config import config

class OriginProtobufSelenium(OriginProtobufGetterBase):
    def __init__(self, driver: Chrome, driver_action_chains: ActionChains ,link_to_place: str) -> None:
        super().__init__()
        self.driver = driver
        self.driver_action_chains = driver_action_chains
        self.url = link_to_place
        self.x_path_of_button = config.BUTTON_REVIEW_XPATH
        self.google_rpc_reviews_base_url = config.GMAPS_RPC_REVIEWS_URL

    def get_origin_protobuf(self) -> Optional[str]:
        self.driver.get(self.url)
        time.sleep(5)
        button_reviews = self.driver.find_element(By.XPATH, self.x_path_of_button)
        self.driver_action_chains.scroll_to_element(button_reviews).perform()
        button_reviews.click()
        time.sleep(5)
        logs: list = self.driver.get_log('performance')
        url = self.get_url_with_pb_from_log(logs)
        self.driver.close()
        return self.get_pb_from_url(url)

    def get_pb_from_url(self, url) -> Optional[str]:
        try:
            return url.split('&')[-1].split('=')[-1]
        except Exception:
            print(
                f'Не удалось извлечь pb из урла по причине его некорректности',
                f'URL >>> {url}'
            ) # TODO сделать логгер!
            return None
 
    def get_url_with_pb_from_log(self, logs: list) -> Optional[str]:
        """
        Return only logs which have a method that start with "Network.response", "Network.request", or "Network.webSocket"
        since we're interested in the network events specifically.
        """
        for entry in logs:
            log = json.loads(entry["message"])["message"]
            if (
                    "Network.requestWillBeSent" in log["method"]
                    and log["params"].get("request")
                    and log["params"]["request"].get("url")
                    and log["params"]["request"]["url"].startswith(self.google_rpc_reviews_base_url)
                    # or "Network.response" in log["method"]
            ):
                return log["params"]["request"]["url"]
        return None