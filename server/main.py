# coding: utf-8

import config

from server import create_app

# initialize the application
app = create_app(config, debug=True)
