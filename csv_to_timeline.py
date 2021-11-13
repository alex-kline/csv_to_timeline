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


#from xml.etree.ElementTree import iterparse
import xml.etree.ElementTree as ET
from xml.dom import minidom
import csv


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

def canonical_date(date):
    if len(date) != 19:
        date = date + ' 00:00:00'
    return date
    pass


def get_events_from_ET (ET_root):
    event_list = []
    for event in ET_root.iter('event'):
        ev_text     = event.find('text').text.strip()
        ev_start    = event.find('start').text.strip()
        ev_end      = event.find('end').text.strip()
        ev_category = event.find('category').text.strip()
        item = [ev_text, ev_start, ev_end, ev_category]
        event_list.append(item)
        # print [ev_start, ev_end, ev_text, ev_category]
    # print (event_list)
    return event_list


def find_unknown_events_in_csv_file (fn_in_csv, event_list):
    f = open(fn_in_csv, 'rt')
    new_event_list = []
    try:
        reader = csv.reader(f, event_list)
        for row in reader:
            print (row)
            row[1] = canonical_date(row[1].strip())
            row[2] = canonical_date(row[2].strip())
            item = [row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()]
            # wenn item nicht schon in der (xml-) event_list -> an event_list anfügen.
            if item in event_list:
                pass
            else:
                new_event_list.append(item)
    finally:
        f.close()
    # print new_event_list
    return new_event_list

def tl_event_add(section_events, event):
    # according to >timeline.xsd<
    # <xs:complexType name="event">
    # <xs:sequence>
    # <xs:element name="start" type="xs:string"/>
    # <xs:element name="end" type="xs:string"/>
    # <xs:element name="text" type="xs:string"/>
    # <xs:element name="progress" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="fuzzy" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="locked" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="ends_today" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="category" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="description" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="hyperlink" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="alert" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="icon" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="default_color" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # <xs:element name="milestone" type="xs:string" minOccurs="0" maxOccurs="1"/>
    # </xs:sequence>
    # </xs:complexType>
    

# https://pymotw.com/3/csv/index.html#using-field-names  == csv -> dictionary (statt list)

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    d_event = {}
    d_event["start"]         = ""
    d_event["end"]           = ""
    d_event["text"]          = ""
    d_event["progress"]      = ""
    d_event["fuzzy"]         = ""
    d_event["locked"]        = ""
    d_event["ends_today"]    = ""
    d_event["category"]      = ""
    d_event["description"]   = ""
    d_event["hyperlink"]     = ""
    d_event["alert"]         = ""
    d_event["icon"]          = ""
    d_event["default_color"] = ""
    d_event["milestone"]     = ""

    new_event               = ET.SubElement(section_events, 'event')


    # ET.SubElement(new_event, 'start').text = event[1]
    # ET.SubElement(new_event, 'end').text   = event[2]
    # ET.SubElement(new_event, 'text').text  = event[0]
    # if event[3]:
    #     ET.SubElement(new_event, 'category').text  = event[3]

    d_event["start"]         = event[1]
    d_event["end"]           = event[2]
    d_event["text"]          = event[0]
    d_event["category"]      = event[3]


    ET.SubElement(new_event, 'start').text = d_event["start"]
    ET.SubElement(new_event, 'end').text   = d_event["end"]
    ET.SubElement(new_event, 'text').text  = d_event["text"]
    if d_event["category"]:
        ET.SubElement(new_event, 'category').text  = d_event["category"]



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


# def rh_timeline_parse (basename = '2013_12_28_Aufklaerung_00' , extension = 'timeline'):
def rh_timeline_parse (basename, extension):
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
    lo_events_new        = []  # Liste der nicht in *.timeline vorhandenen events - aber in der *.csv.

    fn_xml_in  = basename + '.'     + extension
    fn_xml_out = basename + '_out.' + extension
    fn_csv_in  = basename + '_in' + '.' + 'csv'
    fn_csv_out = basename + '_out' + '.' + 'csv'

    timeline_ET_tree = ET.parse(fn_xml_in)
    timeline_ET_root = timeline_ET_tree.getroot()

    # Alle in der File >*.timeline< vorhandenen Events in die Liste >lo_events< aufnehmen
    lo_events = get_events_from_ET (timeline_ET_root)   # aus *.timeline

    # Alle in der File >*.csv< vorhandenen Events lesen jene herausfiltern, die nicht
    # in der >lo_events< vorhanden sind. In der >lo_events_new< sind also keine Doubletten.
    lo_events_new = find_unknown_events_in_csv_file (fn_csv_in, lo_events)
    # Zur Kontrolle die neue, erweiterte event_List als csv-File abspeichern:
    write_all_events_to_csv_file (fn_csv_out, lo_events, lo_events_new)

    # Die >timeline_ET_root< um die neuen events erweitern:
    # find first section '<events>'
    section_events = timeline_ET_root.find('.//events[1]')

    # alle items, die noch nicht in der >*.timeline< waren.
    for event in lo_events_new:
        tl_event_add(section_events, event)

    # format XML tree: https://stackoverflow.com/questions/749796/pretty-printing-xml-in-python
    ET.indent(timeline_ET_root)
    ET.dump(timeline_ET_root)    # print it to console
    # *.timeline-File schreiben:
    timeline_ET_tree.write(fn_xml_out, encoding="utf-8", xml_declaration=True)
    
if __name__ == "__main__":
    print ("BEGIN: timeline_csv_2_xml.py")
    #parse_timeline()
    
    #pymotw_parse_XML(basename = '2013_12_28_Aufklaerung_00' , extension = 'timeline')
    # pymotw_parse_XML(basename = 'tl_tst', extension = 'xml')

    # 2013-12-28_Aufklaerung_00.timeline
    rh_timeline_parse (basename='2013-12-28_Aufklaerung_00', extension='timeline')
    
    print ("\nEND: timeline_csv_2_xml.py")
