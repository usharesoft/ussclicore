# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

import json
import re
from os.path import expanduser
import os
import urllib
import tempfile
import yaml

import download_utils
import printer

__author__="UShareSoft"


def extract_id(uri):
        elements = uri.split("/");
        return elements[len(elements) - 1];                

def check_json_syntax(file):
        try:
                json_data=open(file)
                data = json.load(json_data)
                json_data.close()
                return data
        except ValueError as e:
                printer.out("Syntax of template file ["+file+"] FAILED", printer.ERROR)
                printer.out("JSON parsing error: "+str(e))
                return
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return

def check_yaml_syntax(file):
        try:
                yaml_data=open(file)
                data = yaml.load(yaml_data)
                yaml_data.close()
                return data
        except ValueError as e:
                printer.out("Syntax of template file ["+file+"] FAILED", printer.ERROR)
                printer.out("YAML parsing error: "+str(e))
                return
        except IOError as e:
                printer.out("File error: "+str(e), printer.ERROR)
                return

def query_yes_no(question, default="yes"):
        """Ask a yes/no question via raw_input() and return their answer.

        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

        The "answer" return value is one of "yes" or "no".
        """
        valid = {"yes":True,   "y":True,  "ye":True,
                 "no":False,     "n":False}
        if default == None:
                prompt = " [y/n] "
        elif default == "yes":
                prompt = " [Y/n] "
        elif default == "no":
                prompt = " [y/N] "
        else:
                raise ValueError("invalid default answer: '%s'" % default)

        while True:
                printer.out(question + prompt)
                choice = raw_input().lower()
                if default is not None and choice == '':
                        return valid[default]
                elif choice in valid:
                        return valid[choice]
                else:
                        printer.out("Please respond with 'yes' or 'no' "\
                                     "(or 'y' or 'n').\n")
                             
                             
def remove_special_chars(string):
        return (re.sub('[-]', '_', string)).lower()



def order_list_object_by(objects, attribute):
        if type(attribute) is str:
                return sorted(objects, key=lambda x: getattr(x, attribute).lower(), reverse=False)
        return objects
    
def get_uforge_url_from_ws_url(ws_url):
        if ws_url[-1:]!='/':
                return ws_url.rpartition('/')[0]
        else:
                return ws_url[:-1].rpartition('/')[0]

def get_home_dir():
        return expanduser("~")

def get_remote_regex():
        return (r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$')

def get_file(uri, dest_file_name=None, verify_ssl_certificate=True):
        try:
                regexp = re.compile(get_remote_regex(), re.IGNORECASE)
                if regexp.search(uri) is not None:
                        dlUtils = download_utils.Download(uri, dest_file_name, verify_ssl_certificate)
                        try:
                            dlUtils.start()
                        except Exception, e:
                            return 2
                else:
                        dest_file_name, headers = urllib.urlretrieve(uri)
                return dest_file_name
        except Exception, e:
                print("error downloading "+uri+": "+ str(e))
                return
            
def remove_URI_forbidden_char(string):
        chars= ' '
        return re.sub(chars, '_', string)

def is_superviser_mode(userName):
        if "\\" in userName:
                return True
        else:
                return False

def get_target_username(userName):
    if "\\" in userName:
        return userName.split('\\')[1]