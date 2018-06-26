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
The :mod:`~openlp.plugins.planningcenter.forms.planningcenterform` module contains the GUI for the PlanningCenter importer
"""

import logging
from datetime import datetime

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry, is_win
from openlp.plugins.planningcenter.forms.planningcenterdialog import Ui_PlanningCenterDialog
from openlp.plugins.planningcenter.lib.planningcenter_api import PlanningCenterAPI, SplitLyricsIntoVerses
from openlp.plugins.planningcenter.lib.planningcenter_servicemanager import ServiceManager, Song, CustomSlide


log = logging.getLogger(__name__)

class PlanningCenterForm(QtWidgets.QDialog, Ui_PlanningCenterDialog):
    """
    The :class:`PlanningCenterForm` class is the PlanningCenter dialog.
    """

    def __init__(self, parent=None, plugin=None, db_manager=None):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.plugin = plugin
        self.db_manager = db_manager
        self.setup_ui(self)
        self.service_manager = parent.service_manager

    def initialise(self):
        """
        Initialise the PlanningCenterForm
        """
        self.service_type_combo_box.currentIndexChanged.connect(self.on_service_type_combobox_changed)
        self.plan_selection_combo_box.currentIndexChanged.connect(self.on_plan_selection_combobox_changed)
        self.import_as_new_button.clicked.connect(self.on_import_as_new_button_clicked)

    def exec(self):
        """
        Execute the dialog. This method sets everything back to its initial
        values.
        """
        self.stacked_widget.setCurrentIndex(0)
        self.import_as_new_button.setEnabled(False)
        
        # create an Planning Center API Object
        self.planning_center_api = PlanningCenterAPI()
        
        # set the Service Type Dropdown Box from PCO
        service_types_list = self.planning_center_api.GetServiceTypeList()
        self.service_type_combo_box.clear()
        for service_type in service_types_list:
            self.service_type_combo_box.addItem(service_type['attributes']['name'],service_type['id'])
        self.service_type_combo_box.setCurrentIndex(0)
        self.on_plan_selection_combobox_changed()

        return QtWidgets.QDialog.exec(self)

    def done(self, r):
        """
        Log out of PlanningCenter.
 
        :param r: The result of the dialog.
        """
        log.debug('Closing PlanningCenterForm')
        return QtWidgets.QDialog.done(self, r)

    def on_service_type_combobox_changed(self):
        """
        Set the plan_selection_combo_box content based upon the current service_type_combo_box setting.
        """
        # set the Plan Dropdown Box from PCO
        service_type_id = self.service_type_combo_box.itemData(self.service_type_combo_box.currentIndex())
        plan_list = self.planning_center_api.GetPlanList(service_type_id)
        self.plan_selection_combo_box.clear()
        self.plan_selection_combo_box.addItem('Select Plan Date')
        self.plan_selection_combo_box.setCurrentIndex(0)
        # Get Today's date and see if it is listed... if it is, then select it in the combobox
        date_string = "{dt:%B} {dt.day}, {dt.year}".format(dt=datetime.today())
        for plan in plan_list:
            combo_box_index = self.plan_selection_combo_box.addItem(plan['attributes']['dates'],plan['id'])
            if date_string == plan['attributes']['dates']:
                self.plan_selection_combo_box.setCurrentIndex(combo_box_index)
                self.import_as_new_button.setEnabled(True)
                
    def on_plan_selection_combobox_changed(self):
        """
        Set the Import button enable/disable based upon the current plan_selection_combo_box setting.
        """
        current_index = self.plan_selection_combo_box.currentIndex()
        if current_index == 0 or current_index == -1:
            self.import_as_new_button.setEnabled(False)
        else:
            self.import_as_new_button.setEnabled(True)

    def on_import_as_new_button_clicked(self):
        """
        Create a new service and import all of the PCO items into it
        """
        # get the plan ID for the current plan selection
        plan_id = self.plan_selection_combo_box.itemData(self.plan_selection_combo_box.currentIndex())
        # get the items array from Planning Center
        planning_center_items_dict = self.planning_center_api.GetItemsDict(plan_id)
        # create a YYYYMMDD plan_date 
        datetime_object = datetime.strptime(self.plan_selection_combo_box.currentText(), '%B %d, %Y' )
        plan_date = datetime.strftime(datetime_object, '%Y%m%d')
        
        self.service_manager.on_new_service_clicked()
        planning_center_service_manager = ServiceManager(plan_date)
        # convert the planning center dict to a list of openlp items
        for item in planning_center_items_dict['data']:
            item_title = item['attributes']['title']
        
            if item['attributes']['item_type'] == 'song':
                arrangement_id = item['relationships']['arrangement']['data']['id']
                song_id = item['relationships']['song']['data']['id']
        
                # get arrangement from "included" resources
                arrangement_data = {}
                song_data = {}
                for included_item in planning_center_items_dict['included']:
                    if included_item['type'] == 'Song' and included_item['id'] == song_id:
                        song_data = included_item
                    elif included_item['type'] == 'Arrangement' and included_item['id'] == arrangement_id:
                        arrangement_data = included_item
                        
                    # if we have both song and arrangement set, stop iterating
                    if len(song_data) and len(arrangement_data):
                        break
                    
                author = song_data['attributes']['author']   
                if author is None:
                    author = "Unknown"
        
                lyrics = arrangement_data['attributes']['lyrics']
                arrangement_updated_at = arrangement_data['attributes']['updated_at']
        
                # split the lyrics into verses
                verses = []
                verses = SplitLyricsIntoVerses(lyrics)
                
                song = Song(item_title,author,verses,arrangement_updated_at)
                #song.SetTheme(self.m_songThemeComboBox.GetStringSelection())
                planning_center_service_manager.AddServiceItem(song)
            else:
                custom_slide = CustomSlide(item_title)
                #custom_slide.SetTheme(self.m_slideThemeComboBox.GetStringSelection())
                planning_center_service_manager.AddServiceItem(custom_slide)

        self.service_manager.set_file_name(plan_date)
        self.service_manager.main_window.display_progress_bar(len(planning_center_service_manager.openlp_data))
        self.service_manager.process_service_items(planning_center_service_manager.openlp_data)
        self.service_manager.main_window.finished_progress_bar()
        self.service_manager.application.set_normal_cursor()
        self.service_manager.repaint_service_list(-1, -1)
        self.done(QtWidgets.QDialog.Accepted)

        print("woohoo!")
        
    def on_update_button_clicked(self):
        """
        Update existing service items with those from PCO that have newer updated timestamps
        """
        pass

    @property
    def application(self):
        """
        Adds the openlp to the class dynamically.
        Windows needs to access the application in a dynamic manner.
        """
        if is_win():
            return Registry().get('application')
        else:
            if not hasattr(self, '_application'):
                self._application = Registry().get('application')
            return self._application
