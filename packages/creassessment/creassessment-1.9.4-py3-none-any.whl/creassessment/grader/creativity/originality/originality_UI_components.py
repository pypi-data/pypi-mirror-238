import pandas as pd

from creassessment.grader.creativity.originality.originality_grader import Originality_Grader
from creassessment.grader.creativity.reference_universes.originality.reference_universe_UI_components_102567apps import Reference_Universe_UI_components_102567_apps
from creassessment.grader.creativity.reference_universes.originality.reference_universe_UI_components import Reference_Universe_UI_Components
from creassessment.controler.constants import INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_FILE_PATH, UI_COMPONENTS

class Originality_UI_Components(Originality_Grader):

    ru: Reference_Universe_UI_Components

    def __init__(self, ru: Reference_Universe_UI_Components = Reference_Universe_UI_components_102567_apps()):
        super().__init__(ru)

    def _select_columns_df_app_query_items(self, df_app_query_items: pd.DataFrame) -> pd.DataFrame:
        '''
        Select specific columns from a data extraction of apps. Better implemented in subclasses.
        '''
        index_columns = [INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_APP_NAME]
        df_columns_selection = df_app_query_items[df_app_query_items.columns[df_app_query_items.columns.isin(index_columns + UI_COMPONENTS)]]
        return df_columns_selection.copy()
    
    def _create_app_comb_list(self, df_app_query_funcionalities) -> list:
        '''
        Returns a list containing all items detected. Useful for facilitating computation
        '''
        app_comb_list = []
        for column in df_app_query_funcionalities:
            if df_app_query_funcionalities[column].values > 0:
                app_comb_list.append(column)
        return app_comb_list

    def calculate_sing_originality_grade(self, df_app_query_items: pd.DataFrame,
                                         df_originality_sing: pd.DataFrame,
                                         is_grade_rounded: bool) -> float:
        df_filtered_app_query_items = df_app_query_items[df_app_query_items.columns[df_app_query_items.columns.isin(UI_COMPONENTS)]]
        df_originality_sing = df_originality_sing[df_originality_sing.columns[df_originality_sing.columns.isin(UI_COMPONENTS)]]
        grade = super().calculate_sing_originality_grade(df_filtered_app_query_items, df_originality_sing, is_grade_rounded)
        return grade