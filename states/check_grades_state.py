
import os
import json
import time
from core.base_state import BaseState
from core.logger import get_logger
from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup


class CheckGradesState(BaseState):
    def __init__(self, context, notified_grades_file=None, refresh_interval=15):
        super().__init__(context)
        self.logger = get_logger(self.__class__.__name__)
        self.notified_grades_file = notified_grades_file or os.path.abspath("./grades.json")
        self.notified_grades = self._load_notified_grades()
        self.telegram_bot = self.telegram_bot
        self.refresh_interval = refresh_interval
    
    def handle(self):
        self.monitor_grades()

    def _load_notified_grades(self):
        """Load notified grades from a JSON file."""
        if os.path.exists(self.notified_grades_file):
            self.logger.info("loading grades file.")
            with open(self.notified_grades_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return {}  # Empty dictionary if the file does not exist

    def _save_notified_grades(self):
        """Save notified grades to a JSON file."""
        self.logger.info(f"Saving grades file at {self.notified_grades_file}.")
        # Ensure directory exists
        directory = os.path.dirname(self.notified_grades_file)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(self.notified_grades_file, 'w', encoding='utf-8') as file:
            json.dump(self.notified_grades, file, ensure_ascii=False, indent=4)

    # def _find_term_grades(self):
    #     """Extract grades from the table."""
    #     self.logger.info("Extracting grades from the table.")
    #     result = {}
    #     try:
    #         grades_table = self.driver.find_element(By.XPATH, """.//table[@id="T02"]""")
    #         grades_table_body = grades_table.find_element(By.XPATH, """.//tbody""")
    #         grades_rows = grades_table_body.find_elements(By.XPATH, """.//tr[@class="TableDataRow"]""")

    #         for row in grades_rows:
    #             course_name = row.find_element(By.XPATH, """.//td[4]""").get_attribute("title")
    #             grade_element = row.find_element(By.XPATH, """.//td[7]""")
    #             course_grade = grade_element.find_element(By.XPATH, """.//nobr[1]""").text.strip()
    #             grade_status_element = row.find_element(By.XPATH, """.//td[9]""")
    #             grade_status = grade_status_element.find_element(By.XPATH, """.//nobr[1]""").text.strip()

    #             try:
    #                 numeric_grade = float(course_grade)
    #                 result[course_name] = numeric_grade
    #             except ValueError:
    #                 # Handle non-numeric grades
    #                 self.logger.error("Value error in getting grade.")

    #                 if grade_status == "غيبت كلاسي":
    #                     result[course_name] = "غيبت كلاسي"

    #             sleep(0.3)

    #     except NoSuchElementException:
    #         self.logger.error("Grade table not found.")
    #     return result


    def _find_term_grades(self):
        """Extract grades from the table using BeautifulSoup."""
        self.logger.info("Extracting grades from the table using BeautifulSoup.")
        result = {}
        try:
            # Get the page source from Selenium's driver
            page_source = self.driver.page_source
            
            # Parse the page source with BeautifulSoup
            soup = BeautifulSoup(page_source, 'html.parser')
            
            # Locate the grades table
            grades_table = soup.find("table", {"id": "T02"})
            if not grades_table:
                self.logger.error("Grade table not found.")
                return result
            
            # Locate table rows
            grades_rows = grades_table.find("tbody").find_all("tr", {"class": "TableDataRow"})
            
            for row in grades_rows:
                # Extract course name
                course_name = row.select_one("td:nth-child(4)").get("title", "").strip()
                
                # Extract course grade
                grade_element = row.select_one("td:nth-child(7) nobr")
                course_grade = grade_element.text.strip() if grade_element else None
                
                # Extract grade status
                grade_status_element = row.select_one("td:nth-child(9) nobr")
                grade_status = grade_status_element.text.strip() if grade_status_element else None
                
                try:
                    numeric_grade = float(course_grade)
                    result[course_name] = numeric_grade
                except ValueError:
                    self.logger.error(f"Value error in grade conversion for course: {course_name}")
                    if grade_status == "غيبت كلاسي":
                        result[course_name] = "غيبت كلاسي"

        except Exception as e:
            self.logger.error(f"An error occurred while parsing grades: {e}")
        return result


    def monitor_grades(self):
        """Monitor grades periodically by checking the current page and refreshing it."""
        while True:
            try:
                self.logger.info("Checking grades...")
                
                # Step 1: Check grades on the current page
                grades = self._find_term_grades()  # Extract grades from the current page
                for course_name, course_grade in grades.items():
                    if course_name not in self.notified_grades or self.notified_grades[course_name] != course_grade:
                        # New or updated grade detected
                        self._send_telegram_notification(course_name, course_grade)
                        self.notified_grades[course_name] = course_grade

                # Step 2: Save notified grades
                self._save_notified_grades()

                # Step 3: Refresh the page
                self.logger.info("Refreshing the page...")

                # Click "Previous Term" button
                try:
                    previous_term_button = self.driver.find_element(By.XPATH, """.//img[@title="ترم قبلي"]""")
                    previous_term_button.click()
                    time.sleep(2)  # Wait for the page to load
                except NoSuchElementException:
                    self.logger.info("Previous term button not found. Skipping refresh.")
                    continue

                # Click "Next Term" button to return to the target page
                try:
                    next_term_button = self.driver.find_element(By.XPATH, """.//img[@title="ترم بعدي"]""")
                    next_term_button.click()
                    time.sleep(2)  # Wait for the page to load
                except NoSuchElementException:
                    self.logger.info("Next term button not found. Skipping refresh.")
                    continue

                # Step 4: Sleep until the next check
                self.logger.info(f"Sleeping for {self.refresh_interval} seconds...")
                time.sleep(self.refresh_interval)

            except Exception as e:
                self.logger.error(f"An error occurred during monitoring: {e}")
                from .login_state import LoginState
                self.context.change_state(LoginState(self.context))

    def _send_telegram_notification(self, course_name, course_grade):
        """Send notification via Telegram (stub)."""
        self.logger.info("Sending grades to telegram...")
        self.telegram_bot.send_message(f""""{course_name}" نمره رو زد: {course_grade}""")