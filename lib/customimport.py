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
The :mod:`~openlp.plugins.planningcenter.lib.customimport` module provides
a function that imports a single custom slide into the database and returns
the database ID of the slide.  This mimics the implementation for SongPlugin
that was used to import songs from Planning Center.
"""

from openlp.plugins.custom.lib.db import CustomSlide
from openlp.plugins.custom.lib import CustomXMLBuilder
from openlp.core.common import Registry
from openlp.core.lib import ServiceItem
import re


class PlanningCenterCustomImport(object):
    """
    Creates a custom slide and returns the database ID of that slide

    :param item_title: The text to put on the slide.
    :param html_details: The "details" element from PCO, with html formatting
    :param theme_name:  The theme_name to use for the slide.
    """
    def add_slide(self,item_title,html_details,theme_name):
        custom_slide = CustomSlide()
        custom_slide.title = item_title
        sxml = CustomXMLBuilder()
        slide_content = ''
        if html_details is None:
            slide_content = item_title
        else:
            # we need non-html here, but the input is html
            slide_content = self._process_details(html_details)
        sxml.add_verse_to_lyrics('custom', str(1), slide_content)
        custom_slide.text = str(sxml.extract_xml(), 'utf-8')
        custom_slide.credits = 'pco'
        custom_slide.theme_name = theme_name
        custom = Registry().get('custom')
        custom_db_manager = custom.plugin.db_manager
        custom_db_manager.save_object(custom_slide)
        return custom_slide.id
    """
    Converts the "details" section of a PCO slide into text suitable for 
    slides in OLP
    
    :param html_details: The html_details string from the PCO API
    """
    def _process_details(self,html_details):
        slide_content = ''
        # convert <br> into new lines
        html_details = re.sub(r'<br>','\n',html_details)
        # dump the rest of the html
        html_details = re.sub(r'(<!--.*?-->|<[^>]*>)','',html_details)
        # we now need to deal with extremely long strings and add line breaks
        # every so often... i'm thinking break up lines longer than 80 chars every 10 words
        for line in html_details.split("\n"):
            if len(line) <= 80:
                slide_content += line + "\n"
            else:
                new_line = ''
                counter = 0
                for word in line.split():
                    if counter <= 9:
                        new_line += word + " "
                        counter += 1
                    else:
                        new_line += word + "\n"
                        counter = 0
                slide_content += new_line + "\n"
        return slide_content
        