from creassessment.grader.creativity.fluency.fluency_grader import Fluency_Grader
from creassessment.grader.creativity.reference_universes.fluency.reference_universe_components import Reference_Universe_Components
from creassessment.grader.creativity.reference_universes.fluency.reference_universe_components_99993apps import Reference_Universe_Components_99993_apps

class Fluency_Components(Fluency_Grader):
    ru: Reference_Universe_Components

    def __init__(self, ru: Reference_Universe_Components = Reference_Universe_Components_99993_apps()):
        self.fluency_value = 0
        self.ru = ru
