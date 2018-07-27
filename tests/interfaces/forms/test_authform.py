# -*- coding: utf-8 -*-
# vim: autoindent shiftwidth=4 expandtab textwidth=120 tabstop=4 softtabstop=4
from openlp.plugins.planningcenter.planningcenterplugin import planningcenterplugin
import abc

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
Package to test the openlp.plugins.planningcenter.forms.planningcenterform package.
"""
from unittest import TestCase

from PyQt5 import QtCore, QtTest, QtWidgets

from openlp.core.common import Registry, Settings
from openlp.plugins.planningcenter.forms.planningcenterform import PlanningCenterAuthForm
from openlp.plugins.planningcenter import planningcenterplugin

from tests.helpers.testmixin import TestMixin
from tests.interfaces import MagicMock, patch

class TestPlanningCenterAuthForm(TestCase, TestMixin):
    """
    Test the PlanningCenterAuthForm class
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
        self.form = PlanningCenterAuthForm()

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window

    def ui_defaults_test(self):
        """
        Test the PlanningCenterAuthForm defaults are correct
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

#     def type_verse_text_tests(self):
#         """
#         Test that typing into the verse text edit box returns the correct text
#         """
#         # GIVEN: An instance of the EditVerseForm and some text to type
#         text = 'Amazing Grace, how sweet the sound!'
# 
#         # WHEN: Some verse text is typed into the text edit
#         QtTest.QTest.keyClicks(self.form.verse_text_edit, text)
# 
#         # THEN: The verse text edit should have the verse text in it
#         self.assertEqual(text, self.form.verse_text_edit.toPlainText(),
#                          'The verse text edit should have the typed out verse')
# 
#     def insert_verse_test(self):
#         """
#         Test that clicking the insert button inserts the correct verse marker
#         """
#         # GIVEN: An instance of the EditVerseForm
#         # WHEN: The Insert button is clicked
#         QtTest.QTest.mouseClick(self.form.insert_button, QtCore.Qt.LeftButton)
# 
#         # THEN: The verse text edit should have a Verse:1 in it
#         self.assertIn('---[Verse:1]---', self.form.verse_text_edit.toPlainText(),
#                       'The verse text edit should have a verse marker')
# 
#     def insert_verse_2_test(self):
#         """
#         Test that clicking the up button on the spin box and then clicking the insert button inserts the correct marker
#         """
#         # GIVEN: An instance of the EditVerseForm
#         # WHEN: The spin button and then the Insert button are clicked
#         QtTest.QTest.keyClick(self.form.verse_number_box, QtCore.Qt.Key_Up)
#         QtTest.QTest.mouseClick(self.form.insert_button, QtCore.Qt.LeftButton)
# 
#         # THEN: The verse text edit should have a Verse:1 in it
#         self.assertIn('---[Verse:2]---', self.form.verse_text_edit.toPlainText(),
#                       'The verse text edit should have a "Verse 2" marker')
# 
#     def insert_chorus_test(self):
#         """
#         Test that clicking the verse type combo box and then clicking the insert button inserts the correct marker
#         """
#         # GIVEN: An instance of the EditVerseForm
#         # WHEN: The verse type combo box and then the Insert button are clicked
#         QtTest.QTest.keyClick(self.form.verse_type_combo_box, QtCore.Qt.Key_Down)
#         QtTest.QTest.mouseClick(self.form.insert_button, QtCore.Qt.LeftButton)
# 
#         # THEN: The verse text edit should have a Chorus:1 in it
#         self.assertIn('---[Chorus:1]---', self.form.verse_text_edit.toPlainText(),
#                       'The verse text edit should have a "Chorus 1" marker')
