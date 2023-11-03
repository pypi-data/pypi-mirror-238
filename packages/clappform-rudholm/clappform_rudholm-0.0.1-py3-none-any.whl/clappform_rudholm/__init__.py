"""
Clappform API Wrapper
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2022 Clappform B.V..
:license: MIT, see LICENSE for more details.
"""
__requires__ = ["requests==2.28.1", "pandas==1.5.2"]


# Metadata
__version__ = "0.0.0"
__author__ = "Clappform B.V."
__email__ = "info@clappform.com"
__license__ = "MIT"
__doc__ = "Clappform Python API wrapper"


# %%
import requests
import logging
import json


# %%
class IjssedalException(Exception):
    """REST Exceptions Class"""

class IjssedalREST:
    
    def __init__(self):
        self.id = 1


