import json
import logging
from typing import Tuple
import pandas as pd
import copy

from creassessment.controler.constants import FLUENCY_COMPONENTS_PREFIX, FLUENCY_COMPONENTS_VALUE, UI_COMPONENTS, COMPONENTS_CATEGORIES


class Parser_Components:
    components_freq: dict
    UI_comp_freq: dict #visible design components
    components_categories: dict
    components_categories_freq: dict

    def __init__(self):
        self.components_freq = {}
        self.UI_comp_freq = {}
        self.components_categories = {}
        self.components_categories_freq = {}

    def parse_components(self, file_path, file_name: str, app_name: str, screens) -> Tuple[dict, dict, dict, dict]: 
        '''
        Extracts all component frequency of an app (file_path)
        '''
        #print('Analyzing UI components frequence of ', file_name)
        try:
            for screens_key in screens:
                if(screens[screens_key] != ""):
                    for screen_content in screens[screens_key].split('\n'):
                        if (screen_content[0]=='{'):
                            self.components_freq.__setitem__(screens_key, {})
                            self.UI_comp_freq.__setitem__(screens_key, {})
                            self.components_categories.__setitem__(screens_key, {})
                            self.components_categories_freq.__setitem__(screens_key, {})
                            self.__parse_JSON_components(screens_key, screen_content)
        except Exception as ex: 
            print(f"[{self.__class__.__name__}.{self.parse_components.__name__}] This file " + str(file_name) + " causes exception")
            #logging.exception("[Parser_Design_Components.extract_design_component_freq] This file " + str(file_name) + " causes exception")
            self.__set_non_detected_UI_components_to_zero()
            self.__update_UI_comp_freq()
            self.__update_components_categories_freq()
            return self.components_freq, self.UI_comp_freq, self.components_categories, self.components_categories_freq
        else:
            self.__set_non_detected_UI_components_to_zero()
            self.__update_UI_comp_freq()
            self.__update_components_categories_freq()
            return self.components_freq, self.UI_comp_freq, self.components_categories, self.components_categories_freq
    
    def __parse_JSON_components(self, screens_key, screen_content):
        '''
        screens_key: (File path, File name, App name, Screen name [Designer/Blocks])
        '''
        try:
            y = json.loads(screen_content)
            #insert_component(screen_name, (y['Properties']['$Type'])) #useless
            if('BackgroundImage' in y['Properties']):
                self.__insert_component(screens_key, 'BackgroundImage')
            if('$Components' in y['Properties']):
                self.__sum_comp_and_subcomp(screens_key, y['Properties']['$Components'])
        except Exception as e:
            print(f"[{self.__class__.__name__}.{self.__parse_JSON_components.__name__}] This file JSON  {str(screens_key)} could not be loaded: {e.__class__.__name__}")
            #logging.exception(e)


    def __insert_component(self, screens_key, component_name):
        if (component_name not in self.components_freq[screens_key]):
            self.components_freq[screens_key].__setitem__(component_name, 1)
            self.UI_comp_freq[screens_key].__setitem__(component_name, 1)
        else:
            self.components_freq[screens_key][component_name] = self.components_freq[screens_key][component_name] + 1
            self.UI_comp_freq[screens_key][component_name] = self.UI_comp_freq[screens_key][component_name] + 1

    def __sum_comp_and_subcomp(self, screens_key, components_list):
        for component in components_list:
            self.__insert_component(screens_key, component["$Type"])
            if ('$Components' in component.keys()):
                self.__sum_comp_and_subcomp(screens_key, component['$Components'])

    def __set_non_detected_UI_components_to_zero(self) -> None:
        non_detected_UI_components = UI_COMPONENTS.copy()
        # Remove all items that were detected
        for screens_key in self.components_freq:
            for component in self.components_freq[screens_key]:
                if component in non_detected_UI_components:
                    non_detected_UI_components.remove(component)
        # Set undetected items to 0
        for component in non_detected_UI_components:
            self.components_freq[screens_key].__setitem__(component, 0)
            self.UI_comp_freq[screens_key].__setitem__(component, 0)
            
    def __update_UI_comp_freq(self) -> None:
        '''
        Updates self.UI_comp_freq with the 
            selected components of SELECTED_COLUMNS_FOR_DESIGN
        '''
        for screens_key in self.components_freq.keys():
            for component in self.components_freq[screens_key]:
                if component not in UI_COMPONENTS:
                    self.UI_comp_freq[screens_key].pop(component)
    
    def __update_components_categories_freq(self) -> None:
        '''
        Updates self.design_comp_categories_freq according to App Inventor categories
        '''
        for screens_key in self.components_freq.keys():
            current_screen_component_fluency = 0
            for component_category in COMPONENTS_CATEGORIES.keys():
                self.components_categories[screens_key][component_category] = False
                current_component_category_freq = 0
                for component in COMPONENTS_CATEGORIES[component_category]:
                    if self.__component_freq_contains(screens_key, component):
                        self.components_categories[screens_key][component_category] = True
                        current_component_category_freq += self.components_freq[screens_key][component]
                        #print(f"{self.__class__.__name__} {screens_key[3]}: {component_category} [{design_component}]")
                self.components_categories_freq[screens_key][FLUENCY_COMPONENTS_PREFIX + component_category] = current_component_category_freq
                current_screen_component_fluency += current_component_category_freq
            self.components_categories_freq[screens_key][FLUENCY_COMPONENTS_VALUE] = current_screen_component_fluency


    def __component_freq_contains(self, screen_key, desired_component) -> bool:
        '''Verifies if design_comp_freq contains more than 0 of a component for a screen key'''
        for component in self.components_freq[screen_key]:
            if component == desired_component:
                if self.components_freq[screen_key][component] > 0:
                    return True
        return False
    