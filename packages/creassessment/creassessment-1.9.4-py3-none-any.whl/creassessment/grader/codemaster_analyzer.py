import pandas as pd

from creassessment.controler.app import *

class CodeMaster_Analyzer:

    def __init__(self):
        pass

    #todo
    def analyze_computational_thinking(self, df_app_query_codemaster: pd.DataFrame) -> int:
        '''
        Receives a pd dataframe (app_query_functionalities) and returns three scalars: grade_sing, grade_comb, grade
        '''
        grade = 0
        for ct in df_app_query_codemaster:
            ct_grade = int(df_app_query_codemaster[ct][0])
            grade = grade + ct_grade
            print(f'{ct} : {ct_grade}')
        return grade