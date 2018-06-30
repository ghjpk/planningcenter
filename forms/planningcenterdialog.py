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
        self.append_to_existing_button = QtWidgets.QPushButton(self.plan_selection_page)
        self.append_to_existing_button.setObjectName('append_to_existing_button')
        self.import_button_layout.addWidget(self.append_to_existing_button)
        self.plan_selection_layout.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.import_button_layout)    
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
        self.append_to_existing_button.setText(translate('PlanningCenterPlugin.PlanningCenterForm', 'Append'))
        self.append_to_existing_button.setToolTip(translate('PlanningCenterPlugin.PlanningCenterForm', 'Append To Existing Service'))