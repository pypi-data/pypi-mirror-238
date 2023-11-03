# pycvtools

[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)                 
[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org/downloads/)   

## Functionality of the pyevaltool

- Automated testing of the bot response deployed gpt


```
pip install pyevaltool
```
#### To run
```
from pyevaltool import *
```
#### For GPT test -
```
from pyevaltool import gpt_test
url = # frontend_url something like https://****.azurewebsites.net****
token = token / key
chat_completion_format = {
                "chatId": "",
                "siteInfo": {
                    "domain": ""
                },
                "messages": [
                    {
                        "role": "user",
                        "content": ''
                    }
                ],
                "model": "",
                "stream": False
                }
input_file = input_file_path

gpt_test(url,token,chat_completion_format,input_file)
```


