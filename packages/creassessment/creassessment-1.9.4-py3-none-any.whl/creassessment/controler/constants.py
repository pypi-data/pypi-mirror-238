# Indexes
INDEX_NAME_FOR_FILE_PATH = 'File path'
INDEX_NAME_FOR_FILE_NAME = 'File name'
INDEX_NAME_FOR_APP_NAME = 'App name'
INDEX_NAME_FOR_SCREEN_NAME = 'Screen name'

# Suffixes for dataframes
BLOCKS_SCREEN_SUFIX_IDENTIFIER = 'Blocks'
DESIGNER_SCREEN_SUFIX_IDENTIFIER = 'Designer'

# Column names for constructed data
DF_COL_TEXTUAL_CONTENT = 'textual_content'
DF_COL_PARSER_TOPIC_IDENTIFICATION = 'Topic'
DF_COL_PARSER_TOPIC_PROBABILITY = 'Topic_probability'
DF_COL_PARSER_TAGS = 'Tags'


# Creativity
GRADE_CRIATIVIDADE = 'notaCriatividadeUsuario'


# Originality - Functionality
ORIGINALITY_FUNCTIONALITY = 'originality_Functionality_'
GRADE_ORIGINALITY_SING_FUNC = ORIGINALITY_FUNCTIONALITY + 'GradeOriginalitySingularFunctionalities'
GRADE_ORIGINALITY_COMB_FUNC = ORIGINALITY_FUNCTIONALITY + 'GradeOriginalityCombinedFunctionalities'
GRADE_ORIGINALITY_FUNC = ORIGINALITY_FUNCTIONALITY + 'GradeOriginalityFunctionality'

PREFIX_ORIGINALITY_SINGRADE_FUNCTIONALITY = ORIGINALITY_FUNCTIONALITY + "SingGrade_"
PREFIX_ORIGINALITY_DETECTION_FUNCTIONALITY = ORIGINALITY_FUNCTIONALITY + "Detection_"
#PREFIX_ORIGINALITY_FUNCTIONALITY_FREQUENCY = "originality_SingFreq_Functionality_" # not used


# Originality - UI Components
ORIGINALITY_UI_COMPONENTS = 'originality_UI_Components_'
GRADE_ORIGINALITY_SING_UI_COMPONENTS = ORIGINALITY_UI_COMPONENTS + 'GradeOriginalitySingularUIComponents'
GRADE_ORIGINALITY_COMB_UI_COMPONENTS = ORIGINALITY_UI_COMPONENTS + 'GradeOriginalityCombinedUIComponents'
GRADE_ORIGINALITY_UI_COMPONENTS = ORIGINALITY_UI_COMPONENTS + 'GradeOriginalityUIComponents'

PREFIX_ORIGINALITY_SINGGRADE_UI_COMPONENTS = ORIGINALITY_UI_COMPONENTS + "SingGrade_"
PREFIX_ORIGINALITY_DETECTION_UI_COMPONENTS = ORIGINALITY_UI_COMPONENTS + "Detection_"


UI_COMPONENTS = ["Button", "CheckBox", "DatePicker", "Image", "BackgroundImage", "Label", "ListPicker", "ListView", "Notifier", "PasswordTextBox", "Slider", "Spinner", "Switch", "TextBox", "TimePicker", "WebViewer", "ImagePicker", "VideoPlayer", "Map", "ContactPicker", "EmailPicker", "PhoneNumberPicker"]


