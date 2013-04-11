import sys
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QMainWindow, QSplitter, QTabWidget, QTextEdit

from edd.gui.escene import EScene
from edd.gui.eview import EView

from edd.core.enodehandle import ENodeHandle


class MyNode(ENodeHandle):

    def __init__(self, name):
        ENodeHandle.__init__(self, name)

        self.addInputAttribute("Input")
        self.addOutputAttribute("Output")


class ExampleScene(EScene):

    def __init__(self, view):
        EScene.__init__(self, view)

        return

    def createConnected(self):

        nodeOne = MyNode("MyNode1")
        nodeTwo = MyNode("MyNode2")

        self.cwd().addNode(nodeOne)
        self.cwd().addNode(nodeTwo)

        self.cwd().connectAttributes(nodeOne.getAttributeByName('Output')[0], nodeTwo.getAttributeByName('Input')[0])

if __name__ == "__main__":

    app = QApplication(sys.argv)

    # Setup workspace controls
    kWorkspaceSplitter = QSplitter(Qt.Vertical)
    kWorkspaceSplitter.setObjectName('mainSplitter')

    kResourceTabs = QTabWidget()
    kResourceTabs.setObjectName('kMainTab')
    kResourceTabs.setTabPosition(QTabWidget.South)

    theView = EView()
    theView.Scene = ExampleScene(theView)

    #theView.Scene.createConnected()

    kResourceTabs.addTab(theView, "Workspace")
    kWorkspaceSplitter.addWidget(kResourceTabs)

    console = QTextEdit()


    kWorkspaceSplitter.addWidget(console)

    window = QMainWindow()
    window.setWindowTitle('EDD - Standalone')
    window.setCentralWidget(kWorkspaceSplitter)

    window.show()
    sys.exit(app.exec_())

