from PyQt4.QtCore import Qt, QObject, pyqtSignal, QRectF
from PyQt4.QtGui import QPen, QPolygonF, QGraphicsItem, QGraphicsPolygonItem, QGraphicsTextItem, QColor

from edd.gui.utils.edraw import EDraw
from edd.gui.controls.econtrolsgroup import EControlsGroup

class EFrameLayout(QGraphicsPolygonItem):

    def __init__(self, parent=None, scene=None):
        super(EFrameLayout, self).__init__(parent, scene)

        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setAcceptsHoverEvents(True)

        self.__name = QGraphicsTextItem()
        self.__name.setPlainText('Frame Layout')

        self.__handleWidth = 500
        self.__handleHeight = 20
        self.__separator = 5
        self.__boundExtra = 3 + self.pen().width()
        self.__handleRect = QRectF( 0.0 , 0.0 , self.__handleWidth, self.__handleHeight  )

        self.__controlsBound = 0.0
        self.__controls = []

        self.__isDefaultPen = False
        self.__isCollapsed = True

        self.__pens = { 0: EDraw.EColor.DefaultLeaveHoverPen, 1: EDraw.EColor.DefaultEnterHoverPen }
        self.setPen(self.__pens[self.__isDefaultPen])

    @property
    def Label(self): return self.__name.toPlainText()

    @Label.setter
    def Label(self, label): self.__name.setPlainText( str( label ) )

    @property
    def Width(self): return self.__handleWidth

    @Width.setter
    def Width(self, width):
        self.__handleWidth = width
        self.updateGeometry()

    def toggleContentVisibility(self):
        if not len(self.__controls): return

        if self.__controls[0].isVisible():
            [ control.hide() for control in self.__controls ]
            self.__isCollapsed = True
            return

        [ control.show() for control in self.__controls ]
        self.__isCollapsed = False

    def updateGeometry(self):

        self.__handleRect = QRectF( 0.0 , 0.0 , self.__handleWidth, self.__handleHeight  )

        if not len(self.__controls) or self.__isCollapsed:
            self.__controlsBound = 0.0
            return

        self.__controlsBound = 0.0
        self.__controlsBound = self.__separator
        self.__controlsBound += sum( [ control.boundingRect().height() + self.__separator for control in self.__controls ] )

        step = self.__handleHeight + self.__separator * 2

        for control in self.__controls:

            control.Name.setTextWidth( self.__controlNameWidth )
            control.Width = self.__handleRect.normalized().adjusted( 5.0, 0.0, -5.0, 0.0 ).width()

            control.setPos( 5.0 , step )
            step += control.boundingRect().height() + self.__separator

    def addControl(self, control):
        if not isinstance(control, EControlsGroup): raise AttributeError

        self.__controls.append(control)
        control.setParentItem(self)
        control.setFlag(QGraphicsItem.ItemIsMovable, False)

        self.__controlNameWidth = max([ control.Name.boundingRect().width() for control in self.__controls ]) + 5

        self.__isCollapsed = False
        self.updateGeometry()

    def clear(self):
        [ control.setParentItem(None) for control in self.__controls ]
        self.__controls = []

        self.updateGeometry()

    def mouseDoubleClickEvent(self, mouseEvent):
        QGraphicsPolygonItem.mouseDoubleClickEvent(self, mouseEvent)

        self.toggleContentVisibility()
        self.updateGeometry()

    def shape(self): return QGraphicsItem.shape(self)

    def boundingRect(self):
        return self.__handleRect.normalized().adjusted( 0.0, 0.0, 0.0, self.__controlsBound )

    def paint(self, painter, option, widget=None):

        if not self.__isCollapsed:
            painter.setPen( QPen( QColor( 0, 0, 0, 50 ), 2 , Qt.SolidLine ) )
            painter.setBrush( QColor( 0, 0, 0, 50 ) )
            painter.drawRect( self.boundingRect().adjusted( self.pen().width(), self.__handleHeight , -self.pen().width(), 0.0 ) )

        painter.setPen(self.pen())
        painter.setBrush( EDraw.EColor.LinearGradient( self.__handleRect, Qt.darkGray ) )
        #painter.drawPolygon( QPolygonF( self.__handleRect.normalized().adjusted(-self.__boundExtra, 0.0, self.__boundExtra, 0.0 ) ) )
        painter.drawPolygon( QPolygonF( self.__handleRect ) )

        painter.setPen(Qt.lightGray)
        r = QRectF( 0.0, 0.0, self.__name.boundingRect().width(), self.__handleRect.height() )
        painter.drawText( r, Qt.AlignCenter, self.__name.toPlainText() )


