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
The :mod:`~openlp.plugins.planningcenter.forms.selectplanform` module contains the GUI for the PlanningCenter Service importer
"""

import logging
import re
from datetime import date, datetime

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import Registry, is_win, Settings
from openlp.plugins.planningcenter.forms.selectplandialog import Ui_SelectPlanDialog
from openlp.plugins.planningcenter.forms.editauthform import EditAuthForm
from openlp.plugins.planningcenter.lib.customimport import PlanningCenterCustomImport
from openlp.plugins.planningcenter.lib.planningcenter_api import PlanningCenterAPI
from openlp.plugins.planningcenter.lib.songimport import PlanningCenterSongImport

log = logging.getLogger(__name__)


class SelectPlanForm(QtWidgets.QDialog, Ui_SelectPlanDialog):
    """
    The :class:`PlanningCenterForm` class is the PlanningCenter dialog.
    """

    def __init__(self, parent=None, plugin=None):
        QtWidgets.QDialog.__init__(self, parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
        self.plugin = plugin
        # create an Planning Center API Object
        application_id = Settings().value("planningcenter/application_id")
        secret = Settings().value("planningcenter/secret")
        self.planning_center_api = PlanningCenterAPI(application_id,secret)
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
        self.service_type_combo_box.currentIndexChanged.connect(self.on_service_type_combobox_changed)
        self.plan_selection_combo_box.currentIndexChanged.connect(self.on_plan_selection_combobox_changed)
        self.import_as_new_button.clicked.connect(self.on_import_as_new_button_clicked)
        self.update_existing_button.clicked.connect(self.on_update_existing_button_clicked)
        self.edit_auth_button.clicked.connect(self.on_edit_auth_button_clicked)
        self.import_as_new_button.setEnabled(False)
        self.update_existing_button.setEnabled(False)        
        # set the Service Type Dropdown Box from PCO
        service_types_list = self.planning_center_api.GetServiceTypeList()
        self.service_type_combo_box.clear()
        for service_type in service_types_list:
            self.service_type_combo_box.addItem(service_type['attributes']['name'],service_type['id'])
        self.service_type_combo_box.setCurrentIndex(0)
        self.on_plan_selection_combobox_changed()
        # Set the 2 lists of themes
        theme_manager = Registry().get('theme_manager')
        for theme in theme_manager.get_themes():
            self.song_theme_selection_combo_box.addItem(theme)
            self.slide_theme_selection_combo_box.addItem(theme)

        return QtWidgets.QDialog.exec(self)

    def done(self, r):
        """
        Close dialog.
 
        :param r: The result of the dialog.
        """
        log.debug('Closing PlanningCenterForm')
        self.service_type_combo_box.currentIndexChanged.disconnect()
        self.plan_selection_combo_box.currentIndexChanged.disconnect()
        self.import_as_new_button.clicked.disconnect()
        self.update_existing_button.clicked.disconnect()
        self.edit_auth_button.clicked.disconnect()

        return QtWidgets.QDialog.done(self, r)

    def on_edit_auth_button_clicked(self):
        """
        Open the edit auth screen
        """
        auth_form = EditAuthForm(self)
        auth_form.initialise()
        auth_form.exec()
        self.done(1)
        
    def on_service_type_combobox_changed(self):
        """
        Set the plan_selection_combo_box content based upon the current service_type_combo_box setting.
        """
        # set the Plan Dropdown Box from PCO
        service_type_id = self.service_type_combo_box.itemData(self.service_type_combo_box.currentIndex())
        if service_type_id:
            plan_list = self.planning_center_api.GetPlanList(service_type_id)
            self.plan_selection_combo_box.clear()
            self.plan_selection_combo_box.addItem('Select Plan Date')
            self.plan_selection_combo_box.setCurrentIndex(0)
            
            # Get Today's date and see if it is listed... if it is, then select it in the combobox
            for plan in plan_list:
                self.plan_selection_combo_box.addItem(plan['attributes']['dates'],plan['id'])
                # sort_date=str: 2018-12-21T19:00:00Z
                plan_datetime = datetime.strptime(plan['attributes']['sort_date'].rstrip("Z"),'%Y-%m-%dT%H:%M:%S')
                plan_date = date(plan_datetime.year, plan_datetime.month, plan_datetime.day)
                # if we have any date that matches today or in the future, select it
                today = date.today()
                if plan_date >= today:
                    self.plan_selection_combo_box.setCurrentIndex(self.plan_selection_combo_box.count()-1)
                    self.import_as_new_button.setEnabled(True)
                    self.update_existing_button.setEnabled(True)
                
    def on_plan_selection_combobox_changed(self):
        """
        Set the Import button enable/disable based upon the current plan_selection_combo_box setting.
        """
        current_index = self.plan_selection_combo_box.currentIndex()
        if current_index == 0 or current_index == -1:
            self.import_as_new_button.setEnabled(False)
            self.update_existing_button.setEnabled(False)
        else:
            self.import_as_new_button.setEnabled(True)
            self.update_existing_button.setEnabled(True)

    def on_update_existing_button_clicked(self):
        """
        Call the import function but tell it to also do an update so that it can 
        keep changed items
        """
        self.on_import_as_new_button_clicked(True)

    def on_import_as_new_button_clicked(self, update = False):
        """
        Create a new service and import all of the PCO items into it
        """
        service_manager = Registry().get('service_manager')
        old_service_items = []
        if update:
            old_service_items = service_manager.service_items.copy()
            service_manager.new_file()
        else:
            service_manager.on_new_service_clicked()
        # we only continue here if the service_manager is now empty
        if len(service_manager.service_items) == 0:
            service_manager.application.set_busy_cursor()
            # get the plan ID for the current plan selection
            plan_id = self.plan_selection_combo_box.itemData(self.plan_selection_combo_box.currentIndex())
            # get the items array from Planning Center
            planning_center_items_dict = self.planning_center_api.GetItemsDict(plan_id)
            service_manager.main_window.display_progress_bar(len(planning_center_items_dict['data']))
            # convert the planning center dict to Songs and Add them to the ServiceManager
            pco_id_to_openlp_id = {}
            for item in planning_center_items_dict['data']:
                item_title = item['attributes']['title']
                media_type = ''
                openlp_id = -1
                if item['attributes']['item_type'] == 'song':
                    arrangement_id = item['relationships']['arrangement']['data']['id']
                    song_id = item['relationships']['song']['data']['id']
                    if song_id not in pco_id_to_openlp_id:
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
                        lyrics = arrangement_data['attributes']['lyrics']
                        arrangement_updated_at = datetime.strptime(arrangement_data['attributes']['updated_at'].rstrip("Z"), '%Y-%m-%dT%H:%M:%S')
                        # start importing the song
                        pco_import = PlanningCenterSongImport()
                        theme_name = self.song_theme_selection_combo_box.currentText()
                        openlp_id = pco_import.add_song(item_title,author,lyrics,theme_name,arrangement_updated_at)
                        pco_id_to_openlp_id[song_id] = openlp_id
    
                    openlp_id = pco_id_to_openlp_id[song_id]
                    media_type = 'songs'
                else:
                    """ 
                    PCO has deprecated their custom slide interface and they are 
                    planning to eliminate it in mid-2019, so this interface will not 
                    support their custom slides except to create a custom slide 
                    with just a title
                    """
                    theme_name = self.slide_theme_selection_combo_box.currentText()
                    html_details = item['attributes']['html_details']
                    custom_import = PlanningCenterCustomImport()
                    openlp_id = custom_import.add_slide(item_title,html_details,theme_name)
                    media_type = 'custom'
                
                # get the current values of these values so I can set them back to this value
                media_type_plugin = Registry().get(media_type)
                # the variable suffix names below for "songs" is "song", so change media_type to song
                media_type_suffix = media_type
                if media_type == 'songs':
                    media_type_suffix = 'song'
                previous_remote_triggered = media_type_plugin.remote_triggered
                previous_remote_value = getattr(media_type_plugin, "remote_{0}".format(media_type_suffix))
                # turn on remote song feature to add to service
                media_type_plugin.remote_triggered = True
                setattr(media_type_plugin,"remote_{0}".format(media_type_suffix), openlp_id)
                media_type_plugin.add_to_service(remote=openlp_id)
                # reset values to their previous values
                media_type_plugin.remote_triggered = previous_remote_triggered
                setattr(media_type_plugin,"remote_{0}".format(media_type_suffix), previous_remote_value)
                service_manager.main_window.increment_progress_bar()
                        
            if update:
                for old_service_item in old_service_items:
                    # see if this service_item contained within the current set of service items
                    
                    # see if we have this same value in the new service
                    for service_index,service_item in enumerate(service_manager.service_items):
                        # we can compare songs to songs and custom to custom but not between them
                        if old_service_item['service_item'].name == 'songs' and service_item['service_item'].name == 'songs':
                            if old_service_item['service_item'].audit == service_item['service_item'].audit:
                                # get the timestamp from the xml of both the old and new and compare... 
                                # modifiedDate="2018-06-30T18:44:35Z"
                                old_match = re.search('modifiedDate="(.+?)Z*"', old_service_item['service_item'].xml_version)
                                old_datetime = datetime.strptime(old_match.group(1), '%Y-%m-%dT%H:%M:%S')
                                new_match = re.search('modifiedDate="(.+?)Z*"', service_item['service_item'].xml_version)
                                new_datetime = datetime.strptime(new_match.group(1), '%Y-%m-%dT%H:%M:%S')
                                # if old timestamp is more recent than new, then copy old to new
                                if old_datetime > new_datetime:
                                    service_manager.service_items[service_index] = old_service_item
                                break
                        elif old_service_item['service_item'].name == 'custom' and service_item['service_item'].name == 'custom':
                            """ we don't get actual slide content from the V2 PC API, so all we create by default is a 
                            single slide with matching title and content.  If the content
                            is different between the old serviceitem (previously imported
                            from PC and the new content that we are importing now, then
                            the assumption is that we updated this content and we want to 
                            keep the old content after this update.  If we actually updated
                            something on the PC site in this slide, it would have a
                            different title because that is all we can get the v2API """
                            if old_service_item['service_item'].title == service_item['service_item'].title:
                                if old_service_item['service_item']._raw_frames != service_item['service_item']._raw_frames:
                                    service_manager.service_items[service_index] = old_service_item
                                break
                            
            service_manager.main_window.finished_progress_bar()     
            # select the first item
            item = service_manager.service_manager_list.topLevelItem(0)
            service_manager.service_manager_list.setCurrentItem(item)
            service_manager.repaint_service_list(-1, -1)
            service_manager.application.set_normal_cursor()
        self.done(QtWidgets.QDialog.Accepted)
            

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
