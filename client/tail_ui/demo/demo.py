from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import * 
from PyQt5.QtWidgets import *
import time
import sys

class EmittingStream(QtCore.QObject):  
        textWritten = QtCore.pyqtSignal(str)  #定义一个发送str的信号
        def write(self, data):
            self.textWritten.emit(str(data)) 

class BackendThread(QThread):
     # 通过类成员对象定义信号
    update_date = pyqtSignal(str)

     # 处理业务逻辑
    def run(self):
        while True:
            data = QDateTime.currentDateTime()
            currTime = data.toString("yyyy-MM-dd hh:mm:ss")
            self.update_date.emit( str(currTime) * 5 )
            time.sleep(0.2)
            
    def loghub(self):
        pass

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(531, 648)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("C:/Users/aabgiilln/Desktop/服务日志.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralWidget)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout.addWidget(self.pushButton_2, 0, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(self.centralWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 1, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(self.centralWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout.addWidget(self.pushButton, 1, 2, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(self.centralWidget)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 3)
        MainWindow.setCentralWidget(self.centralWidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionRun = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("C:/Users/aabgiilln/Desktop/运行中.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRun.setIcon(icon1)
        self.actionRun.setObjectName("actionRun")
        self.actionPause = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("C:/Users/aabgiilln/Desktop/播放-暂停.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionPause.setIcon(icon2)
        self.actionPause.setObjectName("actionPause")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("C:/Users/aabgiilln/Desktop/退出 (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionQuit.setIcon(icon3)
        self.actionQuit.setObjectName("actionQuit")
        self.toolBar.addAction(self.actionRun)
        self.toolBar.addAction(self.actionPause)
        self.toolBar.addAction(self.actionQuit)
        
        #下面将输出重定向到textEdit中
        sys.stdout = EmittingStream(textWritten=self.handleDisplay)  
        sys.stderr = EmittingStream(textWritten=self.handleDisplay)
        
        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close) # 给按钮绑定slot -->close()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "实时日志"))
        self.label.setText(_translate("MainWindow", "服务器IP"))
        self.pushButton_2.setText(_translate("MainWindow", "开始"))
        self.label_2.setText(_translate("MainWindow", "服务密码"))
        self.pushButton.setText(_translate("MainWindow", "退出"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionRun.setText(_translate("MainWindow", "Run"))
        self.actionPause.setText(_translate("MainWindow", "Pause"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        
    def initUI(self):
          # 创建线程
        self.backend = BackendThread()
          # 连接信号
        self.backend.update_date.connect(self.handleDisplay)
          # 开始线程
        self.backend.start()

    # 将当前时间输出到文本框
    def handleDisplay(self, data):
        
        cursor = self.textEdit.textCursor()  
        cursor.movePosition(QtGui.QTextCursor.End)
        # self.textEdit.setText(data)
        cursor.insertText(data + '\n')  
        self.textEdit.setTextCursor(cursor)  
        self.textEdit.ensureCursorVisible()

if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    win = Ui_MainWindow()
    win.setupUi(MainWindow)
    win.initUI()
    MainWindow.show()
    sys.exit(app.exec_())
