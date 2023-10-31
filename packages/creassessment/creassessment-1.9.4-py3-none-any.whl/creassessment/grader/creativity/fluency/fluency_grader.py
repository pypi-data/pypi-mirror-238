from typing import Tuple
import pandas as pd

from creassessment.grader.creativity.reference_universes.reference_universe import Reference_Universe

class Fluency_Grader:
    fluency_value: int
    ru: Reference_Universe

    def __init__(self, ru: Reference_Universe):
        self.fluency_value = 0
        self.ru = ru

    def analyze_fluency(self, app_query_scope_freq_df: pd.DataFrame, col_fluency: str) -> Tuple[float, float]:
        if not app_query_scope_freq_df.empty:
            self.fluency_value = int(app_query_scope_freq_df[col_fluency].values)
        return self.grade_norms(), self.fluency_value
    
    def grade_norms(self) -> float:
        grade = 0.0
        for number_of_comp, freq in self.ru.get_freq_sing().items():
            if self.fluency_value >= number_of_comp and self.fluency_value > 0:
                grade = freq/10
        return grade