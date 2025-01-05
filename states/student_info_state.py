
from time import sleep
from core.base_state import BaseState
from core.logger import get_logger
from constants import xpathes
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class StudentInfoState(BaseState):
    def __init__(self, context):
        super().__init__(context)
        self.logger = get_logger(self.__class__.__name__)
    
    def handle(self):
        self._go_to_etelaate_jame_daneshjoo_page()

        self._go_to_semester(semester=self.context.config.semester)

        sleep(5)

        from .check_grades_state import CheckGradesState
        self.context.change_state(CheckGradesState(self.context))

    def _go_to_etelaate_jame_daneshjoo_page(self):
        try:
            self.logger.info('going to etelaate_jame_daneshjoo_page...')
            self.switch_to_main_frame(faci_id=2)
            sleep(4)
            student_full_info = self.driver.find_element(By.XPATH, '//*[@id="mendiv"]/table/tbody/tr[6]/td')
            for _ in range(0, 2): student_full_info.click()
            sleep(4)
        except (NoSuchElementException, TimeoutException):
            self.logger.info("Error in get full info page, going to LoginState")
            from .login_state import LoginState
            self.context.change_state(LoginState(self.context))

    def _go_to_semester(self, semester=None):
        self.logger.info('Going to semester...')
        self.driver.switch_to.default_content()
        sleep(2)
        self.switch_to_main_frame(3)

        terms_status_table = self.driver.find_element(By.XPATH, """//table[@id="T01"]""")
        term_field = terms_status_table.find_element(By.XPATH,
                                                    f"""//tr[@class="TableDataRow"][{semester}]/td[1]""")
        term_field.click()
        sleep(3)
        self.driver.switch_to.frame('FrameNewForm')