from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
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

    job_order_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class,'sidebar__link') "
            "and normalize-space()='Job Order']"
        ))
    )
    job_order_link.click()

    wait.until(EC.url_contains("/admin/job-orders"))
    print("Job Order page:", driver.current_url)

    service_filter = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "serviceTypeFilter")
        )
    )

    Select(service_filter).select_by_visible_text("Air Conditioning")

    wait.until(
        lambda d: Select(
            d.find_element(By.ID, "serviceTypeFilter")
        ).first_selected_option.text.strip() == "Air Conditioning"
    )

    print("Selected filter: Air Conditioning")

    rows = wait.until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "table tbody tr")
        )
    )

    row_texts = [
        row.text.strip()
        for row in rows
        if row.is_displayed() and row.text.strip()
    ]

    row_texts = [
        text for text in row_texts
        if "no job orders found" not in text.lower()
        and "no records found" not in text.lower()
    ]

    if not row_texts:
        print(
            "INCONCLUSIVE: No job order records are displayed "
            "for the selected filter."
        )
    else:
        mismatched_rows = [
            text for text in row_texts
            if "air conditioning" not in text.lower()
        ]

        assert not mismatched_rows, (
            "FAIL: Some displayed job orders do not match "
            "the Air Conditioning filter:\n"
            + "\n".join(mismatched_rows)
        )

        print("PASS: All displayed job orders match the selected filter.")
        print("Matching records:", len(row_texts))

        for index, text in enumerate(row_texts, start=1):
            print(f"{index}. {text}")

    driver.save_screenshot("TC10_Filter_Job_Orders.png")
    print("Screenshot saved: TC10_Filter_Job_Orders.png")
    print("Current URL:", driver.current_url)

except Exception as error:
    print("FAIL:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    try:
        driver.save_screenshot("TC10_Error.png")
        print("Error screenshot saved: TC10_Error.png")
    except Exception:
        pass

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()