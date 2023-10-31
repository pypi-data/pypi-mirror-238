from typing import Tuple
import pandas as pd

from creassessment.utils.creassess_utils import rescale_to_0_10_scale, round_grade

class Flexibility_Grader:
    max_flexibility: int
    grade: float

    def __init__(self):
        self.grade = 0

    def analyze_flexibility(self, app_query_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        self.grade = 0
        for category in app_query_df:
            if app_query_df[category][0]:
                self.grade += 1
        self.grade = rescale_to_0_10_scale(self.grade, self.max_flexibility)
        if is_grade_rounded:
            self.grade = round_grade(self.grade)
        return self.grade, app_query_df
