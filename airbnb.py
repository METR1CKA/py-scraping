from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium import webdriver
from time import sleep
import pandas as pd

opts = Options()

user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"

opts.add_argument(f"{user_agent=}")
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

# Seleccionar la opción de Alojamiento entero
element = driver.find_element(By.XPATH, '//button[@id="tab--tabs--2"]')
element.click()

sleep(1)

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
    "//a[@class='l1ovpqvx atm_1he2i46_1k8pnbi_10saat9 atm_yxpdqi_1pv6nv4_10saat9 atm_1a0hdzc_w1h1e8_10saat9 atm_2bu6ew_929bqk_10saat9 atm_12oyo1u_73u7pn_10saat9 atm_fiaz40_1etamxe_10saat9 bmx2gr4 atm_9j_tlke0l atm_9s_1o8liyq atm_gi_idpfg4 atm_mk_h2mmj6 atm_r3_1h6ojuz atm_rd_glywfm atm_70_5j5alw atm_vy_1wugsn5 atm_tl_1gw4zv3 atm_9j_13gfvf7_1o5j5ji c1ih3c6 atm_bx_48h72j atm_c8_2x1prs atm_g3_1jbyh58 atm_fr_11a07z3 atm_cs_10d11i2 atm_5j_t09oo2 atm_kd_glywfm atm_l8_srw7uq atm_uc_1lizyuv atm_r2_1j28jx2 atm_jb_1fkumsa atm_3f_glywfm atm_26_18sdevw atm_7l_1v2u014 atm_8w_1t7jgwy atm_uc_glywfm__1rrf6b5 atm_kd_glywfm_1w3cfyq atm_uc_aaiy6o_1w3cfyq atm_70_1b8lkes_1w3cfyq atm_3f_glywfm_e4a3ld atm_l8_idpfg4_e4a3ld atm_gi_idpfg4_e4a3ld atm_3f_glywfm_1r4qscq atm_kd_glywfm_6y7yyg atm_uc_glywfm_1w3cfyq_1rrf6b5 atm_kd_glywfm_pfnrn2_1oszvuo atm_uc_aaiy6o_pfnrn2_1oszvuo atm_70_1b8lkes_pfnrn2_1oszvuo atm_3f_glywfm_1icshfk_1oszvuo atm_l8_idpfg4_1icshfk_1oszvuo atm_gi_idpfg4_1icshfk_1oszvuo atm_3f_glywfm_b5gff8_1oszvuo atm_kd_glywfm_2by9w9_1oszvuo atm_uc_glywfm_pfnrn2_1o31aam atm_tr_18md41p_csw3t1 atm_k4_kb7nvz_1o5j5ji atm_3f_glywfm_1nos8r_uv4tnr atm_26_wcf0q_1nos8r_uv4tnr atm_7l_1v2u014_1nos8r_uv4tnr atm_3f_glywfm_4fughm_uv4tnr atm_26_4ccpr2_4fughm_uv4tnr atm_7l_1v2u014_4fughm_uv4tnr atm_3f_glywfm_csw3t1 atm_26_wcf0q_csw3t1 atm_7l_1v2u014_csw3t1 atm_3f_glywfm_1o5j5ji atm_26_4ccpr2_1o5j5ji atm_7l_1v2u014_1o5j5ji dir dir-ltr']",
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

    data.append(
        {
            "Lugar": text_lists[0],
            "Descripcion": text_lists[1],
            "Area": text_lists[2].split("\n")[0],
            "Fecha": text_lists[3].split("\n")[0],
            "Precio": text_lists[4].split("\n")[-1],
            "Calificación promedio": text_lists[5]
            .split("\n")[0]
            .split(":")[-1]
            .strip(),
        }
    )


df = pd.DataFrame(data)

df.to_excel("docs/airbnb/airbnb.xlsx", index=False)

sleep(1)

driver.quit()
