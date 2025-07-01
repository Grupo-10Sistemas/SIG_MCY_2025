import sys
import pymysql
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.uic import loadUi

# Importar las clases CRUD individuales
from clientes_crud import ClientesVentana
from equipos_crud import EquiposVentana
from facturas_crud import FacturasVentana
from cotizaciones_crud import CotizacionesVentana
from ordenestrabajo_crud import OrdenesTrabajoVentana
from seguimientos_crud import SeguimientosVentana

class MainWindow(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("main_window.ui", self)
        self.connection = None
        self.main_connect.clicked.connect(self.connect_to_database)

    def connect_to_database(self):
        host = self.main_text_host.text()
        user = self.main_text_user.text()
        password = self.main_text_pass.text()
        try:
            self.connection = pymysql.connect(
                host=host,
                user=user,
                password=password,
                database='EmpresaDB'
            )
            QMessageBox.information(self, "Conexión Exitosa", "Conectado a EmpresaDB.")
            self.menu = MenuVentana(self, self.connection)
            self.menu.show()
            self.hide()
        except pymysql.MySQLError as e:
            QMessageBox.critical(self, "Error de Conexión", f"No se pudo conectar:\n{str(e)}")

class MenuVentana(QDialog):
    def __init__(self, main_window, connection):
        super().__init__()
        loadUi("menu.ui", self)
        self.connection = connection
        self.main_window = main_window
        self.ir_menu.clicked.connect(self.abrir_tabla)
        self.salir_menu.clicked.connect(self.salir)
        self.cargar_tablas()

    def cargar_tablas(self):
        self.lista_tablas.clear()
        tablas = ["Clientes", "Equipos", "Facturas", "Cotizaciones", "OrdenesTrabajo", "Seguimientos"]
        for tabla in tablas:
            self.lista_tablas.addItem(tabla)

    def abrir_tabla(self):
        tabla = self.lista_tablas.currentText()
        ventanas = {
            "Clientes": ClientesVentana,
            "Equipos": EquiposVentana,
            "Facturas": FacturasVentana,
            "Cotizaciones": CotizacionesVentana,
            "OrdenesTrabajo": OrdenesTrabajoVentana,
            "Seguimientos": SeguimientosVentana
        }
        if tabla in ventanas:
            self.ventana = ventanas[tabla](self.connection)
            self.ventana.exec_()
        else:
            QMessageBox.warning(self, "Advertencia", "Tabla no válida seleccionada.")

    def salir(self):
        self.connection.close()
        QApplication.quit()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    sys.exit(app.exec_())