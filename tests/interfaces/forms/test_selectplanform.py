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
from PyQt5 import QtWidgets
from openlp.core.common import Registry
from openlp.core.ui import ThemeManager
from openlp.plugins.planningcenter.forms.selectplanform import SelectPlanForm
from tests.helpers.testmixin import TestMixin
from tests.interfaces import patch
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

    def tearDown(self):
        """
        Delete all the C++ objects at the end so that we don't have a segfault
        """
        del self.form
        del self.main_window
        
    
    def basic_display_test(self):
        """
        Test that the SelectPlanForm displays with correct defaults
        """
        # GIVEN: An SelectPlanForm instance, with airplane mode enabled, resources available, a theme manager, and a fake date
        
        with patch('PyQt5.QtWidgets.QDialog.exec'):
            with patch('openlp.plugins.planningcenter.forms.selectplanform.date') as mock_date:
                # need to always return 7/27/2018 for date.today()
                mock_date.today.return_value = date(2018,7,29)
                mock_date.side_effect = lambda *args, **kw: date(*args, **kw)
            
            theme_manager = ThemeManager(None)
            self.form.planning_center_api.airplane_mode = True
            self.form.planning_center_api.airplane_mode_directory = TEST_PATH
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
            theme_list = theme_manager.get_themes()
            self.assertEqual(self.form.song_theme_selection_combo_box.count(),
                             len(theme_list),
                             'Count of song themes is incorrect')
            self.assertEqual(self.form.slide_theme_selection_combo_box.count(),
                             len(theme_list),
                             'Count of custom slide themes is incorrect')
            
