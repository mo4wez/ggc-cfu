import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import WebDriverException
from selenium_stealth import stealth

class DriverFactory:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DriverFactory, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_driver(browser_name="edge", proxy=None):
        """
        Returns a WebDriver instance based on the browser_name using webdriver-manager.
        :param browser_name: Name of the browser ("chrome", "firefox", "edge", "safari", "opera")
        :return: WebDriver instance
        """
        if browser_name.lower() == "chrome":
            options = ChromeOptions()
            # options.add_argument("--headless")
            # options.add_argument("--no-sandbox") # for linux
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-proxy-server')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            options.add_experimental_option("detach", True)

            if proxy:
                proxy_obj = DriverFactory.set_proxy(proxy)
                options.proxy = proxy_obj

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

            stealth(driver,
                    languages=["en-US", "en", "fa", "fa-IR"],
                    vendor="Google Inc.",
                    platform="Win64",
                    webgl_vendor="Intel Inc.",
                    renderer="Intel Iris OpenGL Engine",
                    fix_hairline=True,
            )

        elif browser_name.lower() == "firefox":
            options = FirefoxOptions()
            options.set_preference("network.proxy.type", 0)  # Disable proxy settings
            options.set_preference("general.useragent.override", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/112.0.0.0 Safari/537.36")
            
            if proxy:
                proxy_obj = DriverFactory.set_proxy(proxy)
                options.proxy = proxy_obj

            service = FirefoxService(GeckoDriverManager().install())
            driver = webdriver.Firefox(service=service, options=options)

        elif browser_name.lower() == "edge":
            options = EdgeOptions()
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-proxy-server')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/112.0.0.0 Safari/537.36")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            if proxy:
                proxy_obj = DriverFactory.set_proxy(proxy)
                options.proxy = proxy_obj

            service = EdgeService(EdgeChromiumDriverManager().install())
            driver = webdriver.Edge(service=service, options=options)

        elif browser_name.lower() == "safari":
            options = SafariOptions()
            driver = webdriver.Safari(options=options)

        elif browser_name.lower() == "opera":
            options = ChromeOptions()
            options.binary_location = r"C:\\Users\moawe\\Desktop\\vam_bot\\webdrivers\\opera\\operadriver.exe"
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-proxy-server')
            options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            if proxy:
                proxy_obj = DriverFactory.set_proxy(proxy)
                options.proxy = proxy_obj

            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)

        else:
            raise ValueError(f"Unsupported browser: {browser_name}")

        driver.set_window_rect(0, 0, 970, 1080)
        driver.implicitly_wait(2)
        
        return driver

    @staticmethod
    def quit_driver(driver):
        """
        Closes and quits the WebDriver instance.
        :param driver: WebDriver instance to be closed
        """
        if driver:
            driver.quit()

    @staticmethod
    def set_proxy(proxy):
        proxy_obj = Proxy()
        proxy_obj.proxy_type = ProxyType.MANUAL
        proxy_obj.http_proxy = proxy
        proxy_obj.ssl_proxy = proxy
        return proxy_obj
