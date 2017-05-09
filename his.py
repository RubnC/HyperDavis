#!/usr/bin/python3
# -*- coding: utf-8 -*-



import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDir, Qt
from spectral import *
import matplotlib
from scipy import misc

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QSplitter, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QStyleFactory, QGridLayout, QSpacerItem, QDockWidget, QListWidget, QSlider, QCheckBox, QComboBox, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm

global img, nbands, label


class  MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        #self.wid()
       
        
    def initUI(self):  

        global label
        self.layout = QHBoxLayout()
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
        self.textConsole.moveCursor(QtGui.QTextCursor.End)
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

        self.FAKEcolorAction = QAction(QIcon('./icons/rgb.png'), 'False color Bands', self)
        self.FAKEcolorAction.setShortcut('Ctrl+R')
        self.FAKEcolorAction.setStatusTip('False color Bands')
        self.FAKEcolorAction.triggered.connect(self.FAKE) 
        self.FAKEcolorAction.setEnabled(False)

        self.combo=QComboBox()
        self.combo.setEnabled(False)

        #saveAction = QAction(QIcon('./icons/save.png'), 'Save', self)
        #saveAction.setShortcut('Ctrl+S')
        #saveAction.setStatusTip('Save')
        #saveAction.triggered.connect(self.save)  
        #saveAction.setEnabled(True)
     

        newAction = QAction(QIcon('./icons/new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')

        #self.zoominAction = QAction(QIcon('./icons/zoomin.png'), 'Zoom in',  self)
        #self.zoominAction.setShortcut('Ctrl++')
        #self.zoominAction.setStatusTip('Zoom in')
        #self.zoominAction.triggered.connect(self.zoomin) 
        #self.zoominAction.setEnabled(False)
 

        #self.normAction = QAction(QIcon('./icons/norm.png'), 'Original Size',  self)
        #self.normAction.setShortcut('Ctrl+N')
        #self.normAction.setStatusTip('Original Size')
        #self.normAction.setEnabled(False)

        #self.zoomoutAction = QAction(QIcon('./icons/zoomout.png'), 'Zoom out', self)
        #self.zoomoutAction.setShortcut('Ctrl+-')
        #self.zoomoutAction.setStatusTip('./icons/Zoom out')
        #self.zoomoutAction.setEnabled(False)

        #self.cursorAction = QAction(QIcon('./icons/cursor.png'), 'Cursor', self)
        #self.cursorAction.setShortcut('Ctrl+N')
        #self.cursorAction.setStatusTip('Cursor')
        #self.cursorAction.setEnabled(False)

        self.gridAction = QAction(QIcon('./icons/grid.png'), 'Grid', self)
        self.gridAction.setShortcut('Ctrl+G')
        self.gridAction.setStatusTip('Grid')
        self.gridAction.setEnabled(False)

        self.rectangleAction = QAction(QIcon('./icons/rectangle.png'), 'Crop', self)
        self.rectangleAction.setShortcut('Ctrl+D')
        self.rectangleAction.setStatusTip('Crop')
        self.rectangleAction.setEnabled(False)

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
        #EditMenu.addAction(self.zoominAction)
        #EditMenu.addAction(self.normAction)
        #EditMenu.addAction(self.zoomoutAction)
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
        
        self.toolbar1 = self.addToolBar('Tools')
        #toolbar1.addAction(self.zoominAction)
        #toolbar1.addAction(self.normAction)
        #toolbar1.addAction(self.zoomoutAction)
        self.toolbar1.addWidget(self.combo)
        
        #toolbar1.addAction(self.cursorAction)
        self.toolbar1.addAction(self.rectangleAction)
        self.toolbar1.addAction(self.FAKEcolorAction)
        
        self.toolbar1.addAction(self.gridAction)
        self.toolbar1.addAction(self.filterinAction)
        self.toolbar1.addAction(self.filterClearAction)
        self.toolbar1.addAction(self.joinAction)

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


        rgb = get_rgb(img.read_band(0))
        
        #plt.imshow(rgb)
        #plt.show()

        self.main_frame = QWidget()
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)               
        self.axes.axis((0,len(rgb),len(rgb),0))


        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        
        self.canvas.draw()
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)         # the matplotlib canvas

        self.layout.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(self.layout)
        self.setCentralWidget(self.main_frame)
        
        #self.axes.plot(self.x, self.y, 'ro')
        self.axes.imshow(rgb)
        #self.axes.plot([1,2,3])
        self.canvas.draw()



        for i in range(nbands):
            text="Band " + str(i)
            self.combo.addItem(text)



        #1DESDE AQUI 
        #self.main_frame = QWidget()
        #self.fig = Figure((5.0, 4.0), dpi=100)
        #self.fig.add_subplot(111)
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)
        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        

        #vbox = QVBoxLayout()
        #vbox.addWidget(self.canvas)         # the matplotlib canvas
        #vbox.addWidget(self.mpl_toolbar)
        #self.main_frame.setLayout(vbox)
        #self.setCentralWidget(self.main_frame)
        #HASTA AQUÍ AÑADE GRAFICA

       


        #2DESDE AQUÍ 
        #image = QtGui.QImage(len(rgb), len(rgb), 5)

        #for i in range(nbands):
        #    text="Band " + str(i)
        #    self.combo.addItem(text)

        #for x in range(len(rgb2)):
        #    for y in range(len(rgb2)):
                
        #        onColor = QtGui.qRgb(rgb2[y][x][0], rgb2[y][x][0], rgb2[y][x][0])
        #        image.setPixel(x, y, onColor)
        
        
        self.combo.activated[str].connect(self.comboChanged) 
        #pp = QtGui.QPixmap.fromImage(image)
        #self.lbl = label
        #self.lbl.setPixmap(pp)
        #self.zoominAction.setEnabled(True)
        #self.zoomoutAction.setEnabled(True)
        #self.normAction.setEnabled(True)
        self.FAKEcolorAction.setEnabled(True)
        self.combo.setEnabled(True)
        self.rectangleAction.setEnabled(True)
        #2HASTA AQUÍ FUNCIONA REPERESENTAR IMAGEN


    







        #view_indexed(img.read_band(0))
        #print (img.shape)
        #view = imshow(img, (29, 19, 9), title=fileName)
        #view.show()
        
        text="#The image " + fileName + " has been loaded."
        self.textConsole.append(text)
        datos=str(img)
        self.textConsole.append(datos)
        self.listWidget.addItem(fileName)
        
        

        


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



    def comboChanged(self, text):
        

        rgb = get_rgb(img.read_band(int(text.strip("Band"))))
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)
        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        #self.canvas.draw()
        
        self.layout.addWidget(self.canvas)         # the matplotlib canvas
        self.layout.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(self.layout)
        self.setCentralWidget(self.main_frame)
        
        #self.axes.plot(self.x, self.y, 'ro')
        ax=self.axes.imshow(rgb)
        #self.axes.plot([1,2,3])

        self.canvas.draw()
        self.textConsole.append(text + " loaded.")


        
        
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




        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Red")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 40)
        self.lbl1.setText("Blue")

        self.lbl2 = QLabel(self)
        self.lbl2.move(20, 60)
        self.lbl2.setText("Green")

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
        self.setWindowTitle('False color Bands Selector')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(400, 150)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
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
    def FAKEcolor(self):
        print("RGBimage")
        global img
        self.img=img
        imshow(img, (self.sld.value(), self.sld1.value(), self.sld2.value()), title="False color image")
        self.close
    def itmSelected(self):
        print ("holiiiiii")


        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())