# Flexibility & Fluency - Components [12 components]
COMPONENTS_CATEGORIES = {
    'User Interface':           ['Button', 'CheckBox', 'DatePicker', 'Image', 'Label', 'ListPicker',
                                'ListView', 'Notifier', 'PasswordTextBox', 'Slider', 'Spinner',
                                'Switch', 'TextBox', 'TimePicker', 'WebViewer'],
    'Layout':                   ['HorizontalArrangement', 'HorizontalScrollArrangement', 'TableArrangement',
                                'VerticalArrangement', 'VerticalScrollArrangement'],
    'Media':                    ['Camcorder', 'Camera', 'ImagePicker', 'Player', 'Sound', 'SoundRecorder', 
                                'SoundRecorder', 'TextToSpeech', 'Translator', 'VideoPlayer'],
    'Drawing and Animation':    ['Ball', 'Canvas', 'ImageSprite'],
    'Maps':                     ['Circle', 'FeatureCollection', 'LineString', 'Map', 'Marker', 'Navigation',
                                'Polygon', 'Rectangle'],
    'Charts':                   ['Chart', 'ChartData2D'],
    'Sensors':                  ['AccelerometerSensor', 'BarcodeScanner', 'Barometer', 'Clock', 
                                'GyroscopeSensor', 'Hygrometer', 'LightSensor', 'LocationSensor',
                                'MagneticFieldSensor', 'NearField', 'OrientationSensor', 'Pedometer',
                                'ProximitySensor', 'Thermometer'],
    'Social':                   ['ContactPicker', 'EmailPicker', 'PhoneCall', 'PhoneNumberPicker', 'Sharing',
                                'Texting', 'Twitter'],
    'Storage':                  ['CloudDB', 'DataFile', 'File', 'Spreadsheet', 'TinyDB', 'TinyWebDB'],
    'Connectivity':             ['ActivityStarter', 'BluetoothClient', 'BluetoothServer', 'Serial', 'Web'],
    'LEGO® MINDSTORMS®':        ['NxtDrive', 'NxtColorSensor', 'NxtLightSensor', 'NxtSoundSensor',
                                'NxtTouchSensor', 'NxtUltrasonicSensor', 'NxtDirectCommands', 'Ev3Motors',
                                'Ev3ColorSensor', 'Ev3GyroSensor', 'Ev3TouchSensor', 'Ev3UltrasonicSensor',
                                'Ev3Sound', 'Ev3UI', 'Ev3Commands'],
    'Experimental':             ['FirebaseDB']
    }


# Flexibility & Fluency - Blocks
#  Blocks categories = built-in blocks [9 categories] + components blocks [14 categories]
BUILT_IN_BLOCKS_CATEGORIES_KEYWORDS = {
    'Control':      ['controls'],
    'Logic':        ['logic'],
    'Math':         ['math'],
    'Text':         ['text'],
    'Lists':        ['lists'],
    'Dictionaries': ['dictionaries', 'pair'],
    'Colors':       ['color'],
    'Variables':    ['declaration', 'variable'],
    'Procedures':   ['procedures']
}

BUILT_IN_BLOCKS_CATEGORIES = {
    'Control':      ['controls_break', 'controls_choose', 'controls_closeApplication', 'controls_closeScreen', 'controls_closeScreenWithPlainText', 'controls_closeScreenWithValue', 'controls_do_then_return', 'controls_eval_but_ignore', 'controls_forEach', 'controls_forRange', 'controls_for_each_dict', 'controls_getPlainStartText', 'controls_getStartValue', 'controls_if', 'controls_openAnotherScreen', 'controls_openAnotherScreenWithStartValue', 'controls_while'],
    'Logic':        ['logic_boolean', 'logic_compare', 'logic_false', 'logic_negate', 'logic_operation', 'logic_or'],
    'Math':         ['math_abs', 'math_add', 'math_atan2', 'math_bitwise', 'math_ceiling', 'math_compare', 'math_convert_angles', 'math_convert_number', 'math_cos', 'math_divide', 'math_division', 'math_floor', 'math_format_as_decimal', 'math_is_a_number', 'math_multiply', 'math_neg', 'math_number', 'math_number_radix', 'math_on_list', 'math_power', 'math_random_float', 'math_random_int', 'math_random_set_seed', 'math_round', 'math_single', 'math_subtract', 'math_tan', 'math_trig'],
    'Text':         ['text', 'text_changeCase', 'text_compare', 'text_contains', 'text_isEmpty', 'text_is_string', 'text_join', 'text_length', 'text_replace_all', 'text_replace_mappings', 'text_reverse', 'text_segment', 'text_split', 'text_split_at_spaces', 'text_starts_at', 'text_trim', 'obfuscated_text', 'obsufcated_text'],
    'Lists':        ['lists_add_items', 'lists_append_list', 'lists_copy', 'lists_create_with', 'lists_from_csv_row', 'lists_insert_item', 'lists_is_empty', 'lists_is_in', 'lists_is_list', 'lists_join_with_separator', 'lists_length', 'lists_lookup_in_pairs', 'lists_pick_random_item', 'lists_position_in', 'lists_remove_item', 'lists_replace_item', 'lists_reverse', 'lists_select_item', 'lists_to_csv_row', 'lists_to_csv_table', 'lists_from_csv_table'],
    'Dictionaries': ['dictionaries_alist_to_dict', 'dictionaries_combine_dicts', 'dictionaries_copy', 'dictionaries_create_with', 'dictionaries_delete_pair', 'dictionaries_dict_to_alist', 'dictionaries_get_values', 'dictionaries_getters', 'dictionaries_is_dict', 'dictionaries_is_key_in', 'dictionaries_length', 'dictionaries_lookup', 'dictionaries_recursive_lookup', 'dictionaries_recursive_set', 'dictionaries_set_pair', 'dictionaries_walk_all', 'dictionaries_walk_tree', 'pair'],
    'Colors':       ['color_black', 'color_blue', 'color_cyan', 'color_dark_gray', 'color_gray', 'color_green', 'color_light_gray', 'color_magenta', 'color_make_color', 'color_orange', 'color_pink', 'color_red', 'color_split_color', 'color_white', 'color_yellow'],
    'Variables':    ['global_declaration', 'lexical_variable_get', 'lexical_variable_set', 'local_declaration_expression', 'local_declaration_statement'],
    'Procedures':   ['procedures_callnoreturn', 'procedures_callreturn', 'procedures_defnoreturn', 'procedures_defreturn']
}

