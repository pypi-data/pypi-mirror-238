import os
import pandas as pd

from creassessment.grader.creativity.reference_universes.reference_universe import Reference_Universe
from creassessment.controler.constants import RU_COLUMN_TOPIC_TEXT, RU_COLUMN_TOPIC_NUMERIC
from creassessment.utils.creassess_utils import round_grade

class Reference_Universe_Topic(Reference_Universe):
    ''' 
    This RU is a scalar, i.e., only one topic is identified and its probability.
    Thus, there is no avg_sing nor freq_comb, but only freq_sing.
    '''

    def __init__(self, excel_path_ref_un):
        super().__init__(excel_path_ref_un)
    
    def _calc_freq_sing(self, df_ref_un: pd.DataFrame) -> dict:
        '''
        Calculate frequency for topics considering a reference universe
        '''
        dict_freq = df_ref_un.groupby(RU_COLUMN_TOPIC_TEXT).topicoID.value_counts()
        dict_freq.index = dict_freq.index.droplevel(1)
        dict_freq = dict_freq.sort_values(ascending=False)
        dict_freq = dict_freq/len(df_ref_un)*100
        dict_freq = dict_freq.apply(round_grade)
        dict_freq = dict_freq.to_dict()
        return dict_freq

    def _calc_avg_sing(self, df_ref_un) -> tuple:
        pass

    def _calc_freq_comb(self, df_ref_un) -> pd.DataFrame:
        pass
    
    def to_txt(self):
        '''
        Saves the frequencies (singular and combined) of the RU 
            in a txt file using dict notation, so it can be ctrl-v 
            in a well-defined RU
        '''
        print('[Reference_Universe.to_txt] Writing .txt files...')
        with open(f'freq_sing_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(str(self.get_freq_sing()))

    def to_xls(self):
        '''
        Saves the frequencies (singular and combined) of the RU 
            in xls files
        '''
        print('[Reference_Universe.to_xls] Writing .xlsx files...')
        dir_prefix = 'reference_universe_xls_files/'
        if not os.path.exists(dir_prefix):
            os.mkdir(dir_prefix)
        files_suffix = f'_{self.__class__.__name__}_{self.size}apps.xlsx'
        pd.DataFrame.from_dict([self.get_freq_sing()]).reset_index().to_excel(dir_prefix+f'freq_sing'+files_suffix)
        self.df_ru.to_excel(dir_prefix+f'df_ru{self.size}'+files_suffix)
