from selenium import webdriver

GSC_LOGIN_URL = "https://gscsystem.site/login"

driver = webdriver.Chrome()

try:
    driver.get(GSC_LOGIN_URL)

    print("Page title:", driver.title)
    print("Current URL:", driver.current_url)

    input("Press ENTER to close the browser...")

finally:
    driver.quit()