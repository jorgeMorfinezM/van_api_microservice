import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/html/apiTestOrdersTV")

from app import app
application = app
