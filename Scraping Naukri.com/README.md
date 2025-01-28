# Naukri.com Job Scraper

This Python script automates the process of searching and scraping job listings from [Naukri.com](https://www.naukri.com/). It extracts details such as role name, company name, experience required, location, salary, job description, and application link for jobs posted in the last 7 days.

## Features

- **Dynamic Search**: Enter the desired job role, and the script searches for relevant job postings on Naukri.com.
- **Multi-page Scraping**: Automatically navigates and scrapes multiple pages of job listings.
- **Data Extraction**: Extracts key details from each job listing, including:
  - Role Name
  - Company Name
  - Experience Required
  - Location
  - Salary
  - Job Description
  - Date Posted
  - Job Type
  - Application Link
- **Error Handling**: Logs errors encountered during execution to a file named `YourName_Errors.log`.
- **Data Export**: Saves scraped job data to an Excel file for further analysis.

## Requirements

- Python 3.x
- Google Chrome browser
- ChromeDriver compatible with your Chrome version
- Required Python packages (install using `pip`):
  ```bash
  pip install selenium pandas openpyxl
  ```

## Setup Instructions

1. **Clone the Repository**: Clone this repository to your local machine using the following command:
   git clone https://github.com/YourUsername/Job-Scraper.git
   cd Job-Scraper

2. **Set Up Python Environment (Optional but Recommended)**: It's recommended to use a virtual environment to manage dependencies. If you haven't set up a virtual environment, you can do so by running the following commands:
   python -m venv venv
   source venv/bin/activate # On Windows, use venv\Scripts\activate

3. **Install Dependencies**: Install the required packages by running:
   pip install -r requirements.txt

4. **Download ChromeDriver**: This script uses the Chrome browser and ChromeDriver to automate the scraping. Ensure that the version of ChromeDriver matches your Google Chrome version. You can download the correct version of ChromeDriver here: [ChromeDriver Download](https://sites.google.com/chromium.org/driver/)

5. **Run the Script**: To run the script, use the following command:
   python scrapingWebsite.py

6. **Output**: The script will save the scraped job data in an Excel file named job_data_last_7_days_with_description_multiple_pages.xlsx. Errors encountered during the execution are logged in the YourName_Errors.log file.
