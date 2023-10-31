from typing import Tuple
import pandas as pd

from creassessment.grader.creativity.flexibility.flexibility_grader import Flexibility_Grader
from creassessment.controler.constants import COMPONENTS_CATEGORIES, FLEXIBILITY_COMPONENTS_PREFIX

class Flexibility_Components(Flexibility_Grader):

    def __init__(self) -> None:
        super().__init__()
        self.max_flexibility = len(COMPONENTS_CATEGORIES)

    def analyze_flexibility(self, app_query_categories_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        super().analyze_flexibility(app_query_categories_df, is_grade_rounded)
        app_query_categories_grade = app_query_categories_df.copy()
        for category in app_query_categories_df:
            removed_spaces_categories = category.replace(' ', '_')
            removed_trademark = removed_spaces_categories.replace('®', '') #for LEGO®_MINDSTORMS® categories
            app_query_categories_grade.rename(columns={category: FLEXIBILITY_COMPONENTS_PREFIX + removed_trademark}, inplace=True)
        return self.grade, app_query_categories_grade