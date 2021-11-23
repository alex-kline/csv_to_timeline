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


import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv
import datetime

# from >timeline.xsd<
event_fieldnames = ("start", "end", "text", "progress", "fuzzy", "locked", "ends_today",
                    "category", "description", "hyperlink", "alert", "icon", "default_color", "milestone")


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
    # https://stackoverflow.com/questions/17709751/how-make-a-datetime-object-in-year-0-with-python
    # '-624'   =>  '-624-01-01 00:00:00'
    if (year == 'alive'):
        date = str(datetime.date.today())
        date = str(date) + ' 00:00:00'
        return date
    
    year_zero = False
    bc = False

    if (year[0] == '-'):
        bc = True
        year = year[1:]
        # print ("=0>  year: ", year, end = '     ' )
        
    if len(year) < 10:
        year = int(year)
        if (year == 0):
            year_zero = True
            year = 1
        date = datetime.date(year, 1, 1)
        # print ("=1>  date: ", str(date), end = '     ' )
        date = str(date) + ' 00:00:00'
        if year_zero:
            new_date = '1' + date[1:]
            date     = new_date
        if bc:
            date = '-' + date
        # print ("=2>  date: ", date, '\n' )
        return date
    else:
        if bc:
            # print()
            pass
        return year

def new_d_event():
    # return dictionary with keys according to event_fieldnames in >timeline.xsd<
    # all values are preset = ''
    d_event_philosopher = {}
    for cnt, event_fieldname in enumerate (event_fieldnames):
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
        ev_category = xml_event.find('category').text.strip()
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

    lo_new_events = []
    f = open(fn_in_csv, 'r', encoding='utf8')
    try:
        reader = csv.DictReader(f)
        # DictRow:
        for row in reader:
            # print ('DictRow: ', row)
            d_event = new_d_event()
            for key in event_fieldnames:
                try:
                    if row[key]:
                        d_event[key]   = row[key]
                except:
                    pass
                if (key == 'start'):
                    # print ("!!!  start: ", row['start'] )
                    d_event['start'] = canonical_date(row['start'])
                elif (key == 'end'):
                    d_event['end']   = canonical_date(row['end'])
            lo_new_events.append(d_event)
    finally:
        f.close()
    return lo_new_events

def make_color_palette():
    # https://stackoverflow.com/questions/876853/generating-color-ranges-in-python
    # https://seaborn.pydata.org/tutorial/color_palettes.html
    # https://www.kaggle.com/asimislam/python-colors-color-cmap-palette
    # https://coolors.co/
    # https://pymolwiki.org/index.php/Colorblindfriendly
    # https://github.com/drammock/colorblind
    # https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40
    # https://davidmathlogic.com/colorblind/#%23000000-%23E69F00-%2356B4E9-%23009E73-%23F0E442-%230072B2-%23D55E00-%23CC79A7
    
    # https://stackoverflow.com/questions/36657151/cycle-through-list-items
    # https://www.nature.com/articles/nmeth.1618
    
    pass

# tl == timeline
def tl_categories_add(section_categories, lo_new_events):
    # https://stackoverflow.com/questions/36447109/how-to-add-xml-nodes-in-python-using-elementtree
    # Erst werden die unterschiedlichen Kategorien herausgefiltert, dann
    # werden sie an die section >category< angehängt.

    lo_categories = []
    for d_event in lo_new_events:
        if d_event['category'] not in lo_categories:
            lo_categories.append(d_event['category'])

    category_keys = ['name', 'color', 'progress_color', 'done_color', 'font_color']
    for cnt, category in enumerate(lo_categories):
        new_ET_category = ET.SubElement(section_categories, 'category')
        for cnt, key in enumerate(category_keys):
            tag = ET.Element(key)     # i.e. "<name><\name>"
            if (key == 'name'):
                tag.text = category   # ->   "<name>Sokrates<\name>"
            elif (key == 'color'):
                tag.text = '0,128,128'   # ->   "<name>Sokrates<\name>"
            elif (key == 'progress_color'):
                tag.text = '153,254,255'   # ->   "<name>Sokrates<\name>"
            elif (key == 'progress_color'):
                tag.text = '153,254,255'   # ->   "<name>Sokrates<\name>"
            elif (key == 'done_color'):
                tag.text = '153,254,255'   # ->   "<name>Sokrates<\name>"
            elif (key == 'font_color'):
                tag.text = '255,255,255'   # ->   "<name>Sokrates<\name>"
            else:
                tag.text = ''
            new_ET_category.append(tag)  # ->   "<event><name>Sokrates<\name><\event>"

        ET.Element(section_categories).append(new_ET_category)

