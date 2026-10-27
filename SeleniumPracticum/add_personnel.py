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

    personnel_link = wait.until(
        EC.element_to_be_clickable((
            By.CSS_SELECTOR,
            "a.subnav__tab[href*='/admin/system-data/personnel']"
        ))
    )
    personnel_link.click()

    wait.until(EC.url_contains("/admin/system-data/personnel"))
    print("Personnel page:", driver.current_url)

    add_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[contains(@class,'btn-add') "
            "and normalize-space()='Add Personnel']"
        ))
    )
    add_button.click()

    def find_input_by_label(label_text):
        label_xpath = (
            "//label[translate(normalize-space(.), "
            "'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')="
            f"'{label_text.lower()}']"
        )

        label = wait.until(
            EC.presence_of_element_located((By.XPATH, label_xpath))
        )

        field_id = label.get_attribute("for")

        if field_id:
            return wait.until(
                EC.visibility_of_element_located((By.ID, field_id))
            )

        for locator in [
            ".//input",
            "../input",
            "following-sibling::input[1]",
            "following::input[1]"
        ]:
            for field in label.find_elements(By.XPATH, locator):
                if field.is_displayed() and field.is_enabled():
                    return field

        raise Exception(
            f"Could not locate the input for '{label_text}'."
        )

    full_name_field = find_input_by_label("Full name")
    full_name_field.clear()
    full_name_field.send_keys("Michelle Angela")

    service_dropdown = wait.until(
        EC.visibility_of_element_located(
            (By.ID, "newPersonnelService")
        )
    )
    Select(service_dropdown).select_by_visible_text("Air Conditioning")

    contact_field = find_input_by_label("Contact Number")
    contact_field.clear()
    contact_field.send_keys("09875678976")

    submit_button = wait.until(
        EC.element_to_be_clickable((
            By.XPATH,
            "//button[@type='submit' "
            "and contains(@class,'btn-create') "
            "and normalize-space()='Add Personnel']"
        ))
    )
    submit_button.click()

    wait.until(
        lambda d: "Michelle Angela"
        in d.find_element(By.TAG_NAME, "body").text
    )

    print("PASS: Personnel record submitted and name appears on the page.")
    print("Name: Michelle Angela")
    print("Service type: Air Conditioning")
    print("Contact number: 09875678976")

    driver.save_screenshot("TC08_Add_Personnel.png")
    print("Screenshot saved: TC08_Add_Personnel.png")

except Exception as error:
    print("FAIL:", type(error).__name__, error)
    print("Current URL:", driver.current_url)

    try:
        driver.save_screenshot("TC08_Error.png")
        print("Error screenshot saved: TC08_Error.png")
    except Exception:
        pass

finally:
    input("\nPress ENTER in the terminal to close the browser...")
    driver.quit()