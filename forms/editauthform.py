# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4

###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2017 OpenLP Developers                                   #
# Copyright (c) 2018 John Kirkland                                            #
# --------------------------------------------------------------------------- #
# This program is free software; you can redistribute it and/or modify it     #
# under the terms of the GNU General Public License as published by the Free  #
# Software Foundation; version 2 of the License.                              #
#                                                                             #
# This program is distributed in the hope that it will be useful, but WITHOUT #
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or       #
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for    #
# more details.                                                               #
#                                                                             #
# You should have received a copy of the GNU General Public License along     #
# with this program; if not, write to the Free Software Foundation, Inc., 59  #
# Temple Place, Suite 330, Boston, MA 02111-1307 USA                          #
###############################################################################
"""
The :mod:`~openlp.plugins.planningcenter.forms.editauthform` module contains the GUI for editing the authentication values for Planning Center
"""

import logging

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Settings
from openlp.plugins.planningcenter.forms.editauthdialog import Ui_EditAuthDialog
from openlp.plugins.planningcenter.lib.planningcenter_api import PlanningCenterAPI

log = logging.getLogger(__name__)

class EditAuthForm(QtWidgets.QDialog, Ui_EditAuthDialog):
    """
    The :class:`EditAuthForm` class is the PlanningCenter Authentication dialog.
    """

    def __init__(self, parent=None, plugin=None, db_manager=None):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.plugin = plugin
        self.db_manager = db_manager
        self.setup_ui(self)

    def initialise(self):
        """
        Initialise the PlanningCenterForm
        """
        return True

    def exec(self):
        """
        Execute the dialog. This method sets everything back to its initial
        values.
        """
        self.test_credentials_button.clicked.connect(self.on_test_credentials_button_clicked)
        self.save_credentials_button.clicked.connect(self.on_save_credentials_button_clicked)
        self.delete_credentials_button.clicked.connect(self.on_delete_credentials_button_clicked)
        self.delete_credentials_button.setEnabled(False)
        application_id = Settings().value("planningcenter/application_id")
        secret = Settings().value("planningcenter/secret")
        if len(application_id):
            self.application_id_line_edit.setText(application_id)
            self.secret_line_edit.setText(secret)
            self.delete_credentials_button.setEnabled(True)
            
        return QtWidgets.QDialog.exec(self)
    
    def on_delete_credentials_button_clicked(self):
        """
        Deletes the credentials
        """
        Settings().setValue("planningcenter/application_id",'')
        Settings().setValue("planningcenter/secret",'')
        self.done(1)
    
    def on_save_credentials_button_clicked(self):
        """
        Saves the credentials
        """
        are_credentials_good = self.on_test_credentials_button_clicked()
        if are_credentials_good:
            # save the credentials
            Settings().setValue("planningcenter/application_id",self.application_id_line_edit.text())
            Settings().setValue("planningcenter/secret",self.secret_line_edit.text())
        self.done(1)
            
    def done(self, r):
        """
        Close auth dialog.
 
        :param r: The result of the dialog.
        """
        self.test_credentials_button.clicked.disconnect()
        self.save_credentials_button.clicked.disconnect()
        return QtWidgets.QDialog.done(self, r)
    
    def on_test_credentials_button_clicked(self):
        """
        Tests if the credentials are valid
        """
        application_id = self.application_id_line_edit.text()
        secret = self.secret_line_edit.text()
        test_auth = PlanningCenterAPI(application_id, secret)
        organization = test_auth.CheckCredentials()
        if len(organization):
            QtWidgets.QMessageBox.information(self, 'Planning Center Online Authentication Test', 
                                              "Authentication successful for organization: {0}".format(organization), 
                                              QtWidgets.QMessageBox.Ok)
            return True
        else:
            QtWidgets.QMessageBox.warning(self, "Authentication Failed", 
                                          "Authentiation Failed", 
                                          QtWidgets.QMessageBox.Ok)
            return False
