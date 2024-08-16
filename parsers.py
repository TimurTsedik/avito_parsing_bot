from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def get_listing_count(query: str, region: str) -> int:
    # Настройка для подключения к удаленному веб-драйверу (контейнеру с Chrome)
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(
        command_executor='http://chrome:4444/wd/hub',
        options=options
    )

    try:
        # Формируем URL
        url = f"https://www.avito.ru/{region}?q={query}"
        driver.get(url)

        # Используем WebDriverWait для ожидания загрузки нужного элемента
        wait = WebDriverWait(driver, 10)  # Ждем до 10 секунд
        count_element = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "span.page-title-count-wQ7pG[data-marker='page-title/count']")))

        # После появления элемента извлекаем его текст
        count = int(count_element.text.replace(" ", ""))  # Преобразуем текст в число

        return count

    finally:
        driver.quit()
