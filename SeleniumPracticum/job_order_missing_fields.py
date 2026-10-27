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

    wait.until(EC.visibility_of_element_located((By.ID, "jobTitle"))).send_keys(
        "Air conditioning failure"
    )
    wait.until(EC.visibility_of_element_located((By.ID, "description"))).send_keys(
        "The Air conditioning isn't working."
    )

    wait.until(EC.element_to_be_clickable(
        (By.ID, "serviceTypeButton")
    )).click()

    wait.until(EC.element_to_be_clickable(
        (By.ID, "serviceTypeOption0")
    )).click()

    submit_button = wait.until(EC.presence_of_element_located((
        By.XPATH,
        "//button[@type='submit' and contains(@class,'btn-submit') and normalize-space()='Submit Job Order']"
    )))

    driver.execute_script(
        "arguments[0].scrollIntoView({block:'center'});",
        submit_button
    )
    submit_button.click()

    print("Submission attempted.")
    print("Current URL:", driver.current_url)

except Exception as error:
    print("TEST ERROR:", type(error).__name__, error)

finally:
    driver.save_screenshot("TC05_Missing_Building_Room.png")
    print("Screenshot saved: TC05_Missing_Building_Room.png")
    input("Inspect the browser, then press ENTER to close...")
    driver.quit()