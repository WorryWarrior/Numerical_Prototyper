from qtpy import QtWidgets, QtCore, QtGui

from numerical_prototyper.numerical_paths import delete_button


class NumericalMethodCustomizationWidget(QtWidgets.QTabWidget):

    def __init__(self, parent):
        super(NumericalMethodCustomizationWidget, self).__init__(parent)

    def initUI(self):
        self.addTab(self.createLogicTab(), "Logic")
        self.addTab(self.createVariableTab(), "Variable")

        self.setTabPosition(QtWidgets.QTabWidget.East)
        self.setFixedWidth(150)

    def createLogicTab(self):
        scrollWidget, add = self.generateScrollWidget('Logic')

        from numerical_prototyper.numerical_node_customization_window_element \
            import IfElement, WhileElement, ForElement, BreakElement
        add(IfElement)
        add(WhileElement)
        add(ForElement)
        add(BreakElement)

        return scrollWidget

    def createVariableTab(self):
        scrollWidget, add = self.generateScrollWidget('Logic')

        from numerical_prototyper.numerical_node_customization_window_element \
            import VariableElement, LogElement

        add(VariableElement)
        add(LogElement)

        return scrollWidget

    def generateScrollWidget(self, tab):
        widget = QtWidgets.QWidget()
        vBox = QtWidgets.QVBoxLayout()
        vBox.setAlignment(QtCore.Qt.AlignTop)
        widget.setLayout(vBox)
        scrollWidget = QtWidgets.QScrollArea()
        scrollWidget.setWidget(widget)
        scrollWidget.setWidgetResizable(True)

        add = (lambda btnType: vBox.addWidget(self.generateButton(btnType, tab)))

        return scrollWidget, add

    def generateButton(self, commandType, tab):
        # newButton = self.DraggableButton(str(commandType), self)
        newButton = self.DraggableButton(str(commandType.__name__), self)

        newButton.setText(str(commandType.title))
        # newButton.setIcon(QtGui.QIcon(commandType.icon))

        # newButton.setIconSize(QtCore.QSize(100, 100))

        """
        newButton.setStyleSheet("QPushButton{border-radius : 20; border: 2px solid black; "
                                "background-color : rgb(0, 175, 220)}"
                                "QPushButton::hover"
                                "{border-radius : 20;border: 2px solid black;background-color : rgb(0, 210, 220)}")
        
        """
        newButton.setStyleSheet("border: 2px solid black; "
                                "background-color : rgb(255, 255, 255)}"
                                "QPushButton::hover"
                                "{border: 2px solid black;background-color : rgb(200, 200, 200)}")

        newButton.setFixedHeight(40)
        newButton.setFixedWidth(40)

        # newButton.customContextMenuRequested.connect(lambda: self.addCommandFunc(commandType))
        return newButton

    class DraggableButton(QtWidgets.QPushButton):
        def __init__(self, dragData, parent):
            super().__init__(parent)
            self.dragData = dragData

            self.mouse_down = False
            self.mouse_posn = QtCore.QPoint()

        def mousePressEvent(self, event):
            if event.button() == QtCore.Qt.LeftButton:
                self.mouse_down = True
                self.mouse_posn = event.pos()

            event.ignore()
            super().mousePressEvent(event)

        def mouseMoveEvent(self, event):
            if self.mouse_down:
                d = (event.pos() - self.mouse_posn).manhattanLength()

                if d >= QtWidgets.QApplication.startDragDistance():
                    self.dragEvent(QtCore.Qt.CopyAction | QtCore.Qt.MoveAction)
                    event.accept()
                    return

            event.ignore()
            super().mouseMoveEvent(event)

        def dragEvent(self, actions):
            dragster = QtGui.QDrag(self)

            thumb = self.grab()
            dragster.setPixmap(thumb)
            dragster.setHotSpot(QtCore.QPoint(thumb.width() / 2, thumb.height() / 2))

            md = QtCore.QMimeData()
            md.setText(self.dragData)
            dragster.setMimeData(md)

            dragster.exec_(actions)
            dragster.defaultAction()
            return


