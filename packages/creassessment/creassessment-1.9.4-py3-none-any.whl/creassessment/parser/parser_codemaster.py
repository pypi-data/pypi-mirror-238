import string
import pandas as pd

class Parser_CodeMaster:
    screens: int
    #naming: int  # to-do
    events: int
    procedural_abstraction: int
    loops: int
    conditional: int
    operators: int
    lists: int
    data_persistance: int
    sensors: int
    drawing_animation: int
    variables: int
    strings: int
    synchronization: int
    maps: int
    extensions: int

    def __init__(self):
        pass

    def detect_computational_thinking(self, df_blocks_grouped: pd.DataFrame,
                                        df_components: pd.DataFrame, extensions_list):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        self.grade_loops(df_blocks_grouped)
        self.grade_conditional(df_blocks_grouped)
        self.grade_operators(df_blocks_grouped)
        self.grade_lists(df_blocks_grouped)
        self.grade_synchronization(df_blocks_grouped)
        self.grade_maps(df_blocks_grouped)
        self.grade_strings(df_blocks_grouped)
        self.grade_data_persistance(df_blocks_grouped)
        self.grade_sensors(df_blocks_grouped)
        self.grade_drawing_animation(df_blocks_grouped)
        self.grade_events(df_blocks_grouped)
        self.grade_procedural_abstration(df_blocks_grouped)
        self.grade_variables(df_blocks_grouped)
        self.grade_extension(extensions_list)
        self.grade_screens(df_blocks_grouped, df_components)
        return vars(self)
    

    def grade_screens(self, df_blocks_grouped, df_components):
        programmatically_screens_qtd = len(df_blocks_grouped)
        screens_qtd = len(df_components)
        if programmatically_screens_qtd > 1 and screens_qtd > 1:
            self.screens = 3
            return
        elif programmatically_screens_qtd == 1 and screens_qtd > 1:
            self.screens = 2
            return
        elif  programmatically_screens_qtd == 1 and screens_qtd == 1:
            self.screens = 1
            return
        else:
            self.screens = 0

    def grade_extension(self, extensions_list):
        if len(extensions_list) > 0:
            self.extensions = 1
        else:
            self.extensions = 0

    def grade_variables(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        variable_blocks = ["global_declaration", "lexical_variable_get",
			"lexical_variable_set", "local_declaration_statement", "local_declaration_expression"]
        for v_block in variable_blocks:
            if df_blocks_contains(v_block):
                self.variables = 2
                return
        if df_blocks_contains("component_set_get"):
            self.variables = 1
        else:
            self.variables = 0


    def grade_procedural_abstration(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        procedure_definition_qtd = df_blocks_qtd("procedures_defreturn") + df_blocks_qtd("procedures_defnoreturn")
        procedure_call_qtd = df_blocks_qtd("procedures_callreturn") + df_blocks_qtd("procedures_callnoreturn")
        if (procedure_definition_qtd == 1 and procedure_call_qtd == procedure_definition_qtd):
            self.procedural_abstraction = 1
        elif (procedure_definition_qtd > 1 or procedure_call_qtd > procedure_definition_qtd):
            self.procedural_abstraction = 2
            if procedure_call_qtd > procedure_definition_qtd:
                self.procedural_abstraction = 3
        else:
            self.procedural_abstraction = 0


    def grade_drawing_animation(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        if df_blocks_contains("ImageSprite"):
            self.drawing_animation = 3
        elif df_blocks_contains("Ball"):
            self.drawing_animation = 2
        elif df_blocks_contains("Canvas"):
            self.drawing_animation = 1
        else:
            self.drawing_animation = 0

    def grade_sensors(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        sensors = ["AccelerometerSensor", "BarcodeScanner", "Clock", "GyroscopeSensor",
                    "LocationSensor", "NearField", "OrientationSensor", "Pedometer", 
                    "ProximitySensor"]
        sensor_qtd = 0
        for s in sensors:
            if df_blocks_contains(s):
                sensor_qtd = sensor_qtd + 1
        if sensor_qtd > 2:
            self.sensors = 3
        elif sensor_qtd == 2:
            self.sensors = 2
        elif sensor_qtd == 1:
            self.sensors = 1
        else:
            self.sensors = 0

            

    def grade_data_persistance(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        if df_blocks_contains("FirebaseDB") or df_blocks_contains("TinyWebDB"):
            self.data_persistance = 3
        elif df_blocks_contains("TinyDB"):
            self.data_persistance = 2
        elif df_blocks_contains("FusiontablesControl") or df_blocks_contains("File"):
            self.data_persistance = 1
        else:
            self.data_persistance = 0

    def grade_strings(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        strings = ["text_changeCase", "text_compare", "text_contains", "text_is_string", "text_isEmpty", 
    		"text_join", "text_length", "text_replace_all", "text_segment", "text_split", 
    		"text_split_at_spaces", "text_starts_at", "text_trim", "obfuscated_text"]
        for s in strings:
            if df_blocks_contains(s):
                self.strings = 2
                return
        if df_blocks_contains("text"):
            self.strings = 1
        else:
            self.strings = 0


    
    def grade_maps(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        maps_markers = ["Circle", "FeatureCollection", "LineString", "Marker", "Polygon",
                            "Rectangle"]
        for m in maps_markers:
            if df_blocks_contains(m):
                self.maps = 2
                return
        if df_blocks_contains("Map"):
            self.maps = 1
        else:
            self.maps = 0



    def grade_synchronization(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        if df_blocks_contains("Clock"):
            self.synchronization = 1
        else:
            self.synchronization = 0

    def grade_lists(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        lists_qtd = df_blocks_qtd("lists_create_with")
        map_qtd = df_blocks_qtd("lists_lookup_in_pairs")
        if map_qtd > 0:
            self.lists = 3
        elif lists_qtd > 1:
            self.lists = 2
        elif lists_qtd == 1:
            self.lists = 1
        else:
            self.lists = 0



    def grade_operators(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        math_operators = ["math_abs", "math_add", "math_atan2", "math_ceiling", "math_convert_angles", 
    		"math_convert_number", "math_cos", "math_divide", "math_division", "math_floor", 
    		"math_format_as_decimal", "math_is_a_number", "math_multiply", "math_neg",
    		"math_on_list", "math_power", "math_random_float", "math_random_int", 
    		"math_random_set_seed", "math_round", "math_single", "math_subtract", 
    		"math_tan", "math_trig"]
        relational_operators = ["logic_compare", "math_compare"]
        boolean_operators = ["logic_boolean", "logic_false", "logic_negate", "logic_operation", "logic_or"]
        for operator in boolean_operators:
            if df_blocks_contains(operator):
                self.operators = 3
                return
        for operator in relational_operators:
            if df_blocks_contains(operator):
                self.operators = 2
                return
        for operator in math_operators:
            if df_blocks_contains(operator):
                self.operators = 1
                return
        


    def grade_conditional(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        if df_blocks_qtd('elseif') > 0:
            self.conditional = 3
            return
        elif (df_blocks_qtd('else') + df_blocks_qtd('controls_choose')) > 0:
            self.conditional = 2
            return
        elif df_blocks_qtd('controls_if') > 0:
            self.conditional = 1
            return
        else:
            self.conditional = 0


    def grade_loops(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        if df_blocks_contains('controls_forEach'):
            self.loops = 3
            return
        if df_blocks_contains('controls_forRange'):
            self.loops = 2
            return
        if df_blocks_contains('controls_while'):
            self.loops = 1
            return
        else:
            self.loops = 0

    def grade_events(self, df_blocks_grouped):
        df_blocks_contains = lambda x: True if x in df_blocks_grouped else False
        df_blocks_qtd = lambda x: df_blocks_grouped[x].sum() if df_blocks_contains(x) else 0
        events_qtd = df_blocks_qtd("component_event")
        if events_qtd > 2: 
            self.events = 3
        elif events_qtd == 2:
            self.events = 2
        elif events_qtd == 1:
            self.events = 1
        else:
            self.events = 0