BLOCKS_COMPONENTS_CATEGORIES = {
    'User Interface':           ['Button', 'CheckBox', 'DatePicker', 'Image', 'Label', 'ListPicker',
                                'ListView', 'Notifier', 'PasswordTextBox', 'Slider', 'Spinner',
                                'Switch', 'TextBox', 'TimePicker', 'WebViewer'],
    'Layout':                   ['HorizontalArrangement', 'HorizontalScrollArrangement', 'TableArrangement',
                                'VerticalArrangement', 'VerticalScrollArrangement'],
    'Media':                    ['Camcorder', 'Camera', 'ImagePicker', 'Player', 'Sound', 'SoundRecorder', 
                                'SoundRecorder', 'TextToSpeech', 'Translator', 'VideoPlayer', 'SpeechRecognizer', 'YandexTranslate'],
    'Drawing and Animation':    ['Ball', 'Canvas', 'ImageSprite'],
    'Maps':                     ['Circle', 'FeatureCollection', 'LineString', 'Map', 'Marker', 'Navigation',
                                'Polygon', 'Rectangle'],
    'Charts':                   ['Chart', 'ChartData2D'],
    'Sensors':                  ['AccelerometerSensor', 'BarcodeScanner', 'Barometer', 'Clock', 
                                'GyroscopeSensor', 'Hygrometer', 'LightSensor', 'LocationSensor',
                                'MagneticFieldSensor', 'NearField', 'OrientationSensor', 'Pedometer',
                                'ProximitySensor', 'Thermometer'],
    'Social':                   ['ContactPicker', 'EmailPicker', 'PhoneCall', 'PhoneNumberPicker', 'Sharing',
                                'Texting', 'Twitter'],
    'Storage':                  ['CloudDB', 'DataFile', 'File', 'Spreadsheet', 'TinyDB', 'TinyWebDB', 'FusiontablesControl'],
    'Connectivity':             ['ActivityStarter', 'BluetoothClient', 'BluetoothServer', 'Serial', 'Web'],
    'LEGO® MINDSTORMS®':        ['NxtDrive', 'NxtColorSensor', 'NxtLightSensor', 'NxtSoundSensor',
                                'NxtTouchSensor', 'NxtUltrasonicSensor', 'NxtDirectCommands', 'Ev3Motors',
                                'Ev3ColorSensor', 'Ev3GyroSensor', 'Ev3TouchSensor', 'Ev3UltrasonicSensor',
                                'Ev3Sound', 'Ev3UI', 'Ev3Commands'],
    'Experimental':             ['FirebaseDB'],
    'Screen':                   ['Form'],
    'Helpers':                  ['helpers_dropdown', 'helpers_assets', 'helpers_screen_names'],
    }

GENERIC_BLOCKS = {'component_event', 'component_set_get', 'component_component_block', 'component_method'}
COL_EXTENSION = 'Extensions'

# Originality - Topic

ORIGINALITY_TOPIC = 'originality_Topic_'
GRADE_ORIGINALITY_TOPIC = ORIGINALITY_TOPIC + 'GradeOriginalityTopic'

PREFIX_ORIGINALITY_SINGGRADE_TOPIC = ORIGINALITY_TOPIC + "SingGrade_"
PREFIX_ORIGINALITY_DETECTION_TOPIC = ORIGINALITY_TOPIC + "Detection_"


