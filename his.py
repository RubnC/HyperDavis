#!/usr/bin/python3
# -*- coding: utf-8 -*-



import sys
from PyQt5.QtCore import QDir, Qt
from spectral import *
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication, QFileDialog, QLabel, QMessageBox, QSizePolicy, QScrollArea
from PyQt5.QtGui import QIcon, QPixmap, QColor, QPalette, QImage


class Example(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):               
        
        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)

        exitAction = QAction(QIcon('./icons/exit.png'), 'Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.close)

        openAction = QAction(QIcon('./icons/open.png'), 'Open', self)
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open File')
        openAction.triggered.connect(self.showDialog)  

        #fitwindowAction = QAction('Fit to window', self)
        #fitwindowAction.setShortcut('Ctrl+F')
        #fitwindowAction.setEnabled(False)
        #fitwindowAction.isChecked(True)
        #fitwindowAction.triggered.connect(self.fitToWindow)
     

        newAction = QAction(QIcon('new.png'), 'New', self)
        newAction.setShortcut('Ctrl+N')
        newAction.setStatusTip('New File')

        self.zoominAction = QAction(QIcon('zoomin.png'), 'Zoom in',  self)
        self.zoominAction.setShortcut('Ctrl++')
        self.zoominAction.setStatusTip('Zoom in')
        self.zoominAction.setEnabled(False)
        self.zoominAction.triggered.connect(self.zoomIn)

        self.normAction = QAction(QIcon('norm.png'), 'Original Size',  self)
        #self.normAction.setShortcut('Ctrl+N')
        self.normAction.setStatusTip('Original Size')
        self.normAction.setEnabled(False)
        self.normAction.triggered.connect(self.norm)

        self.zoomoutAction = QAction(QIcon('zoomout.png'), 'Zoom out', self)
        #self.zoomoutAction.setShortcut('Ctrl+-')
        self.zoomoutAction.setStatusTip('Zoom out')
        self.zoomoutAction.setEnabled(False)
        self.zoomoutAction.triggered.connect(self.zoomOut)

        self.cursorAction = QAction(QIcon('cursor.png'), 'Cursor', self)
        #self.cursorAction.setShortcut('Ctrl+N')
        self.cursorAction.setStatusTip('Cursor')
        self.cursorAction.setEnabled(False)

        self.gridAction = QAction(QIcon('grid.png'), 'Grid', self)
        self.gridAction.setShortcut('Ctrl+G')
        self.gridAction.setStatusTip('Grid')
        self.gridAction.setEnabled(False)

        self.polylineAction = QAction(QIcon('polyline.png'), 'Draw Polyline', self)
        self.polylineAction.setShortcut('Ctrl+D')
        self.polylineAction.setStatusTip('Draw Polyline')
        self.polylineAction.setEnabled(False)

        self.analyzeAction = QAction(QIcon('analyze.png'), 'Analyze', self)
        self.analyzeAction.setShortcut('Ctrl+A')
        self.analyzeAction.setStatusTip('Analyze')
        self.analyzeAction.setEnabled(False)

        self.joinAction = QAction(QIcon('join.png'), 'Join', self)
        self.joinAction.setShortcut('Ctrl+J')
        self.joinAction.setStatusTip('Join')
        self.joinAction.setEnabled(False)

        self.filterinAction = QAction(QIcon('filter.png'), 'Filters', self)
        #filterinAction.setShortcut('Ctrl+F')
        self.filterinAction.setStatusTip('Filters')
        self.filterinAction.setEnabled(False)

        self.filterClearAction = QAction(QIcon('ClearFilters.png'), 'Clear Filters', self)
        self.filterClearAction.setShortcut('Ctrl+C')
        self.filterClearAction.setStatusTip('Clear Filters')
        self.filterClearAction.setEnabled(False)

        self.chart1Action = QAction(QIcon('chart1.png'), 'Chart 1', self)
        self.chart1Action.setShortcut('Ctrl+1')
        self.chart1Action.setStatusTip('Chart 1')
        self.chart1Action.setEnabled(False)

        self.chart2Action = QAction(QIcon('chart2.png'), 'Chart 2', self)
        self.chart2Action.setShortcut('Ctrl+2')
        self.chart2Action.setStatusTip('Chart 2')
        self.chart2Action.setEnabled(False)

        self.chart3Action = QAction(QIcon('chart3.png'), 'Chart 3', self)
        self.chart3Action.setShortcut('Ctrl+3')
        self.chart3Action.setStatusTip('Chart 3')
        self.chart3Action.setEnabled(False)

        self.combochartAction = QAction(QIcon('ComboChart.png'), 'Combo Chart', self)
        self.combochartAction.setShortcut('Ctrl+4')
        self.combochartAction.setStatusTip('Chart 4')
        self.combochartAction.setEnabled(False)

        self.playAction = QAction(QIcon('play.png'), 'Play', self)
        self.playAction.setShortcut('Ctrl+ ')
        self.playAction.setStatusTip('Play')
        self.playAction.setEnabled(False)

        self.aboutAction = QAction('About', self)
        self.aboutAction.setStatusTip('About')
        

        self.saveAction = QAction('Save', self)
        self.saveAction.setShortcut('Ctrl+S')
        self.saveAction.setEnabled(False)

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
        EditMenu.addAction(self.zoominAction)
        EditMenu.addAction(self.normAction)
        EditMenu.addAction(self.zoomoutAction)
        EditMenu.addSeparator()

        fileMenu.addAction(exitAction)
              
        viewMenu = menubar.addMenu('View')
        viewMenu.addAction('Charts')
        #viewMenu.addAction(fitwindowAction)

        toolsMenu = menubar.addMenu('Tools')
        toolsMenu.addAction('Wavelength')
        toolsMenu.addAction('Filter')
        windowMenu = menubar.addMenu('Window')
        action5 = windowMenu.addAction('Charts')
        helpMenu = menubar.addMenu('Help')
        helpMenu.addAction('Tutorial')
        helpMenu.addAction('Report a bug')
        helpMenu.addAction('Manual')
        helpMenu.addAction(self.aboutAction)

        self.scaleFactor = 0.0
        #self.printer = QPrinter()
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.scrollArea = QScrollArea()
        self.scrollArea.setBackgroundRole(QPalette.Dark)
        self.scrollArea.setWidget(self.imageLabel)
        self.setCentralWidget(self.scrollArea)


#TOOLBAR
        toolbar = self.addToolBar('Open')
        toolbar.addAction(newAction)
        toolbar.addAction(openAction)
        toolbar1 = self.addToolBar('Tools')
        toolbar1.addAction(self.zoominAction)
        toolbar1.addAction(self.normAction)
        toolbar1.addAction(self.zoomoutAction)
        toolbar1.addAction(self.cursorAction)
        toolbar1.addAction(self.polylineAction)
        toolbar1.addAction(self.gridAction)
        toolbar1.addAction(self.filterinAction)
        toolbar1.addAction(self.filterClearAction)
        toolbar1.addAction(self.joinAction)
        toolbar1.addAction(self.analyzeAction)
        toolbar1.addAction(self.chart1Action)
        toolbar1.addAction(self.chart2Action)
        toolbar1.addAction(self.chart3Action)
        toolbar1.addAction(self.combochartAction)
        toolbar1.addAction(self.playAction)

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

    def showDialog(self):
        #fileName, _ = QFileDialog.getOpenFileName(self,"Open Files", '/desktop',"Images (*.*)")
        #options = QFileDialog.Options()
        #options |= QFileDialog.DontUseNativeDialog
        #fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        #fname = QFileDialog.getOpenFileName(self, 'Open file', '/desktop')
        label = QLabel(self)
        self.setCentralWidget(label)
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
        
        
        view = imshow(img, (29, 19, 9))
        #BsqFile
        #view_cube(img, bands=[29, 19, 9])
        print (img)
        self.saveAction.setEnabled(True)

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

    def getPos(self , event):
        x = event.pos().x()
        y = event.pos().y() 
        print (x, y)

    def zoomIn(self):
        self.scaleImage(1.2)

    def norm(self):
        self.imageLabel.adjustSize()
        self.scaleFactor = 1.0

    def zoomOut(self):
        self.scaleImage(0.8)

    #def updateActions(self):
    #    self.zoomInAct.setEnabled(not self.fitToWindowAct.isChecked())
    #    self.zoomOutAct.setEnabled(not self.fitToWindowAct.isChecked())
    #    self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def scaleImage(self, factor):
        self.scaleFactor *= factor
        self.imageLabel.resize(self.scaleFactor * self.imageLabel.pixmap().size())

        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep()/2)))
   
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())