from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gscsystem.site/login"

USERNAME = "angelamichelle.sy@lsu.edu.ph"
PASSWORD = "sy12345"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get(URL)

    wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys(USERNAME)
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys(PASSWORD)

    wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, "button[type='submit']")
    )).click()

    wait.until(EC.element_to_be_clickable((
        By.XPATH,
        "//a[contains(@class,'sidebar__link') and normalize-space()='Job Order Details']"
    ))).click()

    wait.until(EC.url_contains("/user/job-orders"))

    wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR,
        "a.btn-submit[href*='/user/job-orders/create']"
    ))).click()

    wait.until(EC.url_contains("/user/job-orders/create"))

    title_field = wait.until(EC.visibility_of_element_located((By.ID, "jobTitle")))
    title_field.send_keys("Air conditioning failure")

    description_field = wait.until(EC.visibility_of_element_located((By.ID, "description")))
    description_field.send_keys("The Air conditioning isn't working.")

    wait.until(EC.element_to_be_clickable(
        (By.ID, "buildingNameButton")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.ID, "buildingNameOption1")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.ID, "roomNameButton")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.ID, "roomNameOption1")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.ID, "serviceTypeButton")
    )).click()
    wait.until(EC.element_to_be_clickable(
        (By.ID, "serviceTypeOption0")
    )).click()

    assert title_field.get_attribute("value") == "Air conditioning failure"
    assert description_field.get_attribute("value") == "The Air conditioning isn't working."

    submit_button = wait.until(EC.element_to_be_clickable((
        By.CSS_SELECTOR, "button[type='submit'].btn-submit"
    )))
    submit_button.click()

    sleep(2)
    print("Submit button clicked.")
    print("Current URL:", driver.current_url)
    print("Check the browser to verify the submission result.")

except Exception as error:
    print("TEST ERROR:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

finally:
    driver.save_screenshot("TC06_Job_Order_Submission.png")
    print("Screenshot saved: TC06_Job_Order_Submission.png")
    input("Inspect the result, then press ENTER to close...")
    driver.quit()