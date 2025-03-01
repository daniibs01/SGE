import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QInputDialog, QDialog, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt, QDate
import sqlite3
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from PyQt6.QtWidgets import QFileDialog
import os
from g_inicio import Ui_MainWindow
from g_menu import Ui_menuPrincipal  # Importar la clase del menú
from g_crm import Ui_crm #Importo la ventana del crm
from g_inventario import Ui_inventario #Importamos la ventana del inventario
from g_empleados import Ui_Empleados #Importamos la ventana de empleados
from g_TPV import Ui_TPV #Importamos la ventana del TPV
from g_Contabilidad import Ui_Contabilidad #Importamos la ventana de contabilidad
from g_Proyecto import Ui_proyectos #Importamos la ventana de proyectos

#Clase proyectos
class Proyectos(QMainWindow, Ui_proyectos):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        self.btnVolverProyecto.clicked.connect(self.volver_menu)
        self.btnAgregar.clicked.connect(self.agregar_proyecto)
        self.cargar_proyectos()
        self.btnEliminar.clicked.connect(self.eliminar_proyecto)
        self.btnEditar.clicked.connect(self.editar_proyecto)
          
    def editar_proyecto(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            id = self.tableWidget.item(selected_row, 0).text()
            estado = self.tableWidget.item(selected_row, 3).text()
            
            estado, ok = QInputDialog.getItem(self, "Editar Estado", "Estado del proyecto:", ["No comenzado", "En progreso", "Finalizado"], 0, False)
            
            if ok:
                sql = f'''UPDATE proyectos SET estado = ? WHERE id = ?'''
                self.cursor.execute(sql, (estado, id))
                self.conn.commit()
                self.tableWidget.setItem(selected_row, 3, QTableWidgetItem(estado))
                QMessageBox.information(self, "Éxito", "Proyecto actualizado correctamente")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un proyecto para editar")
        
    def eliminar_proyecto(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            id = self.tableWidget.item(selected_row, 0).text()
            
            sql = f'''DELETE FROM proyectos WHERE id = {id}'''
            self.cursor.execute(sql)
            self.conn.commit()
            self.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Éxito", "Proyecto eliminado correctamente")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un proyecto para eliminar")
        
    def agregar_proyecto(self):
        proyecto = self.lineAgregarProyecto.text()
        descripcion = self.lineDescripcionProyecto.text()
        estado = self.comboBox.currentText()
        
        if proyecto:
            try:
                self.cursor.execute("INSERT INTO proyectos (proyecto, descripcion, estado) VALUES (?, ?, ?)", (proyecto, descripcion, estado))
                self.conn.commit()
                self.cargar_proyectos()
                QMessageBox.information(self, "Éxito", "Proyecto agregado correctamente")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Error al insertar en la base de datos: {e}")
        else:
            QMessageBox.warning(self, "Error", "El nombre del proyecto es requerido")
        
    def cargar_proyectos(self):
        try:
            self.cursor.execute("SELECT id, proyecto, descripcion, estado FROM proyectos")
            proyectos = self.cursor.fetchall()
            self.tableWidget.setRowCount(0)
            for row_number, row_data in enumerate(proyectos):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")
 
    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show()
        self.close()

#Clase contabilidad
class contabilidad(QMainWindow, Ui_Contabilidad):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        self.btnVolver.clicked.connect(self.volver_menu)
        self.cargar_ventas()
        self.totalIngresos = 0.0
    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show()
        self.close()
    
    def cargar_ventas(self):
        try:
            self.cursor.execute("SELECT id, cliente, fecha, total FROM ventas")
            ventas = self.cursor.fetchall()
        
            self.tableContabilidad.setRowCount(0)  # Limpiamos la tabla antes de cargar los datos para que no aparezcan datos antiguos
        
            for row_number, row_data in enumerate(ventas):
                self.tableContabilidad.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableContabilidad.setItem(row_number, column_number, QTableWidgetItem(str(data)))
                    self.totalIngresos = sum(float(row[3]) for row in ventas)
                    self.lcdTotal.display(self.totalIngresos)
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")

#Clase TPV
class TPV(QMainWindow, Ui_TPV):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        self.cargar_stock()
        self.total_compra = 0.0  # Atributo para almacenar el total de la compra
        self.metodo_pago = ""
        self.tableInventario.itemDoubleClicked.connect(self.seleccionar_producto)
        self.btnVolver.clicked.connect(self.volver_menu)
        self.btnEliminarLinea.clicked.connect(self.eliminar_producto)  # Conectar el botón de eliminar
        self.btnCobrar.clicked.connect(self.cobrar)  # Conectar el botón de cobrar
        self.btnSeleccionar.clicked.connect(self.seleccionar_cliente)

    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show() 
        self.close()

    def cargar_stock(self):
        try:
            self.cursor.execute("SELECT nombre_producto, unidades_productos, precio_producto FROM inventario") #El 0 indica nombre de producto, el 1 indica las unidades y el 2 el precio
            productos = self.cursor.fetchall()
        
            self.tableInventario.setRowCount(0)  # Limpiamos la tabla antes de cargar los datos para que no aparezcan datos antiguos
        
            for row_number, row_data in enumerate(productos):
                self.tableInventario.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableInventario.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")

    def seleccionar_producto(self, item):
        row = item.row()
        nombre_producto = self.tableInventario.item(row, 0).text()  # Seleccionamos el nombre del producto
        unidades_disponibles = int(self.tableInventario.item(row, 1).text())  # Seleccionamos las unidades disponibles
        precio_producto = float(self.tableInventario.item(row, 2).text())  # Seleccionamos el precio del producto
        # Hacemos que nos mande el mensaje de cuantas unidades queremos seleccionar
        cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"¿Cuántas unidades de {nombre_producto} quieres?", 1, 1, unidades_disponibles)
    
    # El ok es una variable que he creado para que si es "Ok" inserte en el tableWidget los datos
        if ok:
            total = cantidad * precio_producto
            row_count = self.tableTicket.rowCount()
            self.tableTicket.insertRow(row_count)
            self.tableTicket.setItem(row_count, 0, QTableWidgetItem(nombre_producto))
            self.tableTicket.setItem(row_count, 1, QTableWidgetItem(str(cantidad)))
            self.tableTicket.setItem(row_count, 2, QTableWidgetItem(f"{precio_producto:.2f}"))
            self.tableTicket.setItem(row_count, 3, QTableWidgetItem(f"{total:.2f}"))
        
        # Actualizar el total de la compra
            self.total_compra += total
            self.lcdTotalCompra.display(self.total_compra)
         
    def eliminar_producto(self):
        selected_row = self.tableTicket.currentRow()
        if selected_row != -1:
            nombre_producto = self.tableTicket.item(selected_row, 0).text()
            cantidad_actual = int(self.tableTicket.item(selected_row, 1).text())
            precio_producto = float(self.tableTicket.item(selected_row, 2).text())
            
            cantidad, ok = QInputDialog.getInt(self, "Cantidad", f"¿Cuántas unidades de {nombre_producto} quieres eliminar?", 1, 1, cantidad_actual)
            
            if ok:
                if cantidad >= cantidad_actual:
                    total = cantidad_actual * precio_producto
                    self.tableTicket.removeRow(selected_row)
                else:
                    total = cantidad * precio_producto
                    nueva_cantidad = cantidad_actual - cantidad
                    self.tableTicket.setItem(selected_row, 1, QTableWidgetItem(str(nueva_cantidad)))
                    nuevo_total = nueva_cantidad * precio_producto
                    self.tableTicket.setItem(selected_row, 3, QTableWidgetItem(f"{nuevo_total:.2f}"))
                
                # Actualizar el total de la compra
                self.total_compra -= total
                self.lcdTotalCompra.display(self.total_compra)
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar")            

    def seleccionar_cliente(self):
        try:
            self.cursor.execute("SELECT nombre, apellidos, email, empresa FROM clientes")
            clientes = self.cursor.fetchall()
            clientes_list = [f"{cliente[0]} {cliente[1]}" for cliente in clientes]
            cliente, ok = QInputDialog.getItem(self, "Seleccionar Cliente", "Seleccione un cliente:", clientes_list, 0, False)
            if ok and cliente:
                self.cliente_seleccionado = cliente
                nombre, apellidos, email, empresa = next(c for c in clientes if f"{c[0]} {c[1]}" == cliente)
                self.lineNombre.setText(nombre)
                self.lineEmpresa.setText(apellidos)
                self.lineEmal.setText(email)
                self.lineEmpresa.setText(empresa)
                QMessageBox.information(self, "Cliente Seleccionado", f"Cliente seleccionado: {cliente}")
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")

    def generar_factura(self):
    # Verificar si se ha seleccionado un cliente
        if not hasattr(self, 'cliente_seleccionado') or not self.cliente_seleccionado:
            QMessageBox.warning(self, "Error", "No hay ningún cliente seleccionado")
            return

    # Crear la carpeta FACTURAS si no existe
        if not os.path.exists("FACTURAS"):
            os.makedirs("FACTURAS")

    # Contar el número de archivos de factura existentes en el directorio
        factura_num = 1
        while os.path.exists(f"FACTURAS/factura{factura_num:02d}.pdf"):
            factura_num += 1

        file_path = f"FACTURAS/factura{factura_num:02d}.pdf"  # Generar un nombre único para el archivo PDF
        c = canvas.Canvas(file_path, pagesize=letter)
        c.drawString(100, 750, f"Factura {factura_num:02d}")
        c.drawString(100, 735, f"Cliente: {self.cliente_seleccionado}")
        c.drawString(100, 720, f"Total: {self.total_compra:.2f} €")
        c.drawString(100, 705, f"Fecha: {QDate.currentDate().toString('dd-MM-yyyy')}")
        c.drawString(100, 690, f"Metodo de pago: {self.metodo_pago}")

    # Crear la tabla de productos
        data = [["Producto", "Cantidad", "Precio Unitario", "Total"]]
        for row in range(self.tableTicket.rowCount()):
            nombre_producto = self.tableTicket.item(row, 0).text()
            cantidad = self.tableTicket.item(row, 1).text()
            precio = self.tableTicket.item(row, 2).text()
            total = self.tableTicket.item(row, 3).text()
            data.append([nombre_producto, cantidad, precio, total])

    # Crear la tabla en el PDF
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))

    # Añadir la tabla al PDF
        table.wrapOn(c, 100, 600)
        table.drawOn(c, 100, 600 - table._height)

    # Guardar el PDF
        c.save()
        QMessageBox.information(self, "Factura Generada", f"La factura ha sido guardada en {file_path}")
   
    def generar_ticket(self):
        ticket_window = QDialog(self)
        ticket_window.setWindowTitle("Ticket")
        ticket_window.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()

    # Añadir los datos de la tableTicket
        for row in range(self.tableTicket.rowCount()):
            nombre_producto = self.tableTicket.item(row, 0).text()
            cantidad = self.tableTicket.item(row, 1).text()
            precio = self.tableTicket.item(row, 2).text()
            total = self.tableTicket.item(row, 3).text()
            layout.addWidget(QLabel(f"{nombre_producto} - {cantidad} x {precio} € = {total} €"))

    # Añadir el total de la compra
            
        layout.addWidget(QLabel(f"Total: {self.total_compra:.2f} €"))

        ticket_window.setLayout(layout)
        ticket_window.exec()
        
    #Método para cobrar
    def cobrar(self):
    # Verificar si se ha seleccionado un cliente
        if not hasattr(self, 'cliente_seleccionado') or not self.cliente_seleccionado:
            QMessageBox.warning(self, "Error", "No hay ningún cliente seleccionado")
            return

    # Comprobamos si el total de la compra es mayor a 999€ y en ese caso bloqueamos el pago en efectivo
        if self.total_compra > 999:
            QMessageBox.warning(self, "Aviso", "El total de la compra es mayor a 999€. Solo se puede pagar con tarjeta.")
            self.metodo_pago = "Tarjeta"
        else:
        # Primer diálogo para seleccionar el método de pago
            self.metodo_pago, ok = QInputDialog.getItem(self, "Método de Pago", "Seleccione el método de pago:", ["Tarjeta", "Efectivo"], 0, False)
            if not ok:
                return  # Si el usuario cancela, no hacemos nada

    # Segundo diálogo para seleccionar el tipo de comprobante
        tipo_comprobante, ok = QInputDialog.getItem(self, "Tipo de Comprobante", "Seleccione el tipo de comprobante:", ["Ticket", "Factura"], 0, False)
        if ok and tipo_comprobante:
            QMessageBox.information(self, "Cobro", f"Pago con {self.metodo_pago}.\nTipo de comprobante: {tipo_comprobante}")
        # Actualizar el inventario
            for row in range(self.tableTicket.rowCount()):
                nombre_producto = self.tableTicket.item(row, 0).text()
                cantidad_comprada = int(self.tableTicket.item(row, 1).text())
                self.cursor.execute("UPDATE inventario SET unidades_productos = unidades_productos - ? WHERE nombre_producto = ?", (cantidad_comprada, nombre_producto))
            self.conn.commit()
            self.cargar_stock()  # Recargar el inventario para reflejar los cambios

            self.registrar_venta()  # Registrar la venta en la base de datos

            if tipo_comprobante == "Factura":
                self.generar_factura()
            elif tipo_comprobante == "Ticket":
                self.generar_ticket()

        # Limpiar la tabla de ticket
            self.tableTicket.setRowCount(0)
            self.total_compra = 0.0
            self.lcdTotalCompra.display(self.total_compra)
            
    def registrar_venta(self):
        fecha = QDate.currentDate().toString("dd-MM-yyyy")
        try:
            self.cursor.execute("INSERT INTO ventas (cliente, fecha, total) VALUES (?, ?, ?)",
                                (self.cliente_seleccionado, fecha, self.total_compra))
            self.conn.commit()
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al registrar la venta: {e}")


