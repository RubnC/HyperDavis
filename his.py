#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDir, Qt
from spectral import *
import spectral
from matplotlib import *
from scipy import misc
import numpy as np
import glob
from ximea import xiapi
#hyperspy
from spectral import *
#ENVI Headers
import spectral.io.envi as envi
#aviris headers
import spectral.io.aviris as aviris
#Translate files type
import os
from os.path import expanduser
import shutil
#Library for XML read
import xml.etree.ElementTree as ET
#representación del cubo

#Converse to JSON
import xmltodict
import pprint
import json
import wx

from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QSplitter, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QStyleFactory, QGridLayout, QSpacerItem, QDockWidget, QListWidget, QSlider, QCheckBox, QComboBox, QWidget, QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm

global label
XML = False
JSON = False
HDR = False
BIL = False
BSQ = False
BIP = False
ExportPath = ""
ConversePath = "./"
fileName = ""
fileNameNoExt = "raw"




class  MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        #self.wid()
       
        
    def initUI(self):  

        global label

        self.layout = QHBoxLayout()
        self.items = QDockWidget("Loaded Images", self)
        self.listWidget = QListWidget()
        #self.listWidget.setWindowTitle('PyQT QListwidget Demo')
        self.listWidget.itemClicked.connect(self.Clicked)
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

        self.saveAction = QAction(QIcon('./icons/save.png'), 'Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setStatusTip('Save')
        self.saveAction.triggered.connect(self.save)  
        self.saveAction.setEnabled(False)

        self.ConverseAction = QAction(QIcon('./icons/converse.png'), 'Converse', self)
        self.ConverseAction.setStatusTip('Converse')
        self.ConverseAction.triggered.connect(self.Converse) 
        self.ConverseAction.setEnabled(False)

        self.combo=QComboBox()
        self.combo.setStyleSheet('''
        QComboBox { min-width: 120px; min-height: 40px;}    
''')
        self.combo.setEnabled(False)

        self.FAKEcolorAction = QAction(QIcon('./icons/rgb.png'), 'False color Bands', self)
        self.FAKEcolorAction.setShortcut('Ctrl+F')
        self.FAKEcolorAction.setStatusTip('False color Bands')
        self.FAKEcolorAction.triggered.connect(self.FAKE) 
        self.FAKEcolorAction.setEnabled(False)

        

        self.SignatureAction = QAction(QIcon('./icons/chart3.png'), 'Signature', self)
        self.SignatureAction.setShortcut('Ctrl+E')
        self.SignatureAction.setStatusTip('Spectral Signature')
        self.SignatureAction.triggered.connect(self.Signature) 
        self.SignatureAction.setEnabled(False)

        self.RGBAction = QAction(QIcon('./icons/real.png'), 'Show image', self)
        self.RGBAction.setShortcut('Ctrl+L')
        self.RGBAction.setStatusTip('Show RGB image')
        self.RGBAction.triggered.connect(self.RGB) 
        self.RGBAction.setEnabled(False)
        

        newAction = QAction(QIcon('./icons/new1.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')
        newAction.triggered.connect(self.Capture) 
        newAction.setEnabled(False)


        self.gridAction = QAction(QIcon('./icons/grid.png'), 'Grid', self)
        self.gridAction.setShortcut('Ctrl+G')
        self.gridAction.setStatusTip('Grid')
        self.gridAction.setEnabled(False)

        self.rectangleAction = QAction(QIcon('./icons/rectangle.png'), 'Crop', self)
        self.rectangleAction.setShortcut('Ctrl+T')
        self.rectangleAction.setStatusTip('Crop')
        self.rectangleAction.setEnabled(False)

        self.cropCubeAction = QAction(QIcon('./icons/cropCube.png'), 'Crop Cube', self)
        self.cropCubeAction.setShortcut('Ctrl+Y')
        self.cropCubeAction.setStatusTip('Crop Cube')
        self.cropCubeAction.triggered.connect(self.CropCube) 
        self.cropCubeAction.setEnabled(False)

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

        self.SettingAction = QAction(QIcon('./icons/settings.png'), 'Camera Settings', self)
        #filterinAction.setShortcut('Ctrl+F')
        self.SettingAction.setStatusTip('Settings')
        self.SettingAction.setEnabled(True)

        self.filterClearAction = QAction(QIcon('./icons/ClearFilters.png'), 'Clear Filters', self)
        self.filterClearAction.setShortcut('Ctrl+C')
        self.filterClearAction.setStatusTip('Clear Filters')
        self.filterClearAction.setEnabled(True)


        self.aboutAction = QAction('About', self)
        self.aboutAction.setStatusTip('About')
        
        self.statusBar()

        menubar = self.menuBar()
        #sino en mac no funciona
        menubar.setNativeMenuBar(False)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction('Open Recent')
        fileMenu.addAction(self.saveAction)
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
        toolsMenu.addAction(self.ConverseAction)
        toolsMenu.addAction(self.RGBAction)
        toolsMenu.addAction(self.SignatureAction)
        toolsMenu.addAction(self.filterinAction)
        settingMenu = menubar.addMenu('Settings')
        action5 = settingMenu.addAction(self.SettingAction)
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction('Tutorial')
        helpMenu.addAction('Manual')
        helpMenu.addAction(self.aboutAction)

#TOOLBAR
        toolbar = self.addToolBar('Open')

        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar.addAction(self.saveAction)
 
        self.toolbar1 = self.addToolBar('Tools')
        #toolbar1.addAction(self.zoominAction)
        #toolbar1.addAction(self.normAction)
        #toolbar1.addAction(self.zoomoutAction)
        self.toolbar1.addWidget(self.combo)
        self.toolbar1.addAction(self.RGBAction)
        self.toolbar1.addAction(self.FAKEcolorAction)
        self.toolbar1.addAction(self.SignatureAction)
        #toolbar1.addAction(self.cursorAction)
        self.toolbar1.addAction(self.rectangleAction)
        self.toolbar1.addAction(self.cropCubeAction)
        
        
        #self.toolbar1.addAction(self.gridAction)
        #self.toolbar1.addAction(self.filterinAction)
        #self.toolbar1.addAction(self.filterClearAction)
        #self.toolbar1.addAction(self.joinAction)

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

        global img, label, fileName, fileNameNoExt

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



        #Eliminar archivos anteriores // Hay que buscar la manera de borrar al salir
        #files = glob.glob('./Temp/*')
        #for f in files:
        #    os.remove(f)

        #DESDE AQUÍ DESCOMENTAR
        fileName = ""
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath(), "Hyper Files(*lan *.bin *hdr)")
        #print(fileName)
        
        #ESTE BLOQUE FUNCIONA GUAY
        #fileNameHDR1 = "/Users/ruben/Desktop/PROYECTO/HyperDavis/data/0020-1/raw.hdr"
        #img1= envi.open(fileNameHDR1, "/Users/ruben/Desktop/PROYECTO/HyperDavis/data/0020-1/raw")
        #img3=get_rgb(img1.read_band(0))
        #imshow(img3)
        
        #fileNameHDR = "/Users/ruben/Desktop/PROYECTO/HyperDavis/data/Old/raw.hdr"
        #img= envi.open(fileNameHDR, "/Users/ruben/Desktop/PROYECTO/HyperDavis/data/Old/raw.bin")
        #img2=get_rgb(img.read_band(0))
        #print(img2)
        #imshow(img2)
        if ".lan" in fileName:
            img = open_image(fileName)
            self.represent(fileName)
            img2=get_rgb(img.read_band(0))
            print(img2)
            #imshow(img2)
            with open('your_file.txt', 'w') as f:
                for item in img2:
                    f.write("%s\n" % item)  		    #I can not translate LAN files that I have because they doesn't say wavelength for each band    
        elif ".bin" in fileName:
            fileNameHDR = fileName.replace(".bin" , ".hdr")
            img = envi.open(fileNameHDR, fileName)
            self.represent(fileName)
            img2 = get_rgb(img.read_band(0))
            #print (img2)
            #with open('your_file.txt', 'w') as f:
            #    for item in img2:
            #        f.write("%s\n" % item)
            translate = 'gdal_translate -of ENVI '+fileName+ ' ./Temp/raw.gis'
            os.system(translate)	
        elif ".hdr" in fileName:
            fileNameBin = fileName.replace(".hdr" , "")
            translate = 'gdal_translate -of ENVI '+fileNameBin+ ' ./Temp/raw.gis'
            os.system(translate)
            #imgData = open_image(fileName).load()
            img = envi.open(fileName, fileNameBin)
            img2=get_rgb(img.read_band(0))
            #imshow(img2, title="Band 0 - Gray Scale")
            self.represent(fileNameBin)
            #print(img2)
            
        else:
        	QMessageBox.about(self, "", "Please select a *lan *.bin or *.hdr file to start")
    

    def represent(self, fileName):  
        global nbands, img
        nbands = len(img[1, 1])
        #Show image un RGB bands
        
        self.img=img
        rgb = get_rgb(img.read_band(0))
        
        #DESDE AQUI FUNCIONA
        
        self.main_frame = QWidget()
        #self.items = QDockWidget("Loaded Images", self)
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)               
        #self.axes.axis((0,len(rgb),len(rgb),0))
        self.canvas = FigureCanvas(self.fig)
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.canvas)         # the matplotlib canvas
        self.layout.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(self.layout)
        self.setCentralWidget(self.main_frame)
        self.axes.imshow(rgb, animated=True, origin='lower', aspect='equal')
        self.canvas.draw()
        self.combo.clear()
        count = 1
        #prueba = imshow(img,(426, 166, 125), title="RGB Image")
        

        if ".lan" in fileName:
        	for i in (range(nbands)-1):
       			text="Band "+ str(i)
       			self.combo.addItem(text)
        	##print (band, wlength.strip("nm"))
        	#for subelem in elem:
        	#	print(subelem.text)
        else:
            aux_file= str(fileName.rsplit("/", 1)[1])
            aux_file1= str(aux_file.rsplit(".", 1)[0])
            aux_file_path="./Temp/"+aux_file1+".gis.aux.xml"
            tree = ET.parse(aux_file_path)
            root = tree.getroot()
            for elem in root.findall('PAMRasterBand'):
                wlength =elem.find('Description').text
                band = "Band " + elem.get('band') + " - "
                count += 1
                self.combo.addItem(band + wlength)


        #Hay que modificar para coger las bandas automáticamente
        #print("ESTOOOOS" + str(count))
       	self.combo.removeItem(count-2)
        #DESCOMENTAR EN PROD:
        #save_rgb('./Temp/rgb.jpg', img, [426, 166, 125])	

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
        self.ConverseAction.setEnabled(True)
        self.RGBAction.setEnabled(True)
        self.SignatureAction.setEnabled(True)
        self.combo.setEnabled(True)
        self.rectangleAction.setEnabled(True)
        self.cropCubeAction.setEnabled(True)
        self.saveAction.setEnabled(True)
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

    def CropCube(self):    

       self.dialog = cropCubeWindow(self)
    
    def Converse(self):    

       self.dialog = ConverseWindow(self)
    
    def Capture(self):
        #create instance for first connected camera
        cam = xiapi.Camera()

        #start communication
        #to open specific device, use:
        #cam.open_device_by_SN('41305651')
        #(open by serial number)
        print('Opening first camera...')
        cam.open_device()

        #settings
        cam.set_exposure(10000)
        print('Exposure was set to %i us' %cam.get_exposure())

        #create instance of Image to store image data and metadata
        img = xiapi.Image()

        #start data acquisition
        print('Starting data acquisition...')
        cam.start_acquisition()

        for i in range(10):
            #get data and pass them from camera to img
            cam.get_image(img)

            #get raw data from camera
            #for Python2.x function returns string
            #for Python3.x function returns bytes
            data_raw = img.get_image_data_raw()

            #transform data to list
            data = list(data_raw)

            #print image data and metadata
            print('Image number: ' + str(i))
            print('Image width (pixels):  ' + str(img.width))
            print('Image height (pixels): ' + str(img.height))
            print('First 10 pixels: ' + str(data[:10]))
            print('\n')    

        #stop data acquisition
        print('Stopping acquisition...')
        cam.stop_acquisition()

        #stop communication
        cam.close_device()

        print('Done.')
 
    def Clicked(self,item):
        if self.listWidget.count() > 1:
            reply = QMessageBox.question(self, 'Message',"You are going to open: "+item.text(), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                global img, label
                fileName= item.text()
                if ".lan" in fileName:
                    img = open_image(fileName)
                    self.represent(fileName)   
                elif ".bin" in fileName:
                    fileNameHDR = fileName.replace(".bin" , ".hdr")
                    img = envi.open(fileNameHDR, fileName);
                    self.represent(fileName)        
                else: 
                    fileNameHDR = fileName.replace(".hdr" , ".bin")
                    img = envi.open(fileName, fileNameHDR);
                    self.represent(fileName)
            else:
                print("NO") 
        else:
            print("just one")
      
       #self.dialog.show()
    def RGB(self): 
        global fileName
        prueba = imshow(img,(426, 166, 125), title="RGB Image")

    def Signature(self): 
        global fileName
        #app = wx.App()
        #imgData = open_image(fileName).load() 
        #imgData=view(fileName,(426, 166, 125))  
        #print (imgData)
        #imgData = open_image(fileName).load()
        prueba = imshow(img,(426, 166, 125), title="Click on a pixel to see it's spectral signture ")
        #envi.save_image(FullPathBSQ, imgData, ext="", interleave = 'bsq')
        print (prueba)
        #aquí tenemos que meter la función para leer pixel a pixel.   

    #def zoomin(self):
    #    print("holiiiii")
        #unir confunción para salvar imagen
    def save(self):
     	print("holiiiii")
    def comboChanged(self, text):
        self.layout.addWidget(self.canvas)         # the matplotlib canvas
        self.layout.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(self.layout)
        self.setCentralWidget(self.main_frame)
        if "RGB" in text:
        	prueba = imshow(img,(29, 19, 9))
        	print (prueba)
        else:
        	band=text.split(" - ", 1)[0]
        	band = int(band.replace("Band",""))
        	rgb = get_rgb(img.read_band(int(band)))
        	ax=self.axes.imshow(rgb, animated=True)
        #self.canvas = FigureCanvas(self.fig)
        #self.canvas.setParent(self.main_frame)
        #self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)
        #self.canvas.draw()
        
        #self.axes.plot(self.x, self.y, 'ro')
        #ax=self.axes.imshow(rgb, animated=True)
        
        #self.axes.plot([1,2,3])

        self.canvas.draw()
        self.textConsole.append(text + " loaded.")
        

        
        
class FAKEcolorWindow(QMainWindow):
    def __init__(self, parent=None):
        super(FAKEcolorWindow, self).__init__(parent)

        self.FAKEcolorUI()

    def FAKEcolorUI(self):

        self.nbands = nbands-1
        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Red")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 60)
        self.lbl1.setText("Blue")

        self.lbl2 = QLabel(self)
        self.lbl2.move(20, 40)
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
        self.setWindowTitle('Select which band you want to colour in Red, Green, and Blue')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(500, 150)
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

class cropCubeWindow(QMainWindow):
    def __init__(self, parent=None):
        super(cropCubeWindow, self).__init__(parent)

        self.cropCubeUI()

    def cropCubeUI(self):

        self.nbands = nbands-1
        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Low Band")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 40)
        self.lbl1.setText("High Band")


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

        self.textbox = QLineEdit(self)
        self.textbox.move(110, 80)
        self.textbox.resize(220,25)
        self.textbox.setText("File Name")

        self.btn = QPushButton('Ok', self)
        self.btn.move(120, 115)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(220, 115)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.trimCube)
        self.btn.clicked.connect(self.close)

        #self.le.adjustSize()
        self.setWindowTitle('Select which band range you want to save')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(450, 170)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def valuechange(self):
        size = self.sld.value()
        self.label.setText(str(size))

    def valuechange1(self):
        size = self.sld1.value()
        self.label1.setText(str(size))

    def trimCube(self):
        #data = open_image(fileName).load()
        TrimPath="./"
        fileNameNoExt = self.textbox.text()
        if self.sld.value() > self.sld1.value():
            QMessageBox.about(self, "Error", "The lower band cannot be larger than the upper one")
        else:
            TrimPath = QFileDialog.getExistingDirectory(self, "Open a folder", expanduser("~"), QFileDialog.ShowDirsOnly)
            FinalPath= TrimPath+'/'+fileNameNoExt+'.hdr' 
            print("ESTA ES LA RUTA:"+ FinalPath)            
            cube = img[:, :, self.sld.value():self.sld1.value()]
            envi.save_image(FinalPath, cube, ext="", interleave = 'bil')
            #ahora me tengo que abrir la cabecera y modificarla
            
            QMessageBox.about(self, "", "Done!")
        #imshow(img, (self.sld.value(), self.sld1.value(), self.sld2.value()), title="False color image")
        

    
