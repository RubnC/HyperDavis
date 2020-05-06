#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QDir, Qt, QRect
from spectral import *
import spectral
from matplotlib import *
import matplotlib.image as mpimg
#from scipy import misc
import numpy as np
import glob
from ximea import xiapi
#hyperspy
from spectral import *
#ENVI Headers
import spectral.io.envi as envi
#aviris headers
import spectral.io.aviris as aviris
#Translate files type and delete tem files
import os, shutil
from os.path import expanduser
#Library for XML read
import xml.etree.ElementTree as ET
#representación del cubo

#Converse to JSON
import xmltodict
import pprint
import json
import wx
import string
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QSplitter, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea, QDialog, QApplication, QPushButton, QVBoxLayout, QLineEdit, QHBoxLayout, QFrame, QStyleFactory, QGridLayout, QSpacerItem, QDockWidget, QListWidget, QSlider, QCheckBox, QComboBox, QWidget, QSpacerItem
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage, QBrush, QPainter, QWindow, QTextCursor
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import random
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm

#Para pintar sobre la imagen y recortar
#pip3 install opencv-python==4.1.2.30
#conda install -c conda-forge opencv
import cv2

global label
textConsole = ""
img = []
imgMem = []
XML = False
JSON = False
HDR = False
BIL = False
BSQ = False
BIP = False
bandArray = []
ExportPath = ""
ConversePath = "./"
fileName = ""
fileNameNoExt = ""
#recortar imagen
imgCrop = None
p0 = None
p1 = None
p2 = None
p3 = None
p4 = None
p5 = None
p6 = None
p7 = None
p8 = None
p9 = None
R = None
G = None
B = None
#mask to verify if a pixel is inside or outside of polygon
mask = []


