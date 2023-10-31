from typing import Tuple
import pandas as pd

from creassessment.controler.constants import BLOCKS_COMPONENTS_CATEGORIES, BUILT_IN_BLOCKS_CATEGORIES, FLEXIBILITY_PROGRAMMING_PREFIX
from creassessment.grader.creativity.flexibility.flexibility_grader import Flexibility_Grader

class Flexibility_Programming(Flexibility_Grader):

    def __init__(self) -> None:
        super().__init__()
        self.max_flexibility = len(BUILT_IN_BLOCKS_CATEGORIES) + len(BLOCKS_COMPONENTS_CATEGORIES) + 1

    def analyze_flexibility(self, app_query_categories_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        super().analyze_flexibility(app_query_categories_df, is_grade_rounded)
        app_query_categories_grade = app_query_categories_df.copy()
        for category in app_query_categories_df:
            removed_spaces_category = category.replace(' ', '_')
            removed_trademark = removed_spaces_category.replace('®', '') #for LEGO®_MINDSTORMS® categories
            app_query_categories_grade.rename(columns={category: FLEXIBILITY_PROGRAMMING_PREFIX + removed_trademark}, inplace=True)
        return self.grade, app_query_categories_grade