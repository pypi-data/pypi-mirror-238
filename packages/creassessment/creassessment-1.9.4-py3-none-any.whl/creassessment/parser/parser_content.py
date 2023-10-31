import json
from typing import Tuple
import xml.etree.ElementTree as ET


class Parser_Content:
    
    creator: str
    app_name: str

    # Button "Select" or "Exit" are separated
    text_content_by_comp_name: dict 

    # Button "Select" or "Exit" are NOT separated, but separated from Label, Checkbox
    text_content_by_comp_type: dict 

    def __init__(self):
        self.text_content_by_comp_name = {}
        self.text_content_by_comp_type = {}

    def parse_textual_content(self, file_path, file_name, creator, app_name, jsons, xmls) -> Tuple[dict, dict]:
        '''
        Extracts all textual content in 'text', i.e., string blocks AND 
            in components, e.g., button, label, etc.
        ''' 
        self.extract_textual_content_blocks(file_path, file_name, creator, app_name, xmls)
        self.extract_textual_content_components(file_path, file_name, app_name, jsons)
        return self.text_content_by_comp_name, self.text_content_by_comp_type

    def extract_textual_content_blocks(self, file_path, file_name, creator, app_name, xmls):   
        '''
        Extracts all textual content in 'text', i.e., string blocks
        ''' 
        try: 
            self.creator = creator
            self.app_name = app_name
            for screen_key in xmls:
                self.__parse_XML_content(screen_key, xmls[screen_key])
        except Exception as e:
            print("[Parser_Content.__update_textual_content_blocks] This file " + str(file_name) + " causes exception")
            print(e)

    def __parse_XML_content(self, screen_key, docXMLString):
        if(docXMLString != ""): #checking if we have blocks in the screen
            tree = ET.ElementTree(ET.fromstring(docXMLString))
            root = tree.getroot()
            if  screen_key not in self.text_content_by_comp_name:
                self.text_content_by_comp_name[screen_key] = {}
                self.text_content_by_comp_type[screen_key] = {}
            self.text_content_by_comp_name[screen_key]['text_block'] = ""
            self.text_content_by_comp_type[screen_key]['text_block'] = ""
            self.__get_content_text_block(root, screen_key)
        else:
            if screen_key not in self.text_content_by_comp_name:
                self.text_content_by_comp_name[screen_key] = {}
                self.text_content_by_comp_type[screen_key] = {}
            self.text_content_by_comp_name[screen_key]['text_block'] = ""
            self.text_content_by_comp_type[screen_key]['text_block'] = ""

    def __get_content_text_block(self, node, screen_name):
        #Extrator de strings em blocos do tipo Texto
        if("field" in str(node.tag)):
            if("TEXT" in str(node.attrib)):
                self.text_content_by_comp_name[screen_name]['text_block'] += ' '+str(node.text)
                self.text_content_by_comp_type[screen_name]['text_block'] += ' '+str(node.text)
        for child in node:
            self.__get_content_text_block(child, screen_name)
            
    def extract_textual_content_components(self, file_path, file_name, app_name, jsons): 
        '''
        Extracts all textual content in components, e.g., button, label, etc.
        '''  
        try:
            #screens = Decompressor.extract_JSONS(file_path, app_name)
            for screen in jsons:
                if(jsons[screen] != ""):
                    for screen_content in jsons[screen].split('\n'):
                        if (screen_content[0]=='{'):
                            self.__parse_JSON_content(screen, screen_content)
        except Exception as e:
            
            print(f"[{self.__class__.__name__}.{self.extract_textual_content_components.__name__}] This file " + file_name + " causes exception")
            #print(e)

    def __parse_JSON_content(self, screen_name, screen_content):
        # Informações textuais das telas
        #if  screen_name not in self.textual_content:
        self.text_content_by_comp_name.__setitem__(screen_name, {})
        self.text_content_by_comp_type.__setitem__(screen_name, {})
        try:
            y = json.loads(screen_content)
            #self.textual_content[screen_name]['file_name'] = self.file_name
            #self.textual_content[screen_name]['app_name'] = y['Properties']['AppName']
            #self.textual_content[screen_name]['screen_name'] = y['Properties']['$Name']
            if ('Title' in y['Properties']):
                self.text_content_by_comp_name[screen_name]['ScreenTitle'] = y['Properties']['Title']
                self.text_content_by_comp_type[screen_name]['ScreenTitle'] = y['Properties']['Title']
            if ('AboutScreen' in y['Properties']):
                self.text_content_by_comp_name[screen_name]['AboutScreen'] = y['Properties']['AboutScreen']
                self.text_content_by_comp_type[screen_name]['AboutScreen'] = y['Properties']['AboutScreen']
            # Listing strings/textx/etc from componentes (from Designer)
            if('$Components'in y['Properties']):
                self.__get_comp_text_and_sub(y['Properties']['$Components'], screen_name)
        except Exception as e:
            print(f"[Parser_Content.__parse_JSON_content] This file JSON {str(screen_name)} could not be loaded: {e.__class__.__name__}")

    def __get_comp_text_and_sub(self, component_list, screen_name):
        #Extração do conteúdo
        selected_components_for_textual_extraction = {"Text", "ElementsFromString", "Hint", "Prompt", "Message", "ResultName", "Description"}
        for component in component_list:
            for component_for_textual_extraction in selected_components_for_textual_extraction:
                if (component_for_textual_extraction in component):
                    self.text_content_by_comp_name[screen_name][component["$Type"] +':'+ component["$Name"]] = component[component_for_textual_extraction]
                    if component["$Type"] not in self.text_content_by_comp_type[screen_name]:
                        self.text_content_by_comp_type[screen_name][component["$Type"]] = component[component_for_textual_extraction]
                    else:
                        self.text_content_by_comp_type[screen_name][component["$Type"]] += ' ' + (component[component_for_textual_extraction])
            if ('$Components' in component.keys()):
                self.__get_comp_text_and_sub(component['$Components'], screen_name)
