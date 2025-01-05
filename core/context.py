from core.driver_factory import DriverFactory
from states.login_state import LoginState

class GolestanGradeCheckerBot:
    def __init__(self, config, driver=None, browser_name="chrome"):
        self.config = config
        self.browser_name = browser_name
        self.driver = driver if driver else DriverFactory.get_driver(self.browser_name)
        self.state = LoginState(self)

    def get_context_driver(self):
        """Initialize driver only if it doesn't exist or is unusable"""
        if not self.driver:
            print("Creating new WebDriver instance")
            self.driver = DriverFactory.get_driver(self.browser_name)
        else:
            try:
                # Check if driver is still alive by accessing a simple attribute
                print("Reusing existing WebDriver instance")
                self.driver.title  # This will raise an error if the driver is closed
            except Exception as e:
                print(f"Driver seems to be closed or unusable. Error: {e}")
                print("Creating new WebDriver instance")
                self.driver = DriverFactory.get_driver(self.browser_name)
        return self.driver
    
    def change_state(self, new_state):
        self.state = new_state

    def run(self):
        self.get_context_driver()

        while True:
            try:
                self.state.handle()
            except Exception as e:
                print(f"Error during bot run: {e}")
