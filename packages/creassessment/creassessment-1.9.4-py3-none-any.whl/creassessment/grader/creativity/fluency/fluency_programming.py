from creassessment.grader.creativity.fluency.fluency_grader import Fluency_Grader
from creassessment.grader.creativity.reference_universes.fluency.reference_universe_programming import Reference_Universe_Programming
from creassessment.grader.creativity.reference_universes.fluency.reference_universe_programming_99993apps import Reference_Universe_Programming_99993_apps

class Fluency_Programming(Fluency_Grader):
    ru: Reference_Universe_Programming

    def __init__(self, ru: Reference_Universe_Programming = Reference_Universe_Programming_99993_apps()):
        self.fluency_value = 0
        self.ru = ru