import requests
import xml.etree.ElementTree as ET
import json
def xml_to_json(xml_string):
    root = ET.fromstring(xml_string)
    return {root.tag:xml_to_dict(root)}

def xml_to_dict(element):
    d = {}
    if element.attrib:
        d["@attributs"] = element.attrib
    if element.text:
        d[element.tag] = element.text
    for child in element:
        child_data = xml_to_dict(child)
        if child.tag in d:
            if type(d[child.tag]) is list:
                d[child.tag].append(child_data)
            else:
                d[child.tag] = [d[child.tag],child_data]
        else:
            d[child.tag] = child_data
    return d
def jyrl_base(date):
    url = "http://www.cffex.com.cn/sj/jyrl/"+date+"/index_6782.xml"
    response = requests.request("GET", url, headers={}, data={})
    base_json = xml_to_json(response.text)
    base_json = base_json['docs']['doc']
    base_dict = {}
    for i in base_json:
        key = i['pubdate']['pubdate']
        value = i['title']['title']
        if " " == value[0]:
            value = value[1:]
        if key in base_dict.keys():
            base_dict[key].append(value)
        else:
            base_dict[key] = [value]
    print(base_dict)
    # print(response.text)
def jyrl_default():
    url = "http://www.cffex.com.cn/sj/jyrl/202310/index_6782.xml"

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers={}, data={})

    print(response.text)

