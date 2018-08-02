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
Package to test the openlp.plugins.planningcenter.forms.selectplanform package.
"""
from unittest import TestCase
from PyQt5 import QtWidgets, QtTest, QtCore
from openlp.core.common import Registry, Settings
from openlp.core.ui import ThemeManager, ServiceManager
from openlp.core import OpenLP
from openlp.plugins.planningcenter.forms.selectplanform import SelectPlanForm
from openlp.plugins.songs.songsplugin import SongsPlugin
from openlp.plugins.songs.lib.mediaitem import SongMediaItem
from tests.helpers.testmixin import TestMixin
from tests.interfaces import patch, MagicMock
import os
from datetime import date

TEST_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'planningcenter'))

class TestSelectPlanForm(TestCase, TestMixin):
    """
    Test the SelectPlanForm class
    """

    def setUp(self):
        """
        Create the UI
        """
        Registry.create()
        self.setup_application()
        self.main_window = QtWidgets.QMainWindow()
        Registry().register('main_window', self.main_window)
        self.form = SelectPlanForm()
        self.form.planning_center_api.airplane_mode = True
        self.form.planning_center_api.airplane_mode_directory = TEST_PATH
        theme_manager = ThemeManager(None)
        theme_manager.get_themes = MagicMock()
        theme_manager.get_themes.return_value = ['themeA','themeB']

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
    
    def initial_defaults_test(self):
        """
        Test that the SelectPlanForm displays with correct defaults
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, 
        # a theme manager with mocked themes, and a fake date = Sunday (7/29/2018)
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 7/29/2018 for date.today()
            mock_date.today.return_value = date(2018,7,29)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            # WHEN: The form is shown
            self.form.exec()  
        # THEN: The correct count of service types show up in the combo box
        self.assertEqual(self.form.service_type_combo_box.count(), 3,
                         'The service_type_combo_box contains 3 items')
        # The first service type is selected
        self.assertEqual(self.form.service_type_combo_box.currentText(), '01 Grace Bible Fellowship',
                         'The service_type_combo_box defaults to "01 Grace Bible Fellowship"')
        # the selected plan is today (the mocked date is a Sunday)
        self.assertEqual(self.form.plan_selection_combo_box.currentText(), 
                         date.strftime(mock_date.today.return_value,'%B %d, %Y'),
                         'Incorrect default date selected for Plan Date')
        # count the number of themes listed and make sure it matches expected value
        self.assertEqual(self.form.song_theme_selection_combo_box.count(),
                         2, 'Count of song themes is incorrect')
        self.assertEqual(self.form.slide_theme_selection_combo_box.count(),
                         2, 'Count of custom slide themes is incorrect')
            
    def disable_import_buttons_test(self):
        """
        Test that the import buttons are disabled when the "Select Plan Date" element in the Plan Selection List is selected.
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, and the form
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.exec()
            # WHEN: The Select Plan combo box is set to "Select Plan Date"
            index = self.form.plan_selection_combo_box.findText('Select Plan Date')
            self.form.plan_selection_combo_box.setCurrentIndex(index)
            # THEN: "Import New" and "Refresh Service" buttons become inactive
            self.assertEqual(self.form.import_as_new_button.isEnabled(), False, '"Import as New" button should be disabled')
            self.assertEqual(self.form.update_existing_button.isEnabled(), False, '"Refresh Service" button should be disabled')

    def verify_default_plan_date_is_next_sunday_test(self):
        """
        Test that the SelectPlanForm displays Next Sunday's Date by Default
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, 
        # a theme manager with mocked themes, and a fake date = Monday (7/30/2018)
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
            # need to always return 7/29/2018 for date.today()
            mock_date.today.return_value = date(2018,7,30)
            mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            # WHEN: The form is shown
            self.form.exec()
        # THEN: The plan selection date is 8/5 (the following Sunday)
        self.assertEqual(self.form.plan_selection_combo_box.currentText(), 'August 5, 2018',
                         'The next Sunday\'s Date is not selected in the plan_selection_combo_box')
    
    def verify_service_type_changed_called_when_service_type_combo_changed_test(self):
        """
        Test that the "on_service_type_combobox_changed" function is executed when the service_type_combobox is changed
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, 
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.on_service_type_combobox_changed = MagicMock()
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1
            self.form.service_type_combo_box.setCurrentIndex(1)
        # THEN: The on_import_as_new_button_cliced function is called
        self.form.on_service_type_combobox_changed.assert_called_with(1)
    
    def verify_plan_selection_changed_called_when_plan_selection_combo_changed_test(self):
        """
        Test that the "on_plan_selection_combobox_changed" function is executed when the plan_selection_combobox is changed
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, 
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.on_plan_selection_combobox_changed = MagicMock()
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1
            self.form.service_type_combo_box.setCurrentIndex(1)
            self.form.plan_selection_combo_box.setCurrentIndex(3)
        # THEN: The on_import_as_new_button_cliced function is called
        self.form.on_plan_selection_combobox_changed.assert_called_with(3)
    
    def verify_import_function_called_when_import_button_clicked_test(self):
        """
        Test that the "on_import_as_new_button_clicked" function is executed when the "Import New" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, 
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            self.form.on_import_as_new_button_clicked = MagicMock()
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box is set to index 3 and the "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            self.form.plan_selection_combo_box.setCurrentIndex(3)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
        # THEN: The on_import_as_new_button_cliced function is called
        self.form.on_import_as_new_button_clicked.assert_called_with(False)
        
    def verify_service_imported_when_import_button_clicked_test(self):
        """
        Test that a service is imported when the "Import New" button is clicked
        """
        # GIVEN: An SelectPlanForm instance with airplane mode enabled, resources available, mocked out "on_new_service_clicked"
        with patch('PyQt5.QtWidgets.QDialog.exec'), \
                patch('openlp.core.lib.db.Manager.__init__'), \
                patch('openlp.plugins.planningcenter.lib.songimport.PlanningCenterSongImport.add_song') as mock_add_song, \
                patch('openlp.plugins.planningcenter.lib.customimport.PlanningCenterCustomImport.add_slide') as mock_add_slide:
            Registry().register('application', MagicMock())
            Registry().register('service_manager', MagicMock())
            Registry().register('songs', MagicMock())
            Registry().register('custom', MagicMock())
            self.form.exec()
            # WHEN: The Service Type combo is set to index 1 and the Select Plan combo box is set to index 3 and the "Import New" button is clicked
            self.form.service_type_combo_box.setCurrentIndex(1)
            self.form.plan_selection_combo_box.setCurrentIndex(3)
            QtTest.QTest.mouseClick(self.form.import_as_new_button, QtCore.Qt.LeftButton)
        # THEN: The add_song function was called 2 times and add_slide once
        mock_add_slide.assert_called_once()
        self.assertEqual(mock_add_song.call_count, 2, 'Add_song should be called 2 times')
        
    