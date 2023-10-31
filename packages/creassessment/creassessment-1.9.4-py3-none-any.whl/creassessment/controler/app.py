import pandas as pd
import os
from pathlib import Path
from typing import Callable, Tuple, Union
from werkzeug.datastructures import FileStorage

from creassessment.utils.decompressor import Decompressor

from creassessment.parser.parser_components import Parser_Components
from creassessment.parser.parser_blocks import Parser_Blocks
from creassessment.parser.parser_content import Parser_Content
from creassessment.parser.functionality_detector import Functionality_Detector
from creassessment.parser.topic_detector import Topic_Detector
from creassessment.parser.tags_extractor import Tags_Extractor

from creassessment.parser.parser_codemaster import Parser_CodeMaster
from creassessment.grader.codemaster_analyzer import CodeMaster_Analyzer

from creassessment.grader.creativity.creativity_grader import Creativity_Grader

from creassessment.controler.constants import \
    INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_FILE_PATH, \
    INDEX_NAME_FOR_SCREEN_NAME, DF_COL_TEXTUAL_CONTENT, \
    NOT_IDENTIFIED, NOT_IDENTIFIED_PTBR, TOPICS_TRANSLATION

class App:
    creator: str
    file_path: Path
    file_name: str
    app_name: str
    screens_name: str
    jsons: dict
    xmls: dict

    #Blocks
    grouped_blocks_freq: dict #no info on which type of block
    blocks_freq: dict #info on which type of block, e.g., ButtonClick
    programming_categories: dict
    programming_categories_freq: dict
    #Components (from Designer)
    components_freq: dict
    UI_components_freq: dict
    components_categories: dict
    components_categories_freq: dict
    #Content
    text_content_by_comp_type: dict
    text_content_by_comp_name: dict

    #Dependent attributes
    funcionalities: dict

    extentions: set

    def __init__(self, file: Union[Path, FileStorage]):
        self.file_path = file
        self.file_name = file.filename if type(file) == (FileStorage) else Path(file).name
        try:
            self.creator, self.app_name, self.extensions, self.screens_name = Decompressor.decompress(self.file_path)
        except:
            raise Exception("This file " +self.file_name+ " causes exception")
        else:
            # components (from Designer)
            self.components_freq = {}
            self.UI_components_freq = {}
            self.components_categories = {}
            self.components_categories_freq = {}
            # blocks
            self.blocks_freq = {}
            self.grouped_blocks_freq = {}
            self.programming_categories = {}
            self.programming_categories_freq = {}
            # textual content
            self.text_content_by_comp_type = {}
            self.text_content_by_comp_name = {}
            # parse
            self.__parse_raw_data()
    
    def __parse_raw_data(self) -> None:
        try:
            self.jsons = Decompressor.extract_JSONS(self.file_path, self.app_name)
        except:
            self.jsons = {}
        try:
            self.xmls = Decompressor.extract_XMLS(self.file_path, self.app_name)
        except:
            self.xmls = {}
        p_comp = Parser_Components()
        self.components_freq, self.UI_components_freq, \
        self.components_categories, self.components_categories_freq = p_comp.parse_components(self.file_path, 
                                                                                    self.file_name,
                                                                                    self.app_name,
                                                                                    self.jsons)
        p_blocks = Parser_Blocks()
        self.grouped_blocks_freq, self.blocks_freq, \
            self.programming_categories, self.programming_categories_freq = p_blocks.parse_blocks(self.file_path,
                                                                                          self.file_name,
                                                                                          self.creator,
                                                                                          self.app_name,
                                                                                          self.xmls)
        p_content = Parser_Content()
        self.text_content_by_comp_name, self.text_content_by_comp_type = p_content.parse_textual_content(self.file_path, self.file_name,
                                                                self.creator, self.app_name, self.jsons, self.xmls)

            
    ############
    # UI
    ############ 
    def get_df_UI_comp_freq(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Extract and returns the frequence of all UI components (VISIBLE design components) of App Inventor.
            is_detailed_by_screen: True -> discriminate per each screen of the app
                                   False -> groups info about all screens of the app
        '''
        try:
            df_UI = self.__rename_df_index_from_dict_with_four_index(self.UI_components_freq)
            if not is_detailed_by_screen:
                df_UI = df_UI.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                       INDEX_NAME_FOR_APP_NAME]).sum()
            df_UI[df_UI.isna()] = 0
            return df_UI
        except Exception as e:
            print(f'[{self.__class__.__name__}.get_df_UI_comp_freq] This file {self.file_name} causes exception')

    def get_df_components_freq(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Extract and returns the frequence of all components (from Designer) of App Inventor.
            is_detailed_by_screen: True -> discriminate per each screen of the app
                                   False -> groups info about all screens of the app
        '''
        try:
            df_UI = self.__rename_df_index_from_dict_with_four_index(self.components_freq)
            if not is_detailed_by_screen:
                df_UI = df_UI.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                       INDEX_NAME_FOR_APP_NAME]).sum()
            df_UI[df_UI.isna()] = 0
            return df_UI
        except Exception as e:
            print(f'[{self.__class__.__name__}.{self.get_df_components_freq.__name__}] This file {self.file_name} causes exception')

    def get_df_components_categories(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Identify and returns the categories of the use of components palette {COMPONENTS_CATEGORIES} of App Inventor.
            is_detailed_by_screen: True -> discriminate per each screen of the app
                                   False -> groups info about all screens of the app
        '''
        try:
            df_UI = self.__rename_df_index_from_dict_with_four_index(self.components_categories)
            if not is_detailed_by_screen:
                df_UI = df_UI.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                       INDEX_NAME_FOR_APP_NAME]).sum().astype(bool)
            df_UI[df_UI.isna()] = 0
            return df_UI
        except Exception as e:
            print(f'[{self.__class__.__name__}.{self.get_df_components_categories.__name__}] This file {self.file_name} causes exception')

    def get_df_components_categories_freq(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Identify and returns the frequency of components per category {COMPONENTS_CATEGORIES} of App Inventor.
            is_detailed_by_screen: True -> discriminate per each screen of the app
                                   False -> groups info about all screens of the app
        '''
        try:
            df_UI = self.__rename_df_index_from_dict_with_four_index(self.components_categories_freq)
            if not is_detailed_by_screen:
                df_UI = df_UI.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                       INDEX_NAME_FOR_APP_NAME]).sum()
            df_UI[df_UI.isna()] = 0
            return df_UI
        except Exception as e:
            print(f'[{self.__class__.__name__}.{self.get_df_components_categories_freq.__name__}] This file {self.file_name} causes exception')


    ############
    # Content
    ############ 
    def get_df_textual_content(self, is_textual_content_grouped: bool = True,
                               is_discriminated_by_component_name: bool = False,
                               is_discriminated_by_screen: bool = True) -> pd.DataFrame:
        '''
        Extract and returns the textual content of the app.
        is_textual_content_grouped: True -> groups content of each screen of the app
                                            in one column called 'textual_content' 
                                            (useful for rapid text analysis).
                                    False -> all components are separated by its own
                                            type, e.g., ['Button'] = 'Consultar Fechar' etc.
        is_discriminated_by_component_name: True -> all components are separated by its own
                        name and type, e.g., ['Button:abaConsultar'] = 'Consultar'
                                            False -> content separated in one row and as many columns
                        for components types as necessary per screen.
        '''
        #print(f'Analyzing {detail_level} details of the textual content of ', self.file_name)  
        if is_discriminated_by_component_name:
            df_text_content = self.__rename_df_index_from_dict_with_four_index(self.text_content_by_comp_name)
        else:
            df_text_content = self.__rename_df_index_from_dict_with_four_index(self.text_content_by_comp_type)
        df_text_content[df_text_content.isna()] = ''
        if not is_discriminated_by_screen:
            df_text_content = df_text_content.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                       INDEX_NAME_FOR_APP_NAME]).agg(lambda x: ' '.join(set(x)))
            df_text_content['ScreensName'] = self.screens_name
        if is_textual_content_grouped:
            df_textual_content_grouped = df_text_content.copy()
            df_textual_content_grouped[DF_COL_TEXTUAL_CONTENT] = ''
            for column in df_text_content:
                df_text_content = df_text_content.where(pd.notnull(df_text_content), "")
                df_textual_content_grouped[DF_COL_TEXTUAL_CONTENT] += ' ' + df_text_content[column].astype(str)
                df_textual_content_grouped.drop(columns=[column], inplace=True)
            del(df_text_content)
            return df_textual_content_grouped
        return df_text_content
   
    ############
    # Blocks
    ############ 
    def get_df_blocks_freq(self) -> pd.DataFrame:
        df_blocks_freq = self.__rename_df_index_from_dict_with_four_index(self.blocks_freq)
        df_blocks_freq[df_blocks_freq.isna()] = 0
        return df_blocks_freq

    def get_df_grouped_blocks_freq(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        df_grouped_blocks_freq = self.__rename_df_index_from_dict_with_four_index(self.grouped_blocks_freq)
        df_grouped_blocks_freq[df_grouped_blocks_freq.isna()] = 0
        if self.grouped_blocks_freq != {}:
            if not is_detailed_by_screen:
                try:
                    df_grouped_blocks_freq = df_grouped_blocks_freq.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                            INDEX_NAME_FOR_APP_NAME]).sum()
                except:
                    print(f'[{self.__class__.__name__}.{self.get_df_grouped_blocks_freq.__name__}] This file {self.file_name} causes exception')
        return df_grouped_blocks_freq

    def get_df_blocks_plus_grouped_blocks_freq(self) -> Tuple[pd.DataFrame, pd.DataFrame]:
        '''
        Returns dataframes containing all command blocks in the project detailed by screens
        '''
        return self.get_df_grouped_blocks_freq(is_detailed_by_screen=True), self.get_df_blocks_freq()
    
    def get_df_programming_categories(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Returns a dataframe indicating (True or False) for blocks categories in the project 
            Useful for extracting blocks categories in batch caller
        '''
        df_programming_categories = self.__rename_df_index_from_dict_with_four_index(self.programming_categories)
        df_programming_categories[df_programming_categories.isna()] = 0
        if self.programming_categories != {}:
            if not is_detailed_by_screen:
                try:
                    df_programming_categories = df_programming_categories.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                            INDEX_NAME_FOR_APP_NAME]).sum().astype(bool)
                except:
                    print(f'[{self.__class__.__name__}.{self.get_df_programming_categories.__name__}] This file {self.file_name} causes exception')
        return df_programming_categories
    
    def get_df_programming_categories_freq(self, is_detailed_by_screen: bool = False) -> pd.DataFrame:
        '''
        Returns a dataframe containing all blocks categories in the project 
            Useful for extracting blocks categories in batch caller
        '''
        df_programming_categories_freq = self.__rename_df_index_from_dict_with_four_index(self.programming_categories_freq)
        df_programming_categories_freq[df_programming_categories_freq.isna()] = 0
        if self.programming_categories_freq != {}:
            if not is_detailed_by_screen:
                try:
                    df_programming_categories_freq = df_programming_categories_freq.groupby([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                                            INDEX_NAME_FOR_APP_NAME]).sum()
                except:
                    print(f'[{self.__class__.__name__}.{self.get_df_programming_categories_freq.__name__}] This file {self.file_name} causes exception')
        return df_programming_categories_freq


    ############
    # Functionalities
    ############ 
    def get_df_functionalities(self) -> pd.DataFrame:
        '''
        Returns a dataframe indicating True for all detected functions in a project
        '''
        parser_functionality = Functionality_Detector()
        df_blocks_grouped, df_blocks = self.get_df_blocks_plus_grouped_blocks_freq()
        df_textual_content_by_component_type = self.get_df_textual_content(is_textual_content_grouped=False,
                                                            is_discriminated_by_component_name=False,
                                                            is_discriminated_by_screen=True)
        functions_detected = pd.Series(parser_functionality.detect_functionalities(df_blocks_grouped,
                                                                                   df_blocks,
                                                                                   df_textual_content_by_component_type))
        del df_blocks_grouped; del df_blocks; del df_textual_content_by_component_type
        self.funcionalities = pd.DataFrame({(self.file_path, self.file_name, self.app_name): functions_detected})
        df_func = self.__rename_df_index_from_dict_with_three_index(self.funcionalities)
        return df_func

    ############
    # Topic
    ############ 
    def get_df_topic(self) -> pd.DataFrame:
        '''
        Returns a dataframe with the topic and its probability for a project
        '''
        parser_topic = Topic_Detector()
        df_textual_content_by_component_type = self.get_df_textual_content(is_textual_content_grouped=True,
                                                            is_discriminated_by_component_name=False,
                                                            is_discriminated_by_screen=False)
        self.topic = pd.DataFrame({(self.file_path, self.file_name, self.app_name): parser_topic.detect_topic(df_textual_content_by_component_type)})
        del df_textual_content_by_component_type
        df_topic = self.__rename_df_index_from_dict_with_three_index(self.topic)
        return df_topic
    
    def get_df_tags(self) -> pd.DataFrame:
        '''
        Returns a dataframe with the extracted tags for the textual content of a project
        '''
        parser_tags = Tags_Extractor()
        df_textual_content_by_component_type = self.get_df_textual_content(is_textual_content_grouped=True,
                                                            is_discriminated_by_component_name=False,
                                                            is_discriminated_by_screen=False)
        self.tags = pd.DataFrame({(self.file_path, self.file_name, self.app_name): 
                                    parser_tags.get_keywords(df_textual_content_by_component_type)})
        df_tags = self.__rename_df_index_from_dict_with_three_index(self.tags)
        return df_tags

    
    ############
    # Creativity
    ############ 
    def grade_creativity(self, grader: Creativity_Grader = Creativity_Grader(),
                               is_grade_rounded: bool = True,
                               drop_index: bool = True) -> pd.DataFrame:
        '''
        Analyzes the creativity using a Creativity_Grader and returns a pandas DataFrame
        with the grades.
            If is_grade_rounded = True, the grades will be rounded to every 5 tenths
            If drop_index = True, the indexes of each data will be dropped in the
            analysis. This is useful if the computer in which the analysis is running 
            saves files across different folders.
        '''
        fuctionalities = self.get_df_functionalities().copy()
        UI_comp = self.get_df_UI_comp_freq(is_detailed_by_screen=False).copy()
        topic = self.get_df_topic()
        tags = self.get_df_tags()
        components_categories = self.get_df_components_categories()
        programming_categories = self.get_df_programming_categories()
        components_categories_freq = self.get_df_components_categories_freq()
        programming_categories_freq = self.get_df_programming_categories_freq()
        return grader.grade_creativity(fuctionalities, UI_comp, topic, tags,
                                         components_categories, programming_categories,
                                         components_categories_freq, programming_categories_freq,
                                         is_grade_rounded, drop_index=drop_index)

    def grade_creativity_to_json(self, grader: Creativity_Grader,
                                       is_grade_rounded: bool) -> str:
        '''
        Analyzes the creativity using a Creativity_Grader and returns a string JSON
        with the grades.
            If is_grade_rounded = True, the grades will be rounded to every 5 tenths
            If drop_index = True, the indexes of each data will be dropped in the
            analysis. This is useful if the computer in which the analysis is running 
            saves files across different folders.
        '''
        return self.grade_creativity(grader, is_grade_rounded, drop_index=True).to_json(orient="records", force_ascii=False)

    def grade_creativity_to_json_wrapper(self, grader: Creativity_Grader,
                                         is_grade_rounded: bool) -> str:
        '''
        Analyzes the creativity using a Creativity_Grader and returns a string JSON
        with the grades, in which booleans are number and topics are in pt-br.
            If is_grade_rounded = True, the grades will be rounded to every 5 tenths
            If drop_index = True, the indexes of each data will be dropped in the
            analysis. This is useful if the computer in which the analysis is running 
            saves files across different folders.
        '''
        json_grades = self.grade_creativity_to_json(grader, is_grade_rounded)
        # All results in integer form (true -> 1, false -> 0) because CodeMaster system.
        json_grades = json_grades.replace("true", "1.0")
        json_grades = json_grades.replace("false", "0.0")
        detected_topic_ptbr = str(list(map(TOPICS_TRANSLATION.get, filter(lambda topic: topic in json_grades, TOPICS_TRANSLATION)))[0])
        detected_topic_en = str([k for (k, v) in TOPICS_TRANSLATION.items() if v == detected_topic_ptbr][0])
        json_grades = json_grades.replace(detected_topic_en, detected_topic_ptbr)
        json_grades = json_grades.replace(NOT_IDENTIFIED, NOT_IDENTIFIED_PTBR)
        return json_grades

    ############
    # Computational thinking
    ############ 
    def get_ct_concepts(self) -> pd.DataFrame:
        '''
        Returns a dataframe indicating the grade for all
            Computational Thinking concepts in a project
        '''
        parser_ct_concepts = Parser_CodeMaster()
        df_blocks_grouped, df_blocks = self.get_df_blocks_plus_grouped_blocks_freq()
        df_UI_comp = self.get_df_UI_comp_freq(is_detailed_by_screen=True)
        df_textual_content_by_component_type = self.get_df_textual_content(is_textual_content_grouped=False,
                                                            is_discriminated_by_component_name=False,
                                                            is_discriminated_by_screen=True)
        ct_concepts = parser_ct_concepts.detect_computational_thinking(df_blocks_grouped,
                                                                        df_UI_comp,
                                                                        self.extensions)
        del df_blocks_grouped; del df_blocks; del df_textual_content_by_component_type
        return pd.DataFrame({(self.file_name, self.app_name): ct_concepts}).T

    def analyze_ct(self) -> int:
        ct_concepts = self.get_ct_concepts()
        analyzer = CodeMaster_Analyzer()
        grade = analyzer.analyze_computational_thinking(ct_concepts)
        print(f"Computational thinking grade: {grade}")
        return grade

    ############
    # All
    ############ 
    def do_all(self, grader: Creativity_Grader = Creativity_Grader()) -> None:
        '''
        Uses all the extraction functions of app module for extraction.
        Saves the results on a separated XLS for each extraction.
        '''
        print(f"[App.do_all] - Analyzing app {self.app_name}")
        save_df_xls_in_dir = self.__prepare_and_save_df_xls_in_dir()
        #Get UI component frequency
        save_df_xls_in_dir(self.get_df_components_freq(is_detailed_by_screen=False), f"/components_freq.xlsx")
        save_df_xls_in_dir(self.get_df_components_freq(is_detailed_by_screen=True), f"/components_freq_detailed_by_screen.xlsx")
        save_df_xls_in_dir(self.get_df_UI_comp_freq(is_detailed_by_screen=False), f"/UI_components_freq.xlsx")
        save_df_xls_in_dir(self.get_df_UI_comp_freq(is_detailed_by_screen=True), f"/UI_components_detailed_by_screen.xlsx")
        save_df_xls_in_dir(self.get_df_components_categories(is_detailed_by_screen=False), f"/components_categories.xlsx")
        save_df_xls_in_dir(self.get_df_components_categories(is_detailed_by_screen=True), f"/components_categories_detailed_by_screen.xlsx")
        #Get blocks frequency
        df_blocks_grouped, df_blocks = self.get_df_blocks_plus_grouped_blocks_freq()
        save_df_xls_in_dir(df_blocks, "/blocks.xlsx")
        save_df_xls_in_dir(df_blocks_grouped, "/blocks_grouped.xlsx")
        df_programming_categories = self.get_df_programming_categories()
        save_df_xls_in_dir(df_programming_categories, "/programming_categories.xlsx")
        df_programming_categories_freq = self.get_df_programming_categories_freq()
        save_df_xls_in_dir(df_programming_categories_freq, "/programming_categories_freq.xlsx")
        df_programming_categories_freq_per_screen = self.get_df_programming_categories_freq(is_detailed_by_screen=True)
        save_df_xls_in_dir(df_programming_categories_freq_per_screen, "/programming_categories_freq_detailed_by_screen.xlsx")
        #Get detailed textual components
        save_df_xls_in_dir(self.get_df_textual_content(is_discriminated_by_component_name=False,
                                                       is_textual_content_grouped=True,
                                                       is_discriminated_by_screen=True), 
                                                       f"/textual_content_textual_content_grouped_by_screen.xlsx")
        save_df_xls_in_dir(self.get_df_textual_content(is_discriminated_by_component_name=False,
                                                       is_textual_content_grouped=True,
                                                       is_discriminated_by_screen=False), 
                                                       f"/textual_content_textual_content_grouped.xlsx")
        save_df_xls_in_dir(self.get_df_textual_content(is_discriminated_by_component_name=False,
                                                       is_textual_content_grouped=False,
                                                       is_discriminated_by_screen=True),
                                                       f"/textual_content_by_component.xlsx")
        save_df_xls_in_dir(self.get_df_textual_content(is_discriminated_by_component_name=True,
                                                       is_textual_content_grouped=False,
                                                       is_discriminated_by_screen=True),
                                                       f"/textual_content_discriminated_by_component_name.xlsx")
        save_df_xls_in_dir(self.get_df_textual_content(is_discriminated_by_component_name=True,
                                                is_textual_content_grouped=False,
                                                is_discriminated_by_screen=False),
                                                f"/textual_content_discriminated_by_component_name_screen_grouped.xlsx")
        #Get detailed functionalities
        save_df_xls_in_dir(self.get_df_functionalities(), "/functionalities.xlsx") 
        #Get identified topic
        save_df_xls_in_dir(self.get_df_topic(), "/topic.xlsx") 
        #Get identified topic
        save_df_xls_in_dir(self.get_df_tags(), "/tags.xlsx") 
        #Get creativity grade using different RUs
        save_df_xls_in_dir(self.grade_creativity(grader,
                                                 is_grade_rounded=True,
                                                 drop_index=False), "/creativity_ROUNDED.xlsx")
        save_df_xls_in_dir(self.grade_creativity(grader,
                                                 is_grade_rounded=False,
                                                 drop_index=False), "/creativity_NOT_ROUNDED.xlsx")



    def __prepare_and_save_df_xls_in_dir(self) -> Callable:
        '''
        Prepare a directory for saving xls results.
        Returns a function for facilitating saving the results
        '''
        dir = str(self.file_path) + '_results'
        if not os.path.exists(dir):
            os.mkdir(dir)
        df_to_excel = lambda df, name: df.to_excel(dir + name, sheet_name='Sheet_name_1')
        print('Results saved at ', str(dir))
        return df_to_excel

    def __rename_df_index_from_dict_with_four_index(self, d: dict) -> pd.DataFrame:
        if d: #dict is not empty
            df = pd.DataFrame.from_dict(d).T
            df = df.rename_axis([INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME,
                             INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_SCREEN_NAME])
            return df
        else: #return empty df
            return pd.DataFrame()

    def __rename_df_index_from_dict_with_three_index(self, d: dict) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(d).T
        df = df.rename_axis([INDEX_NAME_FOR_FILE_PATH,
                             INDEX_NAME_FOR_FILE_NAME,
                             INDEX_NAME_FOR_APP_NAME])
        return df
    


    def grade_creativity_to_string(self, grader: Creativity_Grader = Creativity_Grader(),
                               is_grade_rounded: bool = True,
                               drop_index: bool = True) -> str:
        '''
        Analyzes the creativity using a Creativity_Grader and outputs the grades.
            If is_grade_rounded = True, the grades will be rounded to every 5 tenths
            If drop_index = True, the indexes of each data will be dropped in the
            analysis. This is useful if the computer in which the analysis is running 
            saves files across different folders.
        '''
        df_assessement = self.grade_creativity(grader, is_grade_rounded, drop_index)
        for col in df_assessement:
            print(f'{col}: {df_assessement[col][0]}')