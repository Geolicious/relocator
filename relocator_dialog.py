# -*- coding: utf-8 -*-
"""
/***************************************************************************
 relocatorDialog
                                 A QGIS plugin
 relocates all your project data to a specific location
                             -------------------
        begin                : 2015-05-01
        git sha              : $Format:%H$
        copyright            : (C) 2015 by Riccardo Klinger / Geolicious
        email                : riccardo.klinger@geolicious.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os
import sys
import tempfile

from PyQt4 import QtGui, uic
from relocator_exec import relocator_exec

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'relocator_dialog_base.ui'))


class relocatorDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(relocatorDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
        self.relocate_path.setReadOnly(False)
        #self.zipper_path.setReadOnly(False)
        self.relocate_path.setText(tempfile.gettempdir())
        #self.zipper_path.setText(tempfile.gettempdir()+ os.sep + "export.zip")
        
        #self.outFileName_zipper = self.zipper_path.text()
        self.cancelButton.clicked.connect(self.close)
        #self.cancelButton_2.clicked.connect(self.close)
        self.pushButton_3.clicked.connect(self.showSaveDialog_relocate)
        self.outFileName_relocate = self.relocate_path.text()
        #self.pushButton_4.clicked.connect(self.showSaveDialog_zipper)        
        self.okButton.clicked.connect(self.relocator)
        #self.okButton_2.clicked.connect(self.zipper)


        self.close()
    def showSaveDialog_relocate(self):
        self.outFileName = str(QtGui.QFileDialog.getExistingDirectory(self, "Output Project Name:"))
        if self.outFileName == None:
            self.okButton.setDisabled(True)
        print self.outFileName_relocate
        self.relocate_path.clear()
        self.relocate_path.setText(self.outFileName)
        self.outFileName_relocate = self.relocate_path.text()
    # def showSaveDialog_zipper(self):
    #     self.outFileName = str(QtGui.QFileDialog.getSaveFileName(self, 'export zip name', str(tempfile.gettempdir()) + os.sep + 'qgis_export.zip', '*.zip'))
    #     if self.outFileName == None:
    #         self.ui.okButton_2.setDisabled(True)
    #     self.zipper_path.clear()
    #     self.zipper_path.setText(self.outFileName)

    def relocator(self):
        #we will have the logic in the exec file!
        path_r = self.outFileName_relocate
        if self.radioButton.isChecked() == True:
            zipit = 1
        else:
            zipit = 0
        relocator_exec(path_r, zipit)
    # def zipper(self):
    #     #we will have the logic in the exec file!
    #     path_z = self.outFileName_zipper
    #     zipper_exec(path_z)