class  MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()

    #Main interface      
    def initUI(self):  

        global label, textConsole

        self.layout = QHBoxLayout()
        #right-side box - loaded images
        self.items = QDockWidget("Loaded Images", self)
        self.listWidget = QListWidget()
        self.listWidget.itemClicked.connect(self.Clicked)
        self.items.setWidget(self.listWidget)
        self.items.setFloating(False)
        self.addDockWidget(Qt.RightDockWidgetArea, self.items)
        label = QLabel(self)
        self.setCentralWidget(label)
        #right-side box CONSOLE
        console = QDockWidget("Output Console", self)
        textConsole = QTextEdit()
        textConsole.setEnabled(False)
        textConsole.setText("#HyperDavis output: ")
        textConsole.setText("#Open an Image to start")
        textConsole.moveCursor(QTextCursor.End)
        textConsole.ensureCursorVisible()
        console.setWidget(textConsole)
        console.setFloating(False)
        #self.setCentralWidget(QTextEdit())
        self.addDockWidget(Qt.RightDockWidgetArea, console)
        
        #Exit function
        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.removeTemp)
        exitAction.triggered.connect(self.close)
        #Open function
        openAction = QAction(QIcon('./icons/open.png'), 'Open File', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.load)
        #Converse tool function
        self.ConverseAction = QAction(QIcon('./icons/converse.png'), 'Converse', self)
        self.ConverseAction.setShortcut('Ctrl+C')
        self.ConverseAction.setStatusTip('Converse')
        self.ConverseAction.triggered.connect(self.Converse) 
        self.ConverseAction.setEnabled(False)
        #Bands combo
        self.combo=QComboBox()
        self.combo.setStyleSheet('''
        QComboBox { min-width: 120px; min-height: 40px;}    
''')
        self.combo.setEnabled(False)
        #FalseColor function
        self.FAKEcolorAction = QAction(QIcon('./icons/rgb.png'), 'False color Bands', self)
        self.FAKEcolorAction.setShortcut('Ctrl+F')
        self.FAKEcolorAction.setStatusTip('False color Bands')
        self.FAKEcolorAction.triggered.connect(self.FAKE) 
        self.FAKEcolorAction.setEnabled(False)
        #Spectral signature function
        self.SignatureAction = QAction(QIcon('./icons/chart3.png'), 'Signature', self)
        self.SignatureAction.setShortcut('Ctrl+E')
        self.SignatureAction.setStatusTip('Spectral Signature')
        self.SignatureAction.triggered.connect(self.Signature) 
        self.SignatureAction.setEnabled(False)
        #RGB Image function
        self.RGBAction = QAction(QIcon('./icons/real.png'), 'Show RGB image', self)
        self.RGBAction.setShortcut('Ctrl+L')
        self.RGBAction.setStatusTip('Show RGB image')
        self.RGBAction.triggered.connect(self.CheckRGB) 
        self.RGBAction.setEnabled(False)
        #New capture (tool function) - NOT COMPLETED
        newAction = QAction(QIcon('./icons/new1.png'), 'New Capture', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New Capture')
        newAction.triggered.connect(self.Capture) 
        newAction.setEnabled(False)
        #Crop rectangle function
        self.cropAction = QAction(QIcon('./icons/rectangle.png'), 'Crop Rectangle', self)
        self.cropAction.setShortcut('Ctrl+T')
        self.cropAction.setStatusTip('Crop Rectangle')
        self.cropAction.triggered.connect(self.cropImage) 
        self.cropAction.setEnabled(False)
        #Crop polygon function
        self.cropPolAction = QAction(QIcon('./icons/polygon.png'), 'Crop Polygon', self)
        self.cropPolAction.setShortcut('Ctrl+T')
        self.cropPolAction.setStatusTip('Crop Polygon')
        self.cropPolAction.triggered.connect(self.cropPolImage) 
        self.cropPolAction.setEnabled(False)
        #Crop Hyperspectral cube
        self.cropCubeAction = QAction(QIcon('./icons/cropCube.png'), 'Crop Cube', self)
        self.cropCubeAction.setShortcut('Ctrl+Y')
        self.cropCubeAction.setStatusTip('Crop Cube')
        self.cropCubeAction.triggered.connect(self.CropCube) 
        self.cropCubeAction.setEnabled(False)
        #Camera settings - NOT COMPLETED
        self.SettingAction = QAction(QIcon('./icons/settings.png'), 'Camera Settings', self)
        self.SettingAction.setStatusTip('Settings')
        self.SettingAction.setEnabled(False)
        #Help action
        self.HelpAction = QAction(QIcon('./icons/question.png'), 'Help', self)
        self.HelpAction.setStatusTip('Help')
        self.HelpAction.setEnabled(True)
        #About comments.
        self.aboutAction = QAction('About', self)
        self.aboutAction.setStatusTip('About')
        
        self.statusBar()

        menubar = self.menuBar()
        #This is needed, otherwise it doesn't work on MAC.
        menubar.setNativeMenuBar(False)
        #File Menu
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)
        #Edit Menu
        EditMenu = menubar.addMenu('Edit')
        EditMenu.addAction(self.ConverseAction)
        EditMenu.addAction(self.cropAction)
        EditMenu.addAction(self.cropPolAction)
        EditMenu.addAction(self.cropCubeAction)
        #Tools Menu
        toolsMenu = menubar.addMenu('Tools')
        toolsMenu.addAction(self.RGBAction)
        toolsMenu.addAction(self.FAKEcolorAction)
        toolsMenu.addAction(self.SignatureAction)
        #Settings  Menu - not completed
        settingMenu = menubar.addMenu('Settings')
        action5 = settingMenu.addAction(self.SettingAction)
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction(self.HelpAction)
        helpMenu.addSeparator()
        helpMenu.addAction(self.aboutAction)
        #Open TOOLBAR
        toolbar = self.addToolBar('Open')
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        #Tools toolbar
        self.toolbar1 = self.addToolBar('Tools')
        self.toolbar1.addWidget(self.combo)
        self.toolbar1.addAction(self.RGBAction)
        self.toolbar1.addAction(self.FAKEcolorAction)
        self.toolbar1.addAction(self.SignatureAction)
        #Edit toolbar
        self.editToolBar = self.addToolBar('Edit')
        self.editToolBar.addAction(self.ConverseAction)
        self.editToolBar.addAction(self.cropAction)
        self.editToolBar.addAction(self.cropPolAction)
        self.editToolBar.addAction(self.cropCubeAction)
        #Exit toolbar
        toolbar2 = self.addToolBar('Exit')
        toolbar2.addAction(exitAction)
        #Ventana principal
        self.setGeometry(0, 0, 700, 500)
        self.setWindowTitle('HyperDavis')    
        self.showMaximized()
        #Icono app
        self.setWindowIcon(QIcon('join.png')) 
        self.show()
        #Append text to right-side console
    def consoleText(text):
        global textConsole
        textConsole.append(text)
        #function to remove temporal files
    def removeTemp(self):
        folder = './Temp'
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path) 
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        
        #Function to load files
    def load(self):

        global img, label, fileName, fileNameNoExt
        #We only allow to the user to choose .hdr file anyway, it is easy to change it an load *.bin, *.lan
        #This if-else is made to manage if once the image is loaded the user wants to load a new one.
        if fileName == "":
            fileName2, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath(), "Hyper Files(*hdr)")
            if fileName != fileName2:
                fileName = fileName2
                self.load2()
            else:
                QMessageBox.about(self, "", "Please select a *.hdr file to start")
        else: 
            fileName2, _ = QFileDialog.getOpenFileName(self, "Open File", QDir.currentPath(), "Hyper Files(*hdr)")
            if fileName2 != "":
                fileName = fileName2
                self.load2()

        #Function to load files
    def load2(self):

        global img, label, fileName, fileNameNoExt
        #We disable all functions (again), just in case the user loaded another file.
        self.FAKEcolorAction.setEnabled(False)
        self.SignatureAction.setEnabled(False)
        self.cropAction.setEnabled(False)
        self.cropPolAction.setEnabled(False)
        self.cropCubeAction.setEnabled(False) 
        folder = './Temp'
        #We delete previus temp files
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.remove(file_path) 
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))
        #This is how we load .lan files (not used because we only allow .hdr at this point). I mostly had problems to know wavelengths with .lan files
        if ".lan" in fileName:
            img = open_image(fileName)
            self.represent(fileName)
            img2=get_rgb(img.read_band(0))
            print(img2)
            #imshow(img2)
            with open('your_file.txt', 'w') as f:
                for item in img2:
                    f.write("%s\n" % item)  		    
        #This is how we load .bin files (not used because we only allow .hdr at this point)
        elif ".bin" in fileName:
            fileNameHDR = fileName.replace(".bin" , ".hdr")
            pureFileName = fileNameHDR.replace(".hdr" , "")
            pureFileName = pureFileName.split('/')
            pureFileName = pureFileName[len(pureFileName)-1]

            translate = 'gdal_translate -of ENVI '+fileName+ ' ./Temp/'+pureFileName+'.gis'
            os.system(translate)
            img = envi.open(fileNameHDR, fileName)
            self.represent(fileName)
            img2 = get_rgb(img.read_band(0))
        #At this point we only use this case. (.bin case works perfectly but in this way we ensure that we have the headers)	
        elif ".hdr" in fileName:
            fileNameBin = fileName.replace(".hdr" , "")
            pureFileName = fileNameBin.split('/')
            pureFileName = pureFileName[len(pureFileName)-1]
            MainWindow.consoleText("Loading cube, please wait...")
            #We use gdal_translate to make it understandable for the other libraries. It will generete an XML-type file
            translate = 'gdal_translate -of ENVI '+fileNameBin+ ' ./Temp/'+pureFileName+'.gis'
            os.system(translate)
            #We load the cube in memory
            img = envi.open(fileName, fileNameBin)
            self.represent(fileNameBin)    

    def represent(self, fileName):  
        global nbands, img, bandArray
        nbands = len(img[1, 1])
        #Show image un RGB bands 
        self.img=img
        #We read the first band
        rgb = get_rgb(img.read_band(0))
        #main frame in UI        
        self.main_frame = QWidget()
        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)               
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

        #If file is .lan we won't have wavelength information, therefore, we only show the number (not enabled at this point. Only .hdr permited)
        if ".lan" in fileName:
        	for i in (range(nbands)):
       			text="Band "+ str(i)
       			self.combo.addItem(text)
        else:
            bandArray=[]
            aux_file= str(fileName.rsplit("/", 1)[1])
            aux_file1= str(aux_file.rsplit(".", 1)[0])
            #We use the XML-type file to get wavelength information for each band.
            aux_file_path="./Temp/"+aux_file1+".gis.aux.xml"
            tree = ET.parse(aux_file_path)
            root = tree.getroot()
            for elem in root.findall('PAMRasterBand'):
                wlength =elem.find('Description').text
                wlength = wlength.replace("nm", "")
                wlength = wlength.rstrip()
                bandArray.append(wlength)
                wlength = wlength + " nm"
                band = "Band " + elem.get('band') + " - "
                #We have wavelength information to the combo element.
                self.combo.addItem(band + wlength)

        self.combo.activated[str].connect(self.comboChanged) 
        self.ConverseAction.setEnabled(True)
        self.RGBAction.setEnabled(True)
        self.combo.setEnabled(True)

        #Text appenended to the right-side console.
        text="#The image " + fileName + " has been loaded."
        MainWindow.consoleText(text)
        datos=str(img)
        MainWindow.consoleText(datos)
        MainWindow.consoleText("#Band 1 loaded")
        redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
        redText= redText + "NOTE: </span>"
        MainWindow.consoleText(redText)
        #We give some tips to the user
        MainWindow.consoleText("#Please, execute RGB tool in order to use the rest of tools")
        self.listWidget.addItem(fileName)
        print (img)
  
    def FAKE(self):    
       MainWindow.consoleText("#Fake Color tool launched")
       self.dialog = FAKEcolorWindow(self)
       
    def RGB(self):    
       MainWindow.consoleText("#RGB tool launched")
       self.dialog = RGBWindow(self)      

    def cropImage(self):    
       MainWindow.consoleText("#Crop tool launched")
       self.dialog = CropWindow(self)       

    def cropPolImage(self):
        MainWindow.consoleText("#Polygon crop tool launched")
        MainWindow.consoleText("Please, click on at least 3 points (max. 10) to draw a polygon and press 's' key to save || press 'q' key to cancel")
        MainWindow.consoleText(" ")
        self.dialog = CropPolWindow(self)

    def CropCube(self):    
       MainWindow.consoleText("#Crop hyperspectral cube tool launched")
       self.dialog = cropCubeWindow(self)
    
    def Converse(self):    
       MainWindow.consoleText("#HyperEspectral conversion tool launched")
       self.dialog = ConverseWindow(self)
       
    #Capture function (not completed)
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
 
    #Load a previous image from the right-side box
    def Clicked(self,item):
        global img, label, img, imgMem, XML, JSON, HDR, BIL, BSQ, BIP, bandArray, ExportPath, ConversePath, fileName, fileNameNoExt, imgCrop
        global p0, p1, p2, p3, p4, R, G, B, mask
        if self.listWidget.count() > 1:
            reply = QMessageBox.question(self, 'Message',"You are going to open: "+item.text(), QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                img = []
                imgMem = []
                XML = False
                JSON = False
                HDR = False
                BIL = False
                BSQ = False
                BIP = False
                bandArray = []
                ExportPath = ""
                ConversePath = "./"
                fileName = ""
                fileNameNoExt = ""
                imgCrop = None
                p0 = None
                p1 = None
                p2 = None
                p3 = None
                p4 = None
                R = None
                G = None
                B = None
                mask = []
                self.SignatureAction.setEnabled(False)
                self.cropAction.setEnabled(False)
                self.cropPolAction.setEnabled(False)
                self.cropCubeAction.setEnabled(False)    
 
                fileName = str(item.text())+".hdr"
                print(fileNameNoExt)
                fileNameBin = fileName.replace(".hdr" , "")
                img = envi.open(fileName, fileNameBin);
                pureFileName = fileNameBin.split('/')
                pureFileName = pureFileName[len(pureFileName)-1]
                translate = 'gdal_translate -of ENVI '+fileNameBin+ ' ./Temp/'+pureFileName+'.gis'
                os.system(translate)
                img = envi.open(fileName, fileNameBin);
                img2= get_rgb(img.read_band(0))
                self.represent(fileNameBin)
            else:
                print("NO") 
        else:
            print("just one")
      
    #Signature tool based on RGB image.
    def Signature(self): 
        global fileName, R, G, B
        MainWindow.consoleText("#Signature tool launched")
        prueba = imshow(img, (R, G, B), origin='lower', title="Click on a pixel to see it's spectral signture ")
        MainWindow.consoleText("Double click on a pixel to see it's spectral signature")
        
    #Detects a change on combo selected element
    def comboChanged(self, text):
        self.layout.addWidget(self.canvas)         # the matplotlib canvas
        self.layout.addWidget(self.mpl_toolbar)
        self.main_frame.setLayout(self.layout)
        self.setCentralWidget(self.main_frame)
        band=text.split(" - ", 1)[0]
        band = int(band.replace("Band",""))
        rgb = get_rgb(img.read_band(int(band)-1))
        ax=self.axes.imshow(rgb, origin='lower', animated=True)
        self.canvas.draw()
        MainWindow.consoleText(text + " loaded.")
    #Function to check and findout the RGB bands    
    def CheckRGB(self):
        global fileName, bandArray, R, G, B
        RGBbandsHDR = False
        bandArrayHDR= []
        Raux = []
        Gaux = []
        Baux = []
        Rflag = False
        Gflag = False
        Bflag = False
        print (fileName)
        with open(fileName, 'r') as myhdr:    
                for line in myhdr:
                    if 'default bands' in line:
                        #This loop looks for the default bands on the header (sometimes is given by the camera)
                        RGBbandsHDR= True
                        print(line)
                        bandArrayStr= line.replace("default bands = {","")
                        bandArrayStr= bandArrayStr.replace("}\n","")
                        bandArrayHDR=list(map(int, bandArrayStr.split(',')))
                        break
                    elif 'wavelength' in line:
                        break
        if RGBbandsHDR == True:
            #If default bands are found we check if the format is RGB or BGR
            if float(bandArray[bandArrayHDR[2]])>650:
                save_rgb('./Temp/rgb.jpg', img, [bandArrayHDR[2],bandArrayHDR[1], bandArrayHDR[0]])   
                RGBbandsHDR = False
                redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
                redText= redText + "TIP: </span>"
                MainWindow.consoleText(redText)
                MainWindow.consoleText("If you don't like the result you can try to adjust each color band manually using the fake color tool.\n"+"\nUsed bands are the following:\n"+"·R: "+str(bandArrayHDR[2])+ "\n·G: " + str(bandArrayHDR[1])+"\n·B: " +str(bandArrayHDR[0])+"")  
                self.dialog = RGBWindow(self)
                self.activeCrop()
                
            else:
                #If it is RGB
                save_rgb('./Temp/rgb.jpg', img, bandArrayHDR)
                RGBbandsHDR = False
                redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
                redText= redText + "TIP: </span>"
                MainWindow.consoleText(redText)
                MainWindow.consoleText("If you don't like the result you can try to adjust each color band manually using the fake color tool.\n"+"\nUsed bands are the following:\n"+"·R: "+str(bandArrayHDR[0])+ "\n·G: " + str(bandArrayHDR[1])+"\n·B: " +str(bandArrayHDR[2])+"")
                self.dialog = RGBWindow(self)
                self.activeCrop()
            #If default bands are not given we have to find them       
        else:
            for i in bandArray: 
                if float(i)>450 and float(i)<495:
                    Baux.append(float(i))
                    Bflag=True
                if float(i)>495 and float(i)<570:
                    Gaux.append(float(i))
                    Gflag=True
                if float(i)>620 and float(i)<750:
                    Raux.append(float(i))
                    Rflag=True
            if Bflag and Gflag and Rflag:
                print ("B:" + str(len(Baux)) +"Wl:" + str(Baux[int(int((len(Baux))/2))]))
                B = bandArray.index(str(Baux[int(int((len(Baux))/2))]))
                print (B)
                print ("G:" + str(len(Gaux)) +"Wl:" + str(Gaux[int(int((len(Gaux))/2))]))
                G = bandArray.index(str(Gaux[int(int((len(Gaux))/2))]))
                print (G)
                print ("R:" + str(len(Raux)) +"Wl:" + str(Raux[int(int((len(Raux))/2))]))
                R = bandArray.index(str(Raux[int(int((len(Raux))/2))]))
                print (R)
                save_rgb('./Temp/rgb.jpg', img, [int(R), int(G), int(B)])
                redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
                redText= redText + "TIP: </span>"
                MainWindow.consoleText(redText)
                MainWindow.consoleText("If you don't like the result you can try to adjust each color band manually using the fake color tool.\n"+"\nUsed bands are the following:\n"+"·R: "+str(int(R))+ "\n·G: " + str(int(G))+"\n·B: " +str(int(B))+"")
                self.dialog = RGBWindow(self)
                self.activeCrop()
                Bflag=False
                Gflag=False
                Rflag=False
            else:
                #If not possible we have to find the better image possible
                self.dialog = AUTOfakeColor(self)
                self.activeCrop()
    #Function to enable the rest of tools            
    def activeCrop(self):
        self.FAKEcolorAction.setEnabled(True)
        self.SignatureAction.setEnabled(True)
        self.cropAction.setEnabled(True)
        self.cropPolAction.setEnabled(True)
        self.cropCubeAction.setEnabled(True)
    


#Class to show the rectangle crop tool
class CropWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(CropWindow, self).__init__(parent)
        self.do_main()

    def do_main(self):
        global imgCrop, p0, p1
        #We show the RGB image saved previously in order to show the user the most real image possible and make it easier.
        if os.path.exists('./Temp/rgb.jpg'):
            imgCrop = cv2.imread("./Temp/rgb.jpg", cv2.IMREAD_COLOR)
            cv2.imshow('image', imgCrop)
            cv2.setMouseCallback('image', self.drag_box)
            #Some instructions to the user...
            MainWindow.consoleText("Drag the cursor to paint a rectangle and press 's' key to save || press 'q' key to cancel")
            while True:
                k = cv2.waitKey(100) & 0xFF
                if k == ord('q') or k == ord('Q') or cv2.getWindowProperty('image', 0) == -1:
                    # wait for 'q' key to exit the program
                    MainWindow.consoleText("'q' pressed")
                    p0=p1=None
                    break
                elif k == ord('s') or k ==ord('S'):
                    # wait for 's' key to save boxed image
                    MainWindow.consoleText("Initial point:" + str(p0))
                    MainWindow.consoleText("Final point:" + str(p1))
                    if p0 is not None and p1 is not None:
                        self.cropCubeUI()

                        break        
            cv2.destroyAllWindows()
        else:
            #Tips for the user
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "NOTE: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("Please, execute RGB tool in automatic mode once and try again")
            QMessageBox.about(self, "", "#Please, execute RGB tool in automatic mode once and try again")

    def draw_box(self, _img, _p0, _p1):
    #Draw box which selected by mouse dragging
        boxed = _img.copy()
        boxed = cv2.rectangle(boxed, _p0, _p1, (0, 255, 0), 1)
        cv2.imshow('image', boxed)

    def save_box(self, _img, _p0, _p1, _dir_out, _filename):
    #Save the boxed area as an image
        global imgCrop

        x0 = int(min(_p0[0], _p1[0]))
        y0 = int(min(_p0[1], _p1[1]))
        x1 = int(max(_p0[0], _p1[0]))
        y1 = int(max(_p0[1], _p1[1]))

        img_boxed = imgCrop[y0:y1, x0:x1]
        cv2.imwrite(os.path.join(_dir_out, _filename + '.jpg'), img_boxed)
        print('saved image x0:{0}, y0:{1}, x1:{2}, y1:{3}'.format(x0, y0, x1, y1))

    def drag_box(self, event, x, y, flags, param):
    #Mouse callback function - by mouse dragging
        global p0, p1, imgCrop

        if event == cv2.EVENT_LBUTTONDOWN:
            p0 = (x, y)
            p1 = None
        elif event == cv2.EVENT_LBUTTONUP:
            if p0 == p1:
                p0 = p1 = None
            else:
                p1 = (x, y)
        if p0 is not None and p1 is None:
            self.draw_box(imgCrop, p0, (x, y))

    def cropCubeUI(self):
    #After cropping the rectangle we give the user the option of cropping the hyperspectral cube.
        self.nbands = nbands
        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Low Band")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 40)
        self.lbl1.setText("High Band")

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(120, 20, 230, 30)
        self.sld.setMinimum(1)
        self.sld.setMaximum(self.nbands+1)

        self.label = QLabel(self)
        self.label.setText("1")
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(1)
        self.sld1.setMaximum(self.nbands)
        self.label1 = QLabel(self)
        self.label1.setText("1")
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)

        self.btn = QPushButton('Ok', self)
        self.btn.move(120, 80)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(220, 80)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.trimCube)
        self.btn.clicked.connect(self.close)

        #self.le.adjustSize()
        self.setWindowTitle('Select which band range you want to save')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(450, 110)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def valuechange(self):
        size = self.sld.value()
        self.label.setText(str(size))

    def valuechange1(self):
        size = self.sld1.value()
        self.label1.setText(str(size))

    def trimCube(self):
        global img, bandArray, p0, p1, imgCrop
        TrimPath=""
        if self.sld.value() > self.sld1.value():
            QMessageBox.about(self, "Error", "The lower band cannot be larger than the upper one")
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "ERROR: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("The lower band cannot be larger than the upper one")
        else:
            TrimPath = QFileDialog.getSaveFileName(self, 'Save File')[0]
            region = img[p0[1]:p1[1], p0[0]:p1[0], self.sld.value()-1:self.sld1.value()]
            MainWindow.consoleText("Saving bands from:" + str(self.sld.value()) + " to: " + str(self.sld1.value()))
            envi.save_image(TrimPath+'.hdr', region, force=True, ext="", interleave = 'bil')
            self.save_box(imgCrop, p0, p1, TrimPath, TrimPath)
            p0 = p1 = None
            cubeArray = bandArray[(self.sld.value()-1):(self.sld1.value())]    
            #The library does not support wavelenght information so we add it manually to the final file
            with open(TrimPath+'.hdr', "a") as f:
                f.write("wavelength units = nm\n")
                f.write("wavelength = {\n")
                for X in cubeArray:
                    f.write(X+"\n,")
                f.write("}")
            QMessageBox.about(self, "", "Completed!")
            MainWindow.consoleText("Saved" + TrimPath)

