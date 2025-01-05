# Base State class (abstract class)
from abc import ABC, abstractmethod
from core.logger import get_logger
from utils.captcha_solver import BotCaptchaSolver
from utils.telegram_bot import TelegramBot
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaseState(ABC):

    def __init__(self, context):
        self.context = context
        self.driver = self.context.driver
        self.logger = get_logger(self.__class__.__name__)
        self.captcha_solver = BotCaptchaSolver(driver=self.driver, api_key=self.context.config.api_key)
        self.telegram_bot = TelegramBot(token=self.context.config.bot_token, chat_id=self.context.config.chat_id)

    @abstractmethod
    def handle(self):
        pass

    def wait_for_element(self, element_id, timeout=20):
        """Utility method to wait for an element to be present."""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            self.logger.debug(f"Element found at {element_id}")

            return element
        except Exception as e:
            self.logger.exception(f"Timeout waiting for element at {element_id} - Exception: {e}")
            raise

    def switch_to_main_frame(self, faci_id):
        # frame_names = (f'Faci{str(faci_id)}', 'Master', 'Form_Body')
        # for name in frame_names:
        #     try:
        #         frame = self.driver.find_element(By.NAME, name)
        #         self.driver.switch_to.frame(frame)
        #         self.logger.info(f'Successfully switched to frame: {name}')
        #         # return  # Exit the method once the correct frame is found and switched to
        #     except Exception as e:
        #         self.logger.warning(f'Could not switch to frame: {name}. Error: {str(e)}') 

        # self.logger.error('Failed to switch to any of the specified frames.')
        # raise Exception('FrameNotFoundError: None of the specified frames were accessible.')

        frame_names = (f'Faci{str(faci_id)}', 'Master', 'Form_Body')
        for name in frame_names:
            frame = self.driver.find_element(By.NAME, name)
            self.logger.info(f'switched to: {frame.tag_name}')
            self.driver.switch_to.frame(frame)

    def fill_field(self, field_id, value):
        """Utility method to fill form fields."""
        try:
            field = self.wait_for_element(field_id, timeout=10)
            field.clear()
            field.send_keys(value)
            self.logger.debug(f"Filled field at {field_id} with value: {value}")
        except Exception as e:
            self.logger.exception(f"Failed to fill field at {field_id} with value: {value} - Exception: {e}")

    def click_button(self, button_id):
        """Utility method to click buttons."""
        try:
            button = self.wait_for_element(button_id, timeout=10)
            button.click()
            self.logger.debug(f"Clicked button at {button_id}")
        except Exception as e:
            self.logger.exception(f"Failed to click button at {button_id} - Exception: {e}")