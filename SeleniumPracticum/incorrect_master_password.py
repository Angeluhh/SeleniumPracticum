from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gscsystem.site/login"

USERNAME = "jamaica.lao@lsu.edu.ph"
PASSWORD = "admin1234"
MASTER_PASSWORD = "yuh"

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

    print("PASS: Master-password prompt displayed.")

    driver.save_screenshot("TC03_Master_Password_Prompt.png")
    print("Screenshot saved: TC03_Master_Password_Prompt.png")

    master_password_field.send_keys(MASTER_PASSWORD)

    verify_button = wait.until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "button[type='submit']")
        )
    )
    verify_button.click()

    wait.until(
        lambda d: d.execute_script(
            "return document.readyState"
        ) == "complete"
    )

    print("Current URL:", driver.current_url)
    print("Page title:", driver.title)

    driver.save_screenshot("TC03_Master_Password_Verification.png")
    print("Screenshot saved: TC03_Master_Password_Verification.png")

    input("Inspect the result, then press ENTER to close...")

except Exception as error:
    print("TEST ERROR:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    driver.save_screenshot("TC03_Master_Password_Error.png")
    print("Error screenshot saved: TC03_Master_Password_Error.png")

    input("Inspect the browser, then press ENTER to close...")

finally:
    driver.quit()