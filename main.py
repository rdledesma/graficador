from PyQt5 import QtWidgets, uic
import sys
from PyQt5.QtWidgets import QApplication, QFileDialog

import pandas as pd
import matplotlib.pyplot as plt
import Geo

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('graph.ui', self) # Load the .ui file
        
        self.selFileButton.clicked.connect(self.openFileNameDialog)
        self.graphButton.clicked.connect(self.plot)
        self.exportButton.clicked.connect(self.exportFile)
        self.show() # Show the GUI
        
    
    
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if fileName:
           self.fileLabel.setText(fileName)
           
           
           sep = self.separatorEditText.text()
           
           self.df = pd.read_csv(fileName, sep=sep)
           self.df['Fecha'] = pd.to_datetime(self.df.Fecha)
           
           #date_range = pd.to_datetime(self.dfImport.Fecha)
           
           self.geoButton.clicked.connect(self.appendGeoInfo)
           
           

           
           
           
           
           
           # self.dfImport = (self.dfImport.set_index('Fecha')
           #        .reindex(date_range)
           #        .rename_axis(['Fecha'])
           #        .fillna(0)
           #        .reset_index())

           
           #self.df['Clear sky BHI'] = self.dfImport['Clear sky BHI'].values
           self.updateTableWidget()
           # self.dfTableWidget.setColumnCount(len(self.df.columns))
           # self.dfTableWidget.setRowCount(len(self.df))
           # self.dfTableWidget.setHorizontalHeaderLabels(self.df.columns)
           
           # self.dfShow = self.df
           
           # self.setDates()
           
           # for i in range(len(self.df)):
           #     for j in range(len(self.df.columns)):
           #         self.dfTableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(self.df.iat[i,j])))


    def setDates(self):
        self.df.Fecha = pd.to_datetime(self.df.Fecha)
        #print(self.df.Fecha.Min())
        #self.dateInitLabel.setText("")

    def plot(self):
        
    
        self.desde = str(self.dateInitEditText.date().month())+'/'+ str(self.dateInitEditText.date().day()) + '/'+str(self.dateInitEditText.date().year())
        self.hasta = str(self.dateFinishEditText.date().month())+'/'+ str(self.dateFinishEditText.date().day()) + '/'+str(self.dateFinishEditText.date().year())
        self.alt = int(self.altEditText.text())
        self.df = Geo.Geo(freq='60', lat=-31.28, long=-57.92, gmt=-3, alt=self.alt, desde=self.desde, hasta=self.hasta, beta=0).df
        self.updateTableWidget()
        
    def appendGeoInfo(self):
        self.alt = int(self.altEditText.text())
        date_range = pd.to_datetime(self.df.Fecha)
        dfGeo = Geo.Geo(range_dates=date_range ,lat=-31.28, long=-57.92, gmt=-3, alt=self.alt, beta=0).df
        self.df = pd.merge(self.df, dfGeo)
        
        self.updateTableWidget()
    
    
    def exportFile(self):
        fileName = self.exportEditText.text()
        self.df.to_csv(fileName, index=False)
    
    def updateTableWidget(self):
        
        self.dfTableWidget.setColumnCount(len(self.df.columns))
        self.dfTableWidget.setRowCount(len(self.df))
        self.dfTableWidget.setHorizontalHeaderLabels(self.df.columns)
        for i in range(len(self.df)):
            for j in range(len(self.df.columns)):
                self.dfTableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(self.df.iat[i,j])))

        
        GHIcc = self.df['GHIargp']
        plt.plot(GHIcc, label="GHIcc")
        plt.legend()
        plt.show()
    

if __name__ == '__main__':

    
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    

    
    app.exec_()
    



    