#Clase empleados
class Empleados(QMainWindow, Ui_Empleados):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        
        self.btnAgregarEmpleado.clicked.connect(self.agregar_empleado)
        self.btnEliminar.clicked.connect(self.eliminar_clientes)
        self.btnVolver.clicked.connect(self.volver_menu)
        self.cargar_empleados()  # IMPORTANTE PARA QUE CARGUEN LOS DATOS DE LA BBDD Y MOSTRARLOS AL ABRIR LA PAGINA
    
    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show()
        self.close()
    
    def agregar_empleado(self):
        nombre = self.lineNombre.text()
        apellidos = self.lineApellidosEmpleado.text()
        email = self.lineEmailEmpleado.text()
        telefono = self.lineTelefonoEmpleado.text()
        clientesA = self.lineClienteEmpleado.text()
        
        if nombre and apellidos and email and telefono and clientesA:
            try:
                self.cursor.execute("INSERT INTO empleados (nombre_empleado, apellido_empleado, email_empleado, telefono_empleado, cliente_asociado) VALUES (?, ?, ?, ?, ?)",
                                    (nombre, apellidos, email, telefono, clientesA))
                self.conn.commit()
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(nombre))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(apellidos))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(email))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(telefono))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(clientesA))
                QMessageBox.information(self, "Éxito", "Empleado introducido correctamente")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Error al insertar en la base de datos: {e}")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")

    def cargar_empleados(self):
        try:
            self.cursor.execute("SELECT id_empleado, nombre_empleado, apellido_empleado, email_empleado, telefono_empleado, cliente_asociado FROM empleados")
            empleados = self.cursor.fetchall()
        
            self.tableWidget.setRowCount(0)  # Limpiamos la tabla antes de cargar los datos para que no aparezcan datos antiguos
        
            for row_number, row_data in enumerate(empleados):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")
            
    def eliminar_clientes(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            id = self.tableWidget.item(selected_row, 0).text()
            
            sql = f'''DELETE FROM empleados WHERE id_empleado = {id}'''
            self.cursor.execute(sql)
            self.conn.commit()
            self.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Éxito", "Empleado eliminado correctamente")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un empleado para eliminar")
            
