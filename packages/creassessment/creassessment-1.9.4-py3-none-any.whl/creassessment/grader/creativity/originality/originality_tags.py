from typing import Tuple
import pandas as pd
import math

from creassessment.grader.creativity.originality.originality_grader import Originality_Grader
from creassessment.grader.creativity.reference_universes.originality.reference_universe_tags import Reference_Universe_Tags
from creassessment.grader.creativity.reference_universes.originality.reference_universe_tags_2734apps import Reference_Universe_PT_Tags_2734_apps
from creassessment.grader.creativity.reference_universes.originality.reference_universe_tags_99411apps import Reference_Universe_Gen_Tags_99411_apps
from creassessment.controler.constants import DF_COL_PARSER_TAGS, NOT_IDENTIFIED
from creassessment.utils.creassess_utils import round_grade

class Originality_Tags(Originality_Grader):

    def __init__(self, ru: Reference_Universe_Tags = Reference_Universe_Gen_Tags_99411_apps()):
        self.ru = ru
        self.freq_sing = self.ru.get_freq_sing()

    def analyze_originality(self, df_app_query_items: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, float, float, pd.DataFrame]:
        '''
        Receives a pd dataframe (app_query_items) and returns three scalars: grade_sing, grade_comb, grade
        '''
        #print(f"\n====== {self.__class__.__name__} ====== ")
        df_originality_sing = self.get_df_originality_sing(df_app_query_items, is_grade_rounded)
        grade_sing = self.calculate_sing_originality_grade(df_app_query_items, df_originality_sing, is_grade_rounded)
        #print('grade: ', grade_sing, '\n')
        grade = grade_sing
        grade_comb = 0
        if is_grade_rounded:
            grade = round_grade(grade)
        #print(f"{self.__class__.__name__}. Originality grade: {grade: .2f}\n")
        return grade_sing, grade_comb, grade, df_originality_sing
    
    def get_df_originality_sing(self, app_query_items: pd.DataFrame, is_grade_rounded: bool) -> pd.DataFrame:
        '''
        Receives a pd dataframe (app_query_items) and returns the originality of the topic in a pd.dataframe
        '''
        app_tags = app_query_items[DF_COL_PARSER_TAGS].values[0]
        df_originality_sing = pd.DataFrame(index=app_query_items.index)
        #print('app_tags: ',  app_tags)
        for tag in app_tags:
            if tag == NOT_IDENTIFIED:
                tag_freq = 0; grade = 0
                #print('App tags not identified')
            elif tag in self.freq_sing.keys():
                tag_freq = int(self.freq_sing[tag])
                base_log = self.ru.biggest_tag_frequency
                grade_with_log_penalty = float((1 - math.log(tag_freq, base_log))*10)
                grade = grade_with_log_penalty
                if is_grade_rounded:
                    grade = round_grade(grade)
            else:
                tag_freq = 0; grade = 10.0
            df_originality_sing[tag] = grade
                #print(f'tag: {tag}  tag freq: {tag_freq}   grade: {df_originality_sing[tag].values}')
            #df_originality_sing.set_index(app_query_items.index)
        return df_originality_sing
    
    def calculate_sing_originality_grade(self, df_app_query_items: pd.DataFrame,
                                         df_originality_sing: pd.DataFrame,
                                         is_grade_rounded: bool) -> float:
        '''
        Receives two pd dataframe (df_app_query_items and df_originality_sing) and
            returns the singular originality grade
        '''
        # Here the df_originality_sing represents df_app_query_items in a better way
        # because the tags df_app_query_items are all in one single cell
        # So we use df_originality_sing to represent df_app_query_items
        return super().calculate_sing_originality_grade(df_originality_sing, df_originality_sing, is_grade_rounded)