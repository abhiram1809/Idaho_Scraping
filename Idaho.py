from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up Chrome WebDriver with options
chrome_options = Options()
chrome_options.add_argument("--start-maximized")
driver = webdriver.Chrome('chromedriver', options=chrome_options)  # Replace with the path to your chromedriver executable

# Open the web page
driver.get('https://qcpi.questcdn.com/cdn/posting/?group=1950787&provider=1950787')  # Replace with the URL of the web page

# Wait for the table to load (you may need to adjust the wait time)
time.sleep(2)

# Find the table element
table = driver.find_element(By.ID, 'table_id')

# Extract the HTML content of the table
table_html = table.get_attribute('outerHTML')

# Use pandas to read the HTML and convert it to a DataFrame
df = pd.read_html(table_html)[0]
df = df[1:]
quest_number_list = df['Quest Number'].tolist()
quest_number_list = [int(num) for num in quest_number_list]
print(quest_number_list)

data = []
# Iterate over the quest numbers
for quest_number in quest_number_list:
    # Click on the quest number XPath
    xpath = "//b[normalize-space()='{}']".format(quest_number)
    quest_number_element = driver.find_element(By.XPATH, xpath)
    time.sleep(1)
    try:
        quest_number_element.click()
        time.sleep(1)
    except:
        print("Element click intercepted. Skipping...")

    # Switch the focus to the new window
    driver.switch_to.window(driver.window_handles[-1])

    tables = driver.find_elements(By.CSS_SELECTOR, '.table.table-borderless.posting-table')
    for table in tables:
        # Extract the HTML content of the table
        table_html = table.get_attribute('outerHTML')

        # Use pandas to read the HTML and convert it to a DataFrame
        df_read = pd.read_html(table_html)[0]
        # Extract relevant information from the DataFrame
        if 'Closing Date:' in df_read[0].values and 'Est. Value Notes:' in df_read[0].values:
            # Retrieve values from adjacent cells
            closing_row_index = df_read[df_read[0] == 'Closing Date:'].index[0]
            est_value_notes_row_index = df_read[df_read[0] == 'Est. Value Notes:'].index[0]
            closing_date_value = df_read.iloc[closing_row_index, 1]
            est_value_notes_value = df_read.iloc[est_value_notes_row_index, 1]
        if 'Description:' in df_read[0].values:
            # Get the index of the row where 'Description:' is found
            row_index = df_read[df_read[0] == 'Description:'].index[0]

            # Retrieve the value from the adjacent right cell
            description_value = df_read.iloc[row_index, 1]

        # Iterate over the rows and store the information
    if description_value and closing_date_value and est_value_notes_value:
        data.append([est_value_notes_value, description_value, closing_date_value])
        # Close the new window and switch back to the original window
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)
    back_to_search_element = driver.find_element(By.XPATH, "//ul[contains(@class,'horizontal-layout')]//b[contains(text(),'Back to Search Postings')]")
    back_to_search_element.click()

# Create a DataFrame from the extracted data
df_extracted = pd.DataFrame(quest_number_list, columns=['Quest Number'])
df_extracted[['Est. Value Notes', 'Description', 'Closing Date']] = data
df_extracted = df_extracted.head()
df_extracted.to_csv('Extracted Columns.csv', index = False)

# Close the browser
driver.quit()
