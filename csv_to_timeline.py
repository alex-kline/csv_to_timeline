#! /usr/bin/python
# -*- coding: latin-1 -*-
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="rh"
__date__ ="$29.12.2013 14:03:33$"

"""
Sinn und Zweck:
Zusammenführen einer +/- vorhandenen *.timeline xml-File mit
den Daten einer *.csv FIle, in der weitere ''events'' im csv-Format stehen.
"""


# from itertools import cycle
from xml.dom import minidom
# import Levenshtein
import codecs
import csv
import datetime
import difflib
# import distance
import itertools
import re
import yaml
import xml.etree.ElementTree as ET
from natsort import natsorted

# from >timeline.xsd<
event_keys = ["start", "end", "text", "progress", "fuzzy", "locked", "ends_today",
                    "category", "description", "hyperlink", "alert", "icon", "default_color", "milestone"]

event_tags = ["start", "end", "text", "progress", "fuzzy", "locked", "ends_today",
                    "category", "description", "hyperlink", "alert", "icon", "default_color", "milestone"]


# Configuration files
# https://martin-thoma.com/configuration-files-in-python/      (u.a. YAML)
# https://www.w3schools.io/file/yaml-python-read-write/
# https://stackoverflow.com/questions/1726802/what-is-the-difference-between-yaml-and-json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def print_yellow (strg, str_end ='\n'):
    print (f"{bcolors.WARNING} " + strg + f"{bcolors.ENDC}", end = str_end)

def prettify(elem):
    """Return a pretty-printed XML string for the Element."""
    raw_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(raw_string)
    return reparsed.toprettyxml(indent="  ")    

def print_dict(dict):
    if dict.items():
        for key, value in dict.items():
            print (key.strip(), end = '')
            for val in value:
                print (val, end = '')
            print

def canonical_date(year):
    # returns canonical date str >YYYY-MM-DD hh:mm:sec<
    # '-624'   =>  '-624-01-01 00:00:00'
    #
    # Python has difficulties with year 0:
    #   https://stackoverflow.com/questions/17709751/how-make-a-datetime-object-in-year-0-with-python
    
    # date == today
    if (year == 'alive'):
        date = str(datetime.date.today())
        date = str(date) + ' 00:00:00'
        return date
    
    year_zero = False
    bc = False

    # Vor Christus?
    if (year[0] == '-'):
        bc = True
        year = year[1:]
        # print ("=0>  year: ", year, end = '     ' )
        
    # Richtiges FOrmat:
    if len(year) < 10:
        year = int(year)
        if (year == 0):
            year_zero = True
            year = 1
        date = datetime.date(year, 1, 1)
        date = str(date) + ' 00:00:00'
        
        # Korrektur Jahr 0
        if year_zero:
            # new_date = '1' + date[1:]
            # date     = new_date
            date     = date
            # print ("=1>  date: ", str(date))
            
        # Korrektur v. Chr.
        if bc:
            date = '-' + date
        return date
    else:
        if bc:
            pass
        return year

def diff_ratio(str_1, str_2):
    # https://stackoverflow.com/questions/6690739/high-performance-fuzzy-string-comparison-in-python-use-levenshtein-or-difflib
    # https://stackoverflow.com/questions/17388213/find-the-similarity-metric-between-two-strings
    diff = difflib.SequenceMatcher(None, str_1, str_2).ratio()
    return diff

def new_d_event():
    # return dictionary with keys according to event_fieldnames in >timeline.xsd<
    # all values are preset = ''
    d_event_philosopher = {}
    for cnt, event_fieldname in enumerate (event_keys):
        d_event_philosopher[event_fieldname] = ''
    return d_event_philosopher

