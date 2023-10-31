import ast
from typing import Tuple
import pandas as pd
#import nltk - 18/04/23 -> commented for integrating it into CodeMaster

from creassessment.grader.creativity.reference_universes.reference_universe import Reference_Universe
from creassessment.controler.constants import DF_COL_PARSER_TAGS, INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME

class Reference_Universe_Tags(Reference_Universe):
    ''' 
    This RU is a vector, i.e., 0+ tags can be identified.
    However, there is no avg_sing nor freq_comb, but only freq_sing.
    '''
    biggest_tag_frequency: int # used to grade the originality (as opposed to using the apps number)

    def __init__(self, excel_path_ref_un):
        self.biggest_tag_frequency = 0
        if excel_path_ref_un != '':
            self._set_freq_ru(excel_path_ref_un)
        else:
            print(f"{self.__class__.__name__}.__init__: Not using excel file (empty path)")

    def _set_freq_ru(self, excel_path_ref_un = '') -> None:
        '''
        Set frequencies (singular and combined) based on a reference universe.
        '''
        self.freq_sing = {}
        if excel_path_ref_un:
            try:
                print('Reading file (this may take a while): ' + excel_path_ref_un)
                self.df_ru = pd.read_excel(excel_path_ref_un)
            except Exception as e:
                print('Problem opening file ' + excel_path_ref_un)
                print(e)
            else:
                self.df_ru = self.df_ru.drop_duplicates(subset=[INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_APP_NAME])
                self.size_without_duplicates = len(self.df_ru)
                self.size = len(self.df_ru)
                self.freq_sing, self.freq_sing_df = self._calc_freq_sing(self.df_ru)
        else:
            print(f"{self.__class__.__name__}.set_freq_ru: Not using excel file (empty path)")

    #def _calc_freq_sing(self, df_ref_un: pd.DataFrame): # 18/04/23 -> commented for integrating it into CodeMaster
    #    '''
    #    Calculate frequency for tags considering a reference universe
    #    '''
    #    try:
    #        all_keywords_list = []
    #        for ind in df_ref_un.index:
    #            keywords_app = df_ref_un.at[ind, DF_COL_PARSER_TAGS]
    #            if keywords_app != 'Not identified':
    #                keywords = ast.literal_eval(df_ref_un.at[ind, DF_COL_PARSER_TAGS])
    #                for keyword in keywords:
    #                    all_keywords_list.append(keyword)
    #        
    #        keyword_frequency_dict = nltk.FreqDist(all_keywords_list)
    #        keyword_frequency_df = pd.DataFrame(keyword_frequency_dict.items(), columns=['word', 'frequency'])
    #        keyword_frequency_df = keyword_frequency_df.sort_values(by='frequency', ascending=False)
    #        keyword_frequency_df = keyword_frequency_df.set_index('word')
    #        keyword_frequency_dict = keyword_frequency_df.to_dict()
    #        return keyword_frequency_dict, keyword_frequency_df
    #    except Exception as e:
    #        print(e)
     #   return 0, 0

    def _calc_avg_sing(self, df_ref_un) -> tuple:
        pass

    def _calc_freq_comb(self, df_ref_un) -> pd.DataFrame:
        pass

    def to_txt(self):
        '''
        Saves the frequencies (singular) of the RU 
            in a txt file using dict notation, so it can be ctrl-v 
            in a well-defined RU
        '''
        print(f'[{self.__class__.__name__}.to_txt] Writing .txt files...')
        with open(f'freq_sing_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(str(self.get_freq_sing()))