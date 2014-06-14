polling-station-importer
========================

Python script to import polling station data from a CSV file into MongoDB.

Install
=======
1. Install cURL. Required to download Python and/or virtualenv (e.g. in Ubuntu: sudo apt-get install curl).
2. Install python-dev. Required to compile 3rd party python libraries. In this case PyMongo. If not installed will result in [this error](http://www.cyberciti.biz/faq/debian-ubuntu-linux-python-h-file-not-found-error-solution/) (e.g. in Ubuntu: sudo apt-get install python-dev).
3. Install the app: sudo bash install.sh

Run
===
1. Start mongo server.
2. Load the virtual environment: source venv/bin/activate
3. Run the app: python parser.py


