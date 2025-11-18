from behave import given, when, then
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import os
from selenium.webdriver.chrome.options import Options


def _parse_letters(letras_csv):
    cleaned = letras_csv.replace('"', "").replace("'", "")
    parts = [
        part.strip()
        for part in cleaned.replace(",", " ").split()
        if part.strip()
    ]
    return [p.lower() for p in parts]


@given('el servidor Flask está corriendo con la palabra "{palabra}"')
def step_open_browser(context, palabra=None):
    chrome_options = Options()

    if os.getenv("CI") == "true":
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")

    service = Service(ChromeDriverManager().install())
    context.driver = webdriver.Chrome(service=service, options=chrome_options)

    if palabra:
        context.driver.get(f"http://127.0.0.1:5000/set_palabra/{palabra}")
        time.sleep(0.5)
    else:
        context.driver.get("http://127.0.0.1:5000")
        time.sleep(1)


@when('ingreso la letra "{letras_csv}" en el campo de intento y presiono el botón')
def step_try_letters(context, letras_csv):
    letras = _parse_letters(letras_csv)
    for letra in letras:
        input_box = context.driver.find_element(By.NAME, "intento")
        input_box.clear()
        input_box.send_keys(letra)
        button = context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        button.click()
        time.sleep(0.5)


@when('ingreso la palabra "{texto}" en el campo de intento y presiono el botón')
def step_input_text(context, texto):
    input_box = context.driver.find_element(By.NAME, "intento")
    input_box.clear()
    input_box.send_keys(texto)
    button = context.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
    button.click()
    time.sleep(0.5)


@then('el juego debe estar ganado')
def step_then_won(context):
    estado = context.driver.find_element(By.ID, "estado-juego")

    terminado = estado.get_attribute("data-terminado") == "True"
    ganado = estado.get_attribute("data-ganado") == "True"
    derrotado = estado.get_attribute("data-derrotado") == "True"

    assert terminado, "El juego no está marcado como terminado."
    assert ganado, "El juego no está marcado como ganado."
    assert not derrotado, "El juego aparece como derrotado cuando debería estar ganado."


@then('el juego debe estar derrotado')
def step_then_lost(context):
    estado = context.driver.find_element(By.ID, "estado-juego")

    terminado = estado.get_attribute("data-terminado") == "True"
    ganado = estado.get_attribute("data-ganado") == "True"
    derrotado = estado.get_attribute("data-derrotado") == "True"

    assert terminado, "El juego no está marcado como terminado."
    assert derrotado, "El juego no está marcado como derrotado."
    assert not ganado, "El juego aparece como ganado cuando debería estar perdido."


@then('las vidas deben ser {vidas:d}')
def step_then_vidas(context, vidas):
    vidas_text = context.driver.find_element(
        By.XPATH, "//p[starts-with(normalize-space(), 'Vidas restantes')]"
    ).text
    corazones = vidas_text.count('❤️')

    assert corazones == vidas, (
        f"Esperaba {vidas} vidas, pero se encontraron {corazones} en: {vidas_text}"
    )


@then("cierro el navegador")
def step_close_browser(context):
    context.driver.quit()
