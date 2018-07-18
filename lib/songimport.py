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
The :mod:`~openlp.plugins.planningcenter.lib.songimport` module provides
2 classes that are used to import Planning Center Online Service Songs into
an OpenLP Service.
"""
import re
from openlp.core.lib.db import Manager
from openlp.core.common import Registry
from openlp.plugins.songs.lib.importers.songimport import SongImport
from openlp.plugins.songs.lib.db import Song

class PlanningCenterSongImport(SongImport):
    """
    The :class:`PlanningCenterSongImport` class subclasses SongImport 
    and provides interfaces for parsing lyrics and adding songs from a 
    Planning Center Service into an OpenLP Service.
    """
    def __init__(self):
        """
        Initialize.  Create a new manager object that always saves songs
        as temporary and pass this into the SongImport init function.
        """
        temp_manager = ManagerThatSavesSongAsTemporary()
        SongImport.__init__(self, temp_manager, filename=None)
        
    def add_song(self,item_title,author,lyrics,theme_name,last_modified):
        """
        Builds and adds song to the database and returns the Song ID
            
        :param item_title: The song title.
        :param author: Author String from Planning Center
        :param lyrics: Lyrics String from Planning Center
        :param theme_name: Theme String to use for this song
        :param last_modified: DateTime of last modified date for this song
        """
        self.set_defaults()
        self.title = item_title
        self.theme_name = theme_name
        if author:
            self.parse_author(author)
        verses = self._SplitLyricsIntoVerses(lyrics)
        for verse in verses:
            if len(verse['verse_type']):
                verse_def = verse['verse_type'] + verse['verse_number']
                self.add_verse(verse_text=verse['verse_text'], verse_def=verse_def)
            else:
                self.add_verse(verse_text=verse['verse_text'])
        self.finish()
        openlp_id = self.manager.song_id
        # set the last_updated date/time based on the PCO date/time so I can look for updates
        song = self.manager.get_object(Song, openlp_id)
        song.last_modified = last_modified
        self.manager.save_object(song)
        return openlp_id
    
    def _SplitLyricsIntoVerses(self,lyrics):  
        """
        Parses Planning Center Lyrics and returns an list of verses, where each 
        verse is a dictionary that looks like:
            verse['verse_type']
            verse['verse_number']
            verse['verse_text']
        :param lyrics: Lyrics String from Planning Center
        """
        # create a regular expression for potential VERSE,CHORUS tags included inline inside the lyrics...
        verseMarkerPattern = re.compile('^(v|verse|c|chorus|bridge|prechorus|instrumental|intro|outro|vamp|breakdown|ending|interlude|tag|misc)\s*(\d*)$',re.IGNORECASE)
        verse_type = ''
        verse_number = ''
        verse_text = ''
        output_verses = []
        input_verses = lyrics.split("\n\n")
        for verse in input_verses:
            for line in verse.split("\n"):
                # strip out curly braces and the content inside {}
                line = re.sub('{.*?}+','',line)
                # strip out any extraneous tags <...>
                line = re.sub('<.*?>','',line)
                # remove beginning/trailing whitespace and line breaks
                line = line.rstrip()
                line = line.lstrip()
                
                regex_match = verseMarkerPattern.search(line)
                if regex_match:
                    if len(verse_text):
                        self._add_verse(output_verses, verse_type, verse_number, verse_text)
                    verse_text = ''
                    verse_type = self._lookup_openlp_verse_type(regex_match.group(1))
                    if regex_match.group(2):
                        verse_number = regex_match.group(2)
                    else:
                        verse_number = ''
                    continue
                else:
                    if len(verse_text):
                        verse_text += "\n{0}".format(line)
                    else:
                        verse_text = line
            if len(verse_text):
                self._add_verse(output_verses, verse_type, verse_number, verse_text)
                verse_text = ''
                verse_type = ''
                verse_number = ''
        return output_verses
    
    def _lookup_openlp_verse_type(self,pco_verse_type):
        """
        Provides a lookup table to map from a Planning Center Verse Type
        to an OpenLP verse type.
        :param pco_verse_type: Planning Center Verse Type String
        """
        pco_verse_type_to_openlp = {}
        pco_verse_type_to_openlp['VERSE'] = 'v'
        pco_verse_type_to_openlp['V'] = 'v'
        pco_verse_type_to_openlp['C'] = 'c'
        pco_verse_type_to_openlp['CHORUS'] = 'c'
        pco_verse_type_to_openlp['PRECHORUS'] = 'p'
        pco_verse_type_to_openlp['INTRO'] = 'i'
        pco_verse_type_to_openlp['ENDING'] = 'e'
        pco_verse_type_to_openlp['BRIDGE'] = 'b'
        pco_verse_type_to_openlp['OTHER'] = 'o'
        
        openlp_verse_type = pco_verse_type_to_openlp['OTHER']
        if pco_verse_type.upper() in pco_verse_type_to_openlp:
            openlp_verse_type = pco_verse_type_to_openlp[pco_verse_type.upper()]
        
        return openlp_verse_type
    
    def _add_verse(self, output_verses, verse_type, verse_number, verse_text):
        """
        Simple utility function that takes verse attributes and adds the verse
        to the output_verses list.
        :param output_verses: The list of verses that will ultimately be returned by 
        the _SplitLyricsIntoVerses function
        :param verse_type: The OpenLP Verse Type, like v,c,e, etc...
        :param verse_number: The verse number, if known, like 1, 2, 3, etc.
        :param verse_text: The parsed verse text returned from _SplitLyricsIntoVerses
        """
        new_verse = {}
        new_verse['verse_type'] = verse_type
        new_verse['verse_number'] = verse_number
        new_verse['verse_text'] = verse_text
        output_verses.append(new_verse)
        
class ManagerThatSavesSongAsTemporary(Manager):
    """
    The :class:`ManagerThatSavesSongAsTemporary` class subclasses Manager and 
    causes any songs that are saved with it to be tagged as "temporary" so they can be deleted
    later upon exit.
    """
    def __init__(self):
        """
        Initialize.  Collect the session from the existing songs database manager
        and then connect to that same session with our new class.
        """
        self.songs = Registry().get('songs')
        session = self.songs.plugin.manager.session
        super(ManagerThatSavesSongAsTemporary, self).__init__('songs', None, session=session)
    def save_object(self,song):
        """
        Minor addition to the Manager.save_object function that saves the song.id
        of the most recent song that was saved through it.  The song.id is used
        by the PlanningCenterSongImport class to add the saved song to a service.
            
        :param song: The song object to save to the database.
        """
        song.temporary = True
        self.song_id = song.id
        super(ManagerThatSavesSongAsTemporary, self).save_object(song)
