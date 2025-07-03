
from PyQt5.QtWidgets import QDialog, QMessageBox, QTableWidgetItem
from PyQt5.uic import loadUi

class ClientesVentana(QDialog):
    def __init__(self, connection):
        super().__init__()
        loadUi("clientes.ui", self)
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.btnAgregar.clicked.connect(self.agregar_cliente)
        self.btnEditar.clicked.connect(self.editar_cliente)
        self.btnEliminar.clicked.connect(self.eliminar_cliente)
        self.btnBuscar.clicked.connect(self.buscar_cliente)
        self.tablaClientes.cellClicked.connect(self.cargar_datos_formulario)

        self.cargar_clientes()

    def cargar_clientes(self):
        self.tablaClientes.setRowCount(0)
        self.cursor.execute("SELECT * FROM Clientes")
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaClientes.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaClientes.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def agregar_cliente(self):
        rut = self.inputRut.text()
        nombre = self.inputNombre.text()
        direccion = self.inputDireccion.text()
        email = self.inputEmail.text()
        telefono = self.inputTelefono.text()

        if not rut or not nombre:
            QMessageBox.warning(self, "Advertencia", "RUT y Nombre son obligatorios.")
            return

        try:
            self.cursor.execute("INSERT INTO Clientes VALUES (%s, %s, %s, %s, %s)",
                                (rut, nombre, direccion, email, telefono))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cliente agregado correctamente.")
            self.cargar_clientes()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al agregar cliente: {str(e)}")

    def editar_cliente(self):
        rut = self.inputRut.text()
        nombre = self.inputNombre.text()
        direccion = self.inputDireccion.text()
        email = self.inputEmail.text()
        telefono = self.inputTelefono.text()

        try:
            self.cursor.execute("""
                UPDATE Clientes SET nombre=%s, direccion=%s, email=%s, telefono=%s
                WHERE rutCliente=%s
            """, (nombre, direccion, email, telefono, rut))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cliente actualizado.")
            self.cargar_clientes()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al editar cliente: {str(e)}")

    def eliminar_cliente(self):
        rut = self.inputRut.text()
        if not rut:
            QMessageBox.warning(self, "Advertencia", "Seleccione un cliente para eliminar.")
            return
        try:
            self.cursor.execute("DELETE FROM Clientes WHERE rutCliente = %s", (rut,))
            self.connection.commit()
            QMessageBox.information(self, "Éxito", "Cliente eliminado.")
            self.cargar_clientes()
            self.limpiar_campos()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al eliminar cliente: {str(e)}")

    def buscar_cliente(self):
        texto = self.inputBuscar.text()
        self.tablaClientes.setRowCount(0)
        consulta = """
            SELECT * FROM Clientes
            WHERE rutCliente LIKE %s OR nombre LIKE %s OR direccion LIKE %s OR email LIKE %s OR telefono LIKE %s
        """
        wildcard = f"%{texto}%"
        self.cursor.execute(consulta, (wildcard,)*5)
        for row_num, row_data in enumerate(self.cursor.fetchall()):
            self.tablaClientes.insertRow(row_num)
            for col_num, data in enumerate(row_data):
                self.tablaClientes.setItem(row_num, col_num, QTableWidgetItem(str(data)))

    def cargar_datos_formulario(self, row, column):
        self.inputRut.setText(self.tablaClientes.item(row, 0).text())
        self.inputNombre.setText(self.tablaClientes.item(row, 1).text())
        self.inputDireccion.setText(self.tablaClientes.item(row, 2).text())
        self.inputEmail.setText(self.tablaClientes.item(row, 3).text())
        self.inputTelefono.setText(self.tablaClientes.item(row, 4).text())

    def limpiar_campos(self):
        self.inputRut.clear()
        self.inputNombre.clear()
        self.inputDireccion.clear()
        self.inputEmail.clear()
        self.inputTelefono.clear()
