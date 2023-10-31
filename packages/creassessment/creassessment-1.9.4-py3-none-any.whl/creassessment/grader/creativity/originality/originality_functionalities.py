from creassessment.grader.creativity.originality.originality_grader import Originality_Grader
from creassessment.grader.creativity.reference_universes.originality.reference_universe_functionalities import Reference_Universe_Functionalities
from creassessment.grader.creativity.reference_universes.originality.reference_universe_functionalities_98770apps import Reference_Universe_Functionalities_98770_apps


class Originality_Functionalities(Originality_Grader):

    ru: Reference_Universe_Functionalities

    def __init__(self, ru: Reference_Universe_Functionalities = Reference_Universe_Functionalities_98770_apps()):
        super().__init__(ru)
