import time
from constant import url
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException, StaleElementReferenceException

class BrowserAutomation:
    def __init__(self, browser):
        self.browser = browser.lower()
        self.driver = self._create_driver()

    def _create_driver(self):
        if self.browser == 'chrome':
            options = webdriver.ChromeOptions()
            options.add_argument("--disable-popup-blocking")
            options.add_argument("--disable-notifications")
            return webdriver.Chrome(options=options)
        else:
            raise ValueError("Unsupported browser. Use 'chrome'.")
    def open_url(self, url):
        try:
            self.driver.get(url)
            self._accept_cookies()
            search_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//input[@name='text']"))
            )
            search_box.click()
            self.human_type(search_box, 'Купить спир альфа')
            time.sleep(1)
            search_box.send_keys(Keys.ENTER)
            self._search_and_click_link()
        except NoSuchElementException as e:
            print(f"Element not found: {e}")
        except TimeoutException as e:
            print(f"Operation timed out: {e}")
        except WebDriverException as e:
            print(f"WebDriver error: {e}")
        finally:
            self.driver.quit()

    def _accept_cookies(self):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Allow all')]"))
            ).click()
            print("Cookies accepted.")
        except TimeoutException:
            print("No cookies acceptance button found or operation timed out.")
        except NoSuchElementException:
            print("No cookies acceptance button found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    def _search_and_click_link(self):
        while True:
            try:
                links = self.driver.find_elements(By.XPATH, "//a[contains(@href, 'spirtalfadc.ru')]")
                if links:
                    for link in links:
                        href = link.get_attribute('href')
                        print(f"Found link: {href}")
                        self.driver.execute_script("arguments[0].removeAttribute('target');", link)
                        print(f"Clicking on the link: {href}")
                        time.sleep(2)
                        link.click()
                        time.sleep(2)
                        self.perform_site_actions()
                        return
                else:
                    self.smooth_scroll(total_scroll_time=10, steps=60)
                    try:
                        next_button = WebDriverWait(self.driver, 10).until(
                            EC.element_to_be_clickable((By.XPATH, "//a[contains(@aria-label, 'Следующая страница')]"))
                        )
                        next_button.click()
                        time.sleep(5)
                    except TimeoutException:
                        print("No 'Next' button found or it is not clickable.")
                        break
            except NoSuchElementException:
                print("Target link not found on the current page.")
                break
            except WebDriverException as e:
                print(f"WebDriver error: {e}")
                break

    def perform_site_actions(self):
        try:
            products = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, 'product')]"))
            )
            for product in products:
                time.sleep(1)
                product.click()
                self.smooth_scroll(total_scroll_time=30, steps=60)
                self.smooth_scroll_up(total_scroll_time=3, steps=40)
                self.navigate_pages()
        except TimeoutException:
            print("Products not found or operation timed out.")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")

    def navigate_pages(self):
        try:
            pages = ["//a[contains(@title, 'МЕДИЦИНСКИЕ СПИРТЫ')]", "//a[contains(@title, 'СПИРТ АЛЬФА')]",
                     "//a[contains(@title, 'Доставка')]", "//a[contains(@title, 'Контакты')]"]
            for page in pages:
                element = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, page))
                )
                element.click()
                self.smooth_scroll(total_scroll_time=30, steps=60)
                self.smooth_scroll_up(total_scroll_time=3, steps=40)
        except TimeoutException:
            print("Navigation element not found or operation timed out.")
        except NoSuchElementException as e:
            print(f"Element not found: {e}")

    def smooth_scroll(self, total_scroll_time=3, steps=30):
        for _ in range(steps):
            self.driver.execute_script("window.scrollBy(0, window.innerHeight/arguments[0]);", steps)
            time.sleep(total_scroll_time / steps)

    def smooth_scroll_up(self, total_scroll_time=3, steps=30):
        for _ in range(steps):
            self.driver.execute_script("window.scrollBy(0, -window.innerHeight/arguments[0]);", steps)
            time.sleep(total_scroll_time / steps)

    def human_type(self, element, text, delay=0.1):
        for char in text:
            element.send_keys(char)
            time.sleep(delay)

if __name__ == "__main__":
    automation = BrowserAutomation(browser='chrome')
    automation.open_url(url)