#Clase inventario
class inventario(QMainWindow, Ui_inventario):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        self.cargar_productos()  # IMPORTANTE PARA QUE CARGUEN LOS DATOS DE LA BBDD Y MOSTRARLOS AL ABRIR LA PAGINA
        self.btnAgregar.clicked.connect(self.agregar_producto)
        self.btnVolver.clicked.connect(self.volver_menu)
        self.btnEliminar.clicked.connect(self.eliminar_productos)

    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show()
        self.close()
        
    def agregar_producto(self):
    #Obtenemos los valores de los campos 
        nombre_producto = self.lineProducto.text()
        precio_producto = self.linePrecio.text()
        unidades_productos = self.lineStock.text()
        
        if nombre_producto and precio_producto and unidades_productos:
            try:
                self.cursor.execute("INSERT INTO inventario (nombre_producto, precio_producto, unidades_productos) VALUES (?, ?, ?)",
                                    (nombre_producto, precio_producto, unidades_productos))
                self.conn.commit()
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(nombre_producto))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(precio_producto))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(unidades_productos))
                QMessageBox.information(self, "Éxito", "Producto introducido correctamente")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Error al insertar en la base de datos: {e}")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")
        
    def cargar_productos(self):
        try:
            self.cursor.execute("SELECT id_productos, nombre_producto, precio_producto, unidades_productos FROM inventario")
            productos = self.cursor.fetchall()
        
            self.tableWidget.setRowCount(0)  # Limpiamos la tabla antes de cargar los datos para que no aparezcan datos antiguos
        
            for row_number, row_data in enumerate(productos):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")
        
        
    def eliminar_productos(self):
        selected_row = self.tableWidget.currentRow()
        if selected_row != -1:
            id = self.tableWidget.item(selected_row, 0).text()
            
            sql = f'''DELETE FROM inventario WHERE id_productos = {id}'''
            self.cursor.execute(sql)
            self.conn.commit()
            self.tableWidget.removeRow(selected_row)
            QMessageBox.information(self, "Éxito", "Producto eliminado correctamente")
        else:
            QMessageBox.warning(self, "Error", "Seleccione un producto para eliminar")    
            
