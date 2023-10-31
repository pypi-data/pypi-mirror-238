from creassessment.grader.creativity.reference_universes.fluency.reference_universe_components import Reference_Universe_Components

class Reference_Universe_Components_99993_apps(Reference_Universe_Components):

    def __init__(self):
        self._set_freq_ru()
        
    def _set_freq_ru(self, excel_path_ref_un = None) -> None:
        self.size = 99993
        self.freq_sing = self.get_freq_sing()
    
    def get_freq_sing(self) -> dict:
        '''
        Raw frequency for components based on 99993 apps
        '''
        return {2: 5,
                3: 10,
                4: 15,
                5: 20,
                6: 25, # Q1
                7: 30,
                8: 35,
                9: 40,
                10: 45,
                12: 50, # Median
                13: 55,
                15: 60,
                17: 65,
                20: 70,
                24: 75, # Q3
                30: 80,
                39: 85,
                54: 90,
                89: 95,
                115: 100 #Kaufman suggestion
                }