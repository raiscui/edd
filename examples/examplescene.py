import sys
from PyQt4.QtCore import Qt, QByteArray
from PyQt4.QtGui import QApplication, QMainWindow, QSplitter, QTabWidget, QTextEdit, QLabel, QImage, QPixmap

from edd.gui.escene import EScene
from edd.gui.eview import EView

from edd.core.enodehandle import ENodeHandle


from PIL import Image, ImageQt
import numpy


class ViewNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.__inputAttr = self.addInputAttribute("Input")
        self.__outputAttr = self.addOutputAttribute("Output")
        self.__control = None

    def setControl(self, control):
        self.__control = control

    def compute(self, plug, data=None):

        im = Image.fromarray(self.__inputAttr.Data)
        self.__data = data or im.convert("RGBA").tostring("raw", "RGBA")

        image = QImage(self.__data, im.size[0], im.size[1], QImage.Format_ARGB32)
        pix = QPixmap.fromImage(image)

        self.__control.setPixmap(pix)


class FileNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.__inputAttr = Image.open("C:\Users\Portable\Desktop\env.jpg")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self, plug, data=None):

        self.__outputAttr.Data = numpy.array(self.__inputAttr)
        print "%s computed..." % self.Name


class BlurNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.__size = 10
        self.__inputAttr = self.addInputAttribute("Input")
        self.__outputAttr = self.addOutputAttribute("Output")

    def compute(self, plug, data=None):

        if self.__inputAttr.Data is None:
            return

        from scipy import ndimage
        theData = self.__inputAttr.Data
        r = theData[:, :, 0]
        g = theData[:, :, 1]
        b = theData[:, :, 2]
        r = ndimage.gaussian_filter(r, order=0, sigma=self.__size)
        g = ndimage.gaussian_filter(g, order=0, sigma=self.__size)
        b = ndimage.gaussian_filter(b, order=0, sigma=self.__size)

        self.__outputAttr.Data = numpy.dstack((r, g, b))


class ExampleScene(EScene):

    def __init__(self, view):
        EScene.__init__(self, view)
        self.__control = None
        return

    def createConnected(self):

        fileNode = FileNode("File")
        blurNode1 = BlurNode("Blur1")
        blurNode2 = BlurNode("Blur2")
        viewNode = ViewNode("Viewer")
        viewNode.setControl(self.__control)

        dummyNode = BlurNode("Dummy")

        self.cwd().addNode(fileNode)
        self.cwd().addNode(blurNode1)
        self.cwd().addNode(blurNode2)
        self.cwd().addNode(viewNode)
        self.cwd().addNode(dummyNode)

        #self.cwd().connectAttributes(nodeOne.getAttributeByName('Output')[0], nodeTwo.getAttributeByName('Input')[0])

    def setControl(self, control):
        self.__control = control

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Setup workspace controls
    kWorkspaceSplitter = QSplitter(Qt.Horizontal)
    kWorkspaceSplitter.setObjectName('mainSplitter')

    kResourceTabs = QTabWidget()
    kResourceTabs.setObjectName('kMainTab')
    kResourceTabs.setTabPosition(QTabWidget.South)

    theView = EView()
    theView.Scene = ExampleScene(theView)

    console = QLabel()

    kResourceTabs.addTab(theView, "Workspace")
    kWorkspaceSplitter.addWidget(console)
    kWorkspaceSplitter.addWidget(kResourceTabs)

    theView.Scene.setControl(console)
    theView.Scene.createConnected()

    window = QMainWindow()
    window.setWindowTitle('EDD - Standalone')
    window.setCentralWidget(kWorkspaceSplitter)

    window.show()
    sys.exit(app.exec_())

