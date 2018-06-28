import urllib.request
import re
from json import loads
from openlp.plugins.planningcenter.lib.planningcenter_auth import pco_application_id, pco_secret
import ssl

class PlanningCenterAPI:
    def __init__(self):
        self.api_url = "https://api.planningcenteronline.com/services/v2/"
        
    def GetFromServicesAPI(self,url_suffix):
        import os, ssl
        if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)): 
            ssl._create_default_https_context = ssl._create_unverified_context
        # create a password manager
        password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        # Add the username and password.
        # If we knew the realm, we could use it instead of None.
        password_mgr.add_password(None, self.api_url, pco_application_id, pco_secret)
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
        return api_response_object
        
    def GetServiceTypeList(self):
        # Get ServiceTypes
        service_types_url_suffix = 'service_types'
        service_types = self.GetFromServicesAPI(service_types_url_suffix)
        return service_types['data']
    
    def GetPlanList(self,service_type_id):
        if service_type_id:
            self.current_service_type_id = service_type_id
            plans_url_suffix = "service_types/{0}/plans?order=-sort_date".format(service_type_id)
            plans = self.GetFromServicesAPI(plans_url_suffix)
            return plans['data']
        
    def GetItemsDict(self,planID):
        itemsURLSuffix = "service_types/{0}/plans/{1}/items?include=song,arrangement".format(self.current_service_type_id,planID)
        items = self.GetFromServicesAPI(itemsURLSuffix)
        return items

def SplitLyricsIntoVerses(lyrics):
    
    # walk through the lyrics, one line at a time
    # if we have a double empty line followed by more than one line, 
    # create a new verse
    
    # the return value will be an array of hashes with 2 elements:  
    # verseTag and raw_slide (matches openLP requirements)
    
    # create a regular expression for potential VERSE,CHORUS tags included
    # inline inside the lyrics... these are on a single line and 
    verseMarkerPattern = re.compile('^(v|verse|c|chorus|bridge|prechorus|instrumental|intro|outro|vamp|breakdown|ending|interlude|tag)\s*(\d*)$',re.IGNORECASE)
        
    lyrics_lines = lyrics.split("\n")
    
    foundEmptyLine = 0
    verseNumber = 1
    verseLines = ''
    outputVerses = []
    verseTagFromLyrics = ''
    nextVerseTagFromLyrics = ''

    for line in lyrics_lines:

        # strip out curly braces and the content inside {}
        line = re.sub('{.*?}+','',line)
        # strip out any extraneous tags <...>
        line = re.sub('<.*?>','',line)
        # remove beginning/trailing whitespace and line breaks
        line = line.rstrip()
        line = line.lstrip()
                
        # if we found any of the verse/chorus markers, 
        # save the text and treat this like a blank line
        if verseMarkerPattern.search(line):
            if len(verseTagFromLyrics):
                nextVerseTagFromLyrics = line
            else:
                verseTagFromLyrics = line
            line=''
                
        if len(line) == 0:
            foundEmptyLine = 1
        
        if foundEmptyLine and len(verseLines):                
            verse = {}
            
            # add verse tags from the lyrics if they are there and
            # reset the verseTagFromLyrics variable
            if len(verseTagFromLyrics):
                verse['verseTag'] = verseTagFromLyrics
                if len(nextVerseTagFromLyrics):
                    verseTagFromLyrics = nextVerseTagFromLyrics
                    nextVerseTagFromLyrics = ''
                else:
                    verseTagFromLyrics = ''
            else:
                verse['verseTag'] = "V{0}".format(verseNumber)
                verseNumber += 1

            verse['raw_slide'] = verseLines
            outputVerses.append(verse)
            
            # reset state variables, including saving this line
            verseLines = line
            foundEmptyLine = 0
        else:       
            if len(verseLines):
                verseLines += "\n" + line
            else:
                verseLines = line
            foundEmptyLine = 0  
            
    # put the very last verseLines into the outputVerses array
    if len(verseLines):
        verse = {}
        if len(verseTagFromLyrics):
            verse['verseTag'] = verseTagFromLyrics
        else:
            verse['verseTag'] = "V{0}".format(verseNumber)
        verse['raw_slide'] = verseLines
        outputVerses.append(verse)
    
    return outputVerses