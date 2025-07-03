from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class OrdenesTrabajoVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("ordenestrabajo.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_orden)
        self.btnEditar.clicked.connect(self.editar_orden)
        self.btnEliminar.clicked.connect(self.eliminar_orden)
        self.btnBuscar.clicked.connect(self.buscar_orden)
        self.tablaOT.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_ordenes()

    def cargar_ordenes(self):
        self.tablaOT.setRowCount(0)
        self.cursor.execute("SELECT * FROM OrdenesTrabajo")
        resultados = self.cursor.fetchall()

        headers = ["ID", "Código", "Fecha Emisión", "Fecha Inicio", "Fecha Término", "Encargado", "Observaciones"]
        self.tablaOT.setColumnCount(len(headers))
        self.tablaOT.setHorizontalHeaderLabels(headers)
        self.tablaOT.setRowCount(len(resultados))

        for row_num, row_data in enumerate(resultados):
            for col_num, data in enumerate(row_data):
                self.tablaOT.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_orden(self):
        try:
            datos = (
                int(self.inputID.text()),
                self.inputCodigo.text(),
                self.inputFechaEmision.text(),
                self.inputFechaInicio.text(),
                self.inputFechaTermino.text(),
                self.inputEncargado.text(),
                self.inputObservaciones.toPlainText()
            )
            self.cursor.execute("""
                INSERT INTO OrdenesTrabajo (
                    otID, codigo, fechaEmision, fechaInicio, fechaTermino,
                    encargado, observaciones
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Orden agregada correctamente.")
            self.cargar_ordenes()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar orden: {str(e)}")

    def editar_orden(self):
        try:
            datos = (
                self.inputCodigo.text(),
                self.inputFechaEmision.text(),
                self.inputFechaInicio.text(),
                self.inputFechaTermino.text(),
                self.inputEncargado.text(),
                self.inputObservaciones.toPlainText(),
                int(self.inputID.text())
            )
            self.cursor.execute("""
                UPDATE OrdenesTrabajo SET
                    codigo=%s, fechaEmision=%s, fechaInicio=%s, fechaTermino=%s,
                    encargado=%s, observaciones=%s
                WHERE otID=%s
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Orden actualizada.")
            self.cargar_ordenes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar orden: {str(e)}")

    def eliminar_orden(self):
        try:
            ot_id = int(self.inputID.text())
            self.cursor.execute("DELETE FROM OrdenesTrabajo WHERE otID = %s", (ot_id,))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Orden eliminada.")
            self.cargar_ordenes()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar orden: {str(e)}")

    def buscar_orden(self):
        texto = self.inputBuscar.text()
        self.tablaOT.setRowCount(0)
        consulta = """
            SELECT * FROM OrdenesTrabajo
            WHERE otID LIKE %s OR codigo LIKE %s OR encargado LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,)*3)
        resultados = self.cursor.fetchall()

        headers = ["ID", "Código", "Fecha Emisión", "Fecha Inicio", "Fecha Término", "Encargado", "Observaciones"]
        self.tablaOT.setColumnCount(len(headers))
        self.tablaOT.setHorizontalHeaderLabels(headers)
        self.tablaOT.setRowCount(len(resultados))

        for row_num, row_data in enumerate(resultados):
            for col_num, data in enumerate(row_data):
                self.tablaOT.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputID.setText(self.tablaOT.item(row, 0).text())
        self.inputCodigo.setText(self.tablaOT.item(row, 1).text())
        self.inputFechaEmision.setText(self.tablaOT.item(row, 2).text())
        self.inputFechaInicio.setText(self.tablaOT.item(row, 3).text())
        self.inputFechaTermino.setText(self.tablaOT.item(row, 4).text())
        self.inputEncargado.setText(self.tablaOT.item(row, 5).text())
        self.inputObservaciones.setPlainText(self.tablaOT.item(row, 6).text())

    def limpiar_campos(self):
        self.inputID.clear()
        self.inputCodigo.clear()
        self.inputFechaEmision.clear()
        self.inputFechaInicio.clear()
        self.inputFechaTermino.clear()
        self.inputEncargado.clear()
        self.inputObservaciones.clear()
        self.inputBuscar.clear()