#Clase crm
class crm (QMainWindow, Ui_crm):
    def __init__(self, rol):
        super().__init__()
        self.setupUi(self)
        self.rol = rol
        self.conn = sqlite3.connect('Gestor.db')
        self.cursor = self.conn.cursor()
        self.cargar_clientes()  # Cargar los clientes al inicializar la ventana


        #Inicializamos los botones
        self.btnVolver.clicked.connect(self.volver_menu)
        self.btnAgregar.clicked.connect(self.agregar_cliente)
        self.btnEliminar.clicked.connect(self.eliminar_clientes)

    #Creamos el boton para volver al menu principal
    def volver_menu(self):
        self.abrir_menu = menu(self.rol)
        self.abrir_menu.show()
        self.close()

    #Creamos el agregar clientes a la tabla de crm
    def agregar_cliente(self):
        nombre = self.lineNombre.text()
        apellido = self.lineApellidos.text()
        email = self.lineEmail.text()
        telefono = self.lineTelefono.text()
        empresa = self.lineEdit_4.text()

        if nombre and apellido and email and telefono:
            try:
                self.cursor.execute("INSERT INTO clientes (nombre, apellidos, email, telefono, empresa) VALUES (?, ?, ?, ?, ?)",
                                    (nombre, apellido, email, telefono, empresa))
                self.conn.commit()
                self.tableWidget.insertRow(self.tableWidget.rowCount())
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 1, QTableWidgetItem(nombre))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 2, QTableWidgetItem(apellido))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 3, QTableWidgetItem(email))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 4, QTableWidgetItem(telefono))
                self.tableWidget.setItem(self.tableWidget.rowCount() - 1, 5, QTableWidgetItem(empresa))
                QMessageBox.information(self, "Éxito", "Cliente introducido correctamente")
            except sqlite3.Error as e:
                QMessageBox.warning(self, "Error", f"Error al insertar en la base de datos: {e}")
        else:
            QMessageBox.warning(self, "Error", "Todos los campos son requeridos")

    #Vamos a cargar los clientes de la BBDD para poder verlos
    def cargar_clientes(self):
        try:
            self.cursor.execute("SELECT id,nombre, apellidos, email, telefono, empresa FROM clientes")
            clientes = self.cursor.fetchall()
        
            self.tableWidget.setRowCount(0)  # Limpiar la tabla antes de cargar los datos
        
            for row_number, row_data in enumerate(clientes):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except sqlite3.Error as e:
            QMessageBox.warning(self, "Error", f"Error al cargar los datos de la base de datos: {e}")
        
    #Vamos a crear el boton de eliminar la fila 
    def eliminar_clientes(self):
          #PARA ELIMINAR SELECCIONAR EL ID
            selected_row = self.tableWidget.currentRow()
            if selected_row != -1:
                id = self.tableWidget.item(selected_row, 0).text()
                
                sql = f'''DELETE FROM clientes WHERE id = {id}'''
                self.cursor.execute(sql)
                self.conn.commit()
                self.tableWidget.removeRow(selected_row)
                QMessageBox.information(self, "Éxito", "Cliente eliminado correctamente")
            else:
                QMessageBox.warning(self, "Error", "Seleccione un cliente para eliminar")
            
        
