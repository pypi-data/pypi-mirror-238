from typing import Tuple
import pandas as pd

from creassessment.grader.creativity.originality.originality_functionalities import Originality_Functionalities
from creassessment.grader.creativity.originality.originality_topic import Originality_Topic
from creassessment.grader.creativity.originality.originality_tags import Originality_Tags
from creassessment.grader.creativity.originality.originality_UI_components import Originality_UI_Components
from creassessment.grader.creativity.fluency.fluency_components import Fluency_Components
from creassessment.grader.creativity.fluency.fluency_programming import Fluency_Programming
from creassessment.grader.creativity.flexibility.flexibility_functionalities import Flexibility_Functionalities
from creassessment.grader.creativity.flexibility.flexibility_programming import Flexibility_Programming
from creassessment.grader.creativity.flexibility.flexibility_components import Flexibility_Components

from creassessment.controler.constants import INDEX_NAME_FOR_APP_NAME, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_FILE_PATH, \
        GRADE_ORIGINALITY_UI_COMPONENTS, GRADE_ORIGINALITY_SING_UI_COMPONENTS, GRADE_ORIGINALITY_COMB_UI_COMPONENTS, PREFIX_ORIGINALITY_SINGGRADE_UI_COMPONENTS, PREFIX_ORIGINALITY_DETECTION_UI_COMPONENTS, \
        PREFIX_ORIGINALITY_DETECTION_FUNCTIONALITY, PREFIX_ORIGINALITY_SINGRADE_FUNCTIONALITY, GRADE_ORIGINALITY_SING_FUNC, GRADE_ORIGINALITY_COMB_FUNC, GRADE_ORIGINALITY_FUNC, \
        DF_COL_PARSER_TAGS, GRADE_ORIGINALITY_TAG, PREFIX_ORIGINALITY_DETECTION_TAG, \
        GRADE_ORIGINALITY_TOPIC, PREFIX_ORIGINALITY_DETECTION_TOPIC, PREFIX_ORIGINALITY_SINGGRADE_TOPIC, \
    FLEXIBILITY_FUNCTIONALITIES, FLEXIBILITY_PROGRAMMING, FLEXIBILITY_COMPONENTS, \
    FLUENCY_COMPONENTS_VALUE, FLUENCY_PROGRAMMING_GRADE, FLUENCY_COMPONENTS_GRADE, FLUENCY_PROGRAMMING_VALUE, \
    GRADE_CRIATIVIDADE


from creassessment.utils.creassess_utils import round_grade

