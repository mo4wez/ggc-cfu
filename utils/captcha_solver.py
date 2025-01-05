# Utility for solving CAPTCHAs
import os
from twocaptcha import TwoCaptcha
from core.logger import get_logger
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BotCaptchaSolver:
    def __init__(self, driver, api_key, captchas_directory='captchas'):
        self.driver = driver
        self.logger = get_logger(self.__class__.__name__)
        self.api_key = api_key
        self.captchas_directory = captchas_directory
        self.twocaptcha_solver = TwoCaptcha(self.api_key, pollingInterval=3, softId=123)

    def solve_it(self, captcha_image_id, field_id):
        """
        Main method to solve the CAPTCHA.
        """
        try:
            captcha_image = self.capture_captcha_image(captcha_image_id)
            self.logger.debug(f"Captcha image saved.")

            # Solve CAPTCHA using 2Captcha API with local image path
            result = self.twocaptcha_solver.normal(captcha_image)
            extracted_text = result['code']
            self.logger.info(f"Captcha result: {extracted_text.upper()}")

            self.enter_captcha_code(extracted_text, field_id)

            # Clean up the local image file after solving
            # self.remove_captcha_image(captcha_image_path)

            return True
        except Exception as e:
            self.logger.error(f"Error solving CAPTCHA: {e}")
            return False

    def capture_captcha_image(self, captcha_image_id):
        """
        Capture the CAPTCHA image from the webpage using Selenium's element screenshot feature.

        Args:
            captcha_image_xpath: XPath to locate CAPTCHA image element.

        Returns:
            str: The local path where the CAPTCHA image is saved.
        """
        try:
            # Locate the CAPTCHA image element
            captcha_image_element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, captcha_image_id))
            )

            # Generate the file path for saving the CAPTCHA image
            # captcha_image_path = os.path.join(self.captchas_directory, 'captcha_image.png')

            # Take a screenshot of the CAPTCHA image element
            img64 = captcha_image_element.screenshot_as_base64

            return img64

        except Exception as e:
            self.logger.error(f"Error capturing CAPTCHA image: {e}")
            raise

    def enter_captcha_code(self, code, field_id):
        # Enter the CAPTCHA solution in the form field
        captcha_field = self.driver.find_element(By.ID, field_id)
        captcha_field.clear()
        captcha_field.send_keys(str(code))

    def refresh_captcha(self, captcha_refresh_id):
        captcha_refresh = self.driver.find_element(By.ID, captcha_refresh_id)
        captcha_refresh.click()
        self.logger.info("Refreshed CAPTCHA image.")

    def remove_captcha_image(self, captcha_image_path):
        """
        Removes the saved CAPTCHA image file after processing.

        Args:
            captcha_image_path: The local path of the CAPTCHA image file.
        """
        try:
            if os.path.exists(captcha_image_path):
                os.remove(captcha_image_path)
                self.logger.debug(f"Captcha image removed from local directory: {captcha_image_path}")
            else:
                self.logger.warning(f"Captcha image path does not exist: {captcha_image_path}")
        except Exception as e:
            self.logger.error(f"Error removing CAPTCHA image: {e}")
