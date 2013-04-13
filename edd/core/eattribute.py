from edd.core.eobject import EObject


class EAttribute(EObject):

    kTypeInput = EObject()
    kTypeOutput = EObject()
    kTypeProperty = EObject()

    kMessageAttributeSet = EObject()
    kMessageAttributeGet = EObject()
    kMessageAttributeRenamed = EObject()

    def __init__(self):
        EObject.__init__(self)

        self.__type = None

        self.__attrName = None
        self.__attrData = None
        self.__handle = None

    def create(self, attributeType, attributeName, attributeData=None):

        self.__type = attributeType
        self.__attrName = attributeName
        self.__attrData = attributeData

        return self

    @property
    def Type(self):
        return self.__type

    @property
    def Name(self):
        return self.__attrName

    @Name.setter
    def Name(self, name):
        self.__attrName = name

        self.Message.emit(self.kMessageAttributeRenamed)

    @property
    def Handle(self):
        return self.__handle

    @Handle.setter
    def Handle(self, handle):
        self.__handle = handle

    @property
    def Data(self):
        self.Message.emit(self.kMessageAttributeGet)

        return self.__attrData

    @Data.setter
    def Data(self, attrData):
        self.__attrData = attrData

        self.Message.emit(self.kMessageAttributeSet)

    def isInput(self):
        if self.__type == self.kTypeInput:
            return True

        return False

    def isOutput(self):
        if self.__type == self.kTypeOutput:
            return True

        return False

    @property
    def isArray(self):
        return None

    @isArray.setter
    def isArray(self, state):
        return

    def clear(self):
        self.__attrData = None







