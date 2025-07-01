# 📦 SIG MCY 2025 – Sistema de Gestión Interna para Maquinarias MCY SpA

Este proyecto corresponde al desarrollo de un sistema de gestión administrativa para la empresa **Maquinarias MCY SpA**, como parte del trabajo final del curso **ICN292 – Sistemas de Información para la Gestión** (UTFSM, 2025-1).

El sistema fue desarrollado en **Python con PyQt5** y utiliza una base de datos **MySQL** para gestionar las operaciones clave del negocio, como el control de clientes, facturación, seguimiento de equipos, entre otros.

---

## 🖥️ Funcionalidades Principales

- **Conexión a base de datos MySQL**
- Gestión completa de:
  - Clientes
  - Equipos
  - Facturas
  - Cotizaciones
  - Órdenes de Trabajo
  - Seguimientos
- Funciones CRUD:
  - Agregar, buscar, editar, eliminar, visualizar registros
- Interfaz gráfica intuitiva hecha con Qt Designer (`.ui`)
- Modularidad y escalabilidad del sistema
- Código limpio y documentado

---

## ⚙️ Requisitos

- Python 3.8 o superior
- MySQL Server (con usuario y base de datos creada)
- Bibliotecas necesarias:

```bash
pip install PyQt5 pymysql
```

---

## 🧱 Estructura del Proyecto

```
SIG_MCY_2025/
│
├── main.py                   # Archivo principal del sistema
├── main_window.ui            # Interfaz de conexión
├── menu.ui                   # Menú principal
│
├── clientes.ui               # UI de módulo Clientes
├── clientes_crud.py          # Lógica Clientes
├── equipos.ui
├── equipos_crud.py
├── facturas.ui
├── facturas_crud.py
├── cotizaciones.ui
├── cotizaciones_crud.py
├── ordenestrabajo.ui
├── ordenestrabajo_crud.py
├── seguimientos.ui
├── seguimientos_crud.py
│
├── basedatos.sql             # Script de creación de la base de datos
├── README.md                 # Este archivo
└── video_demo.mp4            # Video de funcionamiento del sistema (opcional)
```

---

## 🏁 Cómo Ejecutar el Proyecto

1. **Clonar o descargar el repositorio**

```bash
git clone https://github.com/Grupo-10Sistemas/SIG_MCY_2025.git
cd SIG_MCY_2025
```

2. **Configurar la base de datos MySQL**

- Ejecutar el archivo `basedatos.sql` en tu servidor MySQL (por ejemplo, usando MySQL Workbench o consola):

```sql
SOURCE basedatos.sql;
```

3. **Ejecutar el sistema**

```bash
python main.py
```

4. **Ingresar datos de conexión**
- Host: `localhost`
- Usuario: `root` (o el que hayas configurado)
- Contraseña: `tu_clave`
- Base de datos: `EmpresaDB` (ya se conecta automáticamente)




