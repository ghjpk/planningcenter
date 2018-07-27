# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4
###############################################################################
# OpenLP - Open Source Lyrics Projection                                      #
# --------------------------------------------------------------------------- #
# Copyright (c) 2008-2017 OpenLP Developers                                   #
# Copyright (c) 2018      John Kirkland                                       #
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
Package to test the openlp.plugins.planningcenter.forms.editauthform package.
"""
from unittest import TestCase

from PyQt5 import QtCore, QtTest, QtWidgets

from openlp.core.common import Registry, Settings
from openlp.plugins.planningcenter.forms.editauthform import EditAuthForm
from openlp.plugins.planningcenter import planningcenterplugin

from tests.helpers.testmixin import TestMixin
from tests.interfaces import patch

class TestEditAuthForm(TestCase, TestMixin):
    """
    Test the EditAuthForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.application_id = 'abc'
        self.secret = '123' 
        Settings().setValue('planningcenter/application_id', self.application_id)
        Settings().setValue('planningcenter/secret', self.secret)
        # init the planning center plugin
        planning_center_plugin = planningcenterplugin.planningcenterplugin()
        self.form = EditAuthForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def basic_display_test(self):
        """
        Test the EditAuthForm displays the default values from Settings
        """
        # GIVEN: An PlanningCenterAuthForm instance
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            # WHEN: The form is shown
            self.form.exec()
            # THEN: The default values match what is saved in the config
            self.assertEqual(self.form.application_id_line_edit.text(), self.application_id, 
                             'The application_id edit box defaults to the value in settings.')
            self.assertEqual(self.form.secret_line_edit.text(), self.secret,
                             'The secret edit box defaults to the value in settings.')

    def click_delete_credentials_button_test(self):
        """
        Test that clicking the delete credentials button deletes the credentials from Settings
        """
        # GIVEN: An instance of the PlanningCenterAuthForm
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            # WHEN: The form is shown
            self.form.exec()
            # WHEN: The "delete credentials" button is clicked
            QtTest.QTest.mouseClick(self.form.delete_credentials_button, QtCore.Qt.LeftButton)
            # THEN: The application_id and secret should be set to '' in Settings
            self.assertEqual(Settings().value('planningcenter/application_id'),'',
                             'The application_id setting should have been reset.')
            self.assertEqual(Settings().value('planningcenter/secret'),'',
                             'The secret setting should have been reset')
    
    def click_save_credentials_button_test(self):
        """
        Test that we try and save credentials, but they are rejected because they are bad.
        I do not want to store valid credentials in here because this source is openly
        available.
        """
        # GIVEN: An instance of the PlanningCenterAuthForm
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            # WHEN: The form is shown
            self.form.exec()
            # WHEN: The "delete credentials" button is clicked with new credentials set
            application_id = 'def'
            secret = '456'
            self.form.application_id_line_edit.setText(application_id)
            self.form.secret_line_edit.setText(secret)
            with patch('PyQt5.QtWidgets.QMessageBox'):
                QtTest.QTest.mouseClick(self.form.save_credentials_button, QtCore.Qt.LeftButton)
            # THEN: We should test credentials and validate that they did not get saved
            self.assertNotEqual(Settings().value('planningcenter/application_id'), application_id, 
                                'The application_id should not have been saved')
            self.assertNotEqual(Settings().value('planningcenter/secret'), secret,
                                'The secret code should not have been saved')