#Class to show the polygon crop tool
class CropPolWindow(QMainWindow):
    
    def __init__(self, parent=None):
        super(CropPolWindow, self).__init__(parent)
        self.do_main()

    def do_main(self):
        global imgCrop, p0, p1, p2, p3, p4
        p0 = None
        p1 = None
        p2 = None
        p3 = None
        p4 = None
        if os.path.exists('./Temp/rgb.jpg'):
            imgCrop = cv2.imread("./Temp/rgb.jpg", cv2.IMREAD_COLOR)
            cv2.imshow('image', imgCrop)
            cv2.setMouseCallback('image', self.drag_box)

            while True:
                k = cv2.waitKey(100) & 0xFF
                if k == ord('q') or k == ord('Q') or cv2.getWindowProperty('image', 0) == -1:
                    # wait for 'q' key to exit the program
                    p0=p1=p2=p3=p4= None
                    MainWindow.consoleText("'q' pressed")
                    break
                elif k == ord('s') or k == ord('S'):
                    # wait for 's' key to save boxed image
                    if p0 is not None and p1 is not None and p2 is not None:
                        #self.save_box(imgCrop, p0, p1, "./")
                        MainWindow.consoleText("'s' pressed")
                        self.draw_box()
                        MainWindow.consoleText("Please wait...")
                        self.cropCubeUI()
                        break        
            cv2.destroyAllWindows()
        else:
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "NOTE: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("Please, execute RGB tool in automatic mode once and try again")
            QMessageBox.about(self, "", "Please, execute RGB tool in automatic mode once and try again")

    def draw_box(self):
    #Draw box which selected by mouse dragging
        global img, imgCrop, imgMem, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, x0, y0, mask, pts
        #We load the image on memory
        imgMem = open_image(fileName).load()
        #We create a boolean mask array in order to determine which pixels are inside or outside of the drawn polygon
        mask = np.zeros((imgCrop.shape[0], imgCrop.shape[1]))
        cv2.fillConvexPoly(mask, pts, 1)
        mask = mask.astype(np.bool)
        boxed = imgCrop.copy()
        pts = pts.reshape((-1,1,2))
        cv2.polylines(boxed, [pts],True,(0,255,0), 1)
        
        #Ranges depend on how many points are selected:
        if p3 == None:
            x0=[p0[0], p1[0], p2[0]]
            y0=[p0[1], p1[1], p2[1]]
        elif p4 == None:
            x0=[p0[0], p1[0], p2[0], p3[0]]
            y0=[p0[1], p1[1], p2[1], p4[1]]
        elif p5 == None:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1]]
        elif p6 == None:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0], p5[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1], p5[1]]
        elif p7 == None:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1], p5[1], p6[1]]
        elif p8 == None:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1], p5[1], p6[1], p7[1]]
        elif p9 == None:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1], p5[1], p6[1], p7[1], p8[1]]
        else:
            x0=[p0[0], p1[0], p2[0], p3[0], p4[0], p5[0], p6[0], p7[0], p8[0], p9[0]]
            y0=[p0[1], p1[1], p2[1], p4[1], p4[1], p5[1], p6[1], p7[1], p8[1], p9[1]]

        #We limit the range to the rectangle that contains the polygon and if the pixel is outside we gave it a not valid value.
        for y in range(int(min(y0)), int(max(y0))):
            for x in range(int(min(x0)), int(max(x0))):
                if mask[y, x]==False:
                    imgCrop[y, x] = [255, 255, 255]
                    for b in range(0, nbands-1):
                        imgMem[y, x, b]= 974.
                    
        cv2.imshow('image', boxed)

    def save_box(self, _img, _p0, _p1, _p2, _p3, _p4, _p5, _p6, _p7, _p8, _p9, _dir_out, _filename):
    # Save the boxed area as an image
        global imgCrop, x0, y0

        img_boxed = imgCrop[int(min(y0)):int(max(y0)), int(min(x0)):int(max(x0))]
        cv2.imwrite(os.path.join(_dir_out, _filename + '.jpg'), img_boxed)
    #Function to draw a polygon with p3-p10 sides
    def drag_box(self, event, x, y, flags, param):
    #Mouse callback function - by mouse dragging
        global p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, pts, imgCrop, img

        if p0 is None and event == cv2.EVENT_LBUTTONDOWN:
            p0 = (x, y)
            MainWindow.consoleText("·P1:" + str(p0))
        elif p0 is not None and p1 is None and event == cv2.EVENT_LBUTTONDOWN:
            p1 = (x, y)
            MainWindow.consoleText("·P2:" + str(p1))
            pts = np.array([p0, p1], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            p2 = None 
            p3 = None
            p4 = None
            p5 = None
            p6 = None
            p7 = None
            p8 = None
            p9 = None 
        elif p1 is not None and p2 is None and event == cv2.EVENT_LBUTTONDOWN:
            p2 = (x, y)
            MainWindow.consoleText("·P3:" + str(p2))
            pts = np.array([p0, p1, p2], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            p3 = None
            p4 = None
            p5 = None
            p6 = None
            p7 = None
            p8 = None
            p9 = None 
        elif p2 is not None and p3 is None and event == cv2.EVENT_LBUTTONDOWN:
            p3 = (x, y)
            MainWindow.consoleText("·P4:" + str(p3))
            pts = np.array([p0, p1, p2, p3], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed) 
            p4 = None
            p5 = None
            p6 = None
            p7 = None
            p8 = None
            p9 = None 
        elif p3 is not None and p4 is None and event == cv2.EVENT_LBUTTONDOWN:
            p4 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P5:" + str(p4))
            p5 = None
            p6 = None
            p7 = None
            p8 = None
            p9 = None
        elif p4 is not None and p5 is None and event == cv2.EVENT_LBUTTONDOWN:
            p5 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4, p5], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P6:" + str(p5))
            p6 = None
            p7 = None
            p8 = None
            p9 = None
        elif p5 is not None and p6 is None and event == cv2.EVENT_LBUTTONDOWN:
            p6 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4, p5, p6], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P7:" + str(p6))
            p7 = None
            p8 = None
            p9 = None
        elif p6 is not None and p7 is None and event == cv2.EVENT_LBUTTONDOWN:
            p7 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4, p5, p6, p7], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P8:" + str(p7))
            p8 = None
            p9 = None
        elif p7 is not None and p8 is None and event == cv2.EVENT_LBUTTONDOWN:
            p8 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P9:" + str(p8))
            p9 = None 
        elif p8 is not None and p9 is None and event == cv2.EVENT_LBUTTONDOWN:
            p9 = (x, y)
            pts = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9], dtype=np.int32)
            boxed = imgCrop.copy()
            pts = pts.reshape((-1,1,2))
            cv2.polylines(boxed, [pts],True,(0,255,0), 1)
            cv2.imshow('image', boxed)
            MainWindow.consoleText("·P10:" + str(p9))
            MainWindow.consoleText("Maximum of points selected. Press 's' to save or 'q' to cancel")     
            
    #We give the user the option to crop the hyperspectral cube before save the polygon
    def cropCubeUI(self):
        self.nbands = nbands
        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Low Band")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 40)
        self.lbl1.setText("High Band")

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(120, 20, 230, 30)
        self.sld.setMinimum(1)
        self.sld.setMaximum(self.nbands)

        self.label = QLabel(self)
        self.label.setText("1")
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(1)
        self.sld1.setMaximum(self.nbands)
        self.label1 = QLabel(self)
        self.label1.setText("1")
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)


        self.btn = QPushButton('Ok', self)
        self.btn.move(120, 80)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(220, 80)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.trimCube)
        self.btn.clicked.connect(self.close)

        #self.le.adjustSize()
        self.setWindowTitle('Select which band range you want to save')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(450, 110)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def valuechange(self):
        size = self.sld.value()
        self.label.setText(str(size))

    def valuechange1(self):
        size = self.sld1.value()
        self.label1.setText(str(size))
    #We crop the hyperspectral cube after drawing a polygon
    def trimCube(self):
        global img, imagMem, bandArray, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, x0, y0, imgCrop
        #data = open_image(fileName).load()
        TrimPath=""
        if self.sld.value() > self.sld1.value():
            QMessageBox.about(self, "Error", "The lower band cannot be larger than the upper one")
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "ERROR: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("The lower band cannot be larger than the upper one")
        else:
            TrimPath=""
            FinalPath=""
            TrimPath = QFileDialog.getSaveFileName(self, 'Save File')[0]
            print(TrimPath)

            if TrimPath != "":
                FinalPath= TrimPath+'/'+fileNameNoExt+'.hdr' 
                Path= TrimPath+'/'+fileNameNoExt
                region = imgMem[min(y0):max(y0), min(x0):max(x0), self.sld.value()-1:self.sld1.value()]
                MainWindow.consoleText("Saving bands from:" + str(self.sld.value()) + " to: " + str(self.sld1.value()))
                #Save the hyperspectral cube
                envi.save_image(TrimPath+'.hdr', region, force=True, ext="", interleave = 'bil')
                #Save the image
                self.save_box(imgCrop, p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, TrimPath, TrimPath)
                p0 = p1 = None
                cubeArray = bandArray[(self.sld.value()-1):(self.sld1.value())]    
                with open(TrimPath+'.hdr', "a") as f:
                    f.write("wavelength units = nm\n")
                    f.write("wavelength = {\n")
                    for X in cubeArray:
                        f.write(X+"\n,")
                    f.write("}")
                QMessageBox.about(self, "", "Completed!")
                MainWindow.consoleText("Saved in" + TrimPath)

