from edd.core.eobject import EObject
from edd.core.eattribute import EAttribute


class EEdgeHandle(EObject):

    def __init__(self, head, tail):
        EObject.__init__(self)
        self.__head = head
        self.__tail = tail

    @property
    def Head(self):
        return self.__head

    @property
    def Tail(self):
        return self.__tail


