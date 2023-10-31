from creassessment.grader.creativity.reference_universes.fluency.reference_universe_programming import Reference_Universe_Programming

class Reference_Universe_Programming_99993_apps(Reference_Universe_Programming):

    def __init__(self):
        self._set_freq_ru()

    def _set_freq_ru(self, excel_path_ref_un = None) -> None:
        self.size = 99993
        self.freq_sing = self.get_freq_sing()

    def get_freq_sing(self) -> dict:
        '''
        Raw frequency for programming blocks based on 99993 apps
        '''
        return {0: 5,
                2: 10,
                5: 15,
                8: 20,
                11: 25, # Q1
                15: 30,
                21: 35,
                27: 40,
                33: 45,
                39: 50, # Median
                48: 55,
                57: 60,
                69: 65,
                84: 70,
                104: 75, # Q3
                134: 80,
                178: 85,
                259: 90,
                462: 95,
                650: 100 #Kaufman suggestion
                }