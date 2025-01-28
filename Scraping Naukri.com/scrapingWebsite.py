import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# Initialize logging
logging.basicConfig(filename="YourName_Errors.log", level=logging.ERROR)

# Initialize WebDriver
driver = webdriver.Chrome()  # Use your appropriate WebDriver

# Function to search for jobs on Naukri.com
def search_naukri_jobs():
    try:
        # Open Naukri.com homepage
        driver.get("https://www.naukri.com/")
        
        # Wait for the page to load completely
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div[7]/div/div/div[1]/div/div/div/div[1]/div/input'))
        )
        
        # Locate the search bar and enter the job role
        search_box = driver.find_element(By.XPATH, '//*[@id="root"]/div[7]/div/div/div[1]/div/div/div/div[1]/div/input')

        search_word = input("Enter the Role you are searching for: ")
        search_box.clear()

        search_box.send_keys(search_word)  # Job role
        time.sleep(1)

        # Locate the search button and click it
        search_button = driver.find_element(By.XPATH, '//*[@id="root"]/div[7]/div/div/div[6]')
        search_button.click()
        
        # Wait for the results to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "list")]'))
        )
        
        # Print the current URL (search results page)
        print("Search Results URL:", driver.current_url)

    except Exception as e:
        print("An error occurred while searching:", e)
        logging.error(f"Error during job search: {e}")

# Function to scrape job data from the current page
def scrape_page(job_data):
    postings = driver.find_elements(By.CLASS_NAME, 'srp-jobtuple-wrapper')
    for post in postings:
        try:
            role_name = post.find_element(By.CLASS_NAME, 'title').text.strip()
        except Exception as e:
            role_name = "N/A"
            logging.error(f"Error extracting role name: {e}")

        try:
            company_name = post.find_element(By.CLASS_NAME, 'comp-name').text.strip()
        except Exception as e:
            company_name = "N/A"
            logging.error(f"Error extracting company name: {e}")

        try:
            experience = post.find_element(By.CLASS_NAME, 'exp').text.strip()
        except Exception as e:
            experience = "N/A"
            logging.error(f"Error extracting experience: {e}")

        try:
            location = post.find_element(By.CLASS_NAME, 'locWdth').text.strip()
        except Exception as e:
            location = "N/A"
            logging.error(f"Error extracting location: {e}")

        try:
            salary = post.find_element(By.CLASS_NAME, 'sal').text.strip()
        except Exception as e:
            salary = "Not disclosed"
            logging.error(f"Error extracting salary: {e}")

        try:
            job_desc = post.find_element(By.CLASS_NAME, 'ni-job-tuple-icon-srp-description').text.strip()
        except Exception as e:
            job_desc = "N/A"
            logging.error(f"Error extracting job description: {e}")

        try:
            date_posted_text = post.find_element(By.CLASS_NAME, 'job-post-day').text.strip()
            days_ago = int(date_posted_text.split(' ')[0])
        except Exception as e:
            days_ago = None
            logging.error(f"Error extracting date posted: {e}")

        try:
            job_type = post.find_element(By.CLASS_NAME, 'type').text.strip()
        except Exception as e:
            job_type = "N/A"
            logging.error(f"Error extracting job type: {e}")

        try:
            app_link = post.find_element(By.CLASS_NAME, 'apply-link').get_attribute("href")
        except Exception as e:
            app_link = "N/A"
            logging.error(f"Error extracting application link: {e}")

        if days_ago is not None and days_ago <= 7:
            job_data.append({
                'Role Name': role_name,
                'Company Name': company_name,
                'Experience Required': experience,
                'Location': location,
                'Salary': salary,
                'Job Description': job_desc,
                'Date Posted': date_posted_text,
                'Job Type': job_type,
                'Application Link': app_link
            })

# Function to navigate to the next page
def go_to_next_page():
    try:
        # Set an implicit wait (e.g., 10 seconds)
        driver.implicitly_wait(10)  # Wait up to 10 seconds for elements to be found
        
        # Find the "Next" button using the provided XPath and click it
        next_button = driver.find_element(By.XPATH, '//*[@id="lastCompMark"]/a[2]')
        next_button.click()
        
        # Wait for the next page to load completely using an explicit wait
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'srp-jobtuple-wrapper'))
        )
        
        # Add a small delay to ensure the page is fully loaded
        time.sleep(2)
        return True
    except Exception as e:
        print("No more pages or error navigating to the next page:", e)
        logging.error(f"Error navigating to the next page: {e}")
        return False
    finally:
        # Reset implicit wait to avoid affecting other parts of the script
        driver.implicitly_wait(0)  # Reset to default (no implicit wait)




# Main program
try:
    # Option to search for jobs
    search_naukri_jobs()

    # Wait to let the user review search results
    time.sleep(5)

    # List to collect job data
    job_data = []

    # Number of pages to scrape
    total_pages = 10  # Set the limit of pages to scrape

    # Loop through pages dynamically based on the search keyword
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")

        # Scrape the current page
        scrape_page(job_data)

        # Attempt to go to the next page
        if not go_to_next_page():
            break  # Exit if there are no more pages

    # Convert job data to a DataFrame
    df = pd.DataFrame(job_data)

    # Display DataFrame
    print(df)

    # Save data to Excel
    df.to_excel('job_data_last_7_days_with_description_multiple_pages.xlsx', index=False)
    print("Job data saved to Excel file.")

except Exception as e:
    print("An error occurred:", e)
    logging.error(f"Main program error: {e}")

finally:
    # Close the WebDriver
    driver.quit()