def tl_event_add(section_events, d_event):
    # https://stackoverflow.com/questions/36447109/how-to-add-xml-nodes-in-python-using-elementtree
    # Die Inhalte des dict >d_event< werden an die section >events< angehängt.

    new_ET_event = ET.SubElement(section_events, 'event')
    for cnt, key in enumerate(d_event.keys()):
        try:
            if d_event[key]:
                tag = ET.Element(key)     # i.e. "<name><\name>"
                tag.text = d_event[key]   # ->   "<name>Sokrates<\name>"
                new_ET_event.append(tag)  # ->   "<event><name>Sokrates<\name><\event>"
        except:
            print ('Error', key, d_event[key])
            pass
    
    # print(ET.tostring(new_ET_event))
    # ET.SubElement(section_events, 'event').append(new_ET_event)
    ET.Element(section_events).append(new_ET_event)

def write_all_events_to_csv_file (fn_out_csv, event_list, new_event_list):
    f = open(fn_out_csv , 'w')
    try:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        if event_list:
            for item in event_list:
                print ("> ", item)
                writer.writerow(item)
        if new_event_list:
            for item in new_event_list:
                writer.writerow(item)
    finally:
        f.close()

def tl_file_generate (fn_xml_in, fn_xml_out, fn_csv_in, fn_csv_out):
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

    lo_events            = []  # Liste der       in *.timeline vorhandenen events.
    lo_new_events        = []  # Liste der nicht in *.timeline vorhandenen events - aber in der *.csv.

    timeline_ET_tree = ET.parse(fn_xml_in)
    timeline_ET_root = timeline_ET_tree.getroot()

    # Alle in der File >*.timeline< vorhandenen Events in die Liste >lo_events< aufnehmen
    lo_events = get_events_from_ET (timeline_ET_root)   # aus *.timeline

    # Alle in der File >*.csv< vorhandenen Events lesen jene herausfiltern, die nicht
    # in der >lo_events< vorhanden sind. In der >lo_new_events< sind also keine Doubletten.
    # lo_new_events = get_events_from_csv_file (fn_csv_in, lo_events)
    lo_new_events = get_events_from_csv_file (fn_csv_in)
    # Zur Kontrolle die neue, erweiterte event_List als csv-File abspeichern:
    write_all_events_to_csv_file (fn_csv_out, lo_events, lo_new_events)

    # Die >timeline_ET_root< um die neuen events erweitern:
    # find (first) section '<events>'
    section_events = timeline_ET_root.find('.//events[1]')
    # print ('section_events.text: >' + section_events.text + '<')

    # Es werden alle Kategorien eruiert und in die section >category< eingefügt
    section_category = timeline_ET_root.find('.//categories[1]')
    tl_categories_add(section_category, lo_new_events)

    # alle items, die noch nicht in der >*.timeline< waren.
    for d_event in lo_new_events:
        tl_event_add(section_events, d_event)

    # format XML tree: https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    ET.indent(timeline_ET_root)    # format
    ET.dump(timeline_ET_root)      # print it to console
    # *.timeline-File schreiben:
    timeline_ET_tree.write(fn_xml_out, encoding="utf-8", xml_declaration=True)
    

if __name__ == "__main__":
    print ("BEGIN: timeline_csv_2_xml.py")
    
    xml_basename  = '2013-12-28_Aufklaerung_00'
    xml_extension = 'timeline'

    csv_basename  = '2013-12-28_Aufklaerung_00'
    csv_basename  = 'WP-de_Zeittafel_zur_Philosophiegeschichte'
    
    csv_extension = 'csv'

    fn_xml_in  = xml_basename + '.'     + xml_extension
    fn_xml_out = xml_basename + '_out.' + xml_extension

    fn_csv_in  = csv_basename + '.'     + csv_extension
    fn_csv_out = csv_basename + '_out.' + csv_extension

    tl_file_generate (fn_xml_in, fn_xml_out, fn_csv_in, fn_csv_out)

    print ("\nEND: timeline_csv_2_xml.py")
