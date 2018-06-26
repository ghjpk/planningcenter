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
The :mod:`~openlp.plugins.planningcenter.planningcenterplugin` module contains the Plugin class
for the PlanningCenter plugin.
"""

import logging
import os
from tempfile import gettempdir
import sqlite3

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import UiStrings, Registry, translate
from openlp.core.lib import Plugin, StringContent, build_icon
from openlp.core.lib.db import Manager
from openlp.core.lib.ui import create_action
from openlp.core.utils.actions import ActionList
# from openlp.plugins.planningcenter.forms.duplicatesongremovalform import DuplicateSongRemovalForm
from openlp.plugins.planningcenter.forms.planningcenterform import PlanningCenterForm
# from openlp.plugins.planningcenter.lib import clean_song, upgrade
# from openlp.plugins.planningcenter.lib.db import init_schema, Song
# from openlp.plugins.planningcenter.lib.mediaitem import SongSearch
# from openlp.plugins.planningcenter.lib.importer import SongFormat
# from openlp.plugins.planningcenter.lib.importers.openlp import OpenLPSongImport
# from openlp.plugins.planningcenter.lib.mediaitem import SongMediaItem
# from openlp.plugins.planningcenter.lib.planningcentertab import PlanningCenterTab


log = logging.getLogger(__name__)
__default_settings__ = {
    'planningcenter/some default': 'default setting',
#     'planningcenter/db type': 'sqlite',
#     'planningcenter/db username': '',
#     'planningcenter/db password': '',
#     'planningcenter/db hostname': '',
#     'planningcenter/db database': '',
#     'planningcenter/last search type': SongSearch.Entire,
#     'planningcenter/last import type': SongFormat.OpenLyrics,
#     'planningcenter/update service on edit': False,
#     'planningcenter/add song from service': True,
#     'planningcenter/display songbar': True,
#     'planningcenter/display songbook': False,
#     'planningcenter/display copyright symbol': False,
#     'planningcenter/last directory import': '',
#     'planningcenter/last directory export': '',
#     'planningcenter/planningcenterelect username': '',
#     'planningcenter/planningcenterelect password': '',
#     'planningcenter/planningcenterelect searches': ''
}


class planningcenterplugin(Plugin):
    """
    This plugin enables the user to import services from Planning Center Online.
    """
    log.info('PlanningCenter Plugin loaded')

    def __init__(self):
        """
        Create and set up the PlanningCenter plugin.
        """
        #super(planningcenterplugin, self).__init__('planningcenter', __default_settings__, SongMediaItem, PlanningCenterTab)
        super(planningcenterplugin, self).__init__('planningcenter', __default_settings__, version='0.1')
        #self.manager = Manager('planningcenter', init_schema, upgrade_mod=upgrade)
#         self.weight = -10
#         self.icon_path = ':/plugins/plugin_planningcenter.png'
#         self.icon = build_icon(self.icon_path)
        self.planningcenterelect_form = None

#     def check_pre_conditions(self):
#         """
#         Check the plugin can run.
#         """
# #         return self.manager.session is not None
#         return True

    def initialise(self):
        """
        Initialise the plugin
        """
        log.info('PlanningCenter Initialising')
        super(planningcenterplugin, self).initialise()
        self.planningcenterelect_form = PlanningCenterForm(Registry().get('main_window'), self)
        self.planningcenterelect_form.initialise()
#         self.song_import_item.setVisible(True)
#         self.song_export_item.setVisible(True)
#         self.tools_reindex_item.setVisible(True)
#         self.tools_find_duplicates.setVisible(True)
#         action_list = ActionList.get_instance()
#         action_list.add_action(self.song_import_item, UiStrings().Import)
#         action_list.add_action(self.song_export_item, UiStrings().Export)
#         action_list.add_action(self.tools_reindex_item, UiStrings().Tools)
#         action_list.add_action(self.tools_find_duplicates, UiStrings().Tools)

    def add_import_menu_item(self, import_menu):
        """
        Add "PlanningCenter Service" to the **Import** menu.

        :param import_menu: The actual **Import** menu item, so that your actions can use it as their parent.
        """
        self.import_planningcenterelect_item = create_action(
            import_menu, 'import_planningcenterelect_item', text=translate('planningcenterplugin', 'Planning Center Service'),
            statustip=translate('planningcenterplugin', 'Import Planning Center Service Plan from Planning Center Online.'),
            triggers=self.on_import_planningcenterelect_item_triggered
        )
        import_menu.addAction(self.import_planningcenterelect_item)

