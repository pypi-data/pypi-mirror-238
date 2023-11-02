"""
Created on Sep 13 11:21:32 2023
Python file that's read html or xml page as a string and fetch the values
stored between the tags.
@author: ANIKET YADAV
"""

import re

class tagsHandler:

    def __init__(self) -> None:
        pass
    
    def tag_name(self, tag_name, markup_string):
        return re.findall('<%s>(.*?)</%s>'%tag_name, markup_string)
    
