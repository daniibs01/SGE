# Proyecto de Gestión Empresarial

Este proyecto es una aplicación de gestión empresarial desarrollada con PyQt6 y SQLite. La aplicación permite gestionar diferentes aspectos de una empresa, como proyectos, contabilidad, TPV (Terminal Punto de Venta), empleados, inventario y CRM (Customer Relationship Management).

## Requisitos

- Python 3.x
- PyQt6
- SQLite3
- ReportLab

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala las dependencias necesarias utilizando `pip`:

```bash
pip install PyQt6 sqlite3 reportlab
```
## Estructura del Proyecto
main.py: Archivo principal que contiene la lógica de la aplicación.
g_inicio.py: Archivo generado por PyQt6 Designer para la interfaz de inicio de sesión.
g_menu.py: Archivo generado por PyQt6 Designer para la interfaz del menú principal.
g_crm.py: Archivo generado por PyQt6 Designer para la interfaz del CRM.
g_inventario.py: Archivo generado por PyQt6 Designer para la interfaz del inventario.
g_empleados.py: Archivo generado por PyQt6 Designer para la interfaz de empleados.
g_TPV.py: Archivo generado por PyQt6 Designer para la interfaz del TPV.
g_Contabilidad.py: Archivo generado por PyQt6 Designer para la interfaz de contabilidad.
g_Proyecto.py: Archivo generado por PyQt6 Designer para la interfaz de proyectos.

## Funcionalidades

## Inicio de Sesión
- Verificación de credenciales de usuario.
- Redirección al menú principal según el rol del usuario.
  
# Menú Principal
1.- Acceso a diferentes módulos según el rol del usuario:
- CRM
- Inventario
- Empleados
- TPV
- Contabilidad
- Proyectos
  
## CRM
- Agregar, eliminar y visualizar clientes.
- Gestión de información de clientes.
  
## Inventario
- Agregar, eliminar y visualizar productos.
- Gestión de stock y precios de productos.
  
# Empleados
- Agregar, eliminar y visualizar empleados.
- Gestión de información de empleados.
  
## TPV
- Selección de productos y clientes.
- Generación de tickets y facturas.
- Registro de ventas y actualización de inventario.
  
## Contabilidad
- Visualización de ventas.
- Cálculo de ingresos totales.
  
## Proyectos
- Agregar, eliminar y editar proyectos.
- Gestión de estados de proyectos (No comenzado, En progreso, Finalizado).
  
## Uso
1.- Ejecuta el .exe para iniciar la aplicación.
2.- Inicia sesión con tus credenciales.
3.- Navega por los diferentes módulos según tu rol y gestiona la información necesaria.

Contacto
Para cualquier consulta o sugerencia, por favor contacta a becerrasotoda@gmail.com.
