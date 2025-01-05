# Main entry point for running the automation script
from core.context import GolestanGradeCheckerBot
from config import Config 

if __name__ == "__main__":
    config = Config.load_from_env()
    bot = GolestanGradeCheckerBot(config)
    bot.run()