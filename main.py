from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

driver = webdriver.Chrome()
driver.get("https://www.payscale.com/college-salary-report/majors-that-pay-you-back/bachelors")
time.sleep(5)

all_data = []
last_row = None

while True:
    time.sleep(2)

    rows = driver.find_elements(By.CSS_SELECTOR, "table.data-table tbody tr")
    new_data = []
    for row in rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        data = [cell.text for cell in cells]
        new_data.append(data)

    # Check if the first row is same as last time — means we're looping
    if new_data and new_data[0] == last_row:
        print("No new data. Exiting loop.")
        break
    else:
        last_row = new_data[0]  # Update the last seen row
        all_data.extend(new_data)

    # Click next
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "i.icon-right-open")
        next_button.click()
    except NoSuchElementException:
        print("Next button not found. Ending.")
        break

driver.quit()

# Save to CSV
columns = ["Rank", "Major", "Degree Type", "Early Career Pay", "Mid-Career Pay", "% High Mean"]
df = pd.DataFrame(all_data, columns=columns)
df.to_csv("payscale_salaries.csv", index=False)
print("Saved all pages! ✅")