# ET = ElementTree
def get_events_from_ET (ET_root):
    lo_events = []
    for xml_event in ET_root.iter('d_event'):
        # print ('type(xml_event) = ', type(xml_event))
        ev_text     = xml_event.find('text').text.strip()
        ev_start    = xml_event.find('start').text.strip()
        ev_end      = xml_event.find('end').text.strip()
        ev_category = xml_event.find('element_value').text.strip()
        # ev_unknown  = xml_event.find('unknown').text.strip()
        event = [ev_text, ev_start, ev_end, ev_category]
        lo_events.append(event)
        # print [ev_start, ev_end, ev_text, ev_category]
    # print (lo_events)
   
    d_event = {} #
    # print ('Jetzt als dict Anfang')
    for xml_event in ET_root.iter('d_event'):
        # print ('xml_event: ', xml_event, type (xml_event))
        for cnt, event_fieldname in enumerate (event_fieldnames):
            # print ('event_fieldname: ', cnt, event_fieldname)
            # print ('xml_event.find(event_fieldname): ', type (xml_event.find(event_fieldname)))
            if xml_event.find(event_fieldname) is not None:
                d_event[event_fieldname] = xml_event.find(event_fieldname).text.strip()
            else:
                d_event[event_fieldname] = ''
        # lo_events.append(d_event)
        # print [ev_start, ev_end, ev_text, ev_category]
    # print ('Jetzt als dict Ende')

    return lo_events

def get_events_from_csv_file (fn_in_csv):
    # Make list of dictionaries with new events from csv-file
    # nb: find dictionary in list of dictionaries:
    # found_value = next(dictionary for dictionary in list_of_dictionaries if dictionary["odd"] == sought_value)
    # https://stackoverflow.com/questions/9323749/how-to-check-if-one-dictionary-is-a-subset-of-another-larger-dictionary

    lo_new_event = []
    f = open(fn_in_csv, 'r', encoding='utf8')
    try:
        reader = csv.DictReader(f)
        # DictRow:
        for row in reader:
            # print ('DictRow: ', row)
            d_event = new_d_event()
            for key in event_keys:
                try:
                    if row[key]:
                        d_event[key] = row[key]
                except:
                    pass
                if (key == 'start'):
                    d_event['start'] = canonical_date(row['start'])
                elif (key == 'end'):
                    d_event['end']   = canonical_date(row['end'])
            lo_new_event.append(d_event)
    finally:
        f.close()

    return lo_new_event

def get_color_palette():
    # https://stackoverflow.com/questions/876853/generating-color-ranges-in-python
    # https://seaborn.pydata.org/tutorial/color_palettes.html
    # https://www.kaggle.com/asimislam/python-colors-color-cmap-palette
    # https://coolors.co/
    # https://pymolwiki.org/index.php/Colorblindfriendly
    # https://github.com/drammock/colorblind
    # https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40
    # https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
    
    # https://www.nature.com/articles/nmeth.1618
    
    class Colors:
        # https://www.nature.com/articles/nmeth.1618/figures/2
        # orange      = (230,159,0)
        # sky_blue    = (86,180, 233)
        # bluish_green= (0,158,115)
        # yellow      = (240, 228,66)
        # sky_blue    = (0, 114, 178)
        # vermillion  = (213,94,0)
        
        def __init__(self):
            self.orange      = 230,159,0
            self.sky_blue    = 86,180, 233
            self.bluish_green= 0,158,115
            self.yellow      = 240, 228,66
            self.sky_blue    = 0, 114, 178
            self.vermillion  = 213,94,0
            pass

    # print (Colors().__dict__)
    # print (Colors.__dict__)
    # https://stackoverflow.com/questions/12409714/python-class-members
    # https://stackoverflow.com/questions/16228248/how-can-i-get-list-of-values-from-dict
    # lo_color = list(Colors().__dict__.values())
    palette = []
    lo_color = list(Colors().__dict__.values())
    # print ('type(lo_color) = ', type(lo_color))
    for color in lo_color:
        color = str(color)
        palette.append(color[1:-1].replace(' ', ''))
        # print ('type(color) = ', type(color),'>' + color[1:-1] + '<')

    # exit (0)
    return palette