class ConverseWindow(QMainWindow):
    def __init__(self, parent=None):
        super(ConverseWindow, self).__init__(parent)

        self.ConverseUI()

    def ConverseUI(self):
        
        self.Header = QLabel(self)
        self.Header.setText("Headers:")
        self.Header.setGeometry(30, 20, 80, 30)
        
        self.b = QCheckBox("XML",self)
        self.b.move(50,40)

        self.b1 = QCheckBox("JSON",self)
        self.b1.move(50,60)

        #self.b2 = QCheckBox("HDR",self)
        #self.b2.move(50,60)

        self.Inter = QLabel(self)
        self.Inter.setText("Interleave(HDR+RAW):")
        self.Inter.setGeometry(170, 20, 135, 30)

        self.b3 = QCheckBox("BIL",self)
        self.b3.move(190,40)

        self.b4 = QCheckBox("BSQ",self)
        self.b4.move(190,60)

        self.b5 = QCheckBox("BIP",self)
        self.b5.move(190,80)
        
        self.textbox = QLineEdit(self)
        self.textbox.move(55, 115)
        self.textbox.resize(220,25)
        self.textbox.setText("File Name")

        self.btn = QPushButton('Select Path', self)
        self.btn.move(50, 150)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(180, 150)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.PathToConverse)
        self.btn.clicked.connect(self.close)

        #self.le.adjustSize()
        self.setWindowTitle('HyperEspectral conversion tool')
        self.setFixedSize(330, 210)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        
        self.show()
        self.b.stateChanged.connect(self.clickBoxXML)
        self.b1.stateChanged.connect(self.clickBoxJSON)
        #self.b2.stateChanged.connect(self.clickBoxHDR)
        self.b3.stateChanged.connect(self.clickBoxBIL)
        self.b4.stateChanged.connect(self.clickBoxBSQ)
        self.b5.stateChanged.connect(self.clickBoxBIP)
        self.textbox.textChanged.connect(self.newFileName)

    def newFileName(self, text):
        global fileNameNoExt
        fileNameNoExt = self.textbox.text()

    def clickBoxXML(self, state):
        global  XML
        if state == QtCore.Qt.Checked:
            print('Checked')
            XML = True
            print ("XML"+str(XML))
        else:
            print('Unchecked')
            XML = False

    def clickBoxJSON(self, state):
        global  JSON
        if state == QtCore.Qt.Checked:
            print('Checked')
            JSON = True
        else:
            print('Unchecked')
            JSON = False

    #def clickBoxHDR(self, state):
    #    global  HDR
    #    if state == QtCore.Qt.Checked:
    #        #print('Checked')
    #        HDR = True
    #    else:
    #        #print('Unchecked')
    #        HDR = False
    
    def clickBoxBIL(self, state):
        global  BIL
        if state == QtCore.Qt.Checked:
            #print('Checked')
            BIL = True
        else:
            #print('Unchecked')
            BIL = False

    def clickBoxBIP(self, state):
        global  BIP
        if state == QtCore.Qt.Checked:
            #print('Checked')
            BIP = True
        else:
            #print('Unchecked')
            BIP = False

    def clickBoxBSQ(self, state):
        global  BSQ
        if state == QtCore.Qt.Checked:
            print('Checked')
            BSQ = True
        else:
            #print('Unchecked')
            BSQ = False

    def PathToConverse(self):
        global ConversePath, fileNameNoExt
        ConversePath = QFileDialog.getExistingDirectory(self, "Open a folder", expanduser("~"), QFileDialog.ShowDirsOnly)
        self.Converse()
        print (ConversePath)
        #fileName, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath(), "Hyper Files(*lan *.bin *hdr)")
        self.close
    def Converse(self):
        global fileName, ConversePath, fileNameNoExt
        #imgData = open_image(fileName).load()
        #print("hOLA:" + str(XML) + str(JSON) + str(HDR) + str(BIL) + str(BIP) + str(BSQ))
        #print ("NUESTRO FILENAME:" + str(fileName))
        if XML == True:
            print("Convirtiendo a XML")
            #print("aqui el nombre del fichero" + fileNameNoExt)
            CarpetaXML = ConversePath+'/XML'  
            try:
                # Create target Directory
                os.mkdir(CarpetaXML)
                shutil.copy2('./Temp/raw.gis.aux.xml', CarpetaXML)
                os.rename(CarpetaXML+'/raw.gis.aux.xml',CarpetaXML+'/'+fileNameNoExt+'.xml')

            except FileExistsError:
                #print("already exists")
                shutil.copy2('./Temp/raw.gis.aux.xml', CarpetaXML)
                os.rename(CarpetaXML+'/raw.gis.aux.xml',CarpetaXML+'/'+fileNameNoExt+'.xml')   
        #if JSON == True: 
        #    print("Convirtiendo a JSON")
        #    with open('./Temp/raw.gis.aux.xml') as in_file:
        #        doc = in_file.read()
        #        with open('jsondata.json', 'w') as out_file:
        #            json.dump(xmltodict.parse(doc), out_file)
            #pp = pprint.PrettyPrinter(indent=4)
            #pp.pprint(json.dumps(doc))
        #if HDR == True:
        #    CarpetaHDR = ConversePath+'/HDR'
        #    try:
        #        # Create target Directory
        #        os.mkdir(CarpetaHDR)
        #        shutil.copy2('./Temp/raw.hdr', CarpetaHDR)                
        #    except FileExistsError:
        #        #print("already exists")
        #        shutil.copy2('./Temp/raw.hdr', CarpetaHDR)        
        if BIL == True:
            print("Convirtiendo a BIL")
            CarpetaBIL = ConversePath+'/BIL'
            FullPathBIL = CarpetaBIL+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBIL)

                envi.save_image(FullPathBIL, img, ext="", interleave = 'bil')                    
            except FileExistsError:
                print("ya existe")
                envi.save_image(FullPathBIL, img, ext="", interleave = 'bil')
                #print("already exists")
                #shutil.copy2('./Temp/raw.hdr', CarpetaHDR)
        if BIP == True:
            print("Convirtiendo a BIP")
            #data = open_image(fileName).load()
            #envi.save_image(fileNameNoExt+'.hdr', imgData, ext="", interleave = 'bip')
            CarpetaBIP = ConversePath+'/BIP'
            FullPathBIP = CarpetaBIP+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBIP)
                envi.save_image(FullPathBIP, img, ext="", interleave = 'bip')                  
            except FileExistsError:
                print("ya existe")
                envi.save_image(FullPathBIP, img, ext="", interleave = 'bip')
                #print("already exists")
                #shutil.copy2('./Temp/raw.hdr', CarpetaHDR)    
        if BSQ == True:
            print("Convirtiendo a BSQ")
            #data = open_image(fileName).load()
            CarpetaBSQ = ConversePath+'/BSQ'
            FullPathBSQ = CarpetaBSQ+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBSQ)
                envi.save_image(FullPathBSQ, img, ext="", interleave = 'bsq')                       
            except FileExistsError:
                print("ya existe")
                envi.save_image(FullPathBSQ, img, ext="", interleave = 'bsq')
                #print("already exists")
                #shutil.copy2('./Temp/raw.hdr', CarpetaHDR)

        QMessageBox.about(self, "", "Exported Succesfully")
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())
