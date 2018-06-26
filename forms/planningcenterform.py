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
import re
# import os
# from time import sleep
from datetime import datetime

from PyQt5 import QtCore, QtWidgets

from openlp.core import Settings
from openlp.core.common import Registry, is_win
from openlp.core.lib import translate
from openlp.plugins.planningcenter.forms.planningcenterdialog import Ui_PlanningCenterDialog
from openlp.plugins.planningcenter.lib.planningcenter_api import PlanningCenterAPI, SplitLyricsIntoVerses

# reverse engineer songs
from openlp.plugins.planningcenter.lib.planningcenter_servicemanager import ServiceManager, ServiceItem, Song, CustomSlide


log = logging.getLogger(__name__)


# class SearchWorker(QtCore.QObject):
#     """
#     Run the actual PlanningCenter search, and notify the GUI when we find each song.
#     """
#     show_info = QtCore.pyqtSignal(str, str)
#     found_song = QtCore.pyqtSignal(dict)
#     finished = QtCore.pyqtSignal()
#     quit = QtCore.pyqtSignal()
# 
#     def __init__(self, importer, search_text):
#         super().__init__()
#         self.importer = importer
#         self.search_text = search_text
# 
#     def start(self):
#         """
#         Run a search and then parse the results page of the search.
#         """
# #         songs = self.importer.search(self.search_text, 1000, self._found_song_callback)
# #         if len(songs) >= 1000:
# #             self.show_info.emit(
# #                 translate('SongsPlugin.PlanningCenterForm', 'More than 1000 results'),
# #                 translate('SongsPlugin.PlanningCenterForm', 'Your search has returned more than 1000 results, it has '
# #                                                         'been stopped. Please refine your search to fetch better '
# #                                                         'results.'))
#         self.finished.emit()
#         self.quit.emit()

#     def _found_song_callback(self, song):
#         """
#         A callback used by the paginate function to notify watching processes when it finds a song.
# 
#         :param song: The song that was found
#         """
#         self.found_song.emit(song)


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
#         self.thread = None
#         self.worker = None
#         self.song_count = 0
#         self.song = None
        #self.set_progress_visible(False)
        #self.song_select_importer = PlanningCenterImport(self.db_manager)
#         self.save_password_checkbox.toggled.connect(self.on_save_password_checkbox_toggled)
#         self.login_button.clicked.connect(self.on_login_button_clicked)
#         self.search_button.clicked.connect(self.on_search_button_clicked)
#         self.search_combobox.returnPressed.connect(self.on_search_button_clicked)
#         self.stop_button.clicked.connect(self.on_stop_button_clicked)
#         self.logout_button.clicked.connect(self.done)
#         self.search_results_widget.itemDoubleClicked.connect(self.on_search_results_widget_double_clicked)
#         self.search_results_widget.itemSelectionChanged.connect(self.on_search_results_widget_selection_changed)
#         self.view_button.clicked.connect(self.on_view_button_clicked)
#         self.back_button.clicked.connect(self.on_back_button_clicked)
#         self.import_button.clicked.connect(self.on_import_button_clicked)

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
        
#         self.username_edit.setEnabled(True)
#         self.password_edit.setEnabled(True)
#         self.save_password_checkbox.setEnabled(True)
#         self.search_combobox.clearEditText()
#         self.search_combobox.clear()
#         self.search_results_widget.clear()
#         self.view_button.setEnabled(False)
#         if Settings().contains(self.plugin.settings_section + '/planningcenter password'):
#             self.username_edit.setText(Settings().value(self.plugin.settings_section + '/planningcenter username'))
#             self.password_edit.setText(Settings().value(self.plugin.settings_section + '/planningcenter password'))
#             self.save_password_checkbox.setChecked(True)
#         if Settings().contains(self.plugin.settings_section + '/planningcenter searches'):
#             self.search_combobox.addItems(
#                 Settings().value(self.plugin.settings_section + '/planningcenter searches').split('|'))
#         self.username_edit.setFocus()
        return QtWidgets.QDialog.exec(self)

    def done(self, r):
        """
        Log out of PlanningCenter.
 
        :param r: The result of the dialog.
        """
        log.debug('Closing PlanningCenterForm')
# #         if self.stacked_widget.currentIndex() > 0:
# #             progress_dialog = QtWidgets.QProgressDialog(
# #                 translate('SongsPlugin.PlanningCenterForm', 'Logging out...'), '', 0, 2, self)
# #             progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
# #             progress_dialog.setCancelButton(None)
# #             progress_dialog.setValue(1)
# #             progress_dialog.show()
# #             progress_dialog.setFocus()
# #             self.application.process_events()
# #             sleep(0.5)
# #             self.application.process_events()
# #             self.song_select_importer.logout()
# #             self.application.process_events()
# #             progress_dialog.setValue(2)
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

