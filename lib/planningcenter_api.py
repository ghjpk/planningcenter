import urllib.request
import re
from json import loads, load, dump
import os, ssl
from google.protobuf.internal.test_bad_identifiers_pb2 import service

class PlanningCenterAPI:
    def __init__(self, application_id, secret):
        self.api_url = "https://api.planningcenteronline.com/services/v2/"
        self.application_id = application_id
        self.secret = secret
        
    def GetFromServicesAPI(self,url_suffix):
        """ airplane mode will cache responses from PCO such that if you request the same 
            resource a second time, it will respond with the cached response.  This is useful
            for doing development work on an airplane, like, say, from SFO to TPE on July 8th.
            The production default should be False """
        airplane_mode = False
        module_directory = os.path.dirname(__file__)
        airplane_mode_suffix = re.sub('\W','_',url_suffix)
        airplane_mode_filename = "{0}/airplane_mode/{1}.json".format(
            module_directory,airplane_mode_suffix)
        if airplane_mode:
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
        if airplane_mode:
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