#     def add_export_menu_item(self, export_menu):
#         """
#         Give the PlanningCenter plugin the opportunity to add items to the **Export** menu.
# 
#         :param export_menu: The actual **Export** menu item, so that your actions can use it as their parent.
#         """
#         # Main song import menu item - will eventually be the only one
#         self.song_export_item = create_action(
#             export_menu, 'songExportItem',
#             text=translate('planningcenterplugin', '&Song'),
#             tooltip=translate('planningcenterplugin', 'Exports planningcenter using the export wizard.'),
#             triggers=self.on_song_export_item_clicked)
#         export_menu.addAction(self.song_export_item)

#     def add_tools_menu_item(self, tools_menu):
#         """
#         Give the PlanningCenter plugin the opportunity to add items to the **Tools** menu.
# 
#         :param tools_menu: The actual **Tools** menu item, so that your actions can use it as their parent.
#         """
#         log.info('add tools menu')
#         self.tools_reindex_item = create_action(
#             tools_menu, 'toolsReindexItem',
#             text=translate('planningcenterplugin', '&Re-index PlanningCenter'),
#             icon=':/plugins/plugin_planningcenter.png',
#             statustip=translate('planningcenterplugin', 'Re-index the planningcenter database to improve searching and ordering.'),
#             visible=False, triggers=self.on_tools_reindex_item_triggered)
#         tools_menu.addAction(self.tools_reindex_item)
#         self.tools_find_duplicates = create_action(
#             tools_menu, 'toolsFindDuplicates',
#             text=translate('planningcenterplugin', 'Find &Duplicate PlanningCenter'),
#             statustip=translate('planningcenterplugin', 'Find and remove duplicate planningcenter in the song database.'),
#             visible=False, triggers=self.on_tools_find_duplicates_triggered, can_shortcuts=True)
#         tools_menu.addAction(self.tools_find_duplicates)

#     def on_tools_reindex_item_triggered(self):
#         """
#         Rebuild each song.
#         """
#         max_planningcenter = self.manager.get_object_count(Song)
#         if max_planningcenter == 0:
#             return
#         progress_dialog = QtWidgets.QProgressDialog(
#             translate('planningcenterplugin', 'Reindexing planningcenter...'), UiStrings().Cancel, 0, max_planningcenter, self.main_window)
#         progress_dialog.setWindowTitle(translate('planningcenterplugin', 'Reindexing planningcenter'))
#         progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
#         planningcenter = self.manager.get_all_objects(Song)
#         for number, song in enumerate(planningcenter):
#             clean_song(self.manager, song)
#             progress_dialog.setValue(number + 1)
#         self.manager.save_objects(planningcenter)
#         self.media_item.on_search_text_button_clicked()
# 
#     def on_tools_find_duplicates_triggered(self):
#         """
#         Search for duplicates in the song database.
#         """
#         DuplicateSongRemovalForm(self).exec()

    def on_import_planningcenterelect_item_triggered(self):
        """
        Run the PlanningCenter importer.
        """
        self.planningcenterelect_form.exec()
#         self.media_item.on_search_text_button_clicked()

#     def on_song_import_item_clicked(self):
#         """
#         Run the song import wizard.
#         """
#         if self.media_item:
#             self.media_item.on_import_click()
# 
#     def on_song_export_item_clicked(self):
#         """
#         Run the song export wizard.
#         """
#         if self.media_item:
#             self.media_item.on_export_click()

    @staticmethod
    def about():
        """
        Provides information for the plugin manager to display.

        :return: A translatable string with some basic information about the PlanningCenter plugin
        """
        return translate('planningcenterplugin', '<strong>PlanningCenter Plugin</strong>'
                                        '<br />The planningcenter plugin provides an interface to import service plans from the Planning Center Online v2 API.')

#     def uses_theme(self, theme):
#         """
#         Called to find out if the song plugin is currently using a theme.
# 
#         :param theme: The theme to check for usage
#         :return: count of the number of times the theme is used.
#         """
#         return len(self.manager.get_all_objects(Song, Song.theme_name == theme))
# 
#     def rename_theme(self, old_theme, new_theme):
#         """
#         Renames a theme the song plugin is using making the plugin use the new name.
# 
#         :param old_theme: The name of the theme the plugin should stop using.
#         :param new_theme: The new name the plugin should now use.
#         """
#         planningcenter_using_theme = self.manager.get_all_objects(Song, Song.theme_name == old_theme)
#         for song in planningcenter_using_theme:
#             song.theme_name = new_theme
#             self.manager.save_object(song)

