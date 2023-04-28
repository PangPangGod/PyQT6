import sys
import time
from PIL import Image
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, 
    QPushButton, QFileDialog, 
    QPlainTextEdit, QVBoxLayout, 
    QWidget, QLabel)



class MainWindow(QMainWindow):
    tempimglogbox = []
    folder = ''
    timenow = time.strftime("[%H:%M:%S]",time.localtime(time.time()))
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("JPEG Converter")
        widget = QWidget()
        layout = QVBoxLayout()
        
        #SaveRoute
        tempButton = QPushButton("Select Folder to Save")
        tempButton.clicked.connect(self.saveRoute)
        layout.addWidget(tempButton)

        #FileButton
        getFlieButton = QPushButton("Add Images")
        getFlieButton.clicked.connect(self.getFileNames)
        layout.addWidget(getFlieButton)
        
        #ConvertButton
        convertButton = QPushButton("Convert to JPEG Format")
        convertButton.clicked.connect(self.convertFlietoJPEG)
        layout.addWidget(convertButton)
        
        #fixed File Status
        self.fixed_text = QLabel()
        layout.addWidget(self.fixed_text)
        
        #TextBox
        self.textbox = QPlainTextEdit(" ** JPEG EDITOR MADE BY SJH. ver1.0.1** \n")
        layout.addWidget(self.textbox)
        
        #Size, ETC
        self.setFixedSize(QSize(500, 400))
        widget.setLayout(layout)
        self.setCentralWidget(widget)        

        
    #[현재시각]+file이름 textbox에 log형식으로

    
    
    def getFileNames(self): 
        imglogbox = MainWindow.tempimglogbox
        response = QFileDialog.getOpenFileNames(self)
        # os.mkdir(os.getcwd()+"/result",exist_ok=True)
        
        for i in response[0] :
            imglogbox.append(str(i))
            self.textbox.appendPlainText(f"[{MainWindow.timenow}] : {str(i)} has been saved. CONVERT IF YOU WANT")
        
        self.textbox.appendPlainText("======================================================")
        # img = Image.open(a[0])
        # img.show()
    
    
    def convertFlietoJPEG(self) : 
        imglogbox = MainWindow.tempimglogbox
        
        if imglogbox : 
            for i in imglogbox :
                img = Image.open(str(i))
                img_name = MainWindow.getImageName(img.filename)
                img = img.convert("RGB")
                
                #if there is no selected folder, Raise an saveRoute function.
                try :
                    img.save(f"{MainWindow.folder}/{img_name}.jpeg",'jpeg')
                    self.textbox.appendPlainText(f"[{MainWindow.timenow}] Convert Completed. Saved in : {MainWindow.folder}")
                    self.fixed_text.setText(f"Current Route is : {MainWindow.folder}")
                except PermissionError :
                    MainWindow.saveRoute(self)
                    img.save(f"{MainWindow.folder}/{img_name}.jpeg",'jpeg')
                    self.textbox.appendPlainText(f"[{MainWindow.timenow}] Convert Completed. Saved in : {MainWindow.folder}")
                    self.fixed_text.setText(f"Current Route is : {MainWindow.folder}")
            self.textbox.appendPlainText("======================================================")
                
        else :
            self.textbox.appendPlainText("======================================================")
            self.textbox.appendPlainText("ERROR : There is no Image to convert. Add Image Please.")
            self.textbox.appendPlainText("======================================================")
        
        MainWindow.tempimglogbox = []
    
    #Set Save Route    
    def saveRoute(self) :
        MainWindow.folder = QFileDialog.getExistingDirectory(self, "Self Directory")
        self.fixed_text.setText(f"Current Route is : {MainWindow.folder}")
    
    #File Format without Route
    def getImageName(file_location):
        filename = file_location.split('/')[-1]
        filename = filename.split('.')
        filename = filename[0]
        return filename
    
        
        
#구동기                                           
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
