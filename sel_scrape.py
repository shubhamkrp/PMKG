from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import csv

def get_icd10_codes(driver):
    codes = []
    driver.get("https://www.icd10data.com/ICD10CM/Codes")
    time.sleep(3)

    chapters = driver.find_elements(By.CSS_SELECTOR, "a[href^='/ICD10CM/Codes/']")
    chapter_urls = [chapter.get_attribute('href') for chapter in chapters]

    for url in chapter_urls:
        driver.get(url)
        time.sleep(3)
        code_elements = driver.find_elements(By.CSS_SELECTOR, ".identifier a")
        for code_element in code_elements:
            code = code_element.text
            description = code_element.get_attribute('title')
            codes.append((code, description))

    return codes

def save_to_csv(codes, filename="icd10_codes.csv"):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["ICD-10 Code", "Description"])
        writer.writerows(codes)

# Setup WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is in your PATH

try:
    codes = get_icd10_codes(driver)
    save_to_csv(codes)
finally:
    driver.quit()
