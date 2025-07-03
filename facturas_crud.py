from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class FacturasVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("facturas.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_factura)
        self.btnEditar.clicked.connect(self.editar_factura)
        self.btnEliminar.clicked.connect(self.eliminar_factura)
        self.btnBuscar.clicked.connect(self.buscar_factura)
        self.tablaFacturas.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_facturas()

    def cargar_facturas(self):
        self.tablaFacturas.setRowCount(0)
        self.tablaFacturas.setColumnCount(12)
        self.tablaFacturas.setHorizontalHeaderLabels([
            "ID", "Fecha Emisión", "Fecha Vencimiento", "Nombre Cliente",
            "Total Neto", "Total IVA", "Total", "Ingreso", "Clasificación",
            "Año", "Estado", "RUT Cliente"
        ])
        self.cursor.execute("SELECT * FROM Facturas")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaFacturas.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaFacturas.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_factura(self):
        try:
            datos = (
                int(self.inputID.text()),
                self.inputFechaEmision.text(),
                self.inputFechaVencimiento.text(),
                self.inputNombreCliente.text(),
                float(self.inputTotalNeto.text()),
                float(self.inputTotalIVA.text()),
                float(self.inputTotal.text()),
                float(self.inputIngreso.text()),
                self.inputClasificacion.text(),
                int(self.inputAnio.text()),
                self.inputEstado.currentText(),
                self.inputRutCliente.text()
            )
            self.cursor.execute("""
                INSERT INTO Facturas (
                    facturaID, fechaEmision, fechaVencimiento, nombreCliente,
                    totalNeto, totalIVA, total, ingreso, clasificacion,
                    año, estado, rutCliente
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Factura agregada correctamente.")
            self.cargar_facturas()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar factura: {str(e)}")

    def editar_factura(self):
        try:
            datos = (
                self.inputFechaEmision.text(),
                self.inputFechaVencimiento.text(),
                self.inputNombreCliente.text(),
                float(self.inputTotalNeto.text()),
                float(self.inputTotalIVA.text()),
                float(self.inputTotal.text()),
                float(self.inputIngreso.text()),
                self.inputClasificacion.text(),
                int(self.inputAnio.text()),
                self.inputEstado.currentText(),
                self.inputRutCliente.text(),
                int(self.inputID.text())
            )
            self.cursor.execute("""
                UPDATE Facturas SET
                    fechaEmision=%s, fechaVencimiento=%s, nombreCliente=%s,
                    totalNeto=%s, totalIVA=%s, total=%s, ingreso=%s, clasificacion=%s,
                    año=%s, estado=%s, rutCliente=%s
                WHERE facturaID=%s
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Factura actualizada.")
            self.cargar_facturas()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar factura: {str(e)}")

    def eliminar_factura(self):
        try:
            factura_id = int(self.inputID.text())
            self.cursor.execute("DELETE FROM Facturas WHERE facturaID = %s", (factura_id,))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Factura eliminada.")
            self.cargar_facturas()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar factura: {str(e)}")

    def buscar_factura(self):
        texto = self.inputBuscar.text()
        self.tablaFacturas.setRowCount(0)
        self.tablaFacturas.setColumnCount(12)
        self.tablaFacturas.setHorizontalHeaderLabels([
            "ID", "Fecha Emisión", "Fecha Vencimiento", "Nombre Cliente",
            "Total Neto", "Total IVA", "Total", "Ingreso", "Clasificación",
            "Año", "Estado", "RUT Cliente"
        ])
        consulta = """
            SELECT * FROM Facturas
            WHERE facturaID LIKE %s OR nombreCliente LIKE %s OR estado LIKE %s OR rutCliente LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,) * 4)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaFacturas.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaFacturas.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputID.setText(self.tablaFacturas.item(row, 0).text())
        self.inputFechaEmision.setText(self.tablaFacturas.item(row, 1).text())
        self.inputFechaVencimiento.setText(self.tablaFacturas.item(row, 2).text())
        self.inputNombreCliente.setText(self.tablaFacturas.item(row, 3).text())
        self.inputTotalNeto.setText(self.tablaFacturas.item(row, 4).text())
        self.inputTotalIVA.setText(self.tablaFacturas.item(row, 5).text())
        self.inputTotal.setText(self.tablaFacturas.item(row, 6).text())
        self.inputIngreso.setText(self.tablaFacturas.item(row, 7).text())
        self.inputClasificacion.setText(self.tablaFacturas.item(row, 8).text())
        self.inputAnio.setText(self.tablaFacturas.item(row, 9).text())
        self.inputEstado.setCurrentText(self.tablaFacturas.item(row, 10).text())
        self.inputRutCliente.setText(self.tablaFacturas.item(row, 11).text())

    def limpiar_campos(self):
        self.inputID.clear()
        self.inputFechaEmision.clear()
        self.inputFechaVencimiento.clear()
        self.inputNombreCliente.clear()
        self.inputTotalNeto.clear()
        self.inputTotalIVA.clear()
        self.inputTotal.clear()
        self.inputIngreso.clear()
        self.inputClasificacion.clear()
        self.inputAnio.clear()
        self.inputEstado.setCurrentIndex(0)
        self.inputRutCliente.clear()
        self.inputBuscar.clear()

