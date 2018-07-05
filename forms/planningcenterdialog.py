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

from PyQt5 import QtWidgets
from openlp.core.lib import translate

class Ui_PlanningCenterDiaglogAuth(object):
    """
    This is the dialog that collect the Planning Center application ID and secret codes
    """
    def setup_ui(self, planningcenter_dialog_auth):
        planningcenter_dialog_auth.setObjectName('planningcenter_dialog_auth')
        planningcenter_dialog_auth.resize(700, 350)
        self.planningcenter_layout = QtWidgets.QVBoxLayout(planningcenter_dialog_auth)
        self.planningcenter_layout.setSpacing(0)
        self.planningcenter_layout.setContentsMargins(0, 0, 0, 0)
        self.planningcenter_layout.setObjectName('planningcenter_layout')
        self.stacked_widget = QtWidgets.QStackedWidget(planningcenter_dialog_auth)
        self.stacked_widget.setObjectName('stacked_widget')
        self.planningcenter_layout.addWidget(self.stacked_widget)
        
        self.auth_page = QtWidgets.QWidget()
        self.auth_page.setObjectName('auth_page')
        self.stacked_widget.addWidget(self.auth_page)
        
        self.plan_selection_layout = QtWidgets.QFormLayout(self.auth_page)
        self.plan_selection_layout.setContentsMargins(20, 40, 20, 40)
        self.plan_selection_layout.setSpacing(8)
        self.plan_selection_layout.setObjectName('plan_selection_layout')
        
        self.notice_layout = QtWidgets.QVBoxLayout()
        self.notice_layout.setObjectName('notice_layout')
        self.notice_label = QtWidgets.QLabel(self.auth_page)
        self.notice_label.setWordWrap(True)
        self.notice_label.setObjectName('notice_label')
        self.notice_layout.addWidget(self.notice_label)
        
        self.instructions_label = QtWidgets.QLabel(self.auth_page)
        self.instructions_label.setWordWrap(True)
        self.instructions_label.setObjectName('instructions_label')
        self.notice_layout.addWidget(self.instructions_label)
        self.plan_selection_layout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.notice_layout)
        
        # Application ID GUI Elements
        self.application_id_label = QtWidgets.QLabel(self.auth_page)
        #self.application_id_label.setObjectName('application_id_label')
        self.plan_selection_layout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.application_id_label)
        self.application_id_text_edit = QtWidgets.QLineEdit(self.auth_page)
        #self.application_id_text_edit.setObjectName('application_id_text_edit')
        self.plan_selection_layout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.application_id_text_edit)
        self.application_id_label.setBuddy(self.application_id_text_edit)
        self.application_id_text_edit.setFocus()
        
        # Secret GUI Elements (shhhh... it's a secret...)
        self.secret_label = QtWidgets.QLabel(self.auth_page)
        self.secret_label.setObjectName('secret_label')
        self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.secret_label)
        self.secret_text_edit = QtWidgets.QLineEdit(self.auth_page)
        self.secret_text_edit.setObjectName('secret_text_edit')
        self.plan_selection_layout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.secret_text_edit)
        self.secret_label.setBuddy(self.secret_text_edit)
        
        # Buttons
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.setSpacing(8)
        self.button_layout.setContentsMargins(0, -1, -1, -1)
        self.button_layout.setObjectName('button_layout')
        self.test_credentials_button = QtWidgets.QPushButton(self.auth_page)
        self.test_credentials_button.setObjectName('test_credentials_button')
        self.button_layout.addWidget(self.test_credentials_button)
        self.ok_button = QtWidgets.QPushButton(self.auth_page)
        self.ok_button.setObjectName('ok_button')
        self.button_layout.addWidget(self.ok_button)
        self.plan_selection_layout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.button_layout)
        
        self.retranslate_ui(planningcenter_dialog_auth)
        self.stacked_widget.setCurrentIndex(0)
        
        

    def retranslate_ui(self, planningcenter_dialog):
        """
        Translate the GUI.
        """
        planningcenter_dialog.setWindowTitle(translate('PlanningCenterPlugin.PlanningCenterAuthForm', 'Planning Center Service Importer Authentication'))
        self.notice_label.setText(
            translate('PlanningCenterPlugin.PlanningCenterForm', '<strong>Note:</strong> '
                      'An Internet connection and a Planning Center Online Account are required in order to import plans from Planning Center Online.')    
        )
        self.instructions_label.setText(
            translate('PlanningCenterPlugin.PlanningCenterAuthForm',\
"""Enter your <b>Planning Center Online</b> <i>Personal Access Token</i> details in the text boxes \
below.  Personal Access Tokens are created by doing the following:
<ol>
  <li>Log into your Planning Center Online account at<br>https://api.planningcenteronline.com/oauth/applications</li>
  <li>Click the "New Personal Access Token" button at the bottom of the screen.</li>
  <li>Enter a description of your use case (eg. "OpenLP Integration")</li>
  <li>Copy and paste the provided Application ID and Secret values below.</li>
</ol>"""))
        self.application_id_label.setText(translate('PlanningCenterPlugin.PlanningCenterAuthForm', "Application ID"))
        self.secret_label.setText(translate('PlanningCenterPlugin.PlanningCenterAuthForm', "Secret"))
        self.test_credentials_button.setText(translate('PlanningCenterPlugin.PlanningCenterAuthForm','Test Credentials'))
        self.ok_button.setText(translate('PlanningCenterPlugin.PlanningCenterAuthForm','OK'))
        

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
        self.plan_selection_layout.setContentsMargins(80, 60, 80, 60)
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
        
        # Theme List for Songs and Custom Slides
        self.song_theme_selection_label = QtWidgets.QLabel(self.plan_selection_page)
        self.song_theme_selection_label.setObjectName('song_theme_selection_label')
        self.plan_selection_layout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.song_theme_selection_label)
        self.song_theme_selection_combo_box = QtWidgets.QComboBox(self.plan_selection_page)
        self.song_theme_selection_combo_box.setObjectName('song_theme_selection_combo_box')
        self.plan_selection_layout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.song_theme_selection_combo_box)
        self.song_theme_selection_label.setBuddy(self.song_theme_selection_combo_box)
        self.slide_theme_selection_label = QtWidgets.QLabel(self.plan_selection_page)
        self.slide_theme_selection_label.setObjectName('slide_theme_selection_label')
        self.plan_selection_layout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.slide_theme_selection_label)
        self.slide_theme_selection_combo_box = QtWidgets.QComboBox(self.plan_selection_page)
        self.slide_theme_selection_combo_box.setObjectName('slide_theme_selection_combo_box')
        self.plan_selection_layout.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.slide_theme_selection_combo_box)
        
        # Import Button
        self.import_button_layout = QtWidgets.QHBoxLayout()
        self.import_button_layout.setSpacing(8)
        self.import_button_layout.setContentsMargins(0, -1, -1, -1)
        self.import_button_layout.setObjectName('import_button_layout')
        self.import_as_new_button = QtWidgets.QPushButton(self.plan_selection_page)
        self.import_as_new_button.setObjectName('import_as_new_button')
        self.import_button_layout.addWidget(self.import_as_new_button)
        self.update_existing_button = QtWidgets.QPushButton(self.plan_selection_page)
        self.update_existing_button.setObjectName('update_existing_button')
        self.import_button_layout.addWidget(self.update_existing_button)
        self.plan_selection_layout.setLayout(5, QtWidgets.QFormLayout.FieldRole, self.import_button_layout)  
        
        self.edit_auth_button_layout = QtWidgets.QHBoxLayout()
        self.edit_auth_button_layout.setSpacing(8)
        self.edit_auth_button_layout.setContentsMargins(70, 30, 70, 0)
        #self.edit_auth_button_layout.setObjectName('edit_auth_button_layout')
        self.edit_auth_button = QtWidgets.QPushButton(self.plan_selection_page)
        self.edit_auth_button.setObjectName('edit_auth_button')
        self.edit_auth_button_layout.addWidget(self.edit_auth_button)
        self.plan_selection_layout.setLayout(6, QtWidgets.QFormLayout.FieldRole, self.edit_auth_button_layout)  
         
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
        self.import_as_new_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Import New'))
        self.import_as_new_button.setToolTip(translate('PlanningCenterPlugin.PlanningCenterForm', 'Import As New Service'))
        self.update_existing_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Refresh Service'))
        self.update_existing_button.setToolTip(translate('PlanningCenterPlugin.PlanningCenterForm', 'Refresh Existing Service'))
        self.edit_auth_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Edit Authentication'))
        self.edit_auth_button.setToolTip(translate('PlanningCenterPlugin.PlanningCenterForm', 'Edit the Application ID and Secret Code to login to Planning Center Online'))
        self.song_theme_selection_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Song Theme'))
        self.slide_theme_selection_label.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Slide Theme'))