from typing import Tuple
import pandas as pd

from creassessment.grader.creativity.originality.originality_grader import Originality_Grader
from creassessment.grader.creativity.reference_universes.originality.reference_universe_topic import Reference_Universe_Topic
from creassessment.grader.creativity.reference_universes.originality.reference_universe_topics_1682apps import Reference_Universe_Topics_1682_apps
from creassessment.controler.constants import DF_COL_PARSER_TOPIC_IDENTIFICATION
from creassessment.utils.creassess_utils import round_grade

class Originality_Topic(Originality_Grader):

    ru: Reference_Universe_Topic

    def __init__(self, ru: Reference_Universe_Topic = Reference_Universe_Topics_1682_apps()):
        self.ru = ru
        self.freq_sing = self.ru.get_freq_sing()

    def analyze_originality(self, df_app_query_items: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, float, float, pd.DataFrame]:
        '''
        Receives a pd dataframe (app_query_items) and returns three scalars: grade_sing, grade_comb, grade
        '''
        #print(f"\n====== {self.__class__.__name__} ====== ")
        df_originality_sing = self.get_df_originality_sing(df_app_query_items, is_grade_rounded)
        grade_sing = self.calculate_sing_originality_grade(df_app_query_items, df_originality_sing, is_grade_rounded)
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
        app_topic = str(app_query_items[DF_COL_PARSER_TOPIC_IDENTIFICATION].values[0])
        originality_sing_grade_item = float((100 - self.freq_sing[app_topic])/10.0)
        df_originality_sing = pd.DataFrame(index=app_query_items.index)
        df_originality_sing[DF_COL_PARSER_TOPIC_IDENTIFICATION] = round_grade(originality_sing_grade_item) if is_grade_rounded else originality_sing_grade_item
        return df_originality_sing
    
    def calculate_sing_originality_grade(self, df_app_query_items: pd.DataFrame,
                                         df_originality_sing: pd.DataFrame,
                                         is_grade_rounded: bool) -> float:
        '''
        Receives two pd dataframe (df_app_query_items and df_originality_sing) and
            returns the singular originality grade
        '''
        return df_originality_sing[DF_COL_PARSER_TOPIC_IDENTIFICATION].values[0]