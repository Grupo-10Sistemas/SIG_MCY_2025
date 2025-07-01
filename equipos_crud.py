
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class EquiposVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("equipos.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_equipo)
        self.btnEditar.clicked.connect(self.editar_equipo)
        self.btnEliminar.clicked.connect(self.eliminar_equipo)
        self.btnBuscar.clicked.connect(self.buscar_equipo)
        self.tablaEquipos.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_equipos()

    def cargar_equipos(self):
        self.tablaEquipos.setRowCount(0)
        self.cursor.execute("SELECT * FROM Equipos")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaEquipos.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaEquipos.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_equipo(self):
        codigo = self.inputCodigo.text()
        anio = self.inputAnio.text()
        modelo = self.inputModelo.text()
        marca = self.inputMarca.text()
        estado = self.inputEstado.currentText()

        if not codigo or not anio:
            QMessageBox.warning(self, "Advertencia", "Código y año son obligatorios.")
            return

        try:
            self.cursor.execute("INSERT INTO Equipos VALUES (%s, %s, %s, %s, %s)",
                                (codigo, anio, modelo, marca, estado))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Equipo agregado correctamente.")
            self.cargar_equipos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar equipo: {str(e)}")

    def editar_equipo(self):
        codigo = self.inputCodigo.text()
        anio = self.inputAnio.text()
        modelo = self.inputModelo.text()
        marca = self.inputMarca.text()
        estado = self.inputEstado.currentText()

        try:
            self.cursor.execute("""
                UPDATE Equipos SET anio=%s, modelo=%s, marca=%s, estado=%s
                WHERE codigo=%s
            """, (anio, modelo, marca, estado, codigo))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Equipo actualizado.")
            self.cargar_equipos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar equipo: {str(e)}")

    def eliminar_equipo(self):
        codigo = self.inputCodigo.text()
        if not codigo:
            QMessageBox.warning(self, "Advertencia", "Seleccione un equipo para eliminar.")
            return
        try:
            self.cursor.execute("DELETE FROM Equipos WHERE codigo = %s", (codigo,))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Equipo eliminado.")
            self.cargar_equipos()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar equipo: {str(e)}")

    def buscar_equipo(self):
        texto = self.inputBuscar.text()
        self.tablaEquipos.setRowCount(0)
        consulta = """
            SELECT * FROM Equipos
            WHERE codigo LIKE %s OR modelo LIKE %s OR marca LIKE %s OR estado LIKE %s OR anio LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,)*5)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaEquipos.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaEquipos.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputCodigo.setText(self.tablaEquipos.item(row, 0).text())
        self.inputAnio.setText(self.tablaEquipos.item(row, 1).text())
        self.inputModelo.setText(self.tablaEquipos.item(row, 2).text())
        self.inputMarca.setText(self.tablaEquipos.item(row, 3).text())
        self.inputEstado.setCurrentText(self.tablaEquipos.item(row, 4).text())

    def limpiar_campos(self):
        self.inputCodigo.clear()
        self.inputAnio.clear()
        self.inputModelo.clear()
        self.inputMarca.clear()
        self.inputEstado.setCurrentIndex(0)
        self.inputBuscar.clear()