# Originality - Tag
ORIGINALITY_TAG = 'originality_Tag_'
GRADE_ORIGINALITY_TAG = ORIGINALITY_TAG + 'GradeOriginalityTag'

PREFIX_ORIGINALITY_SINGGRADE_TAG = ORIGINALITY_TAG + "SingGrade_"
PREFIX_ORIGINALITY_DETECTION_TAG = ORIGINALITY_TAG + "Detection_"

# Flexibility - Components
FLEXIBILITY_COMPONENTS_PREFIX = 'flexibility_Components_Scope_'
FLEXIBILITY_COMPONENTS = 'flexibility_Components_Scope'

# Flexibility - Blocks
FLEXIBILITY_PROGRAMMING_PREFIX = 'flexibility_Programming_Scope_'
FLEXIBILITY_PROGRAMMING = 'flexibility_Programming_Scope'

# Flexibility - Functionalities
FLEXIBILITY_FUNCTIONALITIES = 'flexibility_Functionalities_Scope'

#Fluency - Components
FLUENCY_COMPONENTS_PREFIX = 'fluency_Components_'
FLUENCY_COMPONENTS_GRADE = 'fluency_Components_Grade'
FLUENCY_COMPONENTS_VALUE = 'fluency_Components_Value'

# Fluency - Blocks
FLUENCY_PROGRAMMING_GRADE = 'fluency_Programming_Grade'
FLUENCY_PROGRAMMING_VALUE = 'fluency_Programming_Value'


# Term for when no tags/topic has been identified
NOT_IDENTIFIED = 'Not identified'
NOT_IDENTIFIED_PTBR = 'Não identificado'


# Others

# RU topic
RU_COLUMN_TOPIC_TEXT = 'topico link'
RU_COLUMN_TOPIC_NUMERIC = 'topicoID'

TOPICS_TRANSLATION = {'Education': 'Educação', 
                 'Environment and botany': 'Meio ambiente e botânica', 
                 'Healthy life and sport': 'Vida saudável e esporte',
                 'Communication': 'Comunicação', 
                 'Medicine and health': 'Medicina e saúde',
                 'Tourism, geography, weather and meteorology': 'Turismo e geografia, tempo e meteorologia',
                 'Food and drinks': 'Comes-e-bebes',
                 'Finance and work': 'Finanças e trabalho', 
                 'Citizenship and social issues': 'Cidadania e questões sociais',
                 'Engineering, physics and construction': 'Engenharia, física e construção',
                 'Cars, vehicles and transport': 'Automóveis, veículos e transporte', 
                 'Productivity': 'Produtividade',
                 'Animals and pets': 'Animais e pets', 
                 'Entertainment': 'Entretenimento', 
                 'Music': 'Música', 
                 'Math': 'Matemática',
                 'Beauty and fashion': 'Beleza e moda', 
                 'Design, painting and photography': 'Design, pintura e fotografia',
                 'Spirituality, belief and fortune telling': 'Espiritualidade, crença e adivinhação', 
                 'Mobile tools': 'Ferramentas do celular',
                 'Robotics, physical computing and automation': 'Robótica, computação física e automação',
                  NOT_IDENTIFIED: 'Não identificado'}



# Statistics helpers
RELEVANT_VARIABLES_FOR_ANALYSIS = [INDEX_NAME_FOR_FILE_PATH,
                                   GRADE_ORIGINALITY_FUNC,
                                   GRADE_ORIGINALITY_UI_COMPONENTS,
                                   PREFIX_ORIGINALITY_DETECTION_TOPIC + DF_COL_PARSER_TOPIC_IDENTIFICATION,
                                   GRADE_ORIGINALITY_TOPIC,
                                   GRADE_ORIGINALITY_TAG,
                                   FLEXIBILITY_COMPONENTS,
                                   FLEXIBILITY_PROGRAMMING,
                                   FLEXIBILITY_FUNCTIONALITIES,
                                   FLUENCY_COMPONENTS_GRADE,
                                   FLUENCY_PROGRAMMING_GRADE,
                                   GRADE_CRIATIVIDADE
                                ]

COL_APP_MONTH = 'AppMonth'

RELEVANT_VARIABLES_FOR_ANALYSIS_PLUS_APP_MONTH = [COL_APP_MONTH] + RELEVANT_VARIABLES_FOR_ANALYSIS