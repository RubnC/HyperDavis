#!/usr/bin/python3
# -*- coding: utf-8 -*-



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDir, Qt
from spectral import *
import matplotlib
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QSplitter, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QStyleFactory, QGridLayout, QSpacerItem, QDockWidget, QListWidget, QSlider, QCheckBox
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt

global img, nbands, label


class  MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        #self.wid()
       
        
    def initUI(self):  

        global label
        #layout = QHBoxLayout()
        self.items = QDockWidget("Images", self)
        self.listWidget = QListWidget()
        #self.listWidget.addItem("item1")
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        #self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        #self.listWidget.itemSelectionChanged.triggered.connect(print("nuevo"))
        label = QLabel(self)
        self.setCentralWidget(label)


        
        self.console = QDockWidget("Output Console", self)
        self.textConsole = QTextEdit()
        self.textConsole.setEnabled(False)
        self.textConsole.setText("#HyperDavis output: ")
        self.console.setWidget(self.textConsole)
        self.console.setFloating(False)
        #self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, self.console)
        

        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openAction = QAction(QIcon('./icons/open.png'), 'Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.load)  

        self.FAKEcolorAction = QAction(QIcon('./icons/rgb.png'), 'FAKE color Bands', self)
        self.FAKEcolorAction.setShortcut('Ctrl+R')
        self.FAKEcolorAction.setStatusTip('FAKE color Bands')
        self.FAKEcolorAction.triggered.connect(self.FAKE) 
        self.FAKEcolorAction.setEnabled(False)
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
        self.zoominAction.triggered.connect(self.zoomin) 
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
        toolsMenu.addAction(self.FAKEcolorAction)
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
        toolbar1.addAction(self.FAKEcolorAction)
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
        global img, nbands, label
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath())
        img = open_image(fileName)  
        #nbands = img.shape
        nbands = len(img[1, 1])
        #print (nbands)
        #print(img.read_band(0))
        #print (len(img.read_band(0)))
        #imshow(img.read_band(0), title="image1", cmap='gray')

        rgb = get_rgb(img.read_band(0))
        rgb2 = rgb*255
        #print (rgb)
        #print (len(rgb))
        #print (rgb2)
        #print (rgb2[0][0][0])

        image = QtGui.QImage(len(rgb), len(rgb), 5)

        for x in range(len(rgb2)):
            for y in range(len(rgb2)):
                onColor = QtGui.qRgb(rgb2[y][x][0], rgb2[y][x][0], rgb2[y][x][0])
                image.setPixel(x, y, onColor)

        #image.scaled(290, 290, Qt.KeepAspectRatio)
        pp = QtGui.QPixmap.fromImage(image)
        self.lbl = label
        self.lbl.setPixmap(pp)

        
        self.lbl.show()
        self.zoominAction.setEnabled(True)
        self.zoomoutAction.setEnabled(True)
        self.normAction.setEnabled(True)
        #pixmap = QPixmap("join.png")
        #img = pixmap.toImage()
        #self.label=label.setPixmap(pixmap)

    







        #view_indexed(img.read_band(0))

        #print (img.shape)
        #view = imshow(img, (29, 19, 9), title=fileName)
        #view.show()
        
        text="#The image " + fileName + " has been loaded."
        self.textConsole.append(text)
        datos=str(img)
        self.textConsole.append(datos)
        self.listWidget.addItem(fileName)
        self.FAKEcolorAction.setEnabled(True)
        

        


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



    def FAKE(self):     

       self.dialog = FAKEcolorWindow(self)
       #self.dialog.show()
    def zoomin(self):
        print("holiiiii")
        
        
class FAKEcolorWindow(QMainWindow):
    def __init__(self, parent=None):
        super(FAKEcolorWindow, self).__init__(parent)

        self.FAKEcolorUI()

    def FAKEcolorUI(self):
        #self.btn = QPushButton('Dialog', self)
        #self.btn.move(20, 20)
        #self.btn.clicked.connect(self.showDialog)
        
        #self.le = QLineEdit(self)
        #self.le.move(130, 22)
        global nbands
        self.nbands = nbands-1

        cb = QCheckBox('Red', self)
        cb.move(20, 20)
        cb.toggle()
        cb.stateChanged.connect(self.on)
        cb1 = QCheckBox('Blue', self)
        cb1.move(20, 40)
        cb1.toggle()
        cb1.stateChanged.connect(self.on1)
        cb2 = QCheckBox('Green', self)
        cb2.move(20, 60)
        cb2.toggle()
        cb2.stateChanged.connect(self.on2)

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(120, 20, 230, 30)
        self.sld.setMinimum(0)
        self.sld.setMaximum(self.nbands)

        self.label = QLabel(self)
        self.label.setText("0")
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(0)
        self.sld1.setMaximum(self.nbands)
        self.label1 = QLabel(self)
        self.label1.setText("0")
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)

        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setFocusPolicy(Qt.NoFocus)
        self.sld2.setGeometry(120, 60, 230, 30)
        self.sld2.setMinimum(0)
        self.sld2.setMaximum(self.nbands)
        self.label2 = QLabel(self)
        self.label2.setText("0")
        self.sld2.valueChanged.connect(self.valuechange2)
        self.label2.setGeometry(370, 60, 80, 30)


        self.btn = QPushButton('Ok', self)
        self.btn.move(100, 100)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(200, 100)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.FAKEcolor)
        self.btn.clicked.connect(self.close)

        
        #self.le.adjustSize()
        self.setWindowTitle('FAKE color Bands Selector')
        self.setFixedSize(400, 150)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def on(self, state):
      
        if state == Qt.Checked:
            self.sld.setEnabled(True)
        else:
            self.sld.setEnabled(False)

    def on1(self, state):
      
        if state == Qt.Checked:
            self.sld1.setEnabled(True)
        else:
            self.sld1.setEnabled(False)
    def on2(self, state):
      
        if state == Qt.Checked:
            self.sld2.setEnabled(True)
        else:
            self.sld2.setEnabled(False)

    def valuechange(self):
        size = self.sld.value()
        self.label.setText(str(size))

    def valuechange1(self):
        size = self.sld1.value()
        self.label1.setText(str(size))

    def valuechange2(self):
        size = self.sld2.value()
        self.label2.setText(str(size))
    def FAKEcolor(self):
        print("RGBimage")
        global img
        self.img=img
        imshow(img, (self.sld.value(), self.sld1.value(), self.sld2.value()), title="image1")
        self.close
    def itmSelected(self):
        print ("holiiiiii")


        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())