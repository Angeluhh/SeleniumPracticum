from urllib.parse import urlparse

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

URL = "https://gscsystem.site/login"

USERNAME = "angelamichelle.sy@lsu.edu.ph"
PASSWORD = "sy12345"

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 20)
results = []


def check_navigation(label, expected_path=None):
    links = driver.find_elements(
        By.XPATH,
        f"//a[contains(@class,'sidebar__link') "
        f"and normalize-space()='{label}']"
    )

    if not links:
        message = f"FAIL: '{label}' link was not found."
        print(message)
        results.append(message)
        return False

    link = links[0]
    target_url = link.get_attribute("href")
    target_path = expected_path or urlparse(target_url).path

    try:
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                f"//a[contains(@class,'sidebar__link') "
                f"and normalize-space()='{label}']"
            ))
        ).click()

        wait.until(
            lambda d: urlparse(d.current_url).path.rstrip("/")
            == target_path.rstrip("/")
        )

        assert driver.title.strip(), (
            f"The {label} page has no browser title."
        )

        message = f"PASS: {label} navigation works."
        print(message)
        print("Page title:", driver.title)
        print("Current URL:", driver.current_url)
        results.append(message)
        return True

    except Exception as error:
        message = (
            f"FAIL: '{label}' navigation did not complete. "
            f"{type(error).__name__}: {error}"
        )
        print(message)
        results.append(message)
        return False


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

    wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class,'sidebar__link') "
            "and normalize-space()='Dashboard']"
        ))
    )

    print("Login successful. Dashboard navigation test started.")

    check_navigation("Dashboard", "/user/dashboard")

    check_navigation("Job Order Details", "/user/job-orders")

    create_button = wait.until(
        EC.visibility_of_element_located((
            By.CSS_SELECTOR,
            "a.btn-submit[href*='/user/job-orders/create']"
        ))
    )

    assert create_button.is_displayed(), (
        "Submit Job Order button is not displayed."
    )

    print("PASS: Submit Job Order button is present.")
    results.append("PASS: Submit Job Order button is present.")

    check_navigation("Facility Booking Details")

    check_navigation("Archived")

    check_navigation("Dashboard", "/user/dashboard")

    logout_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.sidebar__logout[href*='/logout']"
        ))
    )
    logout_button.click()

    wait.until(
        EC.visibility_of_element_located((By.ID, "username"))
    )

    print("PASS: Logout works and returns to the login page.")
    results.append("PASS: Logout works.")

    driver.save_screenshot("TC07_Dashboard_Navigation.png")
    print("Screenshot saved: TC07_Dashboard_Navigation.png")

    print("\nTC-07 TEST SUMMARY")

    for result in results:
        print(result)

    passed = sum(result.startswith("PASS:") for result in results)
    failed = sum(result.startswith("FAIL:") for result in results)

    print(f"\nPassed: {passed}")
    print(f"Failed: {failed}")

except Exception as error:
    print("\nTEST ERROR:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    driver.save_screenshot("TC07_Error.png")
    raise

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()