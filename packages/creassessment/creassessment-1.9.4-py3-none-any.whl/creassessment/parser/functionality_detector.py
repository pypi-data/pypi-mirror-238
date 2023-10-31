import pandas as pd

class Functionality_Detector:

    # CamelCase names for compatibility with CodeMaster
    AccessWebsite: bool
    Animation: bool
    Calculator: bool
    Canvas: bool
    ChooseImageFromGallery: bool
    ConvertSpeechToText: bool
    ConvertTextToSpeech: bool
    CountSteps: bool
    DetectAcceleration: bool
    DisplayInformation: bool
    DisplayListInformation: bool
    Login: bool
    MakeACall: bool
    MakeDataRegistration: bool
    MarkPositionOnMap: bool
    MeasureAirPressure: bool
    MeasureAngularVelocity: bool
    MeasureLightLevel: bool
    MeasureMagneticField: bool
    MeasureProximity: bool
    MeasureRelativeAirHumidity: bool
    MeasureTemperature: bool
    Paint: bool
    PlaySound: bool
    PlayVideo: bool
    RecordAudio: bool
    RecordVideo: bool
    SaveDataInTheCloud: bool
    SaveDataLocally: bool
    ScanQrcode: bool
    ScheduleTime: bool
    ShareArtifact: bool
    ShowDeviceSpatialOrientation: bool
    ShowGeolocation: bool
    ShowPicture: bool
    TakeAPicture: bool
    Translate: bool
    UseApiFromAnotherApp: bool
    UseBluetooth: bool
    UseDataFromForm: bool
    ViewContactList: bool
    ViewMap: bool
    
    # ideas
    # 09/09: HelloWorld/DisplayMessage: bool - app com um botão e um bloco de click botão e Button_set_Text 
    # 09/09: Navigator: telas com só botão de openscreen
    # 09/09: detectar também se tiver somente um componente com background music no PlaySound
    # 09/09: separar em dois? long e short? DisplayInformation
    # 09/09: detectar também se tiver somente um componnente para o AccessWebsite

    def __init__(self):
        pass

    def detect_functionalities(self, df_blocks_grouped: pd.DataFrame, 
                                df_blocks: pd.DataFrame,
                                df_content_textual_content_by_component: pd.DataFrame) -> dict:
        try:
            content_text_block = df_content_textual_content_by_component['text_block'].to_string(header=False, index=False)
        except:
            content_text_block = ''

        if df_blocks_grouped is not None:
            df_grouped_blocks_contains = lambda block: True if block in df_blocks_grouped else False
            df_grouped_blocks_qtd = lambda block: df_blocks_grouped[block].sum() if df_grouped_blocks_contains(block) else 0
        else:
            df_grouped_blocks_contains = lambda block: False
            df_grouped_blocks_qtd = lambda block: 0
        
        if df_blocks is not None: 
            df_blocks_contains = lambda block: True if block in df_blocks else False
        else: 
            df_blocks_contains = lambda block: False

        def len_bt(type, size):
            '''
            Returns if there is a component type which lenght of textual content is bigger than 
            the size parameter. E.g.: label > 20 characters
            '''
            df_filter_col_by_type = lambda type: df_content_textual_content_by_component[[col for col in df_content_textual_content_by_component.columns if type in col]]
            df_filtered = df_filter_col_by_type(type)
            for col in df_filtered:
                if len(df_filtered[~df_filtered[col].isnull()][col].to_string(header=False, index=False)) > size:
                    return True                    
            else: return False

        self.AccessWebsite = df_grouped_blocks_contains('WebViewer') or df_grouped_blocks_contains('Web') or "http://www." in content_text_block
        self.Animation = df_grouped_blocks_contains('ImageSprite') or df_grouped_blocks_contains('Ball')
        self.Calculator = (df_grouped_blocks_contains('math_add') and df_grouped_blocks_contains('math_subtract')
                           and df_grouped_blocks_contains('math_multiply') and df_grouped_blocks_contains('math_division')
                           and df_grouped_blocks_contains('math_number') 
                           and (df_grouped_blocks_contains('Label') or df_grouped_blocks_contains('TextBox'))
                           and df_grouped_blocks_contains('Button'))
        self.Canvas = df_grouped_blocks_contains('Canvas')
        self.ChooseImageFromGallery = df_grouped_blocks_contains('ImagePicker')
        self.ConvertSpeechToText = df_grouped_blocks_contains('SpeechRecognizer')
        self.ConvertTextToSpeech = df_grouped_blocks_contains('TextToSpeech')
        self.CountSteps = df_grouped_blocks_contains('Pedometer')
        self.DetectAcceleration = df_grouped_blocks_contains('AccelerometerSensor')
        self.DisplayInformation = len_bt('Label', 20) or len_bt('TextBox', 20)
        self.DisplayListInformation = df_grouped_blocks_contains('ListView')
        self.Login = (df_grouped_blocks_contains('File') or df_grouped_blocks_contains('TinyDB') or df_grouped_blocks_contains('FirebaseDB') or df_grouped_blocks_contains('TinyWebDB') or df_grouped_blocks_contains('CloudDB')) and df_grouped_blocks_contains('PasswordTextBox')
        self.MakeACall = df_grouped_blocks_contains('PhoneCall')
        self.MakeDataRegistration = df_grouped_blocks_qtd('TextBox') >= 3 and (df_grouped_blocks_contains('File') or df_grouped_blocks_contains('TinyDB') or df_grouped_blocks_contains('FirebaseDB') or df_grouped_blocks_contains('TinyWebDB') or df_grouped_blocks_contains('CloudDB'))
        self.MarkPositionOnMap = df_grouped_blocks_contains('Circle') or df_grouped_blocks_contains('FeatureCollection') or df_grouped_blocks_contains('LineString') or df_grouped_blocks_contains('Marker') or df_grouped_blocks_contains('Polygon') or df_grouped_blocks_contains('Rectangle')
        self.MeasureAirPressure = df_grouped_blocks_contains('Barometer')
        self.MeasureAngularVelocity = df_grouped_blocks_contains('GyroscopeSensor')
        self.MeasureLightLevel = df_grouped_blocks_contains('LightSensor')
        self.MeasureMagneticField = df_grouped_blocks_contains('MagneticFieldSensor')
        self.MeasureProximity = df_grouped_blocks_contains('ProximitySensor')
        self.MeasureRelativeAirHumidity = df_grouped_blocks_contains('Hygrometer')
        self.MeasureTemperature = df_grouped_blocks_contains('Thermometer')
        self.Paint = (df_blocks_contains('Canvas_Clear') or df_blocks_contains('Canvas_DrawArc')
                      or df_blocks_contains('Canvas_DrawCircle') or df_blocks_contains('Canvas_DrawLine')
                      or df_blocks_contains('Canvas_DrawPoint') or df_blocks_contains('Canvas_DrawShape')
                      or df_blocks_contains('Canvas_DrawText') or df_blocks_contains('Canvas_DrawTextAtAngle')
                      or df_blocks_contains('Canvas_SetBackgroundPixelColor'))
        self.PlaySound = df_grouped_blocks_contains('Sound') or df_grouped_blocks_contains('Player')
        self.PlayVideo = df_grouped_blocks_contains('VideoPlayer')
        self.RecordAudio = df_grouped_blocks_contains('SoundRecorder')
        self.RecordVideo = df_grouped_blocks_contains('Camcorder')
        self.SaveDataInTheCloud = df_grouped_blocks_contains('FirebaseDB') or df_grouped_blocks_contains('TinyWebDB') or df_grouped_blocks_contains('CloudDB')
        self.SaveDataLocally = df_grouped_blocks_contains('File') or df_grouped_blocks_contains('TinyDB')
        self.ScanQrcode = df_grouped_blocks_contains('BarcodeScanner')
        self.ScheduleTime = df_grouped_blocks_contains('Clock')
        self.ShareArtifact = df_grouped_blocks_contains('Sharing') or df_grouped_blocks_contains('Texting') or df_grouped_blocks_contains('Twitter')
        self.ShowDeviceSpatialOrientation = df_grouped_blocks_contains('OrientationSensor')
        self.ShowGeolocation = df_grouped_blocks_contains('LocationSensor')
        self.ShowPicture = df_blocks_contains('Image_set_Visible')
        self.TakeAPicture = df_grouped_blocks_contains('Camera')
        self.Translate = df_grouped_blocks_contains('YandexTranslate')
        self.UseApiFromAnotherApp = df_grouped_blocks_contains('ActivityStarter')
        self.UseBluetooth = df_grouped_blocks_contains('BluetoothClient') or df_grouped_blocks_contains('BluetoothServer')
        self.UseDataFromForm = df_grouped_blocks_qtd('TextBox') >= 3
        self.ViewContactList = df_grouped_blocks_contains('ContactPicker') or df_grouped_blocks_contains('EmailPicker') or df_grouped_blocks_contains('PhoneNumberPicker')
        self.ViewMap = df_grouped_blocks_contains('Map') or ( ("http:" in content_text_block or "www." in content_text_block) and "maps" in content_text_block)
        return vars(self)
        
    