class NumericalMethodCustomizationCommandList(QtWidgets.QListWidget):

    def __init__(self, previewTextWindow):
        super(NumericalMethodCustomizationCommandList, self).__init__()

        from numerical_prototyper.numerical_node_customization_window_element import \
            NumericalCustomizationWindowElementBase, WhileElement, ForElement

        self.commands = {}

        for elementClass in NumericalCustomizationWindowElementBase.__subclasses__():
            self.commands[elementClass.__name__] = elementClass

        self.previewTextWindow = previewTextWindow
        self.logicCommands = [WhileElement, ForElement]

        self.initUI()

    def initUI(self):
        self.itemDoubleClicked.connect(self.doubleClickEvent)
        self.itemSelectionChanged.connect(self.selectionChangedEvent)
        self.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)
        self.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.setDefaultDropAction(QtCore.Qt.TargetMoveAction)

        self.changePreviewText()

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            super(NumericalMethodCustomizationCommandList, self).dragEnterEvent(event)

    def dragMoveEvent(self, event):
        if event.mimeData().hasText():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            super(NumericalMethodCustomizationCommandList, self).dragMoveEvent(event)

    def dropEvent(self, event):
        if event.mimeData().hasText():
            newPoint = event.pos()
            newPoint.setY(newPoint.y() + self.rectForIndex(self.indexFromItem(self.item(0))).height() / 2)
            dropIndex = self.indexAt(newPoint).row()
            if dropIndex == -1:
                dropIndex = self.count()

            self.scriptCommand = event.mimeData().text()
            cType = self.commands[event.mimeData().text()]
            newCom = self.addCommand(cType, index=dropIndex)

            from numerical_prototyper.numerical_node_customization_window_element \
                import OpenBlockElement, CloseBlockElement, IfElement, ElseElement, ElseIfElement, \
                CloseBlockSilentlyElement

            if cType in self.logicCommands:
                self.addCommand(OpenBlockElement, index=dropIndex + 1)
                self.addCommand(CloseBlockElement, index=dropIndex + 2)

            if cType is IfElement:
                conditionType = newCom.getParameterValue('-ConditionType')

                if conditionType == 0:
                    self.addCommand(OpenBlockElement, index=dropIndex + 1)
                    self.addCommand(CloseBlockElement, index=dropIndex + 2)
                if conditionType == 1:
                    self.addCommand(OpenBlockElement, index=dropIndex + 1)
                    self.addCommand(CloseBlockSilentlyElement, index=dropIndex + 2)
                    self.addCommand(ElseElement, index=dropIndex + 3)
                    self.addCommand(OpenBlockElement, index=dropIndex + 4)
                    self.addCommand(CloseBlockElement, index=dropIndex + 5)
                if conditionType == 2:
                    self.addCommand(OpenBlockElement, index=dropIndex + 1)
                    self.addCommand(CloseBlockSilentlyElement, index=dropIndex + 2)
                    self.addCommand(ElseIfElement, index=dropIndex + 3)
                    self.addCommand(OpenBlockElement, index=dropIndex + 4)
                    self.addCommand(CloseBlockSilentlyElement, index=dropIndex + 5)
                    self.addCommand(ElseElement, index=dropIndex + 6)
                    self.addCommand(OpenBlockElement, index=dropIndex + 7)
                    self.addCommand(CloseBlockElement, index=dropIndex + 8)

            event.accept()
        else:
            event.setDropAction(QtCore.Qt.MoveAction)
            super(NumericalMethodCustomizationCommandList, self).dropEvent(event)

        self.changePreviewText()
        self.refreshIndents()

    def addCommand(self, commandType, parameters=None, index=None):
        isLoading = parameters is not None
        if isLoading:
            newCommand = commandType(parameters=parameters)
        else:
            newCommand = commandType()

        newWidget = NumericalMethodCustomizationCommandListElement(self, self.deleteSelected)
        newWidget = newCommand.dressWidget(newWidget)

        listWidgetItem = QtWidgets.QListWidgetItem(self)
        listWidgetItem.setSizeHint(newWidget.sizeHint())

        if index is not None:
            lastRow = self.indexFromItem(listWidgetItem).row()
            takenListWidgetItem = self.takeItem(lastRow)
            self.insertItem(index, takenListWidgetItem)

        self.setItemWidget(listWidgetItem, newWidget)
        self.commands[newWidget] = newCommand

        self.addItem(listWidgetItem)

        if isLoading:
            newCommand.parameters = parameters
        else:
            accepted = newCommand.openWindow()

            if accepted:
                newCommand.dressWidget(newWidget)
            # else:
            # self.deleteItem(listWidgetItem)

        if not isLoading:
            self.refreshIndents()

        self.changePreviewText()

        return newCommand

    def doubleClickEvent(self, clickedItem):

        command = self.getCommand(clickedItem)
        if command:
            command.openWindow()
            self.changePreviewText()

            currentWidget = self.itemWidget(clickedItem)
            command.dressWidget(currentWidget)

            self.refreshIndents()

    def selectionChangedEvent(self):
        for i in range(self.count()):
            selectedWidget = self.itemWidget(self.item(i))
            if selectedWidget is not None:
                selectedWidget.setFocused(False)

        try:
            if len(self.selectedItems()):
                self.itemWidget(self.selectedItems()[0]).setFocused(True)
        except AttributeError:
            self.itemWidget(self.selectedItems()[0])


    def getCommand(self, listWidgetItem):
        if self.itemWidget(listWidgetItem):
            return self.commands[self.itemWidget(listWidgetItem)]

    def deleteItem(self, listWidgetItem):
        del self.commands[self.itemWidget(listWidgetItem)]
        self.itemWidget(listWidgetItem).deleteLater()
        self.takeItem(self.row(listWidgetItem))

    def deleteSelected(self):
        for item in self.selectedItems():
            self.deleteItem(item)

        self.changePreviewText()
        self.refreshIndents()

    def changePreviewText(self):
        from numerical_prototyper.numerical_node_customization_window_element \
            import OpenBlockElement, CloseBlockElement, CloseBlockSilentlyElement

        zeroAndAbove = (lambda i: (i < 0) * 0 + (i >= 0) * i)

        self.previewTextWindow.clear()
        self.previewTextWindow.setDefaultText()
        test = ''
        indentIncreaseElements = [OpenBlockElement]
        indentDecreaseElements = [CloseBlockElement, CloseBlockSilentlyElement]
        indentLevel = 0

        for index in range(self.count()):
            command = self.getCommand(self.item(index))

            if command is None:
                return

            commandType = type(command)

            if commandType in indentIncreaseElements:
                indentLevel += 1

            if commandType in indentDecreaseElements:
                indentLevel -= 1

            lineText = f'{self.getTextIndent(indentLevel)}{command.textValue}'

            if lineText.strip() != '':
                test += f'{lineText}\n'

        test += 'end'
        self.previewTextWindow.append(test)

    def getTextIndent(self, indentCount):
        res = ''

        for i in range(indentCount):
            res += '   '

        return res

    def refreshIndents(self):
        zeroAndAbove = (lambda i: (i < 0) * 0 + (i >= 0) * i)
        indent = 0

        from numerical_prototyper.numerical_node_customization_window_element \
            import OpenBlockElement, CloseBlockElement, CloseBlockSilentlyElement

        indentIncreaseElements = [OpenBlockElement]
        indentDecreaseElements = [CloseBlockElement, CloseBlockSilentlyElement]

        for index in range(self.count()):
            command = self.getCommand(self.item(index))
            if command:
                commandWidget = self.itemWidget(self.item(index))
                commandType = type(command)

                if commandType in indentIncreaseElements and self.count() >= 1:
                    indent += 1
                if self.count() >= 1:
                    commandWidget.setIndent(zeroAndAbove(indent))
                    command.indent = zeroAndAbove(indent)

                if commandType in indentDecreaseElements and self.count() >= 1:
                    indent -= 1
            else:
                return None

    def keyPressEvent(self, event):
        super(NumericalMethodCustomizationCommandList, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Delete:
            self.deleteSelected()

        if event == QtGui.QKeySequence.SelectAll:
            self.selectAll()

    def loadData(self, data):
        self.clear()
        for commandSave in data:
            newCommand = self.addCommand(self.commands[commandSave['type']], parameters=commandSave['parameters'])
            newCommand.loadTextValue()

        self.changePreviewText()

        self.refreshIndents()


    def getSaveData(self):
        commandList = []
        commandsOrdered = [self.getCommand(self.item(index)) for index in range(self.count())]

        for command in commandsOrdered:
            commandList.append(command.getSaveData())

        return commandList


class NumericalMethodCustomizationCommandListElement(QtWidgets.QWidget):

    def __init__(self, parent, onDeleteFunction):
        super(NumericalMethodCustomizationCommandListElement, self).__init__(parent)

        self.indent = 0
        self.margins = None

        self.title = QtWidgets.QLabel()
        self.description = QtWidgets.QLabel()
        self.icon = QtWidgets.QLabel()
        self.deleteBtn = QtWidgets.QPushButton()

        self.initUI()
        self.margins = self.layout().getContentsMargins()
        self.deleteBtn.clicked.connect(onDeleteFunction)

    def initUI(self):
        self.deleteBtn.setFlat(True)
        self.deleteBtn.setIcon(QtGui.QIcon(delete_button))
        self.deleteBtn.setVisible(False)

        bold = QtGui.QFont()
        bold.setBold(True)
        self.title.setFont(bold)

        midLayout = QtWidgets.QVBoxLayout()
        midLayout.setSpacing(1)
        midLayout.addWidget(self.title)
        #midLayout.addWidget(self.description)

        mainHLayout = QtWidgets.QHBoxLayout()
        # mainHLayout.addWidget(self.icon)
        mainHLayout.addLayout(midLayout, QtCore.Qt.AlignLeft)
        mainHLayout.addWidget(self.deleteBtn)
        self.setLayout(mainHLayout)

    def setTitle(self, text):
        self.title.setText(text)

    def setDescription(self, text):
        self.description.setText(text)

    def setFocused(self, isFocused):
        self.deleteBtn.setVisible(isFocused)

    def setIndent(self, indent):
        if self.indent == indent:
            return

        self.indent = indent
        if indent >= 0:
            self.layout().setContentsMargins(self.margins[0] + 25 * indent,
                                             self.margins[1],
                                             self.margins[2],
                                             self.margins[3])
        else:
            self.layout().setContentsMargins(self.margins[0],
                                             self.margins[1],
                                             self.margins[2],
                                             self.margins[3])


class NumericalMethodCustomizationPreviewWidget(QtWidgets.QTextEdit):

    def __init__(self, inputs, outputs, methodNameEdit):
        super(NumericalMethodCustomizationPreviewWidget, self).__init__()
        self.inputs = inputs
        self.outputs = outputs
        self.methodNameEdit = methodNameEdit
        self.inputIndices = {}
        self.outputIndices = {}

    def setDefaultText(self):
        self.resetTypeNameIndexDictionaries()

        defaultText = 'function['

        for i in range(len(self.outputs)):
            defaultText += f'out{self.getTypeName(self.outputs[i])}_'
            defaultText += f'{self.getTypeNameIndex(self.outputs[i], False)}'
            if i != len(self.outputs) - 1:
                defaultText += ', '

        defaultText += f']={self.methodNameEdit.text()}('

        for i in range(len(self.inputs)):
            defaultText += f'in{self.getTypeName(self.inputs[i])}_'
            defaultText += f'{self.getTypeNameIndex(self.inputs[i], True)}'
            if i != len(self.inputs) - 1:
                defaultText += ', '

        defaultText += ')'
        super().append(defaultText)

    def getTypeName(self, typeIndex):
        if typeIndex == 0:
            return 'Matrix'
        if typeIndex == 1:
            return 'Num'
        if typeIndex == 2:
            return 'Fun'

    def resetTypeNameIndexDictionaries(self):
        self.inputIndices = {
            0: 1,
            1: 1,
            2: 1
        }
        self.outputIndices = {
            0: 1,
            1: 1,
            2: 1
        }

    def getTypeNameIndex(self, typeIndex, isInput):
        if isInput:
            res = self.inputIndices[typeIndex]
            self.inputIndices[typeIndex] += 1
            return res
        else:
            res = self.outputIndices[typeIndex]
            self.outputIndices[typeIndex] += 1
            return res