# tl == timeline
def tl_append_tag_to_element(ET_Element, element_name, element_value):
    # creates new tag to ET.Element with name: >element_name<
    # sets value of new tag to                 >element_value<
    # appends new tag to element               >ET.Element<
    # if not ET_Element.tag:
    tag        = ET.Element(element_name)
    tag.text   = element_value               # i.e. "<element_name><\element_name>"
    ET_Element.append(tag)  # ->   "<event><element_name>Sokrates<\element_name><\event>"
    # ET.dump (ET_Element)
    return ET_Element

# tl == timeline
def tl_append_multiple_tags_to_element(new_ET_category, do_name_value, do_category):
    category = do_name_value['name']
    color    = do_name_value['color']
    new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='name'           , element_value= category)
    new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='color'          , element_value= color)
    new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='progress_color' , element_value='153,254,255')
    new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='done_color'     , element_value='153,254,255')
    new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='font_color'     , element_value='255,255,255')
    if category in do_category:
        new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='parent'     , element_value=do_category[category])
    return new_ET_category

# tl == timeline
def tl_categories_add(section_categories, lo_new_events):
    # In der >*.timeline< müssen in der Section >categories<
    # alle Kategorien stehen, die bei den events
    # 1. in d_event['category']    ... oder
    # 2. in d_event['parent']      auftauchen
    
    # https://stackoverflow.com/questions/36447109/how-to-add-xml-nodes-in-python-using-elementtree
    # Erst werden die unterschiedlichen Kategorien herausgefiltert, dann
    # werden sie an die section >element_value< angehängt.
    
    lo_long_category  = []
    lo_split_category = []
    
    for d_event in lo_new_events:
        # Eruiere alle Original-Kategorien
        long_category = d_event['category']
        if long_category not in lo_long_category:
            lo_long_category.append(long_category)

        split_category = long_category.split('#')
        split_category = [ item.strip() for item in split_category]

        if (split_category not in lo_split_category):
            lo_split_category.append(split_category)
        if ([split_category[0]] not in lo_split_category):
            lo_split_category.append([split_category[0]])



    lo_long_category.sort()
    lo_split_category.sort()

    lo_category_lists = []
    lo_category       = []
    do_category       = {}

    #  Für jede Kategorie:
    for long_category in lo_long_category:
        # Eruiere die Kategorie und zerlege sie in Teile '#'
    
        split_category = long_category.split('#')
        split_category = [ item.strip() for item in split_category]
    
        cnt_of_categories = len(split_category)
    
        # print_yellow(str(cnt_of_categories) + '   ' + str(split_category) )
    
        # Nur ein Teil => Hauptkategorie
        if (cnt_of_categories == 1):
            main_category = long_category.strip()
            lo_category.append(main_category)
        else:
            for cnt in range(2, cnt_of_categories + 1):
                # print_yellow (str(cnt_of_categories) + ' ########## ' + str(cnt))
                pass
                # cnt_of_categories >= 2
                # d.h. es gibt eine Oberkategorie     zur Subkategorie ==
                # d.h. es gibt eine 'Parent-kategorie zur Subkategorie ==
                # Mache also in einem Dict einen entsprechenden Eintrag:
                # Unterkategorie: Oberkategorie.
                #
                #  Unterteile: hänge die beiden letzten Kategorien an  ...
                # sub_category    = split_category[cnt_of_categories - 1].strip()
                # parent_category = split_category[cnt_of_categories - 2].strip()
                sub_category    = split_category[cnt - 1].strip()
                parent_category = split_category[cnt - 2].strip()
            
                #  1. das dict: { ..., sub_category : parent_category, ...}
                #  type(do_category) == Dictionary
                if sub_category not in do_category:
                    do_category[sub_category] = parent_category
            
                #  2. an die Liste aller Kategorien.
                #    Cave: die Reihenfolge ist wichtig: erst die parent_category dann die sub_category
                #  type(lo_category) == List
                if parent_category not in lo_category:
                    lo_category.append(parent_category)
                if sub_category not in lo_category:
                    lo_category.append(sub_category)



    with open("lo_category.txt", mode="w", encoding='utf8') as file:
        for cnt, value in enumerate(lo_category):
            file.write(value + '\n')

    # <parent>Einführung</parent>
    # for idx in range (len(lo_category[1:-1])):
    #     category_1 = lo_category[idx]
    #     category_2 = lo_category[idx + 1]
    #     # "{:.2f}".format(z)
    #     ratio     = diff_ratio(category_1[:25], category_2[:25])
    #     ratio_str = "{:.5f}".format(ratio, 5)
    #     if (ratio < 0.54):
    #         category_color = str(next(lo_color))
    #     else:
    #         pass
        
    # category_keys = ['name', 'color', 'progress_color', 'done_color', 'font_color']

    lo_main_category = [item for item in lo_split_category if (len(item) == 1)]

    # print('\ndo_category:')
    # print_yellow(str(do_category))
    print('\nlo_split_category:')
    print_yellow(str(lo_split_category))
    # print('\nlo_category:')
    # print_yellow(str(lo_category))
    print('\nlo_main_category:')
    print_yellow(str(lo_main_category))


    lo_color = itertools.cycle(get_color_palette())
    for idx, category in enumerate(lo_category):
        new_ET_category = ET.SubElement(section_categories, 'category')

        if [category] in lo_main_category:
            lo_color = itertools.cycle(get_color_palette())
            color    = '66,66,66'
        else:
            color = str(next(lo_color))  # i.e. "<element_name><\element_name>"

        do_name_value = {}
        do_name_value['name']  = category
        do_name_value['color'] = color
        new_ET_category = tl_append_multiple_tags_to_element(new_ET_category, do_name_value, do_category)

        # new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='name'           , element_value= category)
        # new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='color'          , element_value= color)
        # new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='progress_color' , element_value='153,254,255')
        # new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='done_color'     , element_value='153,254,255')
        # new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='font_color'     , element_value='255,255,255')
        # if category in do_category:
        #     new_ET_category = tl_append_tag_to_element(new_ET_category, element_name='parent'     , element_value=do_category[category])

        ET.Element(section_categories).append(new_ET_category)



