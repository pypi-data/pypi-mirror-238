from cmath import log10
from typing import Tuple
import pandas as pd
import math

from creassessment.grader.creativity.reference_universes.originality.reference_universe_functionalities import Reference_Universe
from creassessment.utils.creassess_utils import round_grade

class Originality_Grader:
    '''
    There are two type of reference universe for items:
        Reference universe singular items
        Reference universe combined items
    '''
    ru: Reference_Universe

    freq_sing: dict
    freq_comb: pd.DataFrame

    def __init__(self, ru: Reference_Universe):
        self.ru = ru
        self.freq_sing = self.ru.get_freq_sing()
        self.freq_comb = self.ru.get_freq_comb()

    def analyze_originality(self, df_app_query_items: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, float, float, pd.DataFrame]:
        '''
        Receives a pd dataframe (app_query_items) and returns three scalars: grade_sing, grade_comb, grade, and df_originality_sing
        '''
        #print(f"\n====== {self.__class__.__name__} ====== ")
        df_app_query_items = self._select_columns_df_app_query_items(df_app_query_items)
        df_originality_sing = self.get_df_originality_sing(df_app_query_items, is_grade_rounded)
        grade_sing = self.calculate_sing_originality_grade(df_app_query_items, df_originality_sing, is_grade_rounded)
        grade_comb = self.calculate_comb_originality_grade(df_app_query_items, is_grade_rounded)
        grade = (grade_sing + grade_comb) / 2
        if is_grade_rounded:
            grade = round_grade(grade)
        #print(f"{self.__class__.__name__}. Originality grade: {grade: .2f}\n")
        return grade_sing, grade_comb, grade, df_originality_sing

    def _select_columns_df_app_query_items(self, df_app_query_items: pd.DataFrame) -> pd.DataFrame:
        '''
        Select specific columns from a data extraction of apps. Better implemented in subclasses.
        '''
        return df_app_query_items

    def get_df_originality_sing(self, app_query_items: pd.DataFrame, is_grade_rounded: bool) -> pd.DataFrame:
        '''
        Receives a pd dataframe (app_query_items) and returns the originality per
            item (e.g.: UI components, functionality) in a pd.dataframe
        '''
        _app_query_items = app_query_items.copy()
        df_originality_sing = pd.DataFrame(index=_app_query_items.index)
        for item in self.freq_sing:
            originality_sing_grade_item = float((100 - self.freq_sing[item])/10.0)
            df_originality_sing[item] = round_grade(originality_sing_grade_item) if is_grade_rounded else originality_sing_grade_item
            if item in _app_query_items.keys():
                _app_query_items = _app_query_items.drop(columns=[item])
        if len(_app_query_items) != 0: #verify if there were items that weren't in the RU (super rare)
            for item in _app_query_items.keys():
                if _app_query_items[item][0]: #is the missing RU item in the app?
                    originality_sing_grade_item = 10.0
                    df_originality_sing[item] = originality_sing_grade_item
        return df_originality_sing
    
    def calculate_sing_originality_grade(self,df_app_query_items: pd.DataFrame,
                                         df_originality_sing: pd.DataFrame,
                                         is_grade_rounded: bool) -> float:
        '''
        Receives two pd dataframe (df_app_query_items and df_originality_sing) and
            returns the singular originality grade
        '''
        sum_items = 0.0; grade = 0.0; qtd_items = 0
        _app_query_items = df_app_query_items.copy()
        for item in df_originality_sing:
            if item in _app_query_items.keys():
                if _app_query_items[item][0]: #is the item in the app?
                    originality_sing_grade_item = float(df_originality_sing[item])
                    sum_items = sum_items + originality_sing_grade_item
                    qtd_items = qtd_items + 1
                _app_query_items = _app_query_items.drop(columns=[item])
        if qtd_items > 0:
            grade = sum_items/qtd_items
            if is_grade_rounded:
                grade = round_grade(grade)
        else:
            grade = 0.0
        return grade

    
    def calculate_comb_originality_grade(self, df_app_query_funcionalities: pd.DataFrame,
                                               is_grade_rounded: bool) -> float:
        '''
        Find the rarity of a combination an app's items in a dataframe
        '''
        app_comb_list = self._create_app_comb_list(df_app_query_funcionalities)
        #print(f'{self.__class__.__name__}. Combination Detected: {app_comb_list}')
        total = self.ru.get_size() #self.freq_comb[0].max()
        if app_comb_list == []: #if there is no function in the list, then the grade should be zero
            comb_originality_grade = 0.0
            #print(f' (No function was detected. Combination list is empty.' +
            #      f' (Originality: {comb_originality_grade:.2f} /10)')
        else:
            comb_count = self.find_comb_count(app_comb_list)
            #print(f' ({self.__class__.__name__}. Combination Count: {comb_count:.2f} / {total}')
            if comb_count > 0.0:
                comb_originality_grade = self.calculate_comb_rarity(comb_count)
                if is_grade_rounded:
                    comb_originality_grade = round_grade(comb_originality_grade)
            else:
                comb_originality_grade = 10.0
            #print(f' ({self.__class__.__name__}. Combination Originality: {comb_originality_grade:.2f} /10)')
        return comb_originality_grade

    def calculate_comb_rarity(self, comb_count) -> float:
        # Opção 1: cálculo da nota usando a frequência
        '''
        total = self.ru.get_size() #self.freq_comb[0].max()
        comb_freq = comb_count/total * 100 
        comb_rarity = (100 - comb_freq)/10

        
        #Opção 2: Cálculo da nota usando a transformação de log base 10 e normalização na escala 0-10

        comb_count_log_10 = math.log10(comb_count)
        print(f' (Count log: {comb_count_log_10}')
        comb_count_log_normalized = self.normalize(comb_count_log_10, 
                                                    math.log10(self.ru.get_max_comb()),
                                                    math.log10(self.ru.get_min_comb()))
        print(f' (Count log normalized: {comb_count_log_normalized}')
        comb_rarity = (1 - comb_count_log_normalized) * 10


        #Opção 3: Cálculo da nota usando a transformação de log base na ordem de magnitude do universo de referência 

        order_of_magnitude_RU_comb = self.order_of_magnitude(self.ru.get_size())
        comb_count_log_order_mag = math.log(comb_count, order_of_magnitude_RU_comb)
        comb_rarity = 10 - comb_count_log_order_mag
        '''
        #Opção 4: Cálculo da nota usando a transformação de log base size RU**1/10, i.e.:
        # 10 - math.log(1, 107151**(1/10)) = 10
        # https://math.stackexchange.com/questions/31338/how-do-i-find-the-base-when-log-is-given
        base_log = self.ru.get_size()
        comb_count_log_size = math.log(comb_count, base_log)*10
        comb_rarity = 10 - comb_count_log_size
        return comb_rarity

    def _create_app_comb_list(self, df_app_query_funcionalities) -> list:
        '''
        Returns a list containing all items detected. Useful for facilitating computation
        '''
        app_comb_list = []
        for column in df_app_query_funcionalities:
            if True in df_app_query_funcionalities[column].values:
                app_comb_list.append(column)
        return app_comb_list

    def find_comb_count(self, app_comb_list) -> int:
        '''
        Finds the combination rarity of an app item combination list and returns a scalar.
        '''
        df_final = self.freq_comb.copy()
        if not df_final.empty:
            for column in df_final:
                if column not in app_comb_list and column != 0:
                    df_final = df_final[df_final[column] == False]
                elif column != 0:
                    df_final = df_final[df_final[column] == True]
            try: 
                if int(df_final[0]) > 0: #there is a least one such combination in the RU
                    return int(df_final[0])
                else:
                    return 0  #returns zero since the combination doesn't exist in the RU
            except Exception as e:
                return 0
        else:
            return 0
    