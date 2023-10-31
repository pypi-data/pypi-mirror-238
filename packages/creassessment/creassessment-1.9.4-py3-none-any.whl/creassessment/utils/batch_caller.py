from pathlib import Path
import re
from typing import Callable
import pandas as pd
import os
import datetime  

from creassessment.controler.app import App
from creassessment.controler.constants import COL_APP_MONTH, INDEX_NAME_FOR_FILE_PATH, RELEVANT_VARIABLES_FOR_ANALYSIS

class Batch_Caller:
    def __init__(self) -> None:
        pass

    def analyze(self, dir_origin: str, function: Callable, filter_columns: list = [], non_win_id: str = 'Not winners') -> str:
        '''
        Analyze all apps in a directory using a function from app.py to analyze some aspect
            dir_origin: folder in which the apps are (it can have subfolders)
            function: function from App to call
            filter_columns: desired columns to keep in a more succinct separated xls
            non_win_id: name of the folder with non-winners / non-finalists apps
        '''
        dir_results = self.__prepare_and_save_results_dir(dir_origin)
        df = pd.DataFrame()
        i = 0
        start_time = datetime.datetime.now()
        print("[Batch_Caller] Analyzing apps in ", dir_origin)
        for path in Path(str(dir_origin)).rglob('*.aia'):
            print('ANALYZING: ', path.name)
            try:
                aia_project = App(str(path))
            except:
                print("[Batch_Caller] This path " +str(path)+ " causes exception")
            else:
                i = i + 1; print('ANALYZED: ', i, path.name)
                result = function(aia_project)
                df = pd.concat([df, result])
                del aia_project; del result
        try:
            end_time = datetime.datetime.now()
            end_time_str = end_time.strftime("%d-%m-%Y-%Hh%Mm%Ss")
            caller_name = re.sub("[>*<*]", "", function.__name__)
            file_results = dir_results+f"/Batch_Caller_Results_{caller_name}_{i}apps_{end_time_str}.xlsx"
            df.to_excel(file_results, sheet_name='Sheet_name_1')
            print('[Batch_Caller.analyze] Results saved in ', file_results)
            print(f'Execution time: {end_time - start_time}')
            # Col for winners/finalists
            if non_win_id:
                df.reset_index(inplace=True)
                df[COL_APP_MONTH] = df[INDEX_NAME_FOR_FILE_PATH].apply(lambda line: "Not winners" if non_win_id in line else "Winners")
            if filter_columns:
                df.reset_index()[filter_columns].to_excel(file_results + "_FILTERED_COLS.xlsx", sheet_name='Sheet_name_1')
                print('[Batch_Caller.analyze] Filtered results saved in ', file_results + "_FILTERED_COLS.xlsx")
            return file_results
        except Exception as e:
            print("[Batch_Caller.analyze] Error in saving the results")
            print(e)


    def __prepare_and_save_results_dir(self, dir_origin):
        dir_results = str(dir_origin) + ' results'
        if not os.path.exists(dir_results):
            os.mkdir(dir_results)
        return dir_results


    def analyze_in_list(self, dir_origin: str, function: Callable, dir_list: str, col: str):
        '''
        Analyze all apps in a directory using a function from app.py to analyze some aspect
        '''
        dir_results = self.__prepare_and_save_results_dir(dir_origin)
        apps_list = pd.read_excel(dir_list)
        df = pd.DataFrame()
        i = 0; j = 0
        for path in Path(str(dir_origin)).rglob('*.aia'):
            j = j + 1; print('FOUND: ', j)
            if path.name in (apps_list[col]).unique():
                try:
                    aia_project = App(str(path))
                except:
                    print("[Batch_Caller] This path " +str(path)+ " causes exception")
                else:
                    i = i + 1; print('ANALYZED: ', i, path.name)
                    result = function(aia_project)
                    df = pd.concat([df, result])
                    del aia_project; del result
            else:
                pass
        try:
            caller_name = re.sub("[>*<*]", "", function.__name__)
            file_results = dir_results+f"/Batch_Caller_Results_{caller_name}_{i}apps.xlsx"
            df.to_excel(file_results, sheet_name='Sheet_name_1')
            print(f'[Batch_Caller.{function.__name__}] Results saved in ', file_results)
            return file_results
        except Exception as e:
            print(f"[Batch_Caller.{function.__name__}] Error in saving the results")
            print(e)

