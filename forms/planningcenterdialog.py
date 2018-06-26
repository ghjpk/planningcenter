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
The :mod:`~openlp.plugins.planningcenter.forms.planningcenterdialog` module contains the user interface code for the dialog
"""

from PyQt5 import QtCore, QtWidgets

from openlp.core.common import HistoryComboBox
from openlp.core.lib import translate, build_icon
from openlp.core.ui import SingleColumnTableWidget


class Ui_PlanningCenterDialog(object):
    """
    The actual Qt components that make up the dialog.
    """
    def setup_ui(self, planningcenter_dialog):
        planningcenter_dialog.setObjectName('planningcenter_dialog')
        planningcenter_dialog.resize(616, 378)
        self.planningcenter_layout = QtWidgets.QVBoxLayout(planningcenter_dialog)
        self.planningcenter_layout.setSpacing(0)
        self.planningcenter_layout.setContentsMargins(0, 0, 0, 0)
        self.planningcenter_layout.setObjectName('planningcenter_layout')
        self.stacked_widget = QtWidgets.QStackedWidget(planningcenter_dialog)
        self.stacked_widget.setObjectName('stacked_widget')
        self.planningcenter_layout.addWidget(self.stacked_widget)
        
        self.plan_selection_page = QtWidgets.QWidget()
        self.plan_selection_page.setObjectName('plan_selection_page')
        self.stacked_widget.addWidget(self.plan_selection_page)
        
        self.plan_selection_layout = QtWidgets.QFormLayout(self.plan_selection_page)
        self.plan_selection_layout.setContentsMargins(120, 100, 120, 100)
        self.plan_selection_layout.setSpacing(8)
        self.plan_selection_layout.setObjectName('plan_selection_layout')
        
        self.notice_layout = QtWidgets.QHBoxLayout()
        self.notice_layout.setObjectName('notice_layout')
        self.notice_label = QtWidgets.QLabel(self.plan_selection_page)
        self.notice_label.setWordWrap(True)
        self.notice_label.setObjectName('notice_label')
        self.notice_layout.addWidget(self.notice_label)
        self.plan_selection_layout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.notice_layout)
        
        # Service Type GUI Elements -- service_type combo_box
        self.service_type_label = QtWidgets.QLabel(self.plan_selection_page)
        self.service_type_label.setObjectName('service_type_label')
        self.plan_selection_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.service_type_label)
        self.service_type_combo_box = QtWidgets.QComboBox(self.plan_selection_page)
        self.service_type_combo_box.setObjectName('service_type_combo_box')
        self.plan_selection_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.service_type_combo_box)
        self.service_type_label.setBuddy(self.service_type_combo_box)

        # Plan Selection GUI Elements
        self.plan_selection_label = QtWidgets.QLabel(self.plan_selection_page)
        self.plan_selection_label.setObjectName('plan_selection_label')
        self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.plan_selection_label)
        self.plan_selection_combo_box = QtWidgets.QComboBox(self.plan_selection_page)
        self.plan_selection_combo_box.setObjectName('plan_selection_combo_box')
        self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.plan_selection_combo_box)
        self.plan_selection_label.setBuddy(self.plan_selection_combo_box)   
        
        # Import Button
        self.import_button_layout = QtWidgets.QHBoxLayout()
        self.import_button_layout.setSpacing(8)
        self.import_button_layout.setContentsMargins(0, -1, -1, -1)
        self.import_button_layout.setObjectName('import_button_layout')
        self.import_as_new_button = QtWidgets.QPushButton(self.plan_selection_page)
        self.import_as_new_button.setObjectName('import_as_new_button')
        self.import_button_layout.addWidget(self.import_as_new_button)
        self.plan_selection_layout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.import_button_layout)    

#         self.password_label = QtWidgets.QLabel(self.plan_selection_page)
#         self.password_label.setObjectName('passwordLabel')
#         self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.password_label)
#         self.password_edit = QtWidgets.QLineEdit(self.plan_selection_page)
#         self.password_edit.setEchoMode(QtWidgets.QLineEdit.Password)
#         self.password_edit.setObjectName('passwordEdit')
#         self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.password_edit)
#         self.save_password_checkbox = QtWidgets.QCheckBox(self.plan_selection_page)
#         self.save_password_checkbox.setTristate(False)
#         self.save_password_checkbox.setObjectName('save_password_checkbox')
#         self.plan_selection_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.save_password_checkbox)
#         self.login_button_layout = QtWidgets.QHBoxLayout()
#         self.login_button_layout.setSpacing(8)
#         self.login_button_layout.setContentsMargins(0, -1, -1, -1)
#         self.login_button_layout.setObjectName('login_button_layout')
#         self.login_spacer = QtWidgets.QWidget(self.plan_selection_page)
#         self.login_spacer.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.login_spacer.setObjectName('login_spacer')
#         self.login_button_layout.addWidget(self.login_spacer)
#         self.login_progress_bar = QtWidgets.QProgressBar(self.plan_selection_page)
#         self.login_progress_bar.setMinimum(0)
#         self.login_progress_bar.setMaximum(3)
#         self.login_progress_bar.setValue(0)
#         self.login_progress_bar.setMinimumWidth(200)
#         self.login_progress_bar.setVisible(False)
#         self.login_button_layout.addWidget(self.login_progress_bar)
#         self.login_button = QtWidgets.QPushButton(self.plan_selection_page)
#         self.login_button.setIcon(build_icon(':/songs/song_author_edit.png'))
#         self.login_button.setObjectName('login_button')
#         self.login_button_layout.addWidget(self.login_button)
#         self.plan_selection_layout.setLayout(4, QtWidgets.QFormLayout.SpanningRole, self.login_button_layout)

#         self.search_page = QtWidgets.QWidget()
#         self.search_page.setObjectName('search_page')
#         self.search_layout = QtWidgets.QVBoxLayout(self.search_page)
#         self.search_layout.setSpacing(8)
#         self.search_layout.setContentsMargins(8, 8, 8, 8)
#         self.search_layout.setObjectName('search_layout')
#         self.search_input_layout = QtWidgets.QHBoxLayout()
#         self.search_input_layout.setSpacing(8)
#         self.search_input_layout.setObjectName('search_input_layout')
#         self.search_label = QtWidgets.QLabel(self.search_page)
#         self.search_label.setObjectName('search_label')
#         self.search_input_layout.addWidget(self.search_label)
#         self.search_combobox = HistoryComboBox(self.search_page)
#         self.search_combobox.setObjectName('search_combobox')
#         self.search_input_layout.addWidget(self.search_combobox)
#         self.search_button = QtWidgets.QPushButton(self.search_page)
#         self.search_button.setIcon(build_icon(':/general/general_find.png'))
#         self.search_button.setObjectName('search_button')
#         self.search_input_layout.addWidget(self.search_button)
#         self.search_layout.addLayout(self.search_input_layout)
#         self.search_progress_layout = QtWidgets.QHBoxLayout()
#         self.search_progress_layout.setSpacing(8)
#         self.search_progress_layout.setObjectName('search_progress_layout')
#         self.search_progress_bar = QtWidgets.QProgressBar(self.search_page)
#         self.search_progress_bar.setMinimum(0)
#         self.search_progress_bar.setMaximum(3)
#         self.search_progress_bar.setValue(0)
#         self.search_progress_layout.addWidget(self.search_progress_bar)
#         self.stop_button = QtWidgets.QPushButton(self.search_page)
#         self.stop_button.setIcon(build_icon(':/songs/song_search_stop.png'))
#         self.stop_button.setObjectName('stop_button')
#         self.search_progress_layout.addWidget(self.stop_button)
#         self.search_layout.addLayout(self.search_progress_layout)
#         self.search_results_widget = QtWidgets.QListWidget(self.search_page)
#         self.search_results_widget.setProperty("showDropIndicator", False)
#         self.search_results_widget.setAlternatingRowColors(True)
#         self.search_results_widget.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
#         self.search_results_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
#         self.search_results_widget.setObjectName('search_results_widget')
#         self.search_layout.addWidget(self.search_results_widget)
#         self.result_count_label = QtWidgets.QLabel(self.search_page)
#         self.result_count_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignCenter)
#         self.result_count_label.setObjectName('result_count_label')
#         self.search_layout.addWidget(self.result_count_label)
#         self.view_layout = QtWidgets.QHBoxLayout()
#         self.view_layout.setSpacing(8)
#         self.view_layout.setObjectName('view_layout')
#         self.logout_button = QtWidgets.QPushButton(self.search_page)
#         self.logout_button.setIcon(build_icon(':/songs/song_author_edit.png'))
#         self.view_layout.addWidget(self.logout_button)
#         self.view_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
#         self.view_layout.addItem(self.view_spacer)
#         self.view_button = QtWidgets.QPushButton(self.search_page)
#         self.view_button.setIcon(build_icon(':/songs/song_search_all.png'))
#         self.view_button.setObjectName('view_button')
#         self.view_layout.addWidget(self.view_button)
#         self.search_layout.addLayout(self.view_layout)
#         self.stacked_widget.addWidget(self.search_page)
#         self.song_page = QtWidgets.QWidget()
#         self.song_page.setObjectName('song_page')
#         self.song_layout = QtWidgets.QGridLayout(self.song_page)
#         self.song_layout.setContentsMargins(8, 8, 8, 8)
#         self.song_layout.setSpacing(8)
#         self.song_layout.setObjectName('song_layout')
#         self.title_label = QtWidgets.QLabel(self.song_page)
#         self.title_label.setObjectName('title_label')
#         self.song_layout.addWidget(self.title_label, 0, 0, 1, 1)
#         self.title_edit = QtWidgets.QLineEdit(self.song_page)
#         self.title_edit.setReadOnly(True)
#         self.title_edit.setObjectName('title_edit')
#         self.song_layout.addWidget(self.title_edit, 0, 1, 1, 1)
#         self.authors_label = QtWidgets.QLabel(self.song_page)
#         self.authors_label.setObjectName('authors_label')
#         self.song_layout.addWidget(self.authors_label, 0, 2, 1, 1)
#         self.author_list_widget = QtWidgets.QListWidget(self.song_page)
#         self.author_list_widget.setObjectName('author_list_widget')
#         self.song_layout.addWidget(self.author_list_widget, 0, 3, 3, 1)
#         self.copyright_label = QtWidgets.QLabel(self.song_page)
#         self.copyright_label.setObjectName('copyright_label')
#         self.song_layout.addWidget(self.copyright_label, 1, 0, 1, 1)
#         self.copyright_edit = QtWidgets.QLineEdit(self.song_page)
#         self.copyright_edit.setReadOnly(True)
#         self.copyright_edit.setObjectName('copyright_edit')
#         self.song_layout.addWidget(self.copyright_edit, 1, 1, 1, 1)
#         self.ccli_label = QtWidgets.QLabel(self.song_page)
#         self.ccli_label.setObjectName('ccli_label')
#         self.song_layout.addWidget(self.ccli_label, 2, 0, 1, 1)
#         self.ccli_edit = QtWidgets.QLineEdit(self.song_page)
#         self.ccli_edit.setReadOnly(True)
#         self.ccli_edit.setObjectName('ccli_edit')
#         self.song_layout.addWidget(self.ccli_edit, 2, 1, 1, 1)
#         self.lyrics_label = QtWidgets.QLabel(self.song_page)
#         self.lyrics_label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
#         self.lyrics_label.setObjectName('lyrics_label')
#         self.song_layout.addWidget(self.lyrics_label, 3, 0, 1, 1)
#         self.lyrics_table_widget = SingleColumnTableWidget(self.song_page)
#         self.lyrics_table_widget.setObjectName('lyrics_table_widget')
#         self.lyrics_table_widget.setRowCount(0)
#         self.song_layout.addWidget(self.lyrics_table_widget, 3, 1, 1, 3)
#         self.song_progress_bar = QtWidgets.QProgressBar(self.song_page)
#         self.song_progress_bar.setMinimum(0)
#         self.song_progress_bar.setMaximum(3)
#         self.song_progress_bar.setValue(0)
#         self.song_progress_bar.setVisible(False)
#         self.song_layout.addWidget(self.song_progress_bar, 4, 0, 1, 4)
#         self.import_layout = QtWidgets.QHBoxLayout()
#         self.import_layout.setObjectName('import_layout')
#         self.back_button = QtWidgets.QPushButton(self.song_page)
#         self.back_button.setIcon(build_icon(':/general/general_back.png'))
#         self.back_button.setObjectName('back_button')
#         self.import_layout.addWidget(self.back_button)
#         self.import_spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
#                                                    QtWidgets.QSizePolicy.Minimum)
#         self.import_layout.addItem(self.import_spacer)
#         self.import_button = QtWidgets.QPushButton(self.song_page)
#         self.import_button.setIcon(build_icon(':/general/general_import.png'))
#         self.import_button.setObjectName('import_button')
#         self.import_layout.addWidget(self.import_button)
#         self.song_layout.addLayout(self.import_layout, 5, 0, 1, 5)
#         self.stacked_widget.addWidget(self.song_page)
#   

#         self.password_label.setBuddy(self.password_edit)
#         self.title_label.setBuddy(self.title_edit)
#         self.authors_label.setBuddy(self.author_list_widget)
#         self.copyright_label.setBuddy(self.copyright_edit)
#         self.ccli_label.setBuddy(self.ccli_edit)
#         self.lyrics_label.setBuddy(self.lyrics_table_widget)

        
        self.retranslate_ui(planningcenter_dialog)
        self.stacked_widget.setCurrentIndex(0)

    def retranslate_ui(self, planningcenter_dialog):
        """
        Translate the GUI.
        """
        planningcenter_dialog.setWindowTitle(translate('PlanningCenterPlugin.PlanningCenterForm', 'Planning Center Service Importer'))
        self.notice_label.setText(
            translate('PlanningCenterPlugin.PlanningCenterForm', '<strong>Note:</strong> '
                      'An Internet connection is required in order to import plans from Planning Center Online.')
        )
        self.service_type_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Service Type:'))
        self.plan_selection_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Select Plan:'))
        self.import_as_new_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Import As New'))
        
#         self.password_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Password:'))
#         self.save_password_checkbox.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Save username and password'))
#         self.login_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Login'))
#         self.search_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Search Text:'))
#         self.search_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Search'))
#         self.stop_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Stop'))
#         self.result_count_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Found %s song(s)') % 0)
#         self.logout_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Logout'))
#         self.view_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'View'))
#         self.title_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Title:'))
#         self.authors_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Author(s):'))
#         self.copyright_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Copyright:'))
#         self.ccli_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'CCLI Number:'))
#         self.lyrics_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Lyrics:'))
#         self.back_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Back'))
#         self.import_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Import'))
