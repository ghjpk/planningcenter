import re
from openlp.core.lib.db import Manager
from openlp.core.common import Registry
from openlp.plugins.songs.lib.importers.songimport import SongImport
from openlp.plugins.songs.lib.db import Song

class PlanningCenterSongImport(SongImport):
    def __init__(self):
        temp_manager = ManagerThatSavesSongAsTemporary()
        SongImport.__init__(self, temp_manager, filename=None)
        
    def add_song(self,item_title,author,lyrics,theme_name,last_modified):
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
        # the return value will be an array of hashes with 3 elements:  
        # verse_type, verse_number, and verse_text
        
        # create a regular expression for potential VERSE,CHORUS tags included
        # inline inside the lyrics... these are on a single line and 
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
        new_verse = {}
        new_verse['verse_type'] = verse_type
        new_verse['verse_number'] = verse_number
        new_verse['verse_text'] = verse_text
        output_verses.append(new_verse)
        
class ManagerThatSavesSongAsTemporary(Manager):
    def __init__(self):
        self.songs = Registry().get('songs')
        session = self.songs.plugin.manager.session
        super(ManagerThatSavesSongAsTemporary, self).__init__('songs', None, session=session)
    def save_object(self,song):
        song.temporary = True
        self.song_id = song.id
        super(ManagerThatSavesSongAsTemporary, self).save_object(song)
