# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'examples/VideoTemplate.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(695, 798)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.downsampleCheck = QtGui.QCheckBox(self.centralwidget)
        self.downsampleCheck.setObjectName(_fromUtf8("downsampleCheck"))
        self.gridLayout_2.addWidget(self.downsampleCheck, 8, 0, 1, 2)
        self.scaleCheck = QtGui.QCheckBox(self.centralwidget)
        self.scaleCheck.setObjectName(_fromUtf8("scaleCheck"))
        self.gridLayout_2.addWidget(self.scaleCheck, 4, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.rawRadio = QtGui.QRadioButton(self.centralwidget)
        self.rawRadio.setObjectName(_fromUtf8("rawRadio"))
        self.gridLayout.addWidget(self.rawRadio, 3, 0, 1, 1)
        self.gfxRadio = QtGui.QRadioButton(self.centralwidget)
        self.gfxRadio.setChecked(True)
        self.gfxRadio.setObjectName(_fromUtf8("gfxRadio"))
        self.gridLayout.addWidget(self.gfxRadio, 2, 0, 1, 1)
        self.stack = QtGui.QStackedWidget(self.centralwidget)
        self.stack.setObjectName(_fromUtf8("stack"))
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.gridLayout_3 = QtGui.QGridLayout(self.page)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.graphicsView = GraphicsView(self.page)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_3.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.stack.addWidget(self.page)
        self.page_2 = QtGui.QWidget()
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.page_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.rawImg = RawImageWidget(self.page_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rawImg.sizePolicy().hasHeightForWidth())
        self.rawImg.setSizePolicy(sizePolicy)
        self.rawImg.setObjectName(_fromUtf8("rawImg"))
        self.gridLayout_4.addWidget(self.rawImg, 0, 0, 1, 1)
        self.stack.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stack, 0, 0, 1, 1)
        self.rawGLRadio = QtGui.QRadioButton(self.centralwidget)
        self.rawGLRadio.setObjectName(_fromUtf8("rawGLRadio"))
        self.gridLayout.addWidget(self.rawGLRadio, 4, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 1, 0, 1, 4)
        self.dtypeCombo = QtGui.QComboBox(self.centralwidget)
        self.dtypeCombo.setObjectName(_fromUtf8("dtypeCombo"))
        self.dtypeCombo.addItem(_fromUtf8(""))
        self.dtypeCombo.addItem(_fromUtf8(""))
        self.dtypeCombo.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.dtypeCombo, 3, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 3, 0, 1, 1)
        self.rgbLevelsCheck = QtGui.QCheckBox(self.centralwidget)
        self.rgbLevelsCheck.setObjectName(_fromUtf8("rgbLevelsCheck"))
        self.gridLayout_2.addWidget(self.rgbLevelsCheck, 4, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.minSpin2 = SpinBox(self.centralwidget)
        self.minSpin2.setEnabled(False)
        self.minSpin2.setObjectName(_fromUtf8("minSpin2"))
        self.horizontalLayout_2.addWidget(self.minSpin2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.maxSpin2 = SpinBox(self.centralwidget)
        self.maxSpin2.setEnabled(False)
        self.maxSpin2.setObjectName(_fromUtf8("maxSpin2"))
        self.horizontalLayout_2.addWidget(self.maxSpin2)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 5, 2, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.minSpin1 = SpinBox(self.centralwidget)
        self.minSpin1.setObjectName(_fromUtf8("minSpin1"))
        self.horizontalLayout.addWidget(self.minSpin1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout.addWidget(self.label_2)
        self.maxSpin1 = SpinBox(self.centralwidget)
        self.maxSpin1.setObjectName(_fromUtf8("maxSpin1"))
        self.horizontalLayout.addWidget(self.maxSpin1)
        self.gridLayout_2.addLayout(self.horizontalLayout, 4, 2, 1, 1)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.minSpin3 = SpinBox(self.centralwidget)
        self.minSpin3.setEnabled(False)
        self.minSpin3.setObjectName(_fromUtf8("minSpin3"))
        self.horizontalLayout_3.addWidget(self.minSpin3)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.maxSpin3 = SpinBox(self.centralwidget)
        self.maxSpin3.setEnabled(False)
        self.maxSpin3.setObjectName(_fromUtf8("maxSpin3"))
        self.horizontalLayout_3.addWidget(self.maxSpin3)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 6, 2, 1, 1)
        self.lutCheck = QtGui.QCheckBox(self.centralwidget)
        self.lutCheck.setObjectName(_fromUtf8("lutCheck"))
        self.gridLayout_2.addWidget(self.lutCheck, 7, 0, 1, 1)
        self.alphaCheck = QtGui.QCheckBox(self.centralwidget)
        self.alphaCheck.setObjectName(_fromUtf8("alphaCheck"))
        self.gridLayout_2.addWidget(self.alphaCheck, 7, 1, 1, 1)
        self.gradient = GradientWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.gradient.sizePolicy().hasHeightForWidth())
        self.gradient.setSizePolicy(sizePolicy)
        self.gradient.setObjectName(_fromUtf8("gradient"))
        self.gridLayout_2.addWidget(self.gradient, 7, 2, 1, 2)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 3, 3, 1, 1)
        self.fpsLabel = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.fpsLabel.setFont(font)
        self.fpsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fpsLabel.setObjectName(_fromUtf8("fpsLabel"))
        self.gridLayout_2.addWidget(self.fpsLabel, 0, 0, 1, 4)
        self.rgbCheck = QtGui.QCheckBox(self.centralwidget)
        self.rgbCheck.setObjectName(_fromUtf8("rgbCheck"))
        self.gridLayout_2.addWidget(self.rgbCheck, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 2, 0, 1, 1)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.framesSpin = QtGui.QSpinBox(self.centralwidget)
        self.framesSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.framesSpin.setProperty("value", 10)
        self.framesSpin.setObjectName(_fromUtf8("framesSpin"))
        self.horizontalLayout_4.addWidget(self.framesSpin)
        self.widthSpin = QtGui.QSpinBox(self.centralwidget)
        self.widthSpin.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.widthSpin.setMaximum(10000)
        self.widthSpin.setProperty("value", 512)
        self.widthSpin.setObjectName(_fromUtf8("widthSpin"))
        self.horizontalLayout_4.addWidget(self.widthSpin)
        self.heightSpin = QtGui.QSpinBox(self.centralwidget)
        self.heightSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.heightSpin.setMaximum(10000)
        self.heightSpin.setProperty("value", 512)
        self.heightSpin.setObjectName(_fromUtf8("heightSpin"))
        self.horizontalLayout_4.addWidget(self.heightSpin)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 2, 1, 1, 2)
        self.sizeLabel = QtGui.QLabel(self.centralwidget)
        self.sizeLabel.setText(_fromUtf8(""))
        self.sizeLabel.setObjectName(_fromUtf8("sizeLabel"))
        self.gridLayout_2.addWidget(self.sizeLabel, 2, 3, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stack.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.downsampleCheck.setText(_translate("MainWindow", "Auto downsample", None))
        self.scaleCheck.setText(_translate("MainWindow", "Scale Data", None))
        self.rawRadio.setText(_translate("MainWindow", "RawImageWidget", None))
        self.gfxRadio.setText(_translate("MainWindow", "GraphicsView + ImageItem", None))
        self.rawGLRadio.setText(_translate("MainWindow", "RawGLImageWidget", None))
        self.dtypeCombo.setItemText(0, _translate("MainWindow", "uint8", None))
        self.dtypeCombo.setItemText(1, _translate("MainWindow", "uint16", None))
        self.dtypeCombo.setItemText(2, _translate("MainWindow", "float", None))
        self.label.setText(_translate("MainWindow", "Data type", None))
        self.rgbLevelsCheck.setText(_translate("MainWindow", "RGB", None))
        self.label_3.setText(_translate("MainWindow", "<--->", None))
        self.label_2.setText(_translate("MainWindow", "<--->", None))
        self.label_4.setText(_translate("MainWindow", "<--->", None))
        self.lutCheck.setText(_translate("MainWindow", "Use Lookup  Table", None))
        self.alphaCheck.setText(_translate("MainWindow", "alpha", None))
        self.fpsLabel.setText(_translate("MainWindow", "FPS", None))
        self.rgbCheck.setText(_translate("MainWindow", "RGB", None))
        self.label_5.setText(_translate("MainWindow", "Image size", None))

from spectrochempy.extern.pyqtgraph import GradientWidget, GraphicsView, SpinBox
from spectrochempy.extern.pyqtgraph.widgets.RawImageWidget import RawImageWidget
