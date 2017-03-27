# Python 3.5.3
# PyQt 5.6.0

import sys, os, hashlib
from PyQt5.QtWidgets import QApplication, QPushButton, QGridLayout, QLabel, \
    QWidget, QComboBox, QSizePolicy, QFileDialog, QLineEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QDir, QCoreApplication

class MainWindow(QWidget):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        
        self.hashTextNoFile = 'No file selected.'
        self.hashText = self.hashTextNoFile
        self.hashChoices = sorted(hashlib.algorithms_available)
        
        # shake algorithms not supported yet due to the user having to specify a length
        # only affects Python 3.6 users, as shake algorithms are not available
        #    in previous versions of python anyway.
        self.hashChoices = [alg for alg in self.hashChoices if not alg.startswith('shake')]
        
        self.initUI()
        
        
    def initUI(self):
        
        self.dirComboBox = QComboBox(self)
        self.dirComboBox.setEditable(True)
        self.dirComboBox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.dirComboBox.currentIndexChanged.connect(self.computeHash)
        
        self.browseButton = QPushButton('&Browse...', self)
        self.browseButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.browseButton.clicked.connect(self.browse)
        
        self.hashAlgLabel = QLabel('Hash algorithm: ')
        self.hashAlgLabel.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.algComboBox = QComboBox(self)
        self.algComboBox.setEditable(False)
        self.algComboBox.addItems(self.hashChoices)
        self.algComboBox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.algComboBox.currentIndexChanged.connect(self.computeHash)
        
        self.fileHashTitle = QLabel('File Hash:')
        self.fileHashTitle.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        
        self.fileHashLabel = QLabel(self.hashTextNoFile)
        
        self.copyButton = QPushButton('&Copy', self)
        self.copyButton.clicked.connect(self.copyHashToClipboard)
        
        self.cmpHash = QLineEdit(self)
        self.cmpHash.setPlaceholderText('Paste hash here.')
        self.cmpHash.textChanged.connect(self.compareHashes)
        
        self.pasteButton = QPushButton('&Paste', self)
        self.pasteButton.clicked.connect(self.paste)
        
        self.resultLabel = QLabel()
        
        mainLayout = QGridLayout(self)
        mainLayout.addWidget(QLabel('File Location:'), 0, 0)
        mainLayout.addWidget(self.dirComboBox, 1, 0, 1, 3)
        mainLayout.addWidget(self.browseButton, 1, 3)
        mainLayout.addWidget(self.hashAlgLabel, 2, 0)
        mainLayout.addWidget(self.algComboBox, 2, 1)
        mainLayout.setRowMinimumHeight(3, 10)
        mainLayout.addWidget(self.fileHashTitle, 4, 0)
        mainLayout.addWidget(self.fileHashLabel, 4, 1, 1, 2)
        mainLayout.addWidget(self.copyButton, 4, 3)
        mainLayout.setRowMinimumHeight(5, 10)
        mainLayout.addWidget(QLabel('Hash to Compare:'), 6, 0)
        mainLayout.addWidget(self.cmpHash, 7, 0, 1, 3)
        mainLayout.addWidget(self.pasteButton, 7, 3)
        mainLayout.addWidget(self.resultLabel, 8, 0, 1, 4)
        
        self.setWindowIcon(QIcon('HashCheckerIcon.png'))
        self.setWindowTitle('Hash Checker')
        self.show()
        
        
    def browse(self):
        # Remove the "[0]" to make this file compatible with PyQt 4
        file = QDir.toNativeSeparators(QFileDialog.getOpenFileName(self, "Find File", QDir.currentPath())[0])
        
        if len(file) > 0:
            if self.dirComboBox.findText(file) == -1:
                self.dirComboBox.addItem(file)
            self.dirComboBox.setCurrentIndex(self.dirComboBox.findText(file))
        
        
    def computeHash(self):
        file = self.dirComboBox.currentText()
        if os.path.isfile(file):
            hashIdx = self.algComboBox.currentIndex()
            m = hashlib.new(self.hashChoices[hashIdx])
            f = open(self.dirComboBox.currentText(),"rb")
            m.update(f.read())
            f.close()
            self.hashText = m.hexdigest()
        else:
            self.hashText = self.hashTextNoFile
        
        self.fileHashLabel.setText(self.hashText)
        self.compareHashes()
        
        
    def copyHashToClipboard(self):
        if self.fileHashLabel.text() != self.hashTextNoFile:
            QCoreApplication.instance().clipboard().setText(self.fileHashLabel.text())
        
        
    def paste(self):
        self.cmpHash.setText(QCoreApplication.instance().clipboard().text())
        
        
    def compareHashes(self):
        if len(self.cmpHash.text()) == 0:
            self.resultLabel.setText('')
            return
        
        hashesEqual = self.fileHashLabel.text() == self.cmpHash.text()
        
        if hashesEqual:
            self.resultLabel.setText('It\'s a match!')
            self.resultLabel.setStyleSheet('color: green;')
        else:
            self.resultLabel.setText('No match!')
            self.resultLabel.setStyleSheet('color: red;')
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())