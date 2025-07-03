
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class CotizacionesVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("cotizaciones.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_cotizacion)
        self.btnEditar.clicked.connect(self.editar_cotizacion)
        self.btnEliminar.clicked.connect(self.eliminar_cotizacion)
        self.btnBuscar.clicked.connect(self.buscar_cotizacion)
        self.tablaCotizaciones.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_cotizaciones()

    def cargar_cotizaciones(self):
        self.tablaCotizaciones.setRowCount(0)
        self.tablaCotizaciones.setColumnCount(5)
        self.tablaCotizaciones.setHorizontalHeaderLabels([
            "ID", "Código", "Monto", "Fecha Emisión", "RUT Cliente"
        ])
        self.cursor.execute("SELECT * FROM Cotizaciones")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaCotizaciones.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaCotizaciones.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_cotizacion(self):
        try:
            datos = (
                int(self.inputID.text()),
                self.inputCodigo.text(),
                float(self.inputMonto.text()),
                self.inputFechaEmision.text(),
                self.inputRutCliente.text()
            )
            self.cursor.execute("""
                INSERT INTO Cotizaciones (
                    cotizacionID, codigo, monto, fechaEmision, rutCliente
                ) VALUES (%s, %s, %s, %s, %s)
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cotización agregada.")
            self.cargar_cotizaciones()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar cotización: {str(e)}")

    def editar_cotizacion(self):
        try:
            datos = (
                self.inputCodigo.text(),
                float(self.inputMonto.text()),
                self.inputFechaEmision.text(),
                self.inputRutCliente.text(),
                int(self.inputID.text())
            )
            self.cursor.execute("""
                UPDATE Cotizaciones SET
                    codigo=%s, monto=%s, fechaEmision=%s, rutCliente=%s
                WHERE cotizacionID=%s
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cotización actualizada.")
            self.cargar_cotizaciones()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar cotización: {str(e)}")

    def eliminar_cotizacion(self):
        try:
            cotizacion_id = int(self.inputID.text())
            self.cursor.execute("DELETE FROM Cotizaciones WHERE cotizacionID = %s", (cotizacion_id,))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cotización eliminada.")
            self.cargar_cotizaciones()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar cotización: {str(e)}")

    def buscar_cotizacion(self):
        texto = self.inputBuscar.text()
        self.tablaCotizaciones.setRowCount(0)
        self.tablaCotizaciones.setColumnCount(5)
        self.tablaCotizaciones.setHorizontalHeaderLabels([
            "ID", "Código", "Monto", "Fecha Emisión", "RUT Cliente"
        ])
        consulta = """
            SELECT * FROM Cotizaciones
            WHERE cotizacionID LIKE %s OR codigo LIKE %s OR rutCliente LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,) * 3)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaCotizaciones.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaCotizaciones.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputID.setText(self.tablaCotizaciones.item(row, 0).text())
        self.inputCodigo.setText(self.tablaCotizaciones.item(row, 1).text())
        self.inputMonto.setText(self.tablaCotizaciones.item(row, 2).text())
        self.inputFechaEmision.setText(self.tablaCotizaciones.item(row, 3).text())
        self.inputRutCliente.setText(self.tablaCotizaciones.item(row, 4).text())

    def limpiar_campos(self):
        self.inputID.clear()
        self.inputCodigo.clear()
        self.inputMonto.clear()
        self.inputFechaEmision.clear()
        self.inputRutCliente.clear()
        self.inputBuscar.clear()
