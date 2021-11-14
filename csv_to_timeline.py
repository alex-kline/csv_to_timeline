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

def canonical_date(date):
    if len(date) != 19:
        date = date + ' 00:00:00'
    return date
    pass


def get_events_from_ET (ET_root):
    lo_events = []
    for xml_event in ET_root.iter('event'):
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
   
    d_event = {}
    print ('Jetzt als dict Anfang')
    for xml_event in ET_root.iter('event'):
        # print ('xml_event: ', xml_event, type (xml_event))
        for cnt, event_fieldname in enumerate (event_fieldnames):
            # print ('event_fieldname: ', cnt, event_fieldname)
            # print ('xml_event.find(event_fieldname): ', type (xml_event.find(event_fieldname)))
            if xml_event.find(event_fieldname) is not None:
                d_event[event_fieldname] = xml_event.find(event_fieldname).text.strip()
            else:
                d_event[event_fieldname] = ''
        # lo_events.append(event)
        # print [ev_start, ev_end, ev_text, ev_category]

    print ('Jetzt als dict Ende')
    return lo_events


def find_unknown_events_in_csv_file (fn_in_csv, event_list):
    # print ('\n fn_in_csv = ', fn_in_csv)
    f = open(fn_in_csv, 'rt')
    lo_new_events = []
    try:
        reader = csv.reader(f)
        next(reader, None)      # skip header
        for row in reader:
            print (row)
            row[1] = canonical_date(row[1].strip())
            row[2] = canonical_date(row[2].strip())
            event = [row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()]
            # wenn event nicht schon in der (xml-) event_list -> an event_list anfügen.
            if event in event_list:
                pass
            else:
                lo_new_events.append(event)
    finally:
        f.close()
    # print lo_new_events
    #
    
    # ---------------------------------------------
    # Similar, but make list of dictionaries
    #
    # nb: find dictionary in list of dictionaries:
    # found_value = next(dictionary for dictionary in list_of_dictionaries if dictionary["odd"] == sought_value)

    f = open(fn_in_csv, 'rt')
    do_new_events = {}
    try:
        reader = csv.DictReader(f)
        for row in reader:
            print ('DictRow: ', row)
            # row[1] = canonical_date(row[1].strip())
            # row[2] = canonical_date(row[2].strip())
            # event = [row[0].strip(), row[1].strip(), row[2].strip(), row[3].strip()]
            # # wenn event nicht schon in der (xml-) event_list -> an event_list anfügen.
            # if event in event_list:
            #     pass
            # else:
            #     lo_new_events.append(event)
    finally:
        f.close()

    return lo_new_events



def tl_event_add(section_events, event):

    #    <xs:complexType name="event">
    #        <xs:sequence>
    #            <xs:element name="start" type="xs:string"/>
    #            <xs:element name="end" type="xs:string"/>
    #            <xs:element name="text" type="xs:string"/>
    #            <xs:element name="progress" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="fuzzy" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="locked" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="ends_today" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="category" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="description" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="hyperlink" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="alert" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="icon" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="default_color" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #            <xs:element name="milestone" type="xs:string" minOccurs="0" maxOccurs="1"/>
    #        </xs:sequence>
    #    </xs:complexType>
    
    # https://pymotw.com/3/csv/index.html#using-field-names  == csv -> dictionary (statt list)
    
    
    
    # type (d_event) == dictionary
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
