
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class SeguimientosVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("seguimientos.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_seguimiento)
        self.btnEditar.clicked.connect(self.editar_seguimiento)
        self.btnEliminar.clicked.connect(self.eliminar_seguimiento)
        self.btnBuscar.clicked.connect(self.buscar_seguimiento)
        self.tablaSeguimientos.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_seguimientos()

    def cargar_seguimientos(self):
        self.tablaSeguimientos.setRowCount(0)
        self.cursor.execute("SELECT * FROM Seguimientos")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaSeguimientos.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaSeguimientos.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_seguimiento(self):
        try:
            datos = (
                self.inputCodigo.text(),
                self.inputFecha.text(),
                self.inputEstado.text(),
                self.inputCliente.text(),
                self.inputObra.text(),
                self.inputFechaEntrega.text(),
                int(self.inputDias.text()),
                self.inputDesde.text(),
                self.inputHasta.text(),
                int(self.inputGuiaID.text()),
                int(self.inputFacturaID.text()),
                self.inputNota.toPlainText()
            )
            self.cursor.execute("""
                INSERT INTO Seguimientos (
                    codigo, fecha, estado, cliente, obra, fechaEntrega,
                    dias, desde, hasta, guiaID, facturaID, nota
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Seguimiento agregado.")
            self.cargar_seguimientos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar seguimiento: {str(e)}")

    def editar_seguimiento(self):
        try:
            datos = (
                self.inputFecha.text(),
                self.inputEstado.text(),
                self.inputCliente.text(),
                self.inputObra.text(),
                self.inputFechaEntrega.text(),
                int(self.inputDias.text()),
                self.inputDesde.text(),
                self.inputHasta.text(),
                int(self.inputFacturaID.text()),
                self.inputNota.toPlainText(),
                self.inputCodigo.text(),
                int(self.inputGuiaID.text())
            )
            self.cursor.execute("""
                UPDATE Seguimientos SET
                    fecha=%s, estado=%s, cliente=%s, obra=%s, fechaEntrega=%s,
                    dias=%s, desde=%s, hasta=%s, facturaID=%s, nota=%s
                WHERE codigo=%s AND guiaID=%s
            """, datos)
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Seguimiento actualizado.")
            self.cargar_seguimientos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar seguimiento: {str(e)}")

    def eliminar_seguimiento(self):
        try:
            codigo = self.inputCodigo.text()
            guia_id = int(self.inputGuiaID.text())
            self.cursor.execute("DELETE FROM Seguimientos WHERE codigo = %s AND guiaID = %s", (codigo, guia_id))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Seguimiento eliminado.")
            self.cargar_seguimientos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar seguimiento: {str(e)}")

    def buscar_seguimiento(self):
        texto = self.inputBuscar.text()
        self.tablaSeguimientos.setRowCount(0)
        consulta = """
            SELECT * FROM Seguimientos
            WHERE codigo LIKE %s OR cliente LIKE %s OR obra LIKE %s OR estado LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,)*4)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaSeguimientos.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaSeguimientos.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputCodigo.setText(self.tablaSeguimientos.item(row, 0).text())
        self.inputFecha.setText(self.tablaSeguimientos.item(row, 1).text())
        self.inputEstado.setText(self.tablaSeguimientos.item(row, 2).text())
        self.inputCliente.setText(self.tablaSeguimientos.item(row, 3).text())
        self.inputObra.setText(self.tablaSeguimientos.item(row, 4).text())
        self.inputFechaEntrega.setText(self.tablaSeguimientos.item(row, 5).text())
        self.inputDias.setText(self.tablaSeguimientos.item(row, 6).text())
        self.inputDesde.setText(self.tablaSeguimientos.item(row, 7).text())
        self.inputHasta.setText(self.tablaSeguimientos.item(row, 8).text())
        self.inputGuiaID.setText(self.tablaSeguimientos.item(row, 9).text())
        self.inputFacturaID.setText(self.tablaSeguimientos.item(row, 10).text())
        self.inputNota.setPlainText(self.tablaSeguimientos.item(row, 11).text())

    def limpiar_campos(self):
        self.inputCodigo.clear()
        self.inputFecha.clear()
        self.inputEstado.clear()
        self.inputCliente.clear()
        self.inputObra.clear()
        self.inputFechaEntrega.clear()
        self.inputDias.clear()
        self.inputDesde.clear()
        self.inputHasta.clear()
        self.inputGuiaID.clear()
        self.inputFacturaID.clear()
        self.inputNota.clear()
        self.inputBuscar.clear()