#     def _update_login_progress(self):
#         """
#         Update the progress bar as the user logs in.
#         """
#         self.login_progress_bar.setValue(self.login_progress_bar.value() + 1)
#         self.application.process_events()
# 
#     def _update_song_progress(self):
#         """
#         Update the progress bar as the song is being downloaded.
#         """
#         self.song_progress_bar.setValue(self.song_progress_bar.value() + 1)
#         self.application.process_events()
# 
#     def _view_song(self, current_item):
#         """
#         Load a song into the song view.
#         """
#         if not current_item:
#             return
#         else:
#             current_item = current_item.data(QtCore.Qt.UserRole)
#         # Stop the current search, if it's running
#         self.song_select_importer.stop()
#         # Clear up the UI
#         self.song_progress_bar.setVisible(True)
#         self.import_button.setEnabled(False)
#         self.back_button.setEnabled(False)
#         self.title_edit.setText('')
#         self.title_edit.setEnabled(False)
#         self.copyright_edit.setText('')
#         self.copyright_edit.setEnabled(False)
#         self.ccli_edit.setText('')
#         self.ccli_edit.setEnabled(False)
#         self.author_list_widget.clear()
#         self.author_list_widget.setEnabled(False)
#         self.lyrics_table_widget.clear()
#         self.lyrics_table_widget.setRowCount(0)
#         self.lyrics_table_widget.setEnabled(False)
#         self.stacked_widget.setCurrentIndex(2)
#         song = {}
#         for key, value in current_item.items():
#             song[key] = value
#         self.song_progress_bar.setValue(0)
#         self.application.process_events()
#         # Get the full song
#         song = self.song_select_importer.get_song(song, self._update_song_progress)
#         if not song:
#             QtWidgets.QMessageBox.critical(
#                 self, translate('SongsPlugin.PlanningCenterForm', 'Incomplete song'),
#                 translate('SongsPlugin.PlanningCenterForm', 'This song is missing some information, like the lyrics, '
#                                                         'and cannot be imported.'),
#                 QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Ok), QtWidgets.QMessageBox.Ok)
#             self.stacked_widget.setCurrentIndex(1)
#             return
#         # Update the UI
#         self.title_edit.setText(song['title'])
#         self.copyright_edit.setText(song['copyright'])
#         self.ccli_edit.setText(song['ccli_number'])
#         for author in song['authors']:
#             QtWidgets.QListWidgetItem(author, self.author_list_widget)
#         for counter, verse in enumerate(song['verses']):
#             self.lyrics_table_widget.setRowCount(self.lyrics_table_widget.rowCount() + 1)
#             item = QtWidgets.QTableWidgetItem(verse['lyrics'])
#             item.setData(QtCore.Qt.UserRole, verse['label'])
#             item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
#             self.lyrics_table_widget.setItem(counter, 0, item)
#         self.lyrics_table_widget.setVerticalHeaderLabels([verse['label'] for verse in song['verses']])
#         self.lyrics_table_widget.resizeRowsToContents()
#         self.title_edit.setEnabled(True)
#         self.copyright_edit.setEnabled(True)
#         self.ccli_edit.setEnabled(True)
#         self.author_list_widget.setEnabled(True)
#         self.lyrics_table_widget.setEnabled(True)
#         self.lyrics_table_widget.repaint()
#         self.import_button.setEnabled(True)
#         self.back_button.setEnabled(True)
#         self.song_progress_bar.setVisible(False)
#         self.song_progress_bar.setValue(0)
#         self.song = song
#         self.application.process_events()
# 
#     def on_save_password_checkbox_toggled(self, checked):
#         """
#         Show a warning dialog when the user toggles the save checkbox on or off.
# 
#         :param checked: If the combobox is checked or not
#         """
#         if checked and self.login_page.isVisible():
#             answer = QtWidgets.QMessageBox.question(
#                 self, translate('SongsPlugin.PlanningCenterForm', 'Save Username and Password'),
#                 translate('SongsPlugin.PlanningCenterForm', 'WARNING: Saving your username and password is INSECURE, your '
#                                                         'password is stored in PLAIN TEXT. Click Yes to save your '
#                                                         'password or No to cancel this.'),
#                 QtWidgets.QMessageBox.StandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No),
#                 QtWidgets.QMessageBox.No)
#             if answer == QtWidgets.QMessageBox.No:
#                 self.save_password_checkbox.setChecked(False)
# 
#     def on_login_button_clicked(self):
#         """
#         Log the user in to PlanningCenter.
#         """
#         self.username_edit.setEnabled(False)
#         self.password_edit.setEnabled(False)
#         self.save_password_checkbox.setEnabled(False)
#         self.login_button.setEnabled(False)
#         self.login_spacer.setVisible(False)
#         self.login_progress_bar.setValue(0)
#         self.login_progress_bar.setVisible(True)
#         self.application.process_events()
#         # Log the user in
#         if not self.song_select_importer.login(
#                 self.username_edit.text(), self.password_edit.text(), self._update_login_progress):
#             QtWidgets.QMessageBox.critical(
#                 self,
#                 translate('SongsPlugin.PlanningCenterForm', 'Error Logging In'),
#                 translate('SongsPlugin.PlanningCenterForm',
#                           'There was a problem logging in, perhaps your username or password is incorrect?')
#             )
#         else:
#             if self.save_password_checkbox.isChecked():
#                 Settings().setValue(self.plugin.settings_section + '/planningcenter username', self.username_edit.text())
#                 Settings().setValue(self.plugin.settings_section + '/planningcenter password', self.password_edit.text())
#             else:
#                 Settings().remove(self.plugin.settings_section + '/planningcenter username')
#                 Settings().remove(self.plugin.settings_section + '/planningcenter password')
#             self.stacked_widget.setCurrentIndex(1)
#         self.login_progress_bar.setVisible(False)
#         self.login_progress_bar.setValue(0)
#         self.login_spacer.setVisible(True)
#         self.login_button.setEnabled(True)
#         self.username_edit.setEnabled(True)
#         self.password_edit.setEnabled(True)
#         self.save_password_checkbox.setEnabled(True)
#         self.search_combobox.setFocus()
#         self.application.process_events()
# 
#     def on_search_button_clicked(self):
#         """
#         Run a search on PlanningCenter.
#         """
#         # Set up UI components
#         self.view_button.setEnabled(False)
#         self.search_button.setEnabled(False)
#         self.search_progress_bar.setMinimum(0)
#         self.search_progress_bar.setMaximum(0)
#         self.search_progress_bar.setValue(0)
#         self.set_progress_visible(True)
#         self.search_results_widget.clear()
#         self.result_count_label.setText(translate('SongsPlugin.PlanningCenterForm', 'Found %s song(s)') % self.song_count)
#         self.application.process_events()
#         self.song_count = 0
#         search_history = self.search_combobox.getItems()
#         Settings().setValue(self.plugin.settings_section + '/planningcenter searches', '|'.join(search_history))
#         # Create thread and run search
#         self.thread = QtCore.QThread()
#         self.worker = SearchWorker(self.song_select_importer, self.search_combobox.currentText())
#         self.worker.moveToThread(self.thread)
#         self.thread.started.connect(self.worker.start)
#         self.worker.show_info.connect(self.on_search_show_info)
#         self.worker.found_song.connect(self.on_search_found_song)
#         self.worker.finished.connect(self.on_search_finished)
#         self.worker.quit.connect(self.thread.quit)
#         self.worker.quit.connect(self.worker.deleteLater)
#         self.thread.finished.connect(self.thread.deleteLater)
#         self.thread.start()
# 
#     def on_stop_button_clicked(self):
#         """
#         Stop the search when the stop button is clicked.
#         """
#         self.song_select_importer.stop()
# 
#     def on_search_show_info(self, title, message):
#         """
#         Show an informational message from the search thread
#         :param title:
#         :param message:
#         """
#         QtWidgets.QMessageBox.information(self, title, message)
# 
#     def on_search_found_song(self, song):
#         """
#         Add a song to the list when one is found.
#         :param song:
#         """
#         self.song_count += 1
#         self.result_count_label.setText(translate('SongsPlugin.PlanningCenterForm', 'Found %s song(s)') % self.song_count)
#         item_title = song['title'] + ' (' + ', '.join(song['authors']) + ')'
#         song_item = QtWidgets.QListWidgetItem(item_title, self.search_results_widget)
#         song_item.setData(QtCore.Qt.UserRole, song)
# 
#     def on_search_finished(self):
#         """
#         Slot which is called when the search is completed.
#         """
#         self.application.process_events()
#         self.set_progress_visible(False)
#         self.search_button.setEnabled(True)
#         self.application.process_events()
# 
#     def on_search_results_widget_selection_changed(self):
#         """
#         Enable or disable the view button when the selection changes.
#         """
#         self.view_button.setEnabled(len(self.search_results_widget.selectedItems()) > 0)
# 
#     def on_view_button_clicked(self):
#         """
#         View a song from PlanningCenter.
#         """
#         self._view_song(self.search_results_widget.currentItem())
# 
#     def on_search_results_widget_double_clicked(self, current_item):
#         """
#         View a song from PlanningCenter
# 
#         :param current_item:
#         """
#         self._view_song(current_item)
# 
#     def on_back_button_clicked(self):
#         """
#         Go back to the search page.
#         """
#         self.stacked_widget.setCurrentIndex(1)
#         self.search_combobox.setFocus()
# 
#     def on_import_button_clicked(self):
#         """
#         Import a song from PlanningCenter.
#         """
#         self.song_select_importer.save_song(self.song)
#         self.song = None
#         if QtWidgets.QMessageBox.question(self, translate('SongsPlugin.PlanningCenterForm', 'Song Imported'),
#                                           translate('SongsPlugin.PlanningCenterForm',
#                                                     'Your song has been imported, would you '
#                                                     'like to import more songs?'),
#                                           QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
#                                           QtWidgets.QMessageBox.Yes) == QtWidgets.QMessageBox.Yes:
#             self.on_back_button_clicked()
#         else:
#             self.application.process_events()
#             self.done(QtWidgets.QDialog.Accepted)
# 
#     def set_progress_visible(self, is_visible):
#         """
#         Show or hide the search progress, including the stop button.
#         """
#         self.search_progress_bar.setVisible(is_visible)
#         self.stop_button.setVisible(is_visible)

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
