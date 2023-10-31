import os
from typing import Tuple
import pandas as pd
import numpy as np

from creassessment.controler.constants import INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME

class Reference_Universe:
    size: int

    df_ru: pd.DataFrame

    freq_sing: dict
    avg_sing: dict
    freq_comb: pd.DataFrame
    
    max_comb: int
    min_comb: int

    #stats
    apps_with_nothing_detected: int #number of projects that do not contain any feature (e.g. UI components, functionality, etc.)
    size_without_duplicates: int


    def __init__(self, excel_path_ref_un):
        if excel_path_ref_un != '':
            self._set_freq_ru(excel_path_ref_un)
            self._set_min_max_comb()
            self.apps_with_nothing_detected = -1
            #print(f"==> Created {self.__class__.__name__} with {self.size} apps\n"
            #    + f"==> Combinations: [MAX: {self.max_comb}, "
            #    + f" MIN: {self.min_comb}]")
        else:
            print("Reference_Universe.__init__: Not using excel file (empty path)")
    
    def get_freq_sing(self) -> dict:
        return self.freq_sing
    
    def get_avg_sing(self) -> dict:
        return self.avg_sing

    def get_freq_comb(self) -> pd.DataFrame:
        return self.freq_comb
    
    def get_size(self) -> int:
        return self.size

    def get_max_comb(self) -> int:
        return self.max_comb
    
    def get_min_comb(self) -> int:
        return self.min_comb

    def _set_min_max_comb(self):
        try:
            self.max_comb = self.freq_comb[0].max()
            self.min_comb = self.freq_comb[0].min()
        except:
            self.max_comb = 0
            self.min_comb = 0
            #print("Reference_Universe._set_min_max: error in setting max_comb and min_comb")

    def _set_freq_ru(self, excel_path_ref_un = '') -> None:
        '''
        Set frequencies (singular and combined) based on a reference universe.
        '''
        self.freq_sing = {}
        self.avg_sing = {}
        self.freq_comb = pd.DataFrame()
        self.size = 0
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
                self.df_ru = self._select_columns_df_ru()
                self.df_ru = self._select_rows_df_ru()
                self.size = len(self.df_ru)
                self.freq_sing = self._calc_freq_sing(self.df_ru)
                self.avg_sing = self._calc_avg_sing(self.df_ru)
                self.freq_comb = self._calc_freq_comb(self.df_ru)
        else:
            print("Reference_Universe.set_freq_ru: Not using excel file (empty path)")

    def _select_columns_df_ru(self):
        '''
        Select specific columns from a data extraction of apps. Better implemented in subclasses.
        '''
        return self.df_ru
    
    def _select_rows_df_ru(self):
        '''
        Select specific rows from a data extraction of apps. Better implemented in subclasses.
        '''
        return self.df_ru

    def _calc_freq_sing(self, df_numeric: pd.DataFrame = None) -> Tuple[pd.DataFrame, dict]:
        '''
        Calculate singular prevalence considering a reference universe
            frequency / prevalence for qualitative. e.g.: contains functionality
        '''
        df_numeric = df_numeric.select_dtypes(include=np.number).copy()
        df_numeric[df_numeric > 0] = 1
        df_freq = pd.DataFrame(df_numeric.sum(numeric_only=True)) 
        df_freq = df_freq.rename(columns={0: "Número de ocorrências"})
        df_freq['Frequência'] = round((df_freq['Número de ocorrências']/len(df_numeric)*100).astype(float),2)
        df_freq = df_freq.sort_values(by=['Número de ocorrências'], ascending=False)
        df_freq.drop(columns=['Número de ocorrências'])
        dict_freq = df_freq.to_dict()['Frequência']
        return df_freq, dict_freq
    
    def _calc_avg_sing(self, df_numeric: pd.DataFrame) -> Tuple[pd.DataFrame, dict]:
        '''
        Returns a dataframe and a dict containing all components' average
            frequency / average for quantitative. e.g.: UI components quantity
        '''
        df_numeric = df_numeric.select_dtypes(include=np.number).copy()
        df_freq = pd.DataFrame(df_numeric.sum()) 
        df_freq = df_freq.rename(columns={0: "Número de ocorrências"})
        df_freq['Frequência MÉDIA'] = round((df_freq['Número de ocorrências']/len(df_numeric)).astype(float),2)
        df_freq = df_freq.sort_values(by=['Número de ocorrências'], ascending=False)
        df_freq.drop(columns=['Número de ocorrências'])
        dict_freq = df_freq.to_dict()['Frequência MÉDIA']
        return df_freq, dict_freq

    def _calc_freq_comb(self, df_features_only: pd.DataFrame) -> pd.DataFrame:
        '''
        Returns a DF containing all combined components' frequency on column '0'
            based on sum: 1=True, 0=False
        '''
        d = df_features_only.value_counts()
        df_comb = pd.DataFrame(d)
        df_comb = df_comb.reset_index()
        return df_comb

    def to_txt(self):
        '''
        Saves the frequencies (singular and combined) of the RU 
            in a txt file using dict notation, so it can be ctrl-v 
            in a well-defined RU
        '''
        print('[Reference_Universe.to_txt] Writing .txt files...')
        with open(f'freq_sing_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(str(self.get_freq_sing()))
        with open(f'avg_sing_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(str(self.get_avg_sing()))
        freq_comb_functionalities_dict = self.get_freq_comb().to_dict()
        with open(f'freq_comb_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(str(freq_comb_functionalities_dict))
        with open(f'stats_{self.__class__.__name__}_{self.size}apps.txt', 'w') as f:
            f.write(f"Size without duplicates: {self.size_without_duplicates}\n" \
                    f"Apps with nothing detected: {self.apps_with_nothing_detected} de {self.size_without_duplicates}")

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
        pd.DataFrame.from_dict([self.get_avg_sing()]).reset_index().to_excel(dir_prefix+f'avg_sing'+files_suffix)
        self.freq_comb.to_excel(dir_prefix+f'freq_comb'+files_suffix)
        pd.DataFrame.from_dict(self.freq_comb_grouped().to_excel(dir_prefix+f'freq_comb_grouped'+files_suffix))
        self.df_ru.to_excel(dir_prefix+f'df_ru{self.size}'+files_suffix)

    def freq_comb_grouped(self) -> pd.DataFrame:
        '''
        Return a pd.Dataframe with combinations in the first column and frequency in the second column
        '''
        dict_comb = {}
        df_combi = self.freq_comb
        for i in range(0, len(self.freq_comb)):
            list_key = []
            for c in df_combi:
                if df_combi.at[i, c] and c != 0: #0 é o "nome" da coluna do nro de comb
                    list_key.append(c)
            tup_key = tuple(list_key)
            value = df_combi.at[i, 0]
            dict_comb[tup_key] = value
        df_comb_simple = pd.DataFrame.from_dict(dict_comb, orient='index')
        return df_comb_simple