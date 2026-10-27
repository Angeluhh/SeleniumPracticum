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

    job_order_link = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//a[contains(@class,'sidebar__link') "
            "and normalize-space()='Job Order Details']"
        ))
    )
    job_order_link.click()

    wait.until(EC.url_contains("/user/job-orders"))
    print("Job Order page:", driver.current_url)

    create_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.btn-submit[href*='/user/job-orders/create']"
        ))
    )
    create_button.click()

    wait.until(EC.url_contains("/user/job-orders/create"))
    print("Create Job Order page:", driver.current_url)

    title_field = wait.until(
        EC.visibility_of_element_located((By.ID, "jobTitle"))
    )
    title_field.clear()
    title_field.send_keys("Air conditioning failure")

    description_field = wait.until(
        EC.visibility_of_element_located((By.ID, "description"))
    )
    description_field.clear()
    description_field.send_keys(
        "The Air conditioning isn't working."
    )

    building_button = wait.until(
        EC.element_to_be_clickable((By.ID, "buildingNameButton"))
    )
    building_button.click()

    building_option = wait.until(
        EC.element_to_be_clickable((By.ID, "buildingNameOption1"))
    )
    building_option.click()

    print("Selected building: LS Building")

    room_button = wait.until(
        EC.element_to_be_clickable((By.ID, "roomNameButton"))
    )
    room_button.click()

    room_option = wait.until(
        EC.element_to_be_clickable((By.ID, "roomNameOption1"))
    )
    room_option.click()

    print("Selected room: LS 212")

    service_button = wait.until(
        EC.element_to_be_clickable((By.ID, "serviceTypeButton"))
    )
    service_button.click()

    service_option = wait.until(
        EC.element_to_be_clickable((By.ID, "serviceTypeOption0"))
    )
    service_option.click()

    print("Selected service type: Air Conditioning")

    assert title_field.get_attribute("value") == "Air conditioning failure"
    assert description_field.get_attribute("value") == (
        "The Air conditioning isn't working."
    )

    assert building_button.text.strip() == "LS Building"
    assert room_button.text.strip() == "LS 212"
    assert service_button.text.strip() == "Air Conditioning"

    print("PASS: Title and description are entered.")
    print("PASS: Building, room, and service type are selected.")

    submit_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[type='submit'].btn-submit"
        ))
    )

    submit_button.click()

    driver.save_screenshot("TC05_Job_Order_Submission.png")

    print("Submit button clicked.")
    print("Inspect Chrome to verify the submission result.")
    print("Screenshot saved: TC05_Job_Order_Submission.png")
    print("Current URL:", driver.current_url)

except Exception as error:
    print("FAIL:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    try:
        driver.save_screenshot("TC05_Error.png")
        print("Error screenshot saved: TC05_Error.png")
    except Exception:
        pass

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()