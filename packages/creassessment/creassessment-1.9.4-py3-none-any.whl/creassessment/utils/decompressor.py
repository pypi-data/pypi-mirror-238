from typing import Iterable, Tuple
from venv import create
from zipfile import ZipFile
import logging
import os

from creassessment.controler.constants import BLOCKS_SCREEN_SUFIX_IDENTIFIER, DESIGNER_SCREEN_SUFIX_IDENTIFIER

class Decompressor:

    def decompress(file) -> Tuple[str, str, set, str]:
        creator = ''; app_name = ''; screens_name = ''
        extensions = set()
        zp = ZipFile(file, mode='r')
        for file in zp.namelist():
            if str(file).endswith('.scm') or str(file).endswith('.bky'): 
                creator = str(file).split('/')[2]
                app_name = str(file).split('/')[3]
                screens_name = screens_name + ' ' + str(file).split('/')[len(str(file).split('/'))-1].split('.')[0]
            if 'assets/external_comps/' in file:
                extension_name = file.split('assets/external_comps/')[1].split('/')[0]
                extensions.add(extension_name)
        return creator, app_name, extensions, screens_name
    
    def decompress_all(file, file_name) -> Tuple[dict, dict]:
        creator = ''; app_name = ''; screens_name = ''
        extensions = set()
        jsons = {}; xmls = {}
        zp = ZipFile(file, mode='r')
        for file in zp.namelist():
            if str(file).endswith('.scm') or str(file).endswith('.bky'): 
                creator = str(file).split('/')[2]
                app_name = str(file).split('/')[3]
                screen_name = str(file).split('/')[len(str(file).split('/'))-1].split('.')[0]
                screens_name = screens_name + ' ' + screen_name
                content = ''
                try:
                    content = zp.read(file).decode('utf-8')
                except: 
                    content = ''
                if (str(file).endswith('.scm')):
                    screen_name = screen_name + ' ' + DESIGNER_SCREEN_SUFIX_IDENTIFIER
                    jsons.__setitem__((file, file_name, app_name, screen_name), content)
                if (str(file).endswith('.bky')):
                    screen_name = screen_name + ' ' + BLOCKS_SCREEN_SUFIX_IDENTIFIER
                    xmls.__setitem__((file, file_name, app_name, screen_name), content)
            if 'assets/external_comps/' in file:
                extension_name = file.split('assets/external_comps/')[1].split('/')[0]
                extensions.add(extension_name)
        return jsons, xmls
    
    def extract_JSONS(file_path, app_name) -> dict:
        jsons = {}
        try:
            zp = ZipFile(file_path, mode='r')
        except Exception as e:
            print("[JSON] This file " + str(file_path) + " cound not be decompressed.")
            #logging.exception("[JSONDecompressor.decompress - 1] This file " + file + " causes exception.")
            #print(e)
        else:
            file_name = str(file_path).split(os.sep)[len(str(file_path).split(os.sep))-1]
            for file in zp.namelist():
                if (str(file).endswith('.scm')):
                    screen_name = str(file).split('/')[len(str(file).split('/'))-1].split('.')[0] + ' ' + DESIGNER_SCREEN_SUFIX_IDENTIFIER
                    try:
                        content = zp.read(file).decode('utf-8')
                        jsons.__setitem__((file_path, file_name, app_name, screen_name), content)
                    except:
                        jsons.__setitem__((file_path, file_name, app_name, screen_name), '')
                        print("[JSON] This file " + str(file) + " screens (.scm) cound not be read.")
                        #logging.exception("[JSONDecompressor.decompress - 2] This file " + file + " causes exception")
            return jsons
    
    def extract_XMLS(file_path, app_name) -> dict:
        xmls = {}
        try: 
            zp = ZipFile(file_path, mode='r')
        except Exception as e:
            print("[XML] This file " + file_path + " could not be decompressed.")
            #logging.exception("This file " + file_path + " could not be decompressed.")
            #print(e)
        else:
            file_name = str(file_path).split(os.sep)[len(str(file_path).split(os.sep))-1]
            for file in zp.namelist():
                if (str(file).endswith('.bky')):    
                    screen_name = str(file).split('/')[len(str(file).split('/'))-1].split('.')[0] + ' ' + BLOCKS_SCREEN_SUFIX_IDENTIFIER
                    try:
                        content = zp.read(file).decode('utf-8')
                        xmls.__setitem__((file_path, file_name, app_name, screen_name), content)
                    except Exception as e:
                        print("[XML] This file " + str(file) + " screen blocks could not be read.")
                        #logging.exception("This file " + file + " causes exception")
                        #print(e)
            return xmls
