from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gscsystem.site/login"

USERNAME = "jamaica.lao@lsu.edu.ph"
PASSWORD = "admin1234"
MASTER_PASSWORD = "GSC"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)

try:
    driver.get(URL)

    username_field = wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )
    password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "password"))
    )

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)

    login_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    login_button.click()

    master_password_field = wait.until(
        EC.visibility_of_element_located((By.ID, "masterPassword"))
    )
    master_password_field.send_keys(MASTER_PASSWORD)

    verify_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    verify_button.click()

    system_data_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class,'sidebar__link') "
            "and normalize-space()='System Data']"
        ))
    )
    system_data_link.click()

    wait.until(EC.url_contains("/admin/system-data/buildings"))

    print("System Data page:", driver.current_url)

    active_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button.btn-status--active[data-id='10'][data-status='active']"
        ))
    )

    record_name = active_button.get_attribute("data-name")
    print("Record to disable:", record_name)
    print("Current status:", active_button.text.strip())

    active_button.click()

    inactive_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[type='submit'][name='target_status'][value='inactive']"
        ))
    )
    inactive_button.click()

    inactive_locator = (
        By.CSS_SELECTOR,
        "button.btn-status[data-id='10'][data-status='inactive']"
    )

    inactive_status = wait.until(
        EC.presence_of_element_located(inactive_locator)
    )

    assert inactive_status.get_attribute("data-status") == "inactive", (
        "FAIL: The record status did not change to Inactive."
    )

    print("PASS: TC-09")
    print("Record:", record_name)
    print("Status successfully changed to Inactive.")

    driver.save_screenshot("TC09_Disable_Facility.png")
    print("Screenshot saved: TC09_Disable_Facility.png")
    print("Current URL:", driver.current_url)

except Exception as error:
    print("FAIL:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    try:
        driver.save_screenshot("TC09_Error.png")
        print("Error screenshot saved: TC09_Error.png")
    except Exception:
        pass

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()