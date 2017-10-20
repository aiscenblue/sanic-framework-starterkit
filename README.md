**Requirements:**
```
  Python 3.5 or higher
  Windows Environment: N/A
```

**Install requirements**  
`pip3 install -r requirements.txt`

**Setup configuration**  
```
open: config/app.py
HOST = "0.0.0.0"
DEBUG = True / False
PORT = 8000
WORKERS = 4  # workers: Number of processes received before it is respected
```

**RUN sanic**  
`python3 run.py`

```
2017-09-25 10:52:54 - (sanic)[DEBUG]: 
                 ▄▄▄▄▄
        ▀▀▀██████▄▄▄       _______________
      ▄▄▄▄▄  █████████▄  /                 \
     ▀▀▀▀█████▌ ▀▐▄ ▀▐█ |   Gotta go fast!  |
   ▀▀█████▄▄ ▀██████▄██ | _________________/
   ▀▄▄▄▄▄  ▀▀█▄▀█════█▀ |/
        ▀▀▀▄  ▀▀███ ▀       ▄▄
     ▄███▀▀██▄████████▄ ▄▀▀▀▀▀▀█▌
   ██▀▄▄▄██▀▄███▀ ▀▀████      ▄██
▄▀▀▀▄██▄▀▀▌████▒▒▒▒▒▒███     ▌▄▄▀
▌    ▐▀████▐███▒▒▒▒▒▐██▌
▀▄▄▄▄▀   ▀▀████▒▒▒▒▄██▀
          ▀▀█████████▀
        ▄▄██▀██████▀█
      ▄██▀     ▀▀▀  █
     ▄█             ▐▌
 ▄▄▄▄█▌              ▀█▄▄▄▄▀▀▄
▌     ▐                ▀▀▄▄▄▀
 ▀▀▄▄▀

2017-09-25 10:52:54 - (sanic)[INFO]: Goin' Fast @ http://0.0.0.0:8000
2017-09-25 10:52:54 - (sanic)[INFO]: Starting worker [24478]
2017-09-25 10:52:54 - (sanic)[INFO]: Starting worker [24479]
2017-09-25 10:52:54 - (sanic)[INFO]: Starting worker [24480]
2017-09-25 10:52:54 - (sanic)[INFO]: Starting worker [24481]

```

**Register blueprint route**

`NOTE :: if it's a sub directory it must consist a __init__.py
file to be recognize as a package`

```
from sanic import Blueprint
from sanic.response import json
from http import HTTPStatus

""" blueprint module for url handler """
module_name = 'index'  #  module name to be registered in the blueprint
or just change the 'index' string to get_file_name(__file__)
it uses the current filename as the root url of your api module
module_name = get_file_name(__file__)

method = Blueprint(module_name, url_prefix='/')

""" http code status """
__status = HTTPStatus  # status codes library


@method.route("/", methods=['GET'])
async def index(requests):
    return json("Welcome to sanic!", __status.OK)
      
```

**READ MORE:** ``https://github.com/channelcat/sanic/``