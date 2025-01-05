# Grades Monitoring Project - Golestan Grades Checker (CFU)

This project monitors grades from a web-based system using Selenium, sends notifications via a Telegram bot when new grades are detected, and saves grade data persistently in a JSON file. It integrates various libraries for handling automation, configuration, CAPTCHA solving, and messaging.

---

## Features
- **Grade Monitoring**: Automatically checks grades periodically using Selenium.
- **Notifications**: Sends Telegram notifications for new or updated grades.
- **CAPTCHA Handling**: Solves CAPTCHA challenges using the 2captcha service.
- **Persistent Storage**: Saves grades data in a JSON file to avoid duplicate notifications.

---

## Prerequisites

- **Python 3.8+**
- WebDriver for Selenium (e.g., ChromeDriver for Google Chrome)
- Telegram Bot Token and Chat ID
- 2captcha API Key

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ggc-cfu.git
   cd ggc-cfu
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the `.env` file:
   Create a file named `.env` in the project directory with the following structure:
   ```env
   MAIN_PAGE_URL=https://education.cfu.ac.ir/forms/authenticateuser/main.htm
   CAPTCHA_API_KEY=YOUR_CAPTCHA_API_KEY
   BOT_TOKEN=TELEGRAM_BOT_TOKEN
   TELEGRAM_CHANNEL_ID=TELEGRAM_CHANNEL_ID
   GOLESTAN_USERNAME=YOUR_USERNAME
   GOLESTAN_PASSWORD=YOUR_PASSWORD
   SEMESTER=SEMESTER_INTEGER
   ```

---

## Usage

1. **Run the Project**:
   ```bash
   python bot.py
   ```

2. **Monitor Grades**:
   - The program will periodically check for grades and send notifications for any changes.


---

## Libraries Used

- **[Selenium](https://www.selenium.dev/)**: For browser automation and web scraping.
- **[environs](https://pypi.org/project/environs/)**: For managing environment variables.
- **[2captcha-python](https://pypi.org/project/2captcha-python/)**: For solving CAPTCHA challenges.
- **[pyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)**: For interacting with the Telegram Bot API.

---

## Known Issues
- Ensure the WebDriver version matches your browser version.
- CAPTCHA challenges may fail if the 2captcha API key is invalid or has insufficient balance.

---

## Author
[moawezz](https://github.com/mo4wez)
