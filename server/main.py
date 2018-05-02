import logging
import config

from server import create_app

print dir(config)
# initialize the application
app = create_app(config, debug=True)
