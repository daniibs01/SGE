# Form implementation generated from reading ui file '.\crm.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_crm(object):
    def setupUi(self, crm):
        crm.setObjectName("crm")
        crm.resize(835, 581)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(crm.sizePolicy().hasHeightForWidth())
        crm.setSizePolicy(sizePolicy)
        crm.setMinimumSize(QtCore.QSize(835, 581))
        crm.setMaximumSize(QtCore.QSize(835, 581))
        self.centralwidget = QtWidgets.QWidget(parent=crm)
        self.centralwidget.setObjectName("centralwidget")
        self.lineApellidos = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineApellidos.setGeometry(QtCore.QRect(166, 99, 133, 31))
        self.lineApellidos.setObjectName("lineApellidos")
        self.btnVolver = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnVolver.setGeometry(QtCore.QRect(700, 460, 121, 71))
        self.btnVolver.setObjectName("btnVolver")
        self.lineEmail = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEmail.setGeometry(QtCore.QRect(313, 99, 133, 31))
        self.lineEmail.setObjectName("lineEmail")
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(606, 99, 133, 31))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.btnAgregar = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnAgregar.setGeometry(QtCore.QRect(540, 10, 111, 61))
        self.btnAgregar.setObjectName("btnAgregar")
        self.btnEliminar = QtWidgets.QPushButton(parent=self.centralwidget)
        self.btnEliminar.setGeometry(QtCore.QRect(700, 10, 111, 61))
        self.btnEliminar.setObjectName("btnEliminar")
        self.lineTelefono = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineTelefono.setGeometry(QtCore.QRect(459, 99, 133, 31))
        self.lineTelefono.setObjectName("lineTelefono")
        self.tableWidget = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.tableWidget.setGeometry(QtCore.QRect(30, 180, 641, 351))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        self.lineNombre = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.lineNombre.setGeometry(QtCore.QRect(20, 99, 133, 31))
        self.lineNombre.setObjectName("lineNombre")
        crm.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(parent=crm)
        self.toolBar.setObjectName("toolBar")
        crm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.retranslateUi(crm)
        QtCore.QMetaObject.connectSlotsByName(crm)

    def retranslateUi(self, crm):
        _translate = QtCore.QCoreApplication.translate
        crm.setWindowTitle(_translate("crm", "CRM"))
        self.lineApellidos.setPlaceholderText(_translate("crm", "Apellidos"))
        self.btnVolver.setText(_translate("crm", "Volver"))
        self.lineEmail.setPlaceholderText(_translate("crm", "Email"))
        self.lineEdit_4.setPlaceholderText(_translate("crm", "Empresa"))
        self.btnAgregar.setText(_translate("crm", "Agregar Cliente"))
        self.btnEliminar.setText(_translate("crm", "Eliminar Clientes"))
        self.lineTelefono.setPlaceholderText(_translate("crm", "Teléfono"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("crm", "ID"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("crm", "Nombre"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("crm", "Apellidos"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("crm", "Email"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("crm", "Teléfono"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("crm", "Empresa"))
        self.lineNombre.setPlaceholderText(_translate("crm", "Nombre"))
        self.toolBar.setWindowTitle(_translate("crm", "toolBar"))
