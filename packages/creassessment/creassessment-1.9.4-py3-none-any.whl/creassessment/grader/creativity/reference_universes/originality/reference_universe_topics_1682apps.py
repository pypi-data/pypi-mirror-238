from creassessment.grader.creativity.reference_universes.originality.reference_universe_topic import Reference_Universe_Topic

class Reference_Universe_Topics_1682_apps(Reference_Universe_Topic):

    def __init__(self):
        super().__init__(self)

    def _set_freq_ru(self, excel_path_ref_un = ''):
        self.size = 1682
        self.freq_sing = self.get_freq_sing()
    
    def get_freq_sing(self):
        '''
        Raw frequency for topics based on 1682 apps
        '''
        return {'Math': 13.0, 
                'Healthy life and sport': 10.5,
                'Communication': 8.5,
                'Tourism, geography, weather and meteorology': 7.0,
                'Food and drinks': 6.0,
                'Finance and work': 5.5,
                'Education': 5.5,
                'Spirituality, belief and fortune telling': 5.5,
                'Robotics, physical computing and automation': 5.0,
                'Music': 4.5,
                'Engineering, physics and construction': 4.0,
                'Productivity': 4.0,
                'Entertainment': 3.5,
                'Mobile tools': 3.0,
                'Environment and botany': 2.5,
                'Design, painting and photography': 2.5,
                'Cars, vehicles and transport': 2.5,
                'Animals and pets': 2.5,
                'Medicine and health': 2.0,
                'Citizenship and social issues': 2.0,
                'Beauty and fashion': 1.0}
    

        



    