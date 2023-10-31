import pandas as pd

from creassessment.grader.creativity.reference_universes.reference_universe import Reference_Universe
from creassessment.controler.constants import INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_FILE_PATH, UI_COMPONENTS

class Reference_Universe_UI_Components(Reference_Universe):

    def __init__(self, excel_path_ref_un):
        super().__init__(excel_path_ref_un)
    
    def _calc_freq_sing(self, df_ref_un) -> dict:
        '''
        Calculate frequency for singular funcionalities considering a reference universe
        '''
        _, dict_freq = super()._calc_freq_sing(df_ref_un)
        return dict_freq
    

    def _select_columns_df_ru(self) -> pd.DataFrame:
        '''
        Selects specific columns. Util for resolve UnicodeEncodeError when exporting to xls, txt, etc.
        '''
        index_columns = [INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_APP_NAME]
        df_columns_selection = self.df_ru[self.df_ru.columns[self.df_ru.columns.isin(index_columns + UI_COMPONENTS)]]
        return df_columns_selection.copy()

    def _select_rows_df_ru(self):
        '''
        Select specific rows from a data extraction of apps. 
        '''
        df_ru_filtered = self.df_ru.copy()
        df_ru_filtered = df_ru_filtered.fillna(0)
        self.apps_with_nothing_detected = 0
        for index, row in self.df_ru.iterrows():
            app_detection_list = []
            for col, value in row.items():
                if col in UI_COMPONENTS:
                    if value > 0:
                        app_detection_list.append(col)
                        break
            if len(app_detection_list) == 0:
                self.apps_with_nothing_detected = self.apps_with_nothing_detected + 1
                print(f"Drop {index}", end = "\t")
                df_ru_filtered = df_ru_filtered.drop(index)
        print(f"Dropped {self.apps_with_nothing_detected} with no detection")
        return df_ru_filtered
    
    def _calc_avg_sing(self, df_ref_un):
        '''
        Returns a dataframe and a dict containing all components' frequency
            (based on sum: 1=True, 0=False)
        '''
        _, dict_freq = super()._calc_avg_sing(df_ref_un.copy().fillna(0))
        return dict_freq

    def _calc_freq_comb(self, df_ref_un) -> pd.DataFrame:
        '''
        Returns a DF containing all combined components' frequency on column '0'
            based on sum: 1=True, 0=False
        '''
        df_features_only = df_ref_un.drop(labels=[INDEX_NAME_FOR_FILE_PATH, 
                                                  INDEX_NAME_FOR_FILE_NAME,
                                                  INDEX_NAME_FOR_APP_NAME], axis=1)
        df_features_only[df_features_only > 0 ] = True
        df_features_only[df_features_only.isna()] = False
        df_comb = super()._calc_freq_comb(df_features_only)
        return df_comb