#This class just show the rgb image
class RGBWindow(QMainWindow):
    def __init__(self, parent=None):
        super(RGBWindow, self).__init__(parent)
        self.RGBUI()

    def RGBUI(self):
        img=mpimg.imread("./Temp/rgb.jpg")
        plt.imshow(img, origin='lower')
        plt.title('RGB Image')
        plt.show()

#This class is used when file doesn't have enough information to represent RGB
class AUTOfakeColor(QMainWindow):
    def __init__(self, parent=None):
        super(AUTOfakeColor, self).__init__(parent)
        self.AUTOfakeColorUI()

    def AUTOfakeColorUI(self):
        #self.dialog = FAKEcolorWindow(self)
        #FAKEcolorWindow.FAKEcolorUI()
        self.lbl = QLabel(self)
        self.lbl.setText("Data cube does not have enough data to represent a real RGB image.\nBest coloring possible will be used if you choose automatic mode.")
        self.lbl.resize(480, 80)
        self.lbl.move(30, 10)
        self.btn = QPushButton('Automatic', self)
        self.btn.move(100, 100)
        self.btn1 = QPushButton('Manual', self)
        self.btn1.move(300, 100)
        self.btn.clicked.connect(self.close)
        self.btn.clicked.connect(self.AUTO)
        self.btn1.clicked.connect(self.close)
        self.btn1.clicked.connect(self.MANUALfakeColor)
        #selcolorf.le.adjustSize()
        self.setWindowTitle('RGB Mode')
        self.setFixedSize(490, 150)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint )
        self.show()
    def MANUALfakeColor(self):
        self.dialog = FAKEcolorWindow(self)
    #Automatic search of best colouring
    def AUTO(self):
        global fileName, bandArray, R, G, B
        global img
        Bflag=False
        Gflag=False
        Rflag=False
        Raux = []
        Gaux = []
        Baux = []
        for i in bandArray: 
                if float(i)>450 and float(i)<495:#buscamos azul
                    Baux.append(float(i))
                    Bflag=True
                if float(i)>495 and float(i)<570:#buscamos verdes
                    Gaux.append(float(i))
                    Gflag=True
                if float(i)>620 and float(i)<750:#buscamos rojos
                    Raux.append(float(i))
                    Rflag=True
        if Bflag or Gflag or Rflag:
            if Bflag and Gflag:
                B = bandArray.index(str(Baux[int(int((len(Baux))/2))]))
                G = bandArray.index(str(Gaux[int(int((len(Gaux))/2))]))
                R = len(bandArray)-1
            elif Bflag and not Gflag:
                B = bandArray.index(str(Baux[int(int((len(Baux))/2))]))
                G = int(B + (B/2))
                R = len(bandArray)-1
            elif Gflag and Rflag:
                B = 0
                G = bandArray.index(str(Gaux[int(int((len(Gaux))/2))]))
                R = bandArray.index(str(Raux[int(int((len(Raux))/2))]))
            elif Gflag and not Rflag:
                B = 0
                G = bandArray.index(str(Gaux[int(int((len(Gaux))/2))]))
                R = len(bandArray)-1
            elif not Gflag and Rflag:
                B = 0
                R = bandArray.index(str(Raux[int(int((len(Raux))/2))]))
                G = int(R - (R/2))
            save_rgb('./Temp/rgb.jpg', img, [int(R), int(G), int(B)])
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "TIP: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("If you don't like the result you can try to adjust each color band manually using the fake color tool.\n"+"\nUsed bands are the following:\n"+"·R: "+str(int(R))+ "\n·G: " + str(int(G))+"\n·B: " +str(int(B))+"")      
            self.dialog = RGBWindow(self)
            #This 'else' is used when the image doesn't have enough information to represent any colour          
        else:
            B = 0
            G = int(len(bandArray)/2)
            R = len(bandArray)-1
            save_rgb('./Temp/rgb.jpg', img, [int(R), int(G), int(B)])
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "TIP: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("If you don't like the result you can try to adjust each color band manually using the fake color tool.\n"+"\nUsed bands are the following:\n"+"·R: "+str(int(R))+ "\n·G: " + str(int(G))+"\n·B: " +str(int(B))+"")
            self.dialog = RGBWindow(self)
    Bflag=False
    Gflag=False
    Rflag=False

