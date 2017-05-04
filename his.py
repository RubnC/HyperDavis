#!/usr/bin/python3
# -*- coding: utf-8 -*-



import sys
from PyQt5.QtCore import QDir, Qt
from spectral import *
import matplotlib
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QSplitter, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QStyleFactory, QGridLayout, QSpacerItem, QDockWidget, QListWidget, QSlider
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt



class  MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        #self.wid()
       
        
    def initUI(self):  

        #layout = QHBoxLayout()
        self.items = QDockWidget("Images", self)
        self.listWidget = QListWidget()
        #self.listWidget.addItem("item1")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        #self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        
        self.console = QDockWidget("Output Console", self)
        self.textConsole = QTextEdit()
        self.textConsole.setEnabled(False)
        self.textConsole.setText("#HyperDavis output: ")
        self.console.setWidget(self.textConsole)
        self.console.setFloating(False)
        self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.console)
        

        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openAction = QAction(QIcon('./icons/open.png'), 'Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.load)  

        self.RGBAction = QAction(QIcon('./icons/rgb.png'), 'RGB Bands', self)
        self.RGBAction.setShortcut('Ctrl+R')
        self.RGBAction.setStatusTip('RGB Bands')
        self.RGBAction.triggered.connect(self.RGB) 
        self.RGBAction.setEnabled(False)
        #saveAction = QAction(QIcon('./icons/save.png'), 'Save', self)
        #saveAction.setShortcut('Ctrl+S')
        #saveAction.setStatusTip('Save')
        #saveAction.triggered.connect(self.save)  
        #saveAction.setEnabled(True)
     

        newAction = QAction(QIcon('./icons/new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')

        self.zoominAction = QAction(QIcon('./icons/zoomin.png'), 'Zoom in',  self)
        self.zoominAction.setShortcut('Ctrl++')
        self.zoominAction.setStatusTip('Zoom in')
        self.zoominAction.setEnabled(False)
 

        self.normAction = QAction(QIcon('./icons/norm.png'), 'Original Size',  self)
        #self.normAction.setShortcut('Ctrl+N')
        self.normAction.setStatusTip('Original Size')
        self.normAction.setEnabled(False)

        self.zoomoutAction = QAction(QIcon('./icons/zoomout.png'), 'Zoom out', self)
        #self.zoomoutAction.setShortcut('Ctrl+-')
        self.zoomoutAction.setStatusTip('./icons/Zoom out')
        self.zoomoutAction.setEnabled(False)

        self.cursorAction = QAction(QIcon('./icons/cursor.png'), 'Cursor', self)
        #self.cursorAction.setShortcut('Ctrl+N')
        self.cursorAction.setStatusTip('Cursor')
        self.cursorAction.setEnabled(False)

        self.gridAction = QAction(QIcon('./icons/grid.png'), 'Grid', self)
        self.gridAction.setShortcut('Ctrl+G')
        self.gridAction.setStatusTip('Grid')
        self.gridAction.setEnabled(False)

        self.polylineAction = QAction(QIcon('./icons/polyline.png'), 'Draw Polyline', self)
        self.polylineAction.setShortcut('Ctrl+D')
        self.polylineAction.setStatusTip('Draw Polyline')
        self.polylineAction.setEnabled(False)

        self.analyzeAction = QAction(QIcon('./icons/analyze.png'), 'Analyze', self)
        self.analyzeAction.setShortcut('Ctrl+A')
        self.analyzeAction.setStatusTip('Analyze')
        self.analyzeAction.setEnabled(False)

        self.joinAction = QAction(QIcon('./icons/join.png'), 'Join', self)
        self.joinAction.setShortcut('Ctrl+J')
        self.joinAction.setStatusTip('Join')
        self.joinAction.setEnabled(False)

        self.filterinAction = QAction(QIcon('./icons/filter.png'), 'Filters', self)
        #filterinAction.setShortcut('Ctrl+F')
        self.filterinAction.setStatusTip('Filters')
        self.filterinAction.setEnabled(False)

        self.filterClearAction = QAction(QIcon('./icons/ClearFilters.png'), 'Clear Filters', self)
        self.filterClearAction.setShortcut('Ctrl+C')
        self.filterClearAction.setStatusTip('Clear Filters')
        self.filterClearAction.setEnabled(False)


        self.aboutAction = QAction('About', self)
        self.aboutAction.setStatusTip('About')
        

        #self.saveAction = QAction('Save', self)
        
        
        self.statusBar()

        menubar = self.menuBar()
        #sino en mac no funciona
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction('Open Recent')
        #fileMenu.addAction(self.saveAction)
        fileMenu.addAction('Save as...')
        fileMenu.addAction('Export as PDF')
        fileMenu.addSeparator()

        EditMenu = menubar.addMenu('Edit')
        EditMenu.addAction(self.zoominAction)
        EditMenu.addAction(self.normAction)
        EditMenu.addAction(self.zoomoutAction)
        EditMenu.addSeparator()

        fileMenu.addAction(exitAction)
              
        viewMenu = menubar.addMenu('View')
        viewMenu.addAction('Charts')
        #viewMenu.addAction(fitwindowAction)

        toolsMenu = menubar.addMenu('Tools')
        toolsMenu.addAction(self.RGBAction)
        toolsMenu.addAction('Filter')
        windowMenu = menubar.addMenu('Window')
        action5 = windowMenu.addAction('Charts')
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction('Tutorial')
        helpMenu.addAction('Report a bug')
        helpMenu.addAction('Manual')
        helpMenu.addAction(self.aboutAction)

#TOOLBAR
        toolbar = self.addToolBar('Open')

        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        
        toolbar1 = self.addToolBar('Tools')
        toolbar1.addAction(self.zoominAction)
        toolbar1.addAction(self.normAction)
        toolbar1.addAction(self.zoomoutAction)
        toolbar1.addAction(self.cursorAction)
        toolbar1.addAction(self.RGBAction)
        toolbar1.addAction(self.polylineAction)
        toolbar1.addAction(self.gridAction)
        toolbar1.addAction(self.filterinAction)
        toolbar1.addAction(self.filterClearAction)
        toolbar1.addAction(self.joinAction)

        #icono 
        toolbar2 = self.addToolBar('Exit')
        toolbar2.addAction(exitAction)
        
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle('HyperDavis')    
        self.showMaximized()
        #Icono app
        self.setWindowIcon(QIcon('join.png')) 
        #imagen
        # Create widget
        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)
      
        #self.resize(pixmap.width(),pixmap.height())
        self.show()

    def load(self):
        #fileName, _ = QFileDialog.getOpenFileName(self,"Open Files", '/desktop',"Images (*.*)")
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        #fname = QFileDialog.getOpenFileName(self, 'Open file', '/desktop')
        #label = QLabel(self)
        #self.setCentralWidget(label)
        #pixmap = QPixmap(fileName)
        #img = pixmap.toImage()
        #label.setPixmap(pixmap)
        #label.resize(pixmap.width(),pixmap.height())
        #label.mousePressEvent = self.getPos
        #c = img.pixel(290,290)
        #QColor(c).setRgb(255, 49, 3)
        #colors = QColor(c).getRgbF()
        #print (colors)
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        img = open_image(fileName)  
        #print (img.shape)
        #view = imshow(img, (29, 19, 9), title=fileName)
        #view.show()
        
        text="#The image " + fileName + " has been loaded."
        self.textConsole.append(text)
        datos=str(img)
        self.textConsole.append(datos)
        self.listWidget.addItem(fileName)
        self.RGBAction.setEnabled(True)

        print (img)

        #view_cube(img, bands=[29, 19, 9])
        #if fileName:
            #image = QImage(fileName)
            #self.zoominAction.setEnabled(True)
            #self.zoomoutAction.setEnabled(True)
            #self.normAction.setEnabled(True)
            
            #if image.isNull():
            #    QMessageBox.information(self, "Image Viewer",
            #            "Cannot load %s." % fileName)
            #    return

            #self.imageLabel.setPixmap(QPixmap.fromImage(image))
            #self.imageLabel.mousePressEvent = self.getPos
            #c = image.pixel(290,290)
            #QColor(c).setRgb(255, 49, 3)
            #colors = QColor(c).getRgbF()
            #print (colors)
            #self.scaleFactor = 1.0
            #self.printAct.setEnabled(True)
            #self.fitwindowAction.setEnabled(True)
            #self.updateActions()
            #self.imageLabel.adjustSize()

        
    #def print_(self):
     ##   dialog = QPrintDialog(self.printer, self)
      #  if dialog.exec_():
       #     painter = QPainter(self.printer)
        #    rect = painter.viewport()
         #   size = self.imageLabel.pixmap().size()
          #  size.scale(rect.size(), Qt.KeepAspectRatio)
           # painter.setViewport(rect.x(), rect.y(), size.width(), size.height())
            #painter.setWindow(self.imageLabel.pixmap().rect())
            #painter.drawPixmap(0, 0, self.imageLabel.pixmap())

    #def fitToWindow(self):
    #    fitToWindow = self.fitToWindowAct.isChecked()
    #    self.scrollArea.setWidgetResizable(fitToWindow)
    #    if not fitToWindow:
    #        self.normalSize()
    #
    #    self.updateActions()

    def RGB(self):     

       self.dialog = RGBwindow(self)
       #self.dialog.show()
        
        
class RGBwindow(QMainWindow):
    def __init__(self, parent=None):
        super(RGBwindow, self).__init__(parent)

        self.RGBUI()

    def RGBUI(self):
        #self.btn = QPushButton('Dialog', self)
        #self.btn.move(20, 20)
        #self.btn.clicked.connect(self.showDialog)
        
        #self.le = QLineEdit(self)
        #self.le.move(130, 22)

        lbl1 = QLabel("Red:",self)
        lbl1.move(20, 20)
        lbl2 = QLabel("Green:",self)
        lbl2.move(20, 40)
        lbl3 = QLabel("Blue:",self)
        lbl3.move(20, 60)

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(120, 20, 230, 30)
        self.sld.setMinimum(0)
        self.sld.setMaximum(200)
        self.label = QLabel(self)
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(0)
        self.sld1.setMaximum(200)
        self.label1 = QLabel(self)
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)

        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setFocusPolicy(Qt.NoFocus)
        self.sld2.setGeometry(120, 60, 230, 30)
        self.sld2.setMinimum(0)
        self.sld2.setMaximum(200)
        self.label2 = QLabel(self)
        self.sld2.valueChanged.connect(self.valuechange2)
        self.label2.setGeometry(370, 60, 80, 30)


        self.btn = QPushButton('Ok', self)
        self.btn.move(100, 100)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(200, 100)
        self.btn1.clicked.connect(self.close)
        self.adjustSize()
        
        #self.le.adjustSize()
        self.setWindowTitle('Bands Selector')
        self.show()

    def valuechange(self):
      size = self.sld.value()
      self.label.setText(str(size))

    def valuechange1(self):
      size = self.sld1.value()
      self.label1.setText(str(size))

    def valuechange2(self):
      size = self.sld2.value()
      self.label2.setText(str(size))
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())