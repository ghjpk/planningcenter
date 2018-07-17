import urllib.request
import re
from json import loads, load, dump
import os, ssl
from openlp.core.lib.db import Manager
from openlp.core.common import Registry
from openlp.plugins.songs.lib.importers.songimport import SongImport

class PlanningCenterAPI:
    def __init__(self, application_id, secret):
        self.api_url = "https://api.planningcenteronline.com/services/v2/"
        self.application_id = application_id
        self.secret = secret
        """ airplane mode will cache responses from PCO such that if you request the same 
            resource a second time, it will respond with the cached response.  This is useful
            for doing development work on an airplane, like, say, from SFO to TPE on July 8th.
            The production default should be False """
        self.airplane_mode = False
        module_directory = os.path.dirname(__file__)
        airplane_mode_directory = "{0}/airplane_mode".format(module_directory)
        if os.path.isdir(airplane_mode_directory):
            self.airplane_mode = True
            self.airplane_mode_directory = airplane_mode_directory
        
    def GetFromServicesAPI(self,url_suffix):
        airplane_mode_suffix = re.sub('\W','_',url_suffix)
        airplane_mode_filename = "{0}/{1}.json".format(
            self.airplane_mode_directory,airplane_mode_suffix)
        if self.airplane_mode:
            if os.path.isfile(airplane_mode_filename):
                with open(airplane_mode_filename) as json_file:  
                    api_response_object = load(json_file)
                    return api_response_object
        
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, self.api_url, self.application_id, self.secret)
        handler = urllib.request.HTTPBasicAuthHandler(password_mgr)
        # create "opener" (OpenerDirector instance)
        opener = urllib.request.build_opener(handler)
        # use the opener to fetch a URL
        opener.open(self.api_url+url_suffix)
        # Install the opener.
        # Now all calls to urllib.request.urlopen use our opener.
        urllib.request.install_opener(opener)
        api_response_string = urllib.request.urlopen(self.api_url+url_suffix, timeout=30).read()
        api_response_object = loads(api_response_string.decode('utf-8'))
        
        # write out the responses as json files for airplane mode...
        if self.airplane_mode:
            with open(airplane_mode_filename, 'w') as outfile:  
                dump(api_response_object, outfile)
            
        return api_response_object
        
    def CheckCredentials(self):
        try:
            response = self.GetFromServicesAPI('')
            organization = response['data']['attributes']['name']
            return organization
        except:
            return ''
        
    def GetServiceTypeList(self):
        # Get ServiceTypes
        service_types_url_suffix = 'service_types'
        service_types = self.GetFromServicesAPI(service_types_url_suffix)
        return service_types['data']
    
    def GetPlanList(self,service_type_id):
        if service_type_id:
            self.current_service_type_id = service_type_id
            # get the 10 next future services (including today)
            future_plans_url_suffix = "service_types/{0}/plans?filter=future&per_page=10&order=sort_date".format(service_type_id)
            future_plans = self.GetFromServicesAPI(future_plans_url_suffix)
            # get the 10 most recent past services
            past_plans_url_suffix = "service_types/{0}/plans?filter=past&per_page=10&order=-sort_date".format(service_type_id)
            past_plans = self.GetFromServicesAPI(past_plans_url_suffix)
            
            plan_list = list(reversed(future_plans['data'])) + past_plans['data']
            return plan_list
        
    def GetItemsDict(self,planID):
        itemsURLSuffix = "service_types/{0}/plans/{1}/items?include=song,arrangement".format(self.current_service_type_id,planID)
        items = self.GetFromServicesAPI(itemsURLSuffix)
        return items

def SplitLyricsIntoVerses(lyrics):  
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
                    _add_verse(output_verses, verse_type, verse_number, verse_text)
                verse_text = ''
                verse_type = lookup_openlp_verse_type(regex_match.group(1))
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
            _add_verse(output_verses, verse_type, verse_number, verse_text)
            verse_text = ''
            verse_type = ''
            verse_number = ''
    return output_verses

def lookup_openlp_verse_type(pco_verse_type):
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

def _add_verse(output_verses, verse_type, verse_number, verse_text):
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