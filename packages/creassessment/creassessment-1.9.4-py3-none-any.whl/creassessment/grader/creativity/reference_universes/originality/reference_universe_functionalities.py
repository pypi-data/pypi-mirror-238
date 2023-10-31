import pandas as pd

from creassessment.grader.creativity.reference_universes.reference_universe import Reference_Universe
from creassessment.controler.constants import INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_FILE_PATH

class Reference_Universe_Functionalities(Reference_Universe):

    def __init__(self, excel_path_ref_un):
        super().__init__(excel_path_ref_un)
    
    def _calc_freq_sing(self, df_ref_un) -> dict:
        '''
        Calculate frequency for singular funcionalities considering a reference universe
        '''
        df_numeric = df_ref_un.copy()
        df_numeric.loc['True'] = int(1)
        df_numeric.loc['False'] = int(0)
        _, dict_freq = super()._calc_freq_sing(df_numeric)
        return dict_freq

    def _calc_avg_sing(self, df_ref_un: pd.DataFrame) -> pd.DataFrame:
        '''
        Returns a dataframe and a dict containing all components' frequency
            (based on sum: 1=True, 0=False)
        '''
        df_numeric = df_ref_un.copy()
        df_numeric.loc['True'] = int(1)
        df_numeric.loc['False'] = int(0)
        _, dict_freq = super()._calc_avg_sing(df_numeric)
        return dict_freq

    def _calc_freq_comb(self, df_ref_un) -> pd.DataFrame:
        '''
        Returns a DF containing all combined components' frequency on column '0'
            based on sum: 1=True, 0=False
        '''
        df_features_only = df_ref_un.drop(labels=[INDEX_NAME_FOR_FILE_PATH,
                                                  INDEX_NAME_FOR_FILE_NAME,
                                                  INDEX_NAME_FOR_APP_NAME], axis=1)
        df_comb = super()._calc_freq_comb(df_features_only)
        return df_comb

    def _select_rows_df_ru(self) -> pd.DataFrame:
        '''
        Select specific rows from a data extraction of apps. 
        E.g., only rows which detection of functionalities is True.
        '''
        df_ru_filtered = self.df_ru.copy()
        self.apps_with_nothing_detected = 0
        for index, row in self.df_ru.iterrows():
            app_detection_list = [col for col in row if col == True]
            if len(app_detection_list) == 0:
                self.apps_with_nothing_detected = self.apps_with_nothing_detected + 1
                print(f"Drop {index}", end = "\t")
                df_ru_filtered = df_ru_filtered.drop(index)
        print(f"Dropped {self.apps_with_nothing_detected} with no detection")
        return df_ru_filtered