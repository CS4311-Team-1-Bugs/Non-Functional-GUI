# -*- coding: utf-8 -*-

import sys
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import pymongo
from bson.objectid import ObjectId
import datetime


class QTablePush(QPushButton):
    global win

    def __init__(self, id, text):
        # init the window
        super(QPushButton, self).__init__()
        self.setIcon(QIcon(QPixmap(text)))
        self.setIconSize(QSize(16, 16))
        self.id = str(id)
        self.setToolTip(text[ :-4 ])
        self.clicked.connect(lambda: win.tool_buttons(text[ :-4 ], self))


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        # init the window
        super(MainWindow, self).__init__(*args, **kwargs)
        client = pymongo.MongoClient(
            "mongodb+srv://aaron:EDVsK1hnYHJEWZry@seacluster.f3vdv.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
        db = client[ 'Test' ]

        self.tools = db[ "Run Config" ]

        # Set the Window Title
        self.setWindowTitle("SEA Tool")
        self.setStyleSheet('background-color:000000;color:ffffff')
        # Make our menu
        menuWidget = QWidget()
        menuLayout = self.make_menuLayout()
        menuWidget.setLayout(menuLayout)
        palette = QPalette()
        palette.setColor(QPalette.Background, QColor("#daf4f7"))
        menuWidget.setPalette(palette)
        menuWidget.setAutoFillBackground(1)
        self.setMenuWidget(menuWidget)
        self.make_toolTable()
        self.make_toolConfig()
        self.run_config()
        self.editMode = 0
        self.currId = 0

    def make_menuLayout(self):
        # set menu layout
        menuLayout = QVBoxLayout()

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  SEA Menu  ")
        menuTitle.setFont(QFont("Times", 20))
        menuTitle.setStyleSheet("border: 3px solid black; color: #000000")
        menuTitle.setAlignment(Qt.AlignCenter)

        # button component of menu
        hLayout = QHBoxLayout()
        runButton = QPushButton("Run")
        runButton.clicked.connect(lambda: self.menu_buttons("Run"))
        toolButton = QPushButton("Tools")
        toolButton.clicked.connect(lambda: self.menu_buttons("Tool"))
        hLayout.addStretch()
        hLayout.addWidget(runButton)
        hLayout.addStretch()
        hLayout.addWidget(toolButton)
        hLayout.addStretch()

        # Add the widgets we created to the menu layout
        menuLayout.addWidget(self.make_HBox(menuTitle, 0))
        hButtons = QWidget()
        hButtons.setLayout(hLayout)
        menuLayout.addWidget(hButtons)

        return menuLayout

    def make_toolConfig(self):

        # Title component of menu
        self.AddTitle = QLabel()
        self.AddTitle.setText("  Add a Run Configuration  ")
        self.AddTitle.setFont(QFont("Times", 16))
        self.AddTitle.setStyleSheet("background-color: #49d1e3")
        self.AddTitle.setAlignment(Qt.AlignLeft)

        # Title component of menu
        configTitle = QLabel()
        configTitle.setText("  Run Configuration ")
        configTitle.setFont(QFont("Times", 12))
        configTitle.setStyleSheet("border: 1px solid black; color: #000000")
        configTitle.setAlignment(Qt.AlignCenter)

        # Tool Specification Section
        runConfig = self.make_toolSpec()


        # Save Button Section
        saveButt = self.make_saveCancel()

        # Add spacing to the page and add our widgets
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.make_HBox(configTitle, 0))
        mainLayout.addWidget(self.make_HBox(runConfig, 1))
        mainLayout.addWidget(saveButt)
        mainLayout.addStretch()

        main = QWidget()
        main.setLayout(mainLayout)

        self.newTool = 1

        self.toolEdit = QDockWidget()
        self.toolEdit.setTitleBarWidget(self.AddTitle)
        self.toolEdit.setWidget(main)
        self.addDockWidget(Qt.RightDockWidgetArea, self.toolEdit)

    def make_toolSpec(self):
        layout = QFormLayout()

        # Run Name with the time and date as the name. Ex: 10:14 04/05/2021 AM
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%I:%M %m/%d/%Y %p")
        self.name = QLabel()
        self.name.setText(timestampStr)
        self.name.setAlignment(Qt.AlignLeft)

        # Run description text input
        self.description = QLineEdit()
        self.description.setAlignment(Qt.AlignLeft)

        # Whitelist Text Input Option
        self.WLIPtxt = QLineEdit()
        self.WLIPtxt.setAlignment(Qt.AlignLeft)

        # Whitelist Browse File Option
        browser = QHBoxLayout()
        self.path = QLineEdit()
        self.path.setAlignment(Qt.AlignLeft)
        browser.addWidget(self.path)
        WLIPpathBrowse = QPushButton("Browse")
        WLIPpathBrowse.clicked.connect(lambda: self.tool_buttons("Browse", self.path))
        browser.addWidget(WLIPpathBrowse)
        browser.addStretch()

        WLIPbrowserWidg = QWidget()
        WLIPbrowserWidg.setLayout(browser)

        # Blacklist Text Input Option
        self.BLIPtxt = QLineEdit()
        self.BLIPtxt.setAlignment(Qt.AlignLeft)

        browser1 = QHBoxLayout()
        self.path = QLineEdit()
        self.path.setAlignment(Qt.AlignLeft)
        browser1.addWidget(self.path)
        BLIPpathBrowse = QPushButton("Browse")
        BLIPpathBrowse.clicked.connect(lambda: self.tool_buttons("Browse", self.path))
        browser1.addWidget(BLIPpathBrowse)
        browser1.addStretch()

        BLIPbrowserWidg = QWidget()
        BLIPbrowserWidg.setLayout(browser1)


        self.outputSpec = QVBoxLayout()

        outSpecLayout = QHBoxLayout()
        scanType = QComboBox()
        scanList = [ "Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3" ]
        scanType.addItems(scanList)
        outSpecLayout.addWidget(scanType)
        outSpecLayout.addStretch()

        holder = QWidget()
        holder.setLayout(outSpecLayout)
        self.outputSpec.addWidget(holder)
        outSpec_widg = QWidget()
        outSpec_widg.setLayout(self.outputSpec)

        orLabel = QLabel("OR")
        self.orLabel().setAlignment(Qt.AlignCenter)

        specFile_container = QHBoxLayout()
        self.specFile = QLineEdit()
        self.specFile.setAlignment(Qt.AlignLeft)
        specFile_container.addWidget(self.specFile)

        browse = QPushButton("Browse")
        browse.clicked.connect(lambda: self.tool_buttons("Browse", self.specFile))
        specFile_container.addWidget(browse)
        specFile_container.addStretch()
        specFile_widg = QWidget()
        specFile_widg.setLayout(specFile_container)

        layout.addRow(QLabel("Run Name"), self.name)
        layout.addRow(QLabel("Run Description"), self.description)
        layout.addRow(QLabel("Whitelisted IP Target"),self.WLIPtxt)
        layout.addRow(orLabel)
        layout.addRow(QLabel("Browse for Whitelist File"), WLIPbrowserWidg)
        layout.addRow(QLabel("Blacklisted IP Target"), self.BLIPtxt)
        layout.addRow(QLabel("OR"))
        layout.addRow(QLabel("Browse for Blacklist File"), BLIPbrowserWidg)
        layout.addRow(QLabel("Scan Type"), outSpec_widg)
        layout.addRow(QLabel("OR"))
        layout.addRow(QLabel("Browse for Run Configuration File"), specFile_widg)

        layoutHolder = QWidget()
        layoutHolder.setLayout(layout)
        return layoutHolder

    def make_saveCancel(self):
        layout = QHBoxLayout()
        save = QPushButton("Save")
        save.setStyleSheet("background-color: #54e86c")
        save.clicked.connect(lambda: self.tool_buttons("Save", None))
        cancel = QPushButton("Cancel")
        cancel.setStyleSheet("background-color: #e6737e")
        cancel.clicked.connect(lambda: self.tool_buttons("Cancel", None))
        layout.addSpacing(20)
        layout.addStretch()
        layout.addStretch()
        layout.addWidget(cancel)
        layout.addWidget(save)

        container = QWidget()
        container.setLayout(layout)
        return container
        # pad a widget with horizontal spacing or stretching

    def make_HBox(self, widget, spacingType):
        layout = QHBoxLayout()
        if spacingType:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        layout.addWidget(widget)
        if spacingType:
            layout.addSpacing(2)
        else:
            layout.addStretch()
        container = QWidget()
        container.setLayout(layout)
        return container

    def make_toolTable(self):

        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Tool List  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        # Create Tool Content Details layer
        self.tableWidget = QTableWidget(1, 4)
        self.tableWidget.setColumnHidden(3, True)
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # column 1
        col1Title = QLabel()
        col1Title.setText("Tool Name")
        nameSortButton = QToolButton()
        nameSortButton.setArrowType(Qt.DownArrow)
        col1Layout = QHBoxLayout()
        col1Layout.addStretch()
        col1Layout.addWidget(col1Title)
        col1Layout.addWidget(nameSortButton)
        col1Layout.addStretch()

        # Set Columns for the table
        col1Widget = QWidget()
        col1Widget.setLayout(col1Layout)
        self.tableWidget.setCellWidget(0, 0, col1Widget)
        self.tableWidget.setCellWidget(0, 1, QLabel("Description of Tool"))
        self.tableWidget.setCellWidget(0, 2, QLabel("  Modify"))
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.horizontalHeader().hide()

        # Add button
        addLayout = QHBoxLayout()
        addLayout.addStretch(1)
        push = QPushButton("Add Tool")
        push.setStyleSheet("background-color: #54e86c")
        push.clicked.connect(lambda: self.tool_buttons("Switcher", None))
        addLayout.addWidget(push)
        holder = QWidget()
        holder.setLayout(addLayout)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tableWidget)
        mainLayout.addWidget(holder)
        mainLayout.addStretch()

        main = QWidget()
        main.setLayout(mainLayout)


        self.toolList = QDockWidget()
        self.toolList.setTitleBarWidget(menuTitle)
        self.toolList.setWidget(main)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolList)

        # Quick code to make the menu buttons work

    def menu_buttons(self, button):
        if button == "Run":
            self.toolList.hide()
            self.toolEdit.hide()
            self.runConfiguration.show()
        else:
            self.toolList.show()
            self.toolEdit.show()
            self.runConfiguration.hide()

    def tool_buttons(self, buttonName, button):

        if buttonName == "Browse":
            fname = QFileDialog.getOpenFileName(None, "Select a file...", "./", filter="All files (*)")
            if isinstance(fname, tuple):
                button.setText(str(fname[ 0 ]))
            else:
                button.setText(str(fname))
        elif "Add" in buttonName:
            label = button.text()
            button.setText("")
            # make layout to hold name and button
            hLayout = QHBoxLayout()
            addedLabel = QLabel(label)
            removeButt = QPushButton("Remove")
            hLayout.addWidget(addedLabel)
            hLayout.addWidget(removeButt)

            # make a holder
            holder = QWidget()
            holder.setLayout(hLayout)
            # add it
            if buttonName == "Add":
                self.options.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda: self.tool_buttons("Remove", label))
            else:
                self.outputSpec.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda: self.tool_buttons("RemoveS", label))

            button.setText("")

        elif "Remove" in buttonName:
            if buttonName == "Remove":
                for i in range(self.options.count()):
                    if i == 0:
                        continue
                        # print(i)
                    print(self.options.itemAt(i).widget().layout().itemAt(0).widget().text())
                    print("button text is", button)
                    if self.options.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                        # print("match at ", i)
                        self.options.itemAt(i).widget().setParent(None)
                        return

            elif buttonName == "RemoveS":
                for i in range(self.outputSpec.count()):
                    if i == 0:
                        continue
                    if self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().text() == button:
                        self.outputSpec.itemAt(i).widget().setParent(None)
                        return
            else:
                for i in range(1, self.tableWidget.rowCount()):
                    # print("target", button.id)
                    # print("actual", self.tableWidget.cellWidget(i, 3).text())
                    if self.tableWidget.cellWidget(i, 3).text() == button.id:
                        # print("Going to remove row", i)
                        self.tableWidget.removeRow(i)
                        removeDict = {"_id": ObjectId(button.id)}
                        self.tools.delete_one(removeDict)

                        removeOpts = {"Tool_id": ObjectId(button.id)}
                        self.optionsDB.delete_many(removeOpts)
                        return

        elif buttonName == "Cancel":
            self.name.setText("")
            self.description.setText("")
            self.path.setText("")
            # self.option.setText("")
            self.specFile.setText("")
            for i in reversed(range(self.options.count())):
                if i == 0:
                    self.options.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.options.itemAt(i).widget().setParent(None)
            for i in reversed(range(self.outputSpec.count())):
                if i == 0:
                    self.outputSpec.itemAt(i).widget().layout().itemAt(0).widget().setText("")
                else:
                    self.outputSpec.itemAt(i).widget().setParent(None)
            if self.editMode == 1:
                self.editMode = 0
                self.AddTitle.setText("Add a Tool")
        elif buttonName == "Save":
            name = self.name.text()
            description = self.description.text()
            wlip = self.WLIPtxt.text()
            blip= self.BLIPtxt.text()
            spec = self.specFile.text()
            if not self.editMode:
                inputStr = {"Run Name": name, "Run Description": description, "Whitelist IP": wlip, "Blacklist": blip,
                            "Run Configuration Specification": spec}
                self.tools.insert_one(inputStr)


            else:
                self.editMode = 0
                self.AddTitle.setText("  Add a Tool  ")
                self.tools.update_one({"_id": self.currId}, {
                    "$set": {"Run Name": name, "Run Description": description, "Whitelist IP": wlip, "Blacklist": blip,
                            "Run Configuration Specification": spec}})


            # Redraw the table and erase the text boxes
            self.drawTable()
            self.tool_buttons("Cancel", None)
        elif buttonName == "Switcher":
            self.editMode = 0
            self.AddTitle.setText("  Add a Tool  ")
            self.tool_buttons("Cancel", None)



        elif buttonName == "Edit":
            Id = ObjectId(button.id)
            self.currId = Id
            self.editMode = 1
            query = {"_id": Id}
            tool = self.tools.find(query)[ 0 ]
            self.name.setText(tool[ "Name" ])
            self.description.setText(tool[ "Description" ])
            self.path.setText(tool[ "Path" ])
            self.specFile.setText(tool[ "Specification" ])

            opt_query = {"Tool_id": Id}
            for i in self.optionsDB.find(opt_query):
                label = i[ "Option" ]
                # make layout to hold name and button
                hLayout = QHBoxLayout()
                addedLabel = QLabel(label)
                removeButt = QPushButton("Remove")
                hLayout.addWidget(addedLabel)
                hLayout.addWidget(removeButt)

                # make a holder
                holder = QWidget()
                holder.setLayout(hLayout)

                self.options.addWidget(holder)
                # set up removal button's button
                removeButt.clicked.connect(lambda checked, a=label: self.tool_buttons("Remove", a))

    def run_config(self):
        # Title component of menu
        menuTitle = QLabel()
        menuTitle.setText("  Run Configuration  ")
        menuTitle.setFont(QFont("Times", 16))
        menuTitle.setStyleSheet("background-color: #49d1e3")
        menuTitle.setAlignment(Qt.AlignLeft)

        outerLayout = QVBoxLayout()
        # Create Run Config Details layer
        runConfigLayout = QFormLayout()
        orLabel = self.orLabel()
        orLabel1 = self.orLabel()
        orLabel2 = self.orLabel()

        # Run Name
        dateTimeObj = datetime.datetime.now()
        timestampStr = dateTimeObj.strftime("%I:%M %m/%d/%Y %p")
        runName = QLabel()
        runName.setAlignment(Qt.AlignLeft)
        runName.setText(timestampStr)
        serifFont = QFont("TimesNewRoman", 15)
        runName.setFont(serifFont)
        runConfigLayout.addRow("Run Name:", runName)

        # Run Description
        runDesc = QLineEdit()
        runDesc.setPlaceholderText("Run Description Default")
        runConfigLayout.addRow("Run Description:", runDesc)

        WLIPtext = QPlainTextEdit()
        WLIPtext.setPlaceholderText("Whitelist IP Default")

        BrowseChoiceLayout = QHBoxLayout()
        BrowseChoiceLayout.addWidget(WLIPtext)
        BrowseChoiceLayout.addWidget(orLabel)
        BrowseChoiceLayout.addWidget(QLabel("Browse for Whitelist Files"))
        BrowseChoiceLayout.addWidget(QLineEdit())
        BrowseChoiceLayout.addWidget(QPushButton("Browse"))
        # buttonConfigFile = QPushButton("Browse")
        BrowseWidget = QWidget()
        BrowseWidget.setLayout(BrowseChoiceLayout)

        BLIPtext = QPlainTextEdit()
        BLIPtext.setPlaceholderText("Blacklist IP Default")
        BrowseChoiceLayout2 = QHBoxLayout()
        BrowseChoiceLayout2.addWidget(BLIPtext)
        BrowseChoiceLayout2.addWidget(orLabel1)
        BrowseChoiceLayout2.addWidget(QLabel("Browse for Blacklist Files"))
        BrowseChoiceLayout2.addWidget(QLineEdit())
        BrowseChoiceLayout2.addWidget(QPushButton("Browse"))
        # buttonConfigFile = QPushButton("Browse")
        BrowseWidget2 = QWidget()
        BrowseWidget2.setLayout(BrowseChoiceLayout2)

        runConfigLayout.addRow("Whitelisted IP Target:", BrowseWidget)
        runConfigLayout.addRow("Blacklisted IP Target:", BrowseWidget2)

        ScanType = QComboBox()
        scanList = [ "Scan Type", "Scan Type 1", "Scan Type 2 ", "Scan Type 3" ]
        ScanType.addItems(scanList)
        runConfigLayout.addRow("Scan Type:", ScanType)
        runConfigLayout.addWidget(orLabel2)
        ConfigFile = QLineEdit()
        ConfigFile.setPlaceholderText("Run Configuration File")
        runConfigLayout.addRow("Browse for Run Configuration File:", ConfigFile, )
        runConfigLayout.addWidget(QPushButton("Browse"))

        buttonWidget = self.make_saveCancel()

        runConfigLayout.addWidget(buttonWidget)
        runConfigLayout.setVerticalSpacing(20)
        runConfigLayout.setHorizontalSpacing(10)
        main = QWidget()
        main.setLayout(runConfigLayout)

        self.runConfiguration = QDockWidget()
        self.runConfiguration.setTitleBarWidget(menuTitle)
        self.runConfiguration.setWidget(main)
        self.addDockWidget(Qt.RightDockWidgetArea, self.runConfiguration)
        self.runConfiguration.setVisible(False)
        return

    def orLabel(self):
        orLabel = QLabel()
        orLabel.setText("-OR-")
        orLabel.setAlignment(Qt.AlignCenter)
        serifFont = QFont("TimesNewRoman", 14)
        orLabel.setFont(serifFont)
        return orLabel


if __name__ == "__main__":
    global win
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

    # tacos = QTablePush(7)
    # print(tacos.id)
