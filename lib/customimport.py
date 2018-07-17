from openlp.plugins.custom.lib.db import CustomSlide
from openlp.plugins.custom.lib import CustomXMLBuilder
from openlp.core.common import Registry

def PlanningCenterCustomImport(item_title,theme_name):
    custom_slide = CustomSlide()
    custom_slide.title = item_title
    sxml = CustomXMLBuilder()
    sxml.add_verse_to_lyrics('custom', str(1), item_title)
    custom_slide.text = str(sxml.extract_xml(), 'utf-8')
    custom_slide.credits = 'pco'
    custom_slide.theme_name = theme_name
    custom = Registry().get('custom')
    custom_db_manager = custom.plugin.db_manager
    custom_db_manager.save_object(custom_slide)
    return custom_slide.id