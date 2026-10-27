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

    service_button = wait.until(
        EC.element_to_be_clickable((By.ID, "serviceTypeButton"))
    )
    service_button.click()

    service_option = wait.until(
        EC.element_to_be_clickable((By.ID, "serviceTypeOption0"))
    )
    service_option.click()

    print("Title: Air conditioning failure")
    print("Description: The Air conditioning isn't working.")
    print("Service type: Air Conditioning")

    building_button = wait.until(
        EC.visibility_of_element_located((By.ID, "buildingNameButton"))
    )
    room_button = wait.until(
        EC.visibility_of_element_located((By.ID, "roomNameButton"))
    )

    assert building_button.text.strip() == "Select a building", (
        "Building should remain unselected for this test."
    )

    assert room_button.text.strip() == "Select a room", (
        "Room should remain unselected for this test."
    )

    print("Building: NOT SELECTED")
    print("Room: NOT SELECTED")

    form_url = driver.current_url

    submit_button = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "button[type='submit'].btn-submit"
        ))
    )
    submit_button.click()

    driver.save_screenshot("TC05_Missing_Building_Room.png")

    building_button = wait.until(
        EC.visibility_of_element_located((By.ID, "buildingNameButton"))
    )
    room_button = wait.until(
        EC.visibility_of_element_located((By.ID, "roomNameButton"))
    )

    current_url = driver.current_url

    body_text = driver.find_element(By.TAG_NAME, "body").text.lower()

    error_elements = driver.find_elements(
        By.CSS_SELECTOR,
        "[role='alert'], .field__error, .invalid-feedback, "
        ".error-message, .form-error"
    )

    error_text = " ".join(
        element.text.lower()
        for element in error_elements
        if element.is_displayed() and element.text.strip()
    )

    validation_text = body_text + " " + error_text

    building_error = any(
        phrase in validation_text
        for phrase in [
            "building is required",
            "please select a building",
            "building field is required"
        ]
    )

    room_error = any(
        phrase in validation_text
        for phrase in [
            "room is required",
            "please select a room",
            "room field is required"
        ]
    )

    explicit_error = (
        building_error
        or room_error
        or any(
            element.get_attribute("aria-invalid") == "true"
            for element in [building_button, room_button]
        )
    )

    if current_url == form_url and explicit_error:
        print("PASS: TC-05")
        print("The incomplete job order is blocked.")
        print("A validation error for the missing fields is detected.")

    elif current_url == form_url:
        print("INCONCLUSIVE: The form remains open, but")
        print("an explicit Building or Room validation error")
        print("was not detected. Inspect the browser for feedback.")

    else:
        print("FAIL: The page navigated after submitting")
        print("the job order with Building and Room unselected.")
        print("Check whether the system accepted the incomplete request.")

    print("Current URL:", driver.current_url)
    print("Screenshot: TC05_Missing_Building_Room.png")

except Exception as error:
    print("TEST ERROR:", type(error).__name__, error)
    print("Current URL:", driver.current_url)
    driver.save_screenshot("TC05_Error.png")
    raise

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()