#Menu principal de la aplicacion
class menu(QMainWindow, Ui_menuPrincipal):
    def __init__(self, rol):
        self.rol = rol
        super().__init__()
        self.setupUi(self)
        
        # Inicializamos los botones
        self.btnCrm.clicked.connect(self.abrir_crm)
        self.btnInventario.clicked.connect(self.abrir_inventario)
        self.btnEmpleados.clicked.connect(self.abrir_empleados)
        self.btnTPV.clicked.connect(self.abrir_tpv)
        self.btnContabilidad.clicked.connect(self.abrir_contabilidad)
        self.btnProyecto.clicked.connect(self.abrir_proyectos)
        
        # Habilitar o deshabilitar botones según el rol
        #El empleado usuario es una prueba, si se cambia o se elimina el usuario todo sigue perfectamente
        if self.rol == "Usuario":
            self.btnEmpleados.setEnabled(False)
            self.btnInventario.setEnabled(False)

        #El rol de empleado solo tiene acceso a TPV
        elif self.rol == "Empleado":
            self.btnCrm.setHidden(True)
            self.btnContabilidad.setHidden(True)
            self.btnProyecto.setHidden(True)
            self.btnInventario.setHidden(True)
            self.btnInventario.setHidden(True)
            self.btnEmpleados.setHidden(True)
        #El rol de comercial tiene acceso solo a CRM
        elif self.rol == "Comercial":
            self.btnTPV.setHidden(True)
            self.btnContabilidad.setHidden(True)
            self.btnProyecto.setHidden(True)
            self.btnInventario.setHidden(True)
            self.btnInventario.setHidden(True)
            self.btnEmpleados.setHidden(True)
        #El rol de ejecutivo tiene acceso a todo menos a TPV
        elif self.rol == "Ejecutivo":
            self.btnTPV.setHidden(True)
            
    def abrir_proyectos(self):
        self.abrir_proyectos_win = Proyectos(self.rol)
        self.abrir_proyectos_win.show()
        self.close()
            
    def abrir_crm(self):
        self.abrir_crm_win = crm(self.rol)
        self.abrir_crm_win.show()
        self.close()
    
    def abrir_inventario(self):
        self.abrir_inventario_win = inventario(self.rol)
        self.abrir_inventario_win.show()
        self.close()

    def abrir_tpv(self):
        self.abrir_tpv_win = TPV(self.rol)
        self.abrir_tpv_win.show()
        self.close()
        
    def abrir_contabilidad(self):
        self.abrir_contabilidad_win = contabilidad(self.rol)
        self.abrir_contabilidad_win.show()
        self.close()
        
    def abrir_empleados(self):
        self.abrir_empleados_win = Empleados(self.rol)
        self.abrir_empleados_win.show()
        self.close()

#Creamos el inicio de sesion
class inicioSesion(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conn = sqlite3.connect('gestor.db')
        self.cursor = self.conn.cursor()
        #inicializamos botones        
        self.pushButton.clicked.connect(self.abrir_menu)

    def verificar_credenciales(self, usuario, contrasena):
        self.cursor.execute("SELECT administrador FROM usuarios WHERE usuario=? AND contrasena=?", (usuario, contrasena))
        result = self.cursor.fetchone()
        if result:
            return result[0]  # Devuelve el rol del usuario
        return None   
    
    def abrir_menu(self):
        usuario = self.lineEdit.text()
        contrasena = self.lineEdit_2.text()
        rol = self.verificar_credenciales(usuario, contrasena)
        if rol:
            # Crear una instancia del menú y pasar el rol del usuario
            self.ventana_menu = menu(rol)
            self.ventana_menu.show()

            # Cerrar la ventana actual (opcional)
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos")
        
if __name__ == "__main__":
    app=QApplication(sys.argv)
    window = inicioSesion()
    window.show()
    sys.exit(app.exec())
