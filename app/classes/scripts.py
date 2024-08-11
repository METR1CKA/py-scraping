# app/classes/scripts.py


from app.utils.pandas_df import PandasDataFrame


class Scripts:
    def __init__(self, scraper):
        self.scraper = scraper
        self.pandas = PandasDataFrame()

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

    def extractPlaces(self):
        data = []
        self.scraper.setProperties()
        selector1 = self.scraper.selector.get("value-1")
        selector2 = self.scraper.selector.get("value-2")
        elements = self.scraper.getElements(self.scraper.by, selector1)
        self.scraper.waitTime(self.scraper.time)
        for element in elements:
            # Acceder a los sub elementos
            texts = element.find_elements(self.scraper.by, selector2)
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
        # self.scraper.elements = data
        df = self.pandas.createDataFrame(data)
        self.pandas.exportToExcel(
            df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )

    def extractTable(self):
        type_selector, selectors = (
            self.scraper.data.get("type-selector"),
            self.scraper.data.get("selectors"),
        )
        headers_rows_by, cols_by = (
            type_selector.get("headers-rows"),
            type_selector.get("cols"),
        )
        headers_selector, rows_selector, cols_selector = (
            selectors.get("headers"),
            selectors.get("rows"),
            selectors.get("cols"),
        )
        headers_rows_by = self.scraper.getByTyped(headers_rows_by)
        cols_by = self.scraper.getByTyped(cols_by)
        headers = self.scraper.getElements(headers_rows_by, headers_selector)
        headers = [header.text for header in headers]
        rows = self.scraper.getElements(headers_rows_by, rows_selector)
        data = []
        for row in rows:
            cols = row.find_elements(cols_by, cols_selector)
            cols = [col.text for col in cols]
            data.append(cols)
        df = self.pandas.createDataFrame(data, headers)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )
        self.scraper.waitTime(self.scraper.data.get("time"))

    def splits(self):
        # Obtener la información de los splits
        self.scraper.setProperties()
        original_data = self.scraper.data
        split_indexes = original_data.get("indexes")
        paths = original_data.get("paths")
        filename = original_data.get("filename")
        time = original_data.get("time")
        selector1 = self.scraper.selector.get("value-1")
        selector2 = self.scraper.selector.get("value-2")
        self.scraper.waitTime(time)
        # Iterar sobre los splits
        for i, split_index in enumerate(split_indexes):
            element = self.scraper.getElement(
                self.scraper.by, selector1.replace(":index", str(split_index))
            )
            element.click()
            self.scraper.waitTime(time)
            elements = self.scraper.getElements(self.scraper.by, selector2)
            headers = []
            data = []
            header_div = elements[0]
            header_texts = header_div.text.split("\n")
            headers = header_texts
            for element in elements[1:]:
                text_list = element.text.split("\n")
                data.append(text_list)
            df = self.pandas.createDataFrame(data, headers)
            self.pandas.exportToExcel(
                data=df, folders=paths, filename=filename.replace(":index", str(i + 1))
            )

    def cups(self):
        # Obtener la información de los splits
        self.scraper.setProperties()
        original_data = self.scraper.data
        cup_indexes = original_data.get("indexes")
        paths = original_data.get("paths")
        time = original_data.get("time")
        selector1 = self.scraper.selector.get("value-1")
        selector2 = self.scraper.selector.get("value-2")
        selector3 = self.scraper.selector.get("value-3")
        selector4 = self.scraper.selector.get("value-4")
        self.scraper.waitTime(time)
        for cup_index in cup_indexes:
            element = self.scraper.getElement(
                self.scraper.by, selector1.replace(":index", str(cup_index))
            )
            element.click()
            self.scraper.waitTime(time)
            elements = self.scraper.getElements(self.scraper.by, selector2)
            folders = paths.get("folders")
            if len(folders) == 3:
                folders.pop()
            if cup_index == 3:
                folders.append(paths.get("kings_cup"))
            if cup_index == 4:
                folders.append(paths.get("kingdom_cup"))
            for sub_element in elements:
                group_element = sub_element.find_element(self.scraper.by, selector3)
                group_split = group_element.text.split("\n")
                group = "_".join(group_split)
                table_elements = sub_element.find_elements(self.scraper.by, selector4)
                headers = []
                data = []
                header_div = table_elements[0]
                header_texts = header_div.text.split("\n")
                headers = header_texts
                for element in table_elements[1:]:
                    text_list = element.text.split("\n")
                    data.append(text_list)
                df = self.pandas.createDataFrame(data, headers)
                self.pandas.exportToExcel(data=df, folders=folders, filename=group)

    def extractTableDivs(self):
        self.scraper.setProperties()
        headers_xpath = self.scraper.selector.get("headers")
        next_element_xpath = self.scraper.selector.get("next_element")
        headers = self.scraper.getElements(self.scraper.by, headers_xpath)
        self.scraper.waitTime(self.scraper.time)
        data = []
        for header in headers:
            self.scraper.scrollIntoView(header)
            title = header.text
            next_element = header.find_element(self.scraper.by, next_element_xpath)
            curiosity = next_element.text
            data.append({"Titulo": title, "Curiosidad": curiosity})
            self.scraper.waitTime(self.scraper.time)
        df = self.pandas.createDataFrame(data)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )

    def extractTables(self):
        # Top20 - OtherPL
        type_selectors, selectors = (
            self.scraper.data.get("type-selectors"),
            self.scraper.data.get("selectors"),
        )
        headers_rows_by, cols_by = (
            type_selectors.get("headers-rows-by"),
            type_selectors.get("cols-by"),
        )
        headers_selector, rows_selector, cols_selector = (
            selectors.get("headers-selector"),
            selectors.get("rows-selector"),
            selectors.get("cols-selector"),
        )
        headers_rows_by = self.scraper.getByTyped(headers_rows_by)
        cols_by = self.scraper.getByTyped(cols_by)
        headers = self.scraper.getElements(headers_rows_by, headers_selector)
        headers = [header.text for header in headers]
        self.scraper.waitTime(1)
        remove_change = self.scraper.data.get("remove-change")
        if remove_change:
            first_change_index = headers.index("Change") if "Change" in headers else -1
            if first_change_index != -1:
                headers = [
                    header
                    for i, header in enumerate(headers)
                    if header != "Change" or i > first_change_index
                ]
        rows = self.scraper.getElements(headers_rows_by, rows_selector)
        data = []
        for row in rows:
            cols = row.find_elements(cols_by, cols_selector)
            cols = [col.text for col in cols if col.text.strip() != ""]
            data.append(cols)
        df = self.pandas.createDataFrame(data, headers)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )
        self.scraper.waitTime(self.scraper.data.get("time"))

    def hallOfFameTable(self):
        type_selectors, selectors = (
            self.scraper.data.get("type-selectors"),
            self.scraper.data.get("selectors"),
        )
        rows_by, cols_headers_by = (
            type_selectors.get("rows-by"),
            type_selectors.get("cols-headers-by"),
        )
        headers_selector, rows_selector, cols_selector = (
            selectors.get("headers-selector"),
            selectors.get("rows-selector"),
            selectors.get("cols-selector"),
        )
        rows_by = self.scraper.getByTyped(rows_by)
        cols_headers_by = self.scraper.getByTyped(cols_headers_by)
        rows = self.scraper.getElements(rows_by, rows_selector)
        headers = []
        data = []
        for i, row in enumerate(rows):
            if i == 0:
                headers = row.find_elements(cols_headers_by, headers_selector)
                headers = [header.text for header in headers]
            else:
                cols = row.find_elements(cols_headers_by, cols_selector)
                cols = [col.text for col in cols]
                data.append(cols)
        df = self.pandas.createDataFrame(data, headers)
        self.pandas.exportToExcel(
            data=df,
            folders=self.scraper.data.get("paths"),
            filename=self.scraper.data.get("filename"),
        )
        self.scraper.waitTime(self.scraper.data.get("time"))

    def meteoreTables(self):
        # Setear datos y acumular las ciudades
        self.scraper.setProperties()
        cities = self.scraper.data.get("cities")
        for city in cities:
            # Acumular datos
            full_data = []
            # Ingresar la primer ciudad
            seearch_city = self.scraper.data.get("search-city")
            selector = seearch_city.get("selector")
            element = self.scraper.getElement(self.scraper.by, selector)
            element.send_keys(city)
            self.scraper.waitTime(seearch_city.get("time"))
            # Seleccionar la primera opción
            select_first = self.scraper.data.get("select-first")
            selector = select_first.get("selector")
            element = self.scraper.getElement(self.scraper.by, selector)
            element.click()
            self.scraper.waitTime(select_first.get("time"))
            # Seleccionar los dias
            days_indexes = self.scraper.data.get("days-indexes")
            for day_index in days_indexes:
                # Ir a la sección de los días
                select_section = self.scraper.data.get("select-section")
                selector = select_section.get("selector")
                element = self.scraper.getElement(
                    self.scraper.by,
                    selector.replace(":day_index", str(day_index)),
                )
                self.scraper.scrollIntoView(element)
                self.scraper.waitTime(select_section.get("time"))
                element.click()
                self.scraper.waitTime(select_section.get("time"))
                # Obtener los datos
                get_elements = self.scraper.data.get("get-elements")
                selector = get_elements.get("selector")
                elements = self.scraper.getElements(self.scraper.by, selector)
                data = [element.text for element in elements]
                data = [entry for entry in data if entry]
                # Procesar los datos
                process_data = []
                for entry in data:
                    parts = entry.split("\n")
                    (
                        hora,
                        temperatura,
                        sensacion_termica,
                        viento,
                        velocidad,
                        indice_uv,
                        fps,
                    ) = parts
                    process_data.append(
                        {
                            "Hora": hora,
                            "Temperatura": temperatura,
                            "Sensación Termica": sensacion_termica,
                            "Viento": viento,
                            "Velocidad": velocidad,
                            "Índice UV": indice_uv,
                            "FPS": fps,
                        }
                    )
                full_data += process_data
            # Crear el DataFrame y guardar en archivo Excel
            df = self.pandas.createDataFrame(full_data)
            self.pandas.exportToExcel(
                df, folders=self.scraper.data.get("paths"), filename=f"{city}.xlsx"
            )
            self.scraper.scrollTop()
            self.scraper.waitTime(self.scraper.data.get("time"))
