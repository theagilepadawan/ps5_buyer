import time
import json

from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def wait_for(condition_function):
  start_time = time.time()
  while time.time() < start_time + 10:
    if condition_function():
      return True
    else:
      time.sleep(0.1)
  raise Exception(
   'Timeout waiting for {}'.format(condition_function)
  )


checkout_URL ="https://coop.no/checkout/checkouttotal/"
product_URL = "https://coop.no/sortiment/obs-sortiment/elektronikk/underholdning/konsoll/playstation-ps4-500gb-d/?variantCode=204940"
coo = {"name" : "manualSetStore_02", "value" : "true"}
coo1 = {"name" : "currentstoreforchain_43", "value" : "3507"}
coo2 = {"name" : "currentstoreforchain_02", "value" : "2541"}
def main():
    config = None
    with open('config.json', 'r') as f:
        config = json.load(f)

    driver = webdriver.Chrome()
    driver.implicitly_wait(5)

    driver.get(product_URL)

    driver.add_cookie(coo)
    driver.add_cookie(coo1)
    driver.add_cookie(coo2)


    driver.find_elements_by_css_selector("[aria-label=Kjøp]")[0].click()

    driver.get(checkout_URL)
    username = driver.find_element_by_xpath("//input[@name='username']")
    username.send_keys(config["username"])

    link = driver.find_element_by_xpath("//input[@name='username']")

    def link_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            link.find_elements_by_id('button')
            return False
        except StaleElementReferenceException:
            return True
    pwd = driver.find_element_by_xpath("//input[@name='password']")
    pwd.send_keys(config["password"])
    pwd.send_keys(Keys.RETURN)

    wait_for(link_has_gone_stale)
    checkbox = driver.find_element_by_xpath("//input[@type='checkbox']")
    checkbox.send_keys(Keys.PAGE_DOWN)
    time.sleep(1)
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))).click()
    checkbox.send_keys(Keys.RETURN)

    driver.close()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
