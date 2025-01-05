
import os
import json
import time
from core.base_state import BaseState
from core.logger import get_logger
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


class CheckAbsencesState(BaseState):
    def __init__(self, context):
        super().__init__(context)
        self.logger = get_logger(self.__class__.__name__)
        self.telegram_bot = self.telegram_bot
    
    def handle(self):
        self.check_absences()

    def check_absences(self):
        try:
            self.logger.info("Putting 1950")
            self.switch_to_main_frame(faci_id=2)
            number_field = self.wait_for_element(element_id="F20851")
            number_field.clear()
            number_field.send_keys("1950")

            sleep(2)

            self.logger.info("clicking OK button...")
            self.click_button(button_id="OK")

            sleep(7)
            self.driver.switch_to.default_content()
            self.switch_to_main_frame(faci_id=3)
            self.fill_field(field_id="GF41254_0", value="40111913299")

            sleep(1)

            # click show report button
            self.driver.switch_to.default_content()
            self.switch_to_main_frame(faci_id=4)
            self.click_button(button_id="IM16_ViewRep")

            sleep(3)

            # extracting absences
            table_body = self.driver.find_element(By.TAG_NAME, 'tbody')
            rows = table_body.find_elements(By.CSS_SELECTOR, 'tr.CTRData')

            for row in rows:
                course_name = row.find_element(By.XPATH, '//*[@id="Table3"]/tbody/tr[1]/td[3]').text.strip()
                absence_date = row.find_element(By.XPATH, '//*[@id="Table3"]/tbody/tr[1]/td[5]').text

                print(f"{course_name} - {absence_date}")

        except Exception as e:
            self.logger.error(f"Error: {e}")
            self.handle()

