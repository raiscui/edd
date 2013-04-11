from PyQt4.QtCore import Qt, QLineF
from PyQt4.QtGui import QPen, QGraphicsView, QGraphicsScene

from edd.core.egraphhandle import EGraphHandle

from edd.gui.edummy import EDummy
from edd.gui.eedge import EEdge
from edd.gui.enode import ENode


class EScene(QGraphicsScene):

    def __init__(self, view=None, parent=None):
        QGraphicsScene.__init__(self, parent)

        if view is None:
            raise AttributeError

        self.__view = view
        self.__create__()

    def __create__(self):

        self.__gridSize = 35

        self.__isGridActive = True
        self.__isAltModifier = False
        self.__isControlModifier = False

        self.__kDummy = EDummy()
        self.__kDummy.setGridSize(self.__gridSize)
        self.__kDummy.onPress.connect(self.__onNodePressed)

        self.addItem(self.__kDummy)

        self.__nodes = {}
        self.__connections = {}

        self.__graphHandle = EGraphHandle()
        self.__graphHandle.Message.connect(self.__messageFilter)

    def __isNode(self, EObject):
        return isinstance(EObject, ENode)

    def __onNodePressed(self):
        if self.__isNode(self.sender()):
            self.__graphHandle.process(self.sender().mapFromPoint(self.__kDummy.scenePos()))
            return

        if not self.__kDummy.isEditMode():
            self.__graphHandle.process(self.__kDummy.Id)

    def __getDataFromId(self, theId):
        handle = self.__graphHandle.getHandleFromId(theId)
        if handle:
            return self.__nodes[handle].mapFromId(theId)

        return None

    def __getResultMessageFromConnection(self, conn):
        return

    def __messageFilter(self, message):

        if message.match(EGraphHandle.kMessageEditBegin):
            #print 'Debug message: Edit begin...'
            self.__kDummy.toggleEditMode()
            return

        if message.match(EGraphHandle.kMessageEditEnd):
            #print 'Debug message: Edit end...'
            if self.__kDummy.isEditMode():
                self.__kDummy.toggleEditMode()
            return

        if message.match(EGraphHandle.kMessageNodeAdded):
            self.addItem(ENode(message.getData()))
            return

        if message.match(EGraphHandle.kMessageNodeRemoved):
            return

        if message.match(EGraphHandle.kMessageConnectionMade):

            dataOne = self.__getDataFromId(message.getData()[0])
            dataTwo = self.__getDataFromId(message.getData()[1])

            if dataOne and dataTwo:

                conn = EEdge(dataOne, dataTwo, message.getData()[2])
                self.__connections[conn.Id] = conn
                self.addItem(conn)

                headData = conn.Head
                tailData = conn.Tail

                print 'Result: Connected %s.%s to %s.%s' % (headData[ENode.kGuiAttributeParentName],
                                                            headData[ENode.kGuiAttributeLongName],
                                                            tailData[ENode.kGuiAttributeParentName],
                                                            tailData[ENode.kGuiAttributeLongName])

            return

        if message.match(EGraphHandle.kMessageConnectionBroke):
            if message.getData() in self.__connections.keys():
                self.removeItem(self.__connections[message.getData()])

                self.__connections.pop(message.getData(), None)

                self.update()

                #print "Disconnected..."

            return

        if message.match(EGraphHandle.kMessageUnknown) or message.match(EGraphHandle.kMessageInternalError):
            print 'No event <%s>' % message.getData()
            if self.__kDummy.isEditMode():
                self.__kDummy.toggleEditMode()
                self.update()

    @property
    def Handle(self):
        return self.__graphHandle

    def build(self, handle):
        if not isinstance(handle, EGraphHandle):
            raise AttributeError

    def addItem(self, QGraphicsItem):

        if self.__isNode(QGraphicsItem):
            QGraphicsItem.setZValue(0.0)
            QGraphicsItem.onPress.connect(self.__onNodePressed)

            self.__nodes[QGraphicsItem.Id] = QGraphicsItem

        QGraphicsScene.addItem(self, QGraphicsItem)

    def cwd(self):
        return self.__graphHandle

    def ls(self):
        return self.__nodes.values()

    def drawBackground(self, painter, rect):
        self.update()

        if self.__isGridActive:

            painter.setPen(Qt.NoPen)
            painter.fillRect(rect, Qt.lightGray)

            left = int(rect.left()) - (int(rect.left()) % self.__gridSize)
            top = int(rect.top()) - (int(rect.top()) % self.__gridSize)
            lines = []
            right = int(rect.right())
            bottom = int(rect.bottom())
            for x in range(left, right, self.__gridSize):
                lines.append(QLineF(x, rect.top(), x, rect.bottom()))
            for y in range(top, bottom, self.__gridSize):
                lines.append(QLineF(rect.left(), y, rect.right(), y))

            painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
            painter.drawLines(lines)
            return

        painter.fillRect(rect, Qt.lightGray)

    def mouseMoveEvent(self, mouseEvent):
        QGraphicsScene.mouseMoveEvent(self, mouseEvent)

        self.__kDummy.setPos(mouseEvent.scenePos())

    def mousePressEvent(self, mouseEvent):
        QGraphicsScene.mousePressEvent(self, mouseEvent)

        if self.__isControlModifier:
            return

        if mouseEvent.button() == Qt.RightButton:
            self.__kDummy.toggleEditMode()

    def mouseReleaseEvent(self, mouseEvent):

        if mouseEvent.button() == Qt.RightButton:
            self.__kDummy.toggleEditMode()

        self.update()

        QGraphicsScene.mouseReleaseEvent(self, mouseEvent)

    def keyPressEvent(self, keyEvent):
        QGraphicsScene.keyPressEvent(self, keyEvent)

        if keyEvent.key() == Qt.Key_Control:
            self.__view.setDragMode(QGraphicsView.ScrollHandDrag)
            self.__isControlModifier = True

        if keyEvent.key() == Qt.Key_Alt:
            self.__isAltModifier = True
            self.__previousSelectedNode = None

        if keyEvent.key() == 88:
            self.__kDummy.setSnapMode(True)

    def keyReleaseEvent(self, keyEvent):
        QGraphicsScene.keyReleaseEvent(self, keyEvent)

        if keyEvent.key() == Qt.Key_Control:
            self.__view.setDragMode(QGraphicsView.NoDrag)
            self.__isControlModifier = False

        if keyEvent.key() == Qt.Key_Alt:
            self.__isAltModifier = False
            self.__previousSelectedNode = None

        if keyEvent.key() == 88:
            self.__kDummy.setSnapMode(False)


        
        