def tl_events_add(section_events, lo_new_event):
    # https://stackoverflow.com/questions/36447109/how-to-add-xml-nodes-in-python-using-elementtree
    # Die Inhalte des dict >d_event< werden an die section >events< angehängt.

    # https://stackoverflow.com/questions/46798641/how-to-only-allow-digits-letters-and-certain-characters-in-a-string-in-python
    # elif not re.match('^[a-zA-Z0-9()$%_/.]*$',password):
    # '^[a-zA-Z0-9()$%_/.,]*$'
    
    allowed_chars = []
    
    for d_event in lo_new_event:
        for key in d_event.keys():
            # print(type(d_event[key]), end = '  ')
            # print(d_event[key], end = '  ')
            # if (key != 'category') and (re.match('^[()]*$', d_event[key])):

            # l_str = d_event[key]
            # for chr in l_str:
            #     if not chr in allowed_chars:
            #         # print_yellow (chr, '')
            #         allowed_chars.append(chr)
            if (key != 'category') and ('(' in d_event[key]) or (')' in d_event[key]):
                print        ('key= >' + key + '<  d_event[key]: >', end = '')
                print_yellow (str(d_event[key]), '')
                print        ('<')
                break                #    <---| https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
        else:                        #    <---| https://stackoverflow.com/questions/653509/breaking-out-of-nested-loops
            new_ET_event = ET.SubElement(section_events, 'event')
        
            # event_keys = ["start", "end", "text", "progress", "fuzzy", "locked", "ends_today","category",
            #               "description", "hyperlink", "alert", "icon", "default_color", "milestone"]
        
            ET.Element(section_events).append(new_ET_event)
        
            new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='start'        , element_value=d_event['start'])
            new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='end'          , element_value=d_event['end'])
            new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='text'         , element_value=d_event['text'])
        
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='progress'     , element_value='0')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='fuzzy'        , element_value='False')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='locked'       , element_value='False')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='ends_today'   , element_value='False')
            
            lo_split_category = d_event['category'].split('#')
            cnt_of_categories = len(lo_split_category)
            d_event_category = lo_split_category[cnt_of_categories-1].strip()
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='category'     , element_value=d_event['category'])
            new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='category'     , element_value=d_event_category)
        
            # # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='category', element_value='')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='description'  , element_value='')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='hyperlink'    , element_value='')
            # # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='alert', element_value='')
            # # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='icon', element_value='')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='default_color', element_value='200,200,200')
            # new_ET_event = tl_append_tag_to_element(new_ET_event, element_name='milestone'    , element_value='')
    
    # print_yellow ('\n allowed_chars: ' + str(sorted(allowed_chars)))


