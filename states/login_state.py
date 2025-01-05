from time import sleep
from core.base_state import BaseState
from core.logger import get_logger
from constants import xpathes
from selenium.webdriver.common.by import By


class LoginState(BaseState):
    def __init__(self, context):
        super().__init__(context)
        self.logger = get_logger(self.__class__.__name__)

    def handle(self):
        self.driver.get(self.context.config.main_page_url)
        self.logger.info("Navigating to the Golestan login page...")
        sleep(4)

        self.switch_to_main_frame(faci_id=1)

        self.fill_field(field_id=xpathes.USERNAME_FIELD_ID, value=self.context.config.golestan_username)
        self.fill_field(field_id=xpathes.PASSWORD_FIELD_ID, value=self.context.config.golestan_password)

        self.captcha_solver.solve_it(xpathes.CAPTCHA_IMAGE_ID, xpathes.CAPTCHA_FIELD_ID)

        self.click_button(xpathes.LOGIN_BTN_ID)
        self.driver.switch_to.default_content()

        sleep(3)

        try:
            self.driver.switch_to.frame("Faci1")
            self.logger.info("Switched to the 'Faci1' frame.")
            self.driver.switch_to.frame("Message")
            self.logger.info("Switched to the 'Message' frame.")

            message_element = self.driver.find_element(By.XPATH, "/html/body/table/tbody/tr[1]/td[6]")
            message_text = message_element.text

            if "لطفا كد امنيتي را به صورت صحيح وارد نماييد" in message_text:
                self.logger.info(f"Error message is present!")
                self.handle()
            else:
                self.logger.info("Error message not found.")

        except Exception as e:
            self.logger.error(f"Error in switching to Message frame: {e}")

        finally:
            self.driver.switch_to.default_content()


        # Lazy Import
        from .student_info_state import StudentInfoState
        self.context.change_state(StudentInfoState(self.context))
        self.logger.info("Changing state to StudentInfoState")



    

