
from typing import Tuple
import xml.etree.ElementTree as ET

from creassessment.controler.constants import BLOCKS_COMPONENTS_CATEGORIES, BUILT_IN_BLOCKS_CATEGORIES, BUILT_IN_BLOCKS_CATEGORIES_KEYWORDS, COL_EXTENSION, FLUENCY_PROGRAMMING_VALUE, GENERIC_BLOCKS


class Parser_Blocks:
    grouped_blocks_freq: dict
    blocks_freq: dict
    creator: str
    app_name: str

    def __init__(self):
        self.grouped_blocks_freq = {}
        self.blocks_freq = {}
        self.programming_categories = {}
        self.programming_categories_freq_and_fluency = {}

    def parse_blocks(self, file_path, file_name, creator, app_name, jsons) -> Tuple[dict, dict, dict, dict]: 
        '''
        Descompress and extract the programming blocks in a XML file.
        screens_key: (File path, File name, App name, Screen name [Designer/Blocks])
        ''' 
        #s_grouped = lambda is_grouped: "[event blocks grouped] " if is_grouped else ''
        #print(f'Analyzing blocks frequence {s_grouped(is_grouped)}of ', file_name)  
        try:
            self.creator = creator
            self.app_name = app_name
            if jsons == {}:
                return self.grouped_blocks_freq, self.blocks_freq, self.programming_categories, self.programming_categories_freq_and_fluency
            else:
                for screens_key in jsons:
                    self.__parse_XML_blocks(jsons[screens_key], screens_key, file_name)
                self.__update_programming_categories()
        except Exception as e:
            print("[Parser_Blocks.extract_blocks] This file " + file_name + " causes exception")
            print(e)
        else:
            return self.grouped_blocks_freq, self.blocks_freq, self.programming_categories, self.programming_categories_freq_and_fluency
    
    def __parse_XML_blocks(self, docXMLString, screens_key, file_name):
        if screens_key not in self.grouped_blocks_freq:
            self.grouped_blocks_freq[screens_key] = {}
            self.blocks_freq[screens_key] = {}
        if(docXMLString != ""):
            try:
                tree = ET.ElementTree(ET.fromstring(docXMLString))
                root = tree.getroot()
                self.__get_blocks_frequency(root, screens_key)
            except Exception as e:
                print("[Parser_Blocks.__update_blocks] This file " + file_name + " " + str(screens_key) + " causes exception")
                #print(e)

    def __get_blocks_frequency(self, node, screens_key):
        self.__extract_builtin_blocks_freq(node, screens_key)
        self.__extract_mutation_blocks_freq(node, screens_key)
        for child in node:
            self.__get_blocks_frequency(child, screens_key)

    def __extract_builtin_blocks_freq(self, node, screens_key):
        if("block" in str(node.tag)):
            if "type" in node.attrib:
                if ((node.attrib['type']) not in self.grouped_blocks_freq[screens_key]):
                    self.grouped_blocks_freq[screens_key].__setitem__((node.attrib['type']), 1)
                    self.blocks_freq[screens_key].__setitem__((node.attrib['type']), 1)
                else:
                    self.grouped_blocks_freq[screens_key][(node.attrib['type'])] += 1
                    self.blocks_freq[screens_key][(node.attrib['type'])] += 1
    
    def __extract_mutation_blocks_freq(self, node, screens_key):
        if "mutation" in str(node.tag):
            if("component_type" in str(node.attrib)):
                component = str(node.attrib['component_type'])
                block = ''
                if 'set_or_get' in node.attrib:
                    block = str(node.attrib['set_or_get'])
                    if 'property_name' in node.attrib:
                        block = block + '_' + str(node.attrib['property_name'])
                elif 'method_name' in node.attrib:
                    block = str(node.attrib['method_name'])
                elif 'event_name' in node.attrib:
                    block = str(node.attrib['event_name'])
                #Group mutation blocks from designer components
                grouped_key = component
                if (grouped_key not in self.grouped_blocks_freq[screens_key]):
                    self.grouped_blocks_freq[screens_key].__setitem__(grouped_key, 1)
                else:
                    self.grouped_blocks_freq[screens_key][grouped_key] += 1
                key = component + '_' + block
                if (key not in self.blocks_freq[screens_key]):
                    self.blocks_freq[screens_key].__setitem__(key, 1)
                else:
                    self.blocks_freq[screens_key][key] += 1
    
    def __init_programming_categories_for_screen(self, screens_key) -> None:
        '''Initialize programming_categories and programming_categories_freq with 0 and False for a screen_key'''
        self.programming_categories[screens_key] = {}; self.programming_categories_freq_and_fluency[screens_key] = {}
        for category in BUILT_IN_BLOCKS_CATEGORIES:
            self.programming_categories_freq_and_fluency[screens_key].__setitem__(category, 0)
            self.programming_categories[screens_key].__setitem__(category, False)
        for blocks_components_categories in BLOCKS_COMPONENTS_CATEGORIES:
            self.programming_categories_freq_and_fluency[screens_key].__setitem__(blocks_components_categories, 0)
            self.programming_categories[screens_key].__setitem__(blocks_components_categories, False)
        self.programming_categories_freq_and_fluency[screens_key].__setitem__(COL_EXTENSION, 0)
        self.programming_categories[screens_key].__setitem__(COL_EXTENSION, False)

    def __update_programming_categories(self) -> None:
        '''Sum (for programming_categories_freq) and identify (programming_categories) the category of blocks
        based on the exact name of the blocks'''
        for screens_key in self.grouped_blocks_freq.keys():
            current_screen_programming_fluency = 0
            self.__init_programming_categories_for_screen(screens_key)
            for current_grouped_block in self.grouped_blocks_freq[screens_key]:
                found_current_grouped_block_category = False
                for built_in_category, category_blocks in BUILT_IN_BLOCKS_CATEGORIES.items():
                    if current_grouped_block in category_blocks:
                        #print('Found category: ', built_in_category, ' for block:', current_grouped_block)
                        current_screen_programming_fluency +=  self.grouped_blocks_freq[screens_key][current_grouped_block]
                        self.programming_categories_freq_and_fluency[screens_key][built_in_category] += self.grouped_blocks_freq[screens_key][current_grouped_block]
                        self.programming_categories[screens_key][built_in_category] = True
                        found_current_grouped_block_category = True
                for components_category, components_category_blocks in BLOCKS_COMPONENTS_CATEGORIES.items():
                    if current_grouped_block in components_category_blocks:
                        current_screen_programming_fluency +=  self.grouped_blocks_freq[screens_key][current_grouped_block]
                        self.programming_categories_freq_and_fluency[screens_key][components_category] += self.grouped_blocks_freq[screens_key][current_grouped_block]
                        self.programming_categories[screens_key][components_category] = True
                        found_current_grouped_block_category = True
                if not found_current_grouped_block_category:
                    if current_grouped_block not in GENERIC_BLOCKS:
                        #print("\n\nNot found category for grouped block: ", current_grouped_block, "\n\n")
                        self.programming_categories_freq_and_fluency[screens_key][COL_EXTENSION] += self.grouped_blocks_freq[screens_key][current_grouped_block]
                        self.programming_categories[screens_key][COL_EXTENSION] = True
            self.programming_categories_freq_and_fluency[screens_key].__setitem__(FLUENCY_PROGRAMMING_VALUE, current_screen_programming_fluency)


    def __update_built_in_programming_category_from_keywords(self) -> None:
        # not used / ignore
        for screens_key in self.grouped_blocks_freq.keys():
            current_screen_programming_fluency = 0
            self.programming_categories[screens_key] = {}; self.programming_categories_freq_and_fluency[screens_key] = {}
            for built_in_blocks_category in BUILT_IN_BLOCKS_CATEGORIES_KEYWORDS.keys():
                current_programming_category_freq = 0
                self.programming_categories[screens_key].__setitem__(built_in_blocks_category, False)
                for block_keyword in BUILT_IN_BLOCKS_CATEGORIES_KEYWORDS[built_in_blocks_category]:
                    if self.__grouped_blocks_freq_contains(screens_key, block_keyword):
                        self.programming_categories[screens_key][built_in_blocks_category] = True
                        current_programming_category_freq += self.__grouped_blocks_freq_category_sum(screens_key, block_keyword)
                current_screen_programming_fluency += current_programming_category_freq
                self.programming_categories_freq_and_fluency[screens_key][built_in_blocks_category] = current_programming_category_freq
            self.programming_categories_freq_and_fluency[screens_key][FLUENCY_PROGRAMMING_VALUE] = current_screen_programming_fluency

    def __grouped_blocks_freq_contains(self, screens_key, block_keyword) -> bool:
        '''Verifies if grouped_blocks_freq contains a block_keyword for screens key'''
        for current_block in self.grouped_blocks_freq[screens_key]:
            if block_keyword in current_block:
                return True
        return False

    def __grouped_blocks_freq_category_sum(self, screens_key, block_keyword) -> int:
        '''Sum all grouped_blocks_freq for a block category and screen key considering block_keyword'''
        programming_categories_sum = 0
        for current_block in self.grouped_blocks_freq[screens_key]:
            if block_keyword in current_block:
                programming_categories_sum += self.grouped_blocks_freq[screens_key][current_block]
        return programming_categories_sum
    