#Fake color window      
class FAKEcolorWindow(QMainWindow):
    def __init__(self, parent=None):
        super(FAKEcolorWindow, self).__init__(parent)

        self.FAKEcolorUI()

    def FAKEcolorUI(self):

        self.nbands = nbands
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
        self.sld.setMinimum(1)
        self.sld.setMaximum(self.nbands)

        self.label = QLabel(self)
        self.label.setText("1")
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(1)
        self.sld1.setMaximum(self.nbands)
        self.label1 = QLabel(self)
        self.label1.setText("1")
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)

        self.sld2 = QSlider(Qt.Horizontal, self)
        self.sld2.setFocusPolicy(Qt.NoFocus)
        self.sld2.setGeometry(120, 60, 230, 30)
        self.sld2.setMinimum(1)
        self.sld2.setMaximum(self.nbands)
        self.label2 = QLabel(self)
        self.label2.setText("1")
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
        MainWindow.consoleText("·R:" + str(self.sld.value()))
        MainWindow.consoleText("·G:" + str(self.sld1.value()))
        MainWindow.consoleText("·B:" + str(self.sld2.value()))
        imshow(img, (self.sld.value(), self.sld1.value(), self.sld2.value()), origin='lower', title="False color image")
        self.close
#cropCube tool window
class cropCubeWindow(QMainWindow):
    def __init__(self, parent=None):
        super(cropCubeWindow, self).__init__(parent)
        self.cropCubeUI()

    def cropCubeUI(self):

        self.nbands = nbands
        self.lbl = QLabel(self)
        self.lbl.move(20, 20)
        self.lbl.setText("Low Band")

        self.lbl1 = QLabel(self)
        self.lbl1.move(20, 40)
        self.lbl1.setText("High Band")

        self.sld = QSlider(Qt.Horizontal, self)
        self.sld.setFocusPolicy(Qt.NoFocus)
        self.sld.setGeometry(120, 20, 230, 30)
        self.sld.setMinimum(1)
        self.sld.setMaximum(self.nbands)

        self.label = QLabel(self)
        self.label.setText("1")
        self.sld.valueChanged.connect(self.valuechange)
        self.label.setGeometry(370, 20, 80, 30)

        self.sld1 = QSlider(Qt.Horizontal, self)
        self.sld1.setFocusPolicy(Qt.NoFocus)
        self.sld1.setGeometry(120, 40, 230, 30)
        self.sld1.setMinimum(1)
        self.sld1.setMaximum(self.nbands)
        self.label1 = QLabel(self)
        self.label1.setText("1")
        self.sld1.valueChanged.connect(self.valuechange1)
        self.label1.setGeometry(370, 40, 80, 30)


        self.btn = QPushButton('Ok', self)
        self.btn.move(120, 80)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(220, 80)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.trimCube)
        self.btn.clicked.connect(self.close)

        #self.le.adjustSize()
        self.setWindowTitle('Select which band range you want to save')
        self.setWindowIcon(QIcon('rgb.png')) 
        self.setFixedSize(450, 110)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        self.show()

    def valuechange(self):
        size = self.sld.value()
        self.label.setText(str(size))

    def valuechange1(self):
        size = self.sld1.value()
        self.label1.setText(str(size))

    def trimCube(self):
        global bandArray
        TrimPath=""
        if self.sld.value() > self.sld1.value():
            QMessageBox.about(self, "Error", "The lower band cannot be larger than the upper one")
            redText = "<span style=\" font-size:10pt; font-weight:600; color:#ff0000;\" >"
            redText= redText + "ERROR: </span>"
            MainWindow.consoleText(redText)
            MainWindow.consoleText("The lower band cannot be larger than the upper one")
        else:
            TrimPath = QFileDialog.getSaveFileName(self, 'Save File')[0]            
            cube = img[:, :, self.sld.value()-1:self.sld1.value()]
            MainWindow.consoleText("Saving bands from:" + str(self.sld.value()) + " to: " + str(self.sld1.value()))
            envi.save_image(TrimPath+'.hdr', cube, force=True, ext="", interleave = 'bil')
            cubeArray = bandArray[(self.sld.value()-1):(self.sld1.value())]
            
            with open(TrimPath+'.hdr', "a") as f:
                f.write("wavelength units = nm\n")
                f.write("wavelength = {\n")
                for X in cubeArray:
                    f.write(X+"\n,")
                f.write("}")
            QMessageBox.about(self, "", "Completed!")
        
    #Conversion tool window
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
        self.textbox.setText("FileName")

        self.btn = QPushButton('Select Path', self)
        self.btn.move(50, 150)
        self.btn1 = QPushButton('Cancel', self)
        self.btn1.move(180, 150)
        self.btn1.clicked.connect(self.close)
        self.btn.clicked.connect(self.PathToConverse)
        self.btn.clicked.connect(self.close)

        self.setWindowTitle('HyperEspectral conversion tool')
        self.setFixedSize(330, 210)
        self.setWindowFlags(QtCore.Qt.Window |QtCore.Qt.CustomizeWindowHint |QtCore.Qt.WindowTitleHint |QtCore.Qt.WindowCloseButtonHint |QtCore.Qt.WindowStaysOnTopHint)
        
        self.show()
        self.b.stateChanged.connect(self.clickBoxXML)
        #self.b1.stateChanged.connect(self.clickBoxJSON)
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
            XML = True
        else:
            XML = False

    def clickBoxJSON(self, state):
        global  JSON
        if state == QtCore.Qt.Checked:
            JSON = True
        else:
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
            BIL = True
        else:
            BIL = False

    def clickBoxBIP(self, state):
        global  BIP
        if state == QtCore.Qt.Checked:
            BIP = True
        else:
            BIP = False

    def clickBoxBSQ(self, state):
        global  BSQ
        if state == QtCore.Qt.Checked:
            BSQ = True
        else:
            #print('Unchecked')
            BSQ = False
    #We let the user to choose the path and name
    def PathToConverse(self):
        global ConversePath, fileNameNoExt
        ConversePath=""
        ConversePath = QFileDialog.getExistingDirectory(self, "Open a folder", expanduser("~"), QFileDialog.ShowDirsOnly)
        if ConversePath != "":
            self.Converse()
            print (ConversePath)

        self.close
    def Converse(self):
        #In the choosen path we create diferent folders for each export result (XML, BIL, BIP, BSQ)
        global fileName, ConversePath, fileNameNoExt
        fileNameNoExt = self.textbox.text()
        if XML == True:
            print("Convirtiendo a XML")
            print("aqui el nombre del fichero" + fileName)
            CarpetaXML = ConversePath+'/XML'  
            try:
                # Create target Directory
                pureFileName = fileName.split('/')
                print(pureFileName)
                #print("VALOR:"+(len(fileName)))
                pureFileName = pureFileName[len(pureFileName)-1]
                pureFileName = pureFileName.replace(".hdr" , "")
                os.mkdir(CarpetaXML)
                shutil.copy2('./Temp/'+pureFileName+'.gis.aux.xml', CarpetaXML)
                os.rename(CarpetaXML+'/'+pureFileName+'.gis.aux.xml',CarpetaXML+'/'+fileNameNoExt+'.xml')

            except FileExistsError:
                #print("already exists")
                pureFileName = pureFileName.split('/')
                pureFileName = pureFileName[len(pureFileName)-1]
                pureFileName = pureFileName.replace(".hdr" , "")
                shutil.copy2('./Temp/'+pureFileName+'.gis.aux.xml', CarpetaXML)
                os.rename(CarpetaXML+'/'+pureFileName+'.gis.aux.xml',CarpetaXML+'/'+fileNameNoExt+'.xml')   
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
            MainWindow.consoleText("Converting to BIL...")
            CarpetaBIL = ConversePath+'/BIL'
            FullPathBIL = CarpetaBIL+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBIL)
                print (FullPathBIL)
                envi.save_image(FullPathBIL, img, force=True, ext="", interleave = 'bil')
                MainWindow.consoleText("DONE")                    
            except FileExistsError:
                print("ya existe")
                print (FullPathBIL)
                envi.save_image(FullPathBIL, img, force=True, ext="", interleave = 'bil')
                MainWindow.consoleText("DONE")
                
        if BIP == True:
            MainWindow.consoleText("Converting to BIP...")
            CarpetaBIP = ConversePath+'/BIP'
            FullPathBIP = CarpetaBIP+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBIP)
                envi.save_image(FullPathBIP, img, force=True, ext="", interleave = 'bip')
                MainWindow.consoleText("DONE")                  
            except FileExistsError:
                print("ya existe")
                envi.save_image(FullPathBIP, img, force=True, ext="", interleave = 'bip')
                MainWindow.consoleText("DONE")
   
        if BSQ == True:
            MainWindow.consoleText("Converting to BSQ...")
            CarpetaBSQ = ConversePath+'/BSQ'
            FullPathBSQ = CarpetaBSQ+'/'+fileNameNoExt+'.hdr'
            try:
                # Create target Directory
                os.mkdir(CarpetaBSQ)
                envi.save_image(FullPathBSQ, img, force=True, ext="", interleave = 'bsq')
                MainWindow.consoleText("DONE")                       
            except FileExistsError:
                print("ya existe")
                envi.save_image(FullPathBSQ, img, force=True, ext="", interleave = 'bsq')
                MainWindow.consoleText("DONE")

        QMessageBox.about(self, "", "Exported Succesfully")
        MainWindow.consoleText("Exported Succesfully")

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())