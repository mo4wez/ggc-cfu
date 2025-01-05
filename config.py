# Configuration and settings

from environs import Env

class Config:
    LOG_LEVEL = "INFO"
    def __init__(self, main_page_url,golestan_username, golestan_password,semester, api_key, bot_token, chat_id):
        self.main_page_url = main_page_url
        self.golestan_username = golestan_username
        self.golestan_password = golestan_password
        self.semester = semester
        self.api_key = api_key
        self.bot_token = bot_token
        self.chat_id = chat_id

    @staticmethod
    def load_from_env():
        """Load configuration from environment variables using the environs library."""
        env = Env()
        env.read_env()  # Read .env file, if it exists

        return Config(
            main_page_url=env.str("MAIN_PAGE_URL"),
            golestan_username=env.str("GOLESTAN_USERNAME"),
            golestan_password=env.str("GOLESTAN_PASSWORD"),
            semester=env.str("SEMESTER"),
            api_key=env.str("CAPTCHA_API_KEY"),
            bot_token=env.str("BOT_TOKEN"),
            chat_id=env.str("TELEGRAM_CHANNEL_ID")
            )