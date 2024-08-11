# app/classes/airbnb.py


from app.utils.base_scraper import BaseScraper


class Airbnb(BaseScraper):
    def __init__(self, scraper):
        self.scraper = scraper

    def modal(self):
        # Verificar si el modal existe
        isFailed = False
        original_data = self.scraper.data
        modal1 = self.scraper.data.get("modal-opts-1")
        type_place = modal1.get("type-place")
        try:
            by = self.scraper.getByTyped(type_place.get("by"))
            element = self.scraper.getElement(by, type_place.get("selector"))
            element.click()
        except:
            isFailed = True
        self.scraper.waitTime(type_place.get("time"))
        # Si no falla realizar la siguiente acción
        if not isFailed:
            # Ir a los servicios
            dropdown_services = modal1.get("dropdown-services")
            self.scraper.setData(dropdown_services)
            self.scraper.SCROLL()
            # Mostrar los servicios
            more_services = modal1.get("more-services")
            self.scraper.setData(more_services)
            self.scraper.CLICK()
            # Seleccionar los servicios
            services = modal1.get("services")
            by = self.scraper.getByTyped(services.get("by"))
            list_services = services.get("list")
            selector = services.get("selector")
            for service in list_services:
                element = self.scraper.getElement(
                    by, selector.replace(":name", service)
                )
                element.click()
                self.scraper.waitTime(services.get("time"))
        # Si falla realizar la siguiente acción
        if isFailed:
            modal2 = self.scraper.data.get("modal-opts-2")
            self.scraper.setData(modal2.get("type-place"))
            self.scraper.CLICK()
        # Ir al idioma
        rest_modal = original_data.get("rest-modal")
        dropdown_language = rest_modal.get("dropdown-language")
        self.scraper.setData(dropdown_language)
        self.scraper.CLICK()
        # Seleccionar el idioma
        select_language = rest_modal.get("select-language")
        self.scraper.setData(select_language)
        self.scraper.CLICK()
        # Enviar la búsqueda
        send = rest_modal.get("send")
        self.scraper.setData(send)
        self.scraper.CLICK()

    def processElements(self):
        data = []
        self.scraper.setProperties()
        for element in self.scraper.elements:
            # Acceder a los sub elementos
            texts = element.find_elements(self.scraper.by, self.scraper.selector)
            # Extraer el texto de los sub elementos
            text_lists = [text.text for text in texts]
            lugar, descripcion, areaArr, fechaArr, precioArr, calificacionArr = (
                text_lists
            )
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
        self.scraper.elements = data