def write_all_events_to_csv_file (fn_out_csv, lo_event, lo_new_event):
    # fn_csv_out, lo_event, lo_new_event
    f = open(fn_out_csv , 'w')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        if lo_event:
            for item in lo_event:
                print ("> ", item)
                writer.writerow(item)
        if lo_new_event:
            for item in lo_new_event:
                writer.writerow(item)
    finally:
        f.close()

def timeline_file_make (fn_xml_in, fn_xml_out, fn_csv_in, fn_csv_out):
    """
    1)a) Liest eine *.timeline-File (xml),
      b) parsed diese xml-Struktur
            -> timeline_ET_tree -> timeline_ET_root
    2)a) Liest eine *.csv-File (csv)
    
    """
    xml_dict            = dict()
    read_dict           = dict()
    inside_event_S      = False
    inside_single_event = False

    lo_event            = []  # Liste der       in *.timeline vorhandenen events.
    lo_new_event        = []  # Liste der nicht in *.timeline vorhandenen events - aber in der *.csv.

    timeline_ET_tree = ET.parse(fn_xml_in)
    timeline_ET_root = timeline_ET_tree.getroot()

    # Alle in der File >*.timeline< vorhandenen Events in die Liste >lo_event< aufnehmen
    lo_event = get_events_from_ET (timeline_ET_root)   # aus *.timeline

    # Alle in der File >*.csv< vorhandenen Events lesen:
    lo_new_event = get_events_from_csv_file (fn_csv_in)
    # Zur Kontrolle die neue event_List als csv-File abspeichern:
    # write_all_events_to_csv_file (fn_csv_out, lo_event, lo_new_event)

    # Die >timeline_ET_root< um die neuen events erweitern:
    # find (first) section '<events>'
    section_events = timeline_ET_root.find('.//events[1]')
    # print ('section_events.text: >' + section_events.text + '<')

    # Es werden alle vorhandenen Kategorien eruiert
    section_category = timeline_ET_root.find('.//categories[1]')
    # und in die section >element_value< eingefügt (????)
    tl_categories_add(section_category, lo_new_event)

    # alle items, die noch nicht in der >*.timeline< waren.
    tl_events_add(section_events, lo_new_event)

    # format XML tree: https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    ET.indent(timeline_ET_root)    # format
    # ET.dump(timeline_ET_root)      # print it to console
    # *.timeline-File schreiben:
    timeline_ET_tree.write(fn_xml_out, encoding="utf-8", xml_declaration=True)
    
if __name__ == "__main__":
    print ("BEGIN: timeline_csv_2_xml.py")
    get_color_palette()
    
    # exit (0)
    
    tl_basename   = '2013-12-28_Aufklaerung_00'
    tl_extension  = 'timeline'

    csv_basename  = '2013-12-28_Aufklaerung_00'
    csv_basename  = 'WP-de_Zeittafel_zur_Philosophiegeschichte_SMALL'
    csv_basename  = 'WP-de_Zeittafel_zur_Philosophiegeschichte'
    
    csv_extension = 'csv'

    fn_csv_in     = csv_basename + '.'     + csv_extension
    fn_csv_out    = csv_basename + '_out.' + csv_extension

    fn_tl_in     = tl_basename + '.' + tl_extension
    # fn_tl_out    = tl_basename + '_out.' + tl_extension
    fn_tl_out    = csv_basename + '_out.' + tl_extension


    timeline_file_make (fn_tl_in, fn_tl_out, fn_csv_in, fn_csv_out)

    print ("\nEND: timeline_csv_2_xml.py")