#     def import_planningcenter(self, import_format, **kwargs):
#         """
#         Add the correct importer class
# 
#         :param import_format: The import_format to be used
#         :param kwargs: The arguments
#         :return: the correct importer
#         """
#         class_ = SongFormat.get(import_format, 'class')
#         importer = class_(self.manager, **kwargs)
#         importer.register(self.media_item.import_wizard)
#         return importer

    def set_plugin_text_strings(self):
        """
        Called to define all translatable texts of the plugin
        """
        # Name PluginList
        self.text_strings[StringContent.Name] = {
            'singular': translate('planningcenterplugin', 'PlanningCenter', 'name singular'),
            'plural': translate('planningcenterplugin', 'PlanningCenter', 'name plural')
        }
        # Name for MediaDockManager, SettingsManager
        self.text_strings[StringContent.VisibleName] = {
            'title': translate('planningcenterplugin', 'PlanningCenter', 'container title')
        }
        # Middle Header Bar
        tooltips = {
            'load': '',
            'import': translate('planningcenterplugin', 'Import All Plan Items into Current Service'),
            'new': translate('planningcenterplugin', 'Add a new song.'),
            'edit': translate('planningcenterplugin', 'Edit the selected song.'),
            'delete': translate('planningcenterplugin', 'Delete the selected song.'),
            'preview': translate('planningcenterplugin', 'Preview the selected song.'),
            'live': translate('planningcenterplugin', 'Send the selected song live.'),
            'service': translate('planningcenterplugin', 'Add the selected song to the service.')
        }
        self.set_plugin_ui_text_strings(tooltips)

#     def first_time(self):
#         """
#         If the first time wizard has run, this function is run to import all the new planningcenter into the database.
#         """
#         self.application.process_events()
#         self.on_tools_reindex_item_triggered()
#         self.application.process_events()
#         db_dir = os.path.join(gettempdir(), 'openlp')
#         if not os.path.exists(db_dir):
#             return
#         song_dbs = []
#         song_count = 0
#         for sfile in os.listdir(db_dir):
#             if sfile.startswith('planningcenter_') and sfile.endswith('.sqlite'):
#                 self.application.process_events()
#                 song_dbs.append(os.path.join(db_dir, sfile))
#                 song_count += planningcenterplugin._count_planningcenter(os.path.join(db_dir, sfile))
#         if not song_dbs:
#             return
#         self.application.process_events()
#         progress = QtWidgets.QProgressDialog(self.main_window)
#         progress.setWindowModality(QtCore.Qt.WindowModal)
#         progress.setWindowTitle(translate('OpenLP.Ui', 'Importing PlanningCenter'))
#         progress.setLabelText(translate('OpenLP.Ui', 'Starting import...'))
#         progress.setCancelButton(None)
#         progress.setRange(0, song_count)
#         progress.setMinimumDuration(0)
#         progress.forceShow()
#         self.application.process_events()
#         for db in song_dbs:
#             importer = OpenLPSongImport(self.manager, filename=db)
#             importer.do_import(progress)
#             self.application.process_events()
#         progress.setValue(song_count)
#         self.media_item.on_search_text_button_clicked()

    def finalise(self):
        """
        Time to tidy up on exit
        """
        log.info('PlanningCenter Finalising')
        self.new_service_created()
        # Clean up files and connections
#         self.manager.finalise()
#         self.song_import_item.setVisible(False)
#         self.song_export_item.setVisible(False)
#         self.tools_reindex_item.setVisible(False)
#         self.tools_find_duplicates.setVisible(False)
#         action_list = ActionList.get_instance()
#         action_list.remove_action(self.song_import_item, UiStrings().Import)
#         action_list.remove_action(self.song_export_item, UiStrings().Export)
#         action_list.remove_action(self.tools_reindex_item, UiStrings().Tools)
#         action_list.remove_action(self.tools_find_duplicates, UiStrings().Tools)
        super(planningcenterplugin, self).finalise()

    def new_service_created(self):
        """
        Remove temporary planningcenter from the database
        """
#         planningcenter = self.manager.get_all_objects(Song, Song.temporary is True)
#         for song in planningcenter:
#             self.manager.delete_object(Song, song.id)

#     @staticmethod
#     def _count_planningcenter(db_file):
#         """
#         Provide a count of the planningcenter in the database
# 
#         :param db_file: the database name to count
#         """
#         connection = sqlite3.connect(db_file)
#         cursor = connection.cursor()
#         cursor.execute('SELECT COUNT(id) AS song_count FROM planningcenter')
#         song_count = cursor.fetchone()[0]
#         connection.close()
#         try:
#             song_count = int(song_count)
#         except (TypeError, ValueError):
#             song_count = 0
#         return song_count
