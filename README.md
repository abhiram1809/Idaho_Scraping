# Idaho_Scraping

This project is a web scraper that extracts contract data from a specific website for the state of Idaho. It uses Selenium WebDriver and Pandas library to automate the process of navigating through web pages, scraping data from tables, and storing the extracted information in a structured format.

## Features

- Extracts contract data from the specified website.
- Retrieves information such as closing date, estimated value notes, and description for each contract.
- Stores the extracted data in a CSV file for further analysis or processing.

## Installation

1. Clone the repository to your local machine.
```Terminal
    git clone https://github.com/your-username/idaho-contract-scraper.git
```

2. Install the required dependencies using `pip`.
```Terminal
    pip install -r requirements.txt
```

3. Download and configure Chrome WebDriver.
- Download the appropriate Chrome WebDriver for your operating system from the official website: [Chrome WebDriver Downloads](https://sites.google.com/a/chromium.org/chromedriver/downloads)
- Place the WebDriver executable in the project directory or add it to your system's PATH environment variable.

## Usage

1. Run the `Idaho.py` script.
```Terminal
    python Idaho.py
```
