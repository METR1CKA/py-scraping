from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

opts = Options()
opts.add_argument("--start-maximized")
opts.add_argument("--disable-extensions")
opts.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=ChromeService(), options=opts)

# Ingresar a la página de Airbnb
driver.get("https://www.airbnb.mx/")
sleep(5)

# Buscar alojamiento
element = driver.find_element(By.XPATH, '//input[@id="bigsearch-query-location-input"]')
sleep(1)
element.send_keys("Tor")
sleep(1)

# Seleccionar la primera opción
element = driver.find_element(
    By.XPATH, '//div[@id="bigsearch-query-location-suggestion-0"]'
)
element.click()
sleep(1)

# Seleccionar la fecha de llegada
element = driver.find_element(
    By.XPATH,
    '//div[@class="p1m42al0 atm_c8_km0zk7 atm_g3_18khvle atm_fr_1m9t47k atm_7l_1esdqks atm_cs_6adqpa atm_ks_15vqwwr atm_sq_1l2sidv atm_vy_1osqo2v dir dir-ltr"]',
)
element.click()
sleep(1)

# Elegir la opción flexible
element = driver.find_element(By.XPATH, '//button[@id="tab--tabs--2"]')
element.click()
sleep(1)

# Seleccionar el tiempo que me gustaria quedarme
element = driver.find_element(
    By.XPATH, '//label[@id="flexible_trip_lengths-one_month"]'
)
element.click()
sleep(1)

# Seleccionar cuando quiero ir
element = driver.find_element(
    By.XPATH,
    '//span[@class="l15ntb32 atm_ks_15vqwwr atm_ax_idpfg4 atm_bb_idpfg4 atm_9s_1txwivl atm_h_1h6ojuz atm_fc_1h6ojuz dir dir-ltr"]',
)
element.click()
sleep(1)

# Seleccionar los huespedes
element = driver.find_element(
    By.XPATH, '//*[@id="search-tabpanel"]/div/div[5]/div[2]/div[1]/div/div[2]'
)
element.click()
sleep(1)

# Seleccionar el número de adultos
element = driver.find_element(By.XPATH, '//*[@id="stepper-adults"]/button[2]')
element.click()
sleep(1)

# Enviar la búsqueda
element = driver.find_element(
    By.XPATH,
    '//button[@data-testid="structured-search-input-search-button"]',
)
element.click()
sleep(5)

# Seleccionar el filtrador
element = driver.find_element(
    By.XPATH,
    '//button[@data-testid="category-bar-filter-button"]',
)
element.click()
sleep(1)

isFailed = False

try:
    # Seleccionar la opción de Alojamiento entero
    element = driver.find_element(By.XPATH, '//button[@id="tab--tabs--2"]')
    element.click()
except Exception as e:
    isFailed = True

sleep(1)

# Filtros de búsqueda si falla
if isFailed:
    # Seleccionar la opción de Alojamiento entero
    element = driver.find_element(
        By.XPATH,
        "/html/body/div[10]/div/div/section/div/div/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div/section/div/div[2]/div[1]/div[3]/span",
    )
    element.click()
    sleep(1)

# Filtros de búsqueda si no falla
if not isFailed:
    # Seleccionar la opción de Alojamiento entero
    element = driver.find_element(By.XPATH, '//button[@id="tab--tabs--2"]')
    element.click()

    # Seleccionar los servicios
    element = driver.find_element(
        By.XPATH,
        '//section[@aria-labelledby="filter-section-heading-id-FILTER_SECTION_CONTAINER:MORE_FILTERS_AMENITIES_WITH_SUBCATEGORIES"]',
    )
    driver.execute_script("arguments[0].scrollIntoView();", element)
    sleep(1)

    # Mostrar más servicios
    element = driver.find_element(
        By.XPATH,
        '//span[@class="lsqfxex atm_9s_1txwivl atm_h_1h6ojuz atm_cx_i2wt44 atm_le_ftgil2__oggzyc dir dir-ltr"]',
    )
    element.click()
    sleep(1)

    services = [
        "Lavadora",
        "Wifi",
        "Cocina",
        "Aire acondicionado",
        "Secadora",
        "Televisión",
        "Plancha",
        "Área para trabajar",
    ]

    for service in services:
        element = driver.find_element(
            By.XPATH,
            f'//input[@name="{service}"]',
        )
        element.click()
        sleep(1)

# Seleccionar el idioma del anfitrión
element = driver.find_element(
    By.XPATH,
    '//*[@id="filter-section-heading-id-FILTER_SECTION_CONTAINER:HOST_LANGUAGE"]',
)
driver.execute_script("arguments[0].scrollIntoView();", element)
element.click()
sleep(1)

# Mostrar más servicios
element = driver.find_element(
    By.XPATH,
    '//input[@id="filter-item-host_languages-es-row-checkbox"]',
)
element.click()
sleep(1)

# Enviar los filtros
element = driver.find_element(
    By.XPATH,
    "/html/body/div[10]/div/div/section/div/div/div[2]/div/div[2]/footer/div/a",
)
element.click()
sleep(5)

elements = driver.find_elements(
    By.XPATH,
    '//*[@id="site-content"]/div/div[2]/div[1]/div/div/div/div/div',
)
sleep(1)

data = []

for element in elements:
    texts = element.find_elements(
        By.XPATH, ".//div/div[2]/div/div/div/div/div/div[2]/div"
    )
    text_lists = [text.text for text in texts]

    lugar, descripcion, areaArr, fechaArr, precioArr, calificacionArr = text_lists

    # Hacer split de los datos
    areaArr = areaArr.split("\n")
    fechaArr = fechaArr.split("\n")
    precioArr = precioArr.split("\n")
    calificacionArr = calificacionArr.split("\n")

    # Extraer el area y validarla
    area, *rest = areaArr
    area = area if area != "" else "N/A"

    # Extraer la fecha y validarla
    fecha, *rest = fechaArr
    fecha = fecha if fecha != "" else "N/A"

    # Extraer el precio y validarla
    precio = precioArr[-1].strip() if precioArr[-1] != "" else "N/A"

    # Extraer la calificación y validarla
    calificacion, *rest = calificacionArr
    calificacion = calificacion.split(":")[-1].strip()
    calificacion = calificacion if calificacion != "" else "N/A"

    data.append(
        {
            "Lugar": lugar,
            "Descripcion": descripcion,
            "Area": area,
            "Fecha": fecha,
            "Precio": precio,
            "Calificación promedio": calificacion,
        }
    )


df = pd.DataFrame(data)
df.to_excel("docs/airbnb/airbnb.xlsx", index=False)
sleep(1)

driver.quit()