class Creativity_Grader:
    grader_originality_functionality: Originality_Functionalities
    grader_originality_UI_components: Originality_UI_Components
    grader_originality_topics: Originality_Topic
    grader_originality_tags: Originality_Tags
    grader_fluency_components: Fluency_Components
    grader_fluency_programming: Fluency_Programming
    grader_flexibility_components: Flexibility_Components
    grader_flexibility_programming: Flexibility_Programming
    grader_flexibility_functionalities: Flexibility_Functionalities

    creativity_grade: float

    originality_functionality_grade: float
    originality_UI_components_grade: float
    originality_topic_grade: float
    originality_tag_grade: float

    def __init__(self, grader_originality_functionality: Originality_Functionalities = Originality_Functionalities(),
                       grader_originality_UI_components: Originality_UI_Components = Originality_UI_Components(),
                       grader_originality_topics: Originality_Topic = Originality_Topic(),
                       grader_originality_tags: Originality_Tags = Originality_Tags(),
                       grader_fluency_components: Fluency_Components = Fluency_Components(),
                       grader_fluency_programming: Fluency_Programming = Fluency_Programming(),
                       grader_flexibility_components: Flexibility_Components = Flexibility_Components(),
                       grader_flexibility_programming: Flexibility_Programming = Flexibility_Programming(),
                       grader_flexibility_functionalities: Flexibility_Functionalities = Flexibility_Functionalities()):
        self.grader_originality_functionality = grader_originality_functionality
        self.grader_originality_UI_components = grader_originality_UI_components
        self.grader_originality_topics = grader_originality_topics
        self.grader_originality_tags = grader_originality_tags
        self.grader_fluency_components = grader_fluency_components
        self.grader_fluency_programming = grader_fluency_programming
        self.grader_flexibility_components = grader_flexibility_components
        self.grader_flexibility_programming = grader_flexibility_programming
        self.grader_flexibility_functionalities = grader_flexibility_functionalities


    def grade_creativity(self, app_query_functionalities_df: pd.DataFrame,
                               app_query_UI_components_df: pd.DataFrame,
                               app_query_topic_df: pd.DataFrame,
                               app_query_tag_df: pd.DataFrame,
                               app_query_components_categories_df: pd.DataFrame,
                               app_query_programming_categories_df: pd.DataFrame,
                               app_query_components_categories_freq_df: pd.DataFrame,
                               app_query_programming_categories_freq_df: pd.DataFrame,
                               is_grade_rounded: bool,
                               drop_index = True) ->  pd.DataFrame:
        '''
        Grade the product creativity planes of an app
        app_query_functionalities_df = the pd.DataFrame containing all functionalities extracted
        app_query_UI_components_df = the pd.DataFrame containing the selected UI components extracted
        drop_index = if True, do not consider the constructed index of INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_APP_NAME
                    Useful specially for servers path which are not very reliable
        '''
        self.originality_functionality_grade = 0.0
        self.originality_UI_components_grade = 0.0
        self.originality_topic_grade = 0.0
        self.originality_tag_grade = 0.0
        self.flexibility_components_grade = 0.0
        self.flexibility_programming_grade = 0.0
        self.flexibility_functionalities_grade = 0.0
        self.fluency_components_grade = 0.0
        self.fluency_components_value = 0.0
        self.fluency_programming_grade = 0.0
        self.fluency_programming_value = 0.0

        self.creativity_grade = 0.0

        detection_functionality_df, grades_functionality_df = self.grade_originality_functionality(app_query_functionalities_df, is_grade_rounded)
        detection_UI_components_df, grades_UI_components_df = self.grade_originality_UI_components(app_query_UI_components_df, is_grade_rounded)
        detection_topic_df, grades_topic_df = self.grade_originality_topic(app_query_topic_df, is_grade_rounded)
        detection_tag_df, grades_tag_df = self.grade_originality_tag(app_query_tag_df, is_grade_rounded)
        self.flexibility_components_grade, flexibility_components_categories_df = self.grade_flexibility_components(app_query_components_categories_df, is_grade_rounded)
        self.flexibility_programming_grade, flexibility_programming_categories_df = self.grade_flexibility_programming(app_query_programming_categories_df, is_grade_rounded)
        self.flexibility_functionalities_grade, _ = self.grade_flexibility_functionalities(app_query_functionalities_df, is_grade_rounded)
        self.fluency_components_grade, self.fluency_components_value = self.grade_fluency_components(app_query_components_categories_freq_df, is_grade_rounded)
        self.fluency_programming_grade, self.fluency_programming_value = self.grade_fluency_programming(app_query_programming_categories_freq_df, is_grade_rounded)

        self.creativity_grade = float((self.originality_functionality_grade 
                                       + self.originality_UI_components_grade
                                       + self.originality_topic_grade
                                       + self.originality_tag_grade
                                       + self.flexibility_components_grade
                                       + self.flexibility_programming_grade
                                       + self.flexibility_functionalities_grade
                                       + self.fluency_components_grade
                                       + self.fluency_programming_grade) / 9)
        if is_grade_rounded:
            self.creativity_grade = round_grade(self.creativity_grade)
        if drop_index:
            drop_col_index = lambda df: df.reset_index().drop(columns=[INDEX_NAME_FOR_FILE_PATH, INDEX_NAME_FOR_FILE_NAME, INDEX_NAME_FOR_APP_NAME])
            frames = [drop_col_index(detection_functionality_df), drop_col_index(grades_functionality_df),
                      drop_col_index(detection_UI_components_df), drop_col_index(grades_UI_components_df),
                      drop_col_index(detection_topic_df), drop_col_index(grades_topic_df),
                      drop_col_index(detection_tag_df), drop_col_index(grades_tag_df),
                      drop_col_index(flexibility_components_categories_df), drop_col_index(flexibility_programming_categories_df)]
        else:
            frames = [detection_functionality_df.copy(), grades_functionality_df.copy(),
                      detection_UI_components_df.copy(), grades_UI_components_df.copy(),
                      detection_topic_df.copy(), grades_topic_df.copy(),
                      detection_tag_df.copy(), grades_tag_df.copy(),
                      flexibility_components_categories_df.copy(), flexibility_programming_categories_df.copy()]
        creativity_df = pd.concat(frames, axis=1)        
        creativity_df[FLEXIBILITY_COMPONENTS] = self.flexibility_components_grade
        creativity_df[FLEXIBILITY_PROGRAMMING] = self.flexibility_programming_grade
        creativity_df[FLEXIBILITY_FUNCTIONALITIES] = self.flexibility_functionalities_grade
        
        creativity_df[FLUENCY_COMPONENTS_GRADE] = self.fluency_components_grade
        creativity_df[FLUENCY_COMPONENTS_VALUE] = self.fluency_components_value
        creativity_df[FLUENCY_PROGRAMMING_GRADE] = self.fluency_programming_grade
        creativity_df[FLUENCY_PROGRAMMING_VALUE] = self.fluency_programming_value

        creativity_df[GRADE_CRIATIVIDADE] = self.creativity_grade
        
        return creativity_df


    def grade_originality_functionality(self, app_query_functionalities_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
        '''
        Analyzes the originality of functionalities based on a Reference Universe
        '''
        grade_sing, grade_comb, self.originality_functionality_grade, df_originality_sing = self.grader_originality_functionality.analyze_originality(app_query_functionalities_df, is_grade_rounded)
        grades_functionality_df = df_originality_sing.copy()
        grades_functionality_df = grades_functionality_df.add_prefix(PREFIX_ORIGINALITY_SINGRADE_FUNCTIONALITY)
        grades_functionality_df[GRADE_ORIGINALITY_SING_FUNC] = grade_sing
        grades_functionality_df[GRADE_ORIGINALITY_COMB_FUNC] = grade_comb
        grades_functionality_df[GRADE_ORIGINALITY_FUNC] = self.originality_functionality_grade
        detection_functionality_df = app_query_functionalities_df.copy().add_prefix(PREFIX_ORIGINALITY_DETECTION_FUNCTIONALITY)
        return detection_functionality_df, grades_functionality_df

    def grade_originality_UI_components(self, app_query_UI_components_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
        '''
        Analyzes the originality of UI components based on a Reference Universe
        '''
        grade_sing, grade_comb, self.originality_UI_components_grade, df_originality_sing = self.grader_originality_UI_components.analyze_originality(app_query_UI_components_df, is_grade_rounded)
        grades_UI_components_df = df_originality_sing.copy()
        grades_UI_components_df = grades_UI_components_df.add_prefix(PREFIX_ORIGINALITY_SINGGRADE_UI_COMPONENTS)
        grades_UI_components_df[GRADE_ORIGINALITY_SING_UI_COMPONENTS] = grade_sing
        grades_UI_components_df[GRADE_ORIGINALITY_COMB_UI_COMPONENTS] = grade_comb
        grades_UI_components_df[GRADE_ORIGINALITY_UI_COMPONENTS] = self.originality_UI_components_grade
        detection_UI_components_df = app_query_UI_components_df.copy().add_prefix(PREFIX_ORIGINALITY_DETECTION_UI_COMPONENTS)
        return detection_UI_components_df, grades_UI_components_df

    def grade_originality_topic(self, app_query_topic_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
        grade_sing, _, self.originality_topic_grade, df_originality_sing = self.grader_originality_topics.analyze_originality(app_query_topic_df, is_grade_rounded)
        grades_topic_df = df_originality_sing.copy()
        grades_topic_df = grades_topic_df.add_prefix(PREFIX_ORIGINALITY_SINGGRADE_TOPIC)
        grades_topic_df[GRADE_ORIGINALITY_TOPIC] = grade_sing
        detection_topic_df = app_query_topic_df.copy().add_prefix(PREFIX_ORIGINALITY_DETECTION_TOPIC)
        return detection_topic_df, grades_topic_df
    
    
    def grade_originality_tag(self, app_query_tag_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[pd.DataFrame, pd.DataFrame]:
        grade_sing, _, self.originality_tag_grade, df_originality_sing = self.grader_originality_tags.analyze_originality(app_query_tag_df, is_grade_rounded)
        grades_tag_df = pd.DataFrame(index=df_originality_sing.index)
        #grades_tag_df[PREFIX_ORIGINALITY_SINGGRADE_TAG] = str(df_originality_sing.values)
        grades_tag_df[GRADE_ORIGINALITY_TAG] = grade_sing
        extracted_tags_list = app_query_tag_df[DF_COL_PARSER_TAGS].values[0]
        extracted_tags_str = ', '.join(map(str, extracted_tags_list)) 
        app_query_tag_df[DF_COL_PARSER_TAGS] = extracted_tags_str
        extracted_tag_df = app_query_tag_df.copy().add_prefix(PREFIX_ORIGINALITY_DETECTION_TAG)
        return extracted_tag_df, grades_tag_df

    def grade_flexibility_components(self, app_query_components_categories_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        grade_flexibility_components, flexbility_components_categories_df = self.grader_flexibility_components.analyze_flexibility(app_query_components_categories_df, is_grade_rounded)
        return grade_flexibility_components, flexbility_components_categories_df

    def grade_flexibility_programming(self, app_query_programming_categories_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        grade_flexibility_programming, flexbility_programming_categories_df = self.grader_flexibility_programming.analyze_flexibility(app_query_programming_categories_df, is_grade_rounded)
        return grade_flexibility_programming, flexbility_programming_categories_df

    def grade_flexibility_functionalities(self, app_query_functionalities_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, pd.DataFrame]:
        self.flexibility_functionalities_grade, _ = self.grader_flexibility_functionalities.analyze_flexibility(app_query_functionalities_df, is_grade_rounded)
        return self.flexibility_functionalities_grade, _ # detection/grade of functionalities already are in grade_originality_functionality

    def grade_fluency_components(self, app_query_components_categories_freq_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, int]:
        fluency_grade, fluency_value = self.grader_fluency_components.analyze_fluency(app_query_components_categories_freq_df, FLUENCY_COMPONENTS_VALUE)
        return fluency_grade, fluency_value
    
    def grade_fluency_programming(self, app_query_programming_categories_freq_df: pd.DataFrame, is_grade_rounded: bool) -> Tuple[float, int]:
        fluency_grade, fluency_value = self.grader_fluency_programming.analyze_fluency(app_query_programming_categories_freq_df, FLUENCY_PROGRAMMING_VALUE)
        return fluency_grade, fluency_value

