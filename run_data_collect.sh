#!/bin/bash
set -e

FILE="outfile.txt"
FILE=${FILE%.*}_`date +%d%b%y`.${FILE#*.}
echo $FILE


venv/bin/python -m pip freeze > requirements.txt

venv/bin/python main.py >> ./out/$FILE

venv/bin/python data_reporters/texas_reporter.py > ./out/report.txt



# pyenv virtualenv 3.10.8 datapoker
# pyenv uninstall datapoker
# ls ~/.pyenv/versions/
# ln -s ~/.pyenv/versions/3.10.8/envs/datapoker venv  -->  Where venv lives from pyenv-virtualenv

# venv/bin/python -m pip install requests
# venv/bin/python -m pip install ipython
# venv/bin/python -m pip install firebase-admin                  
# venv/bin/python -m pip install beautifulsoup4 
# venv/bin/python -m pip install pandas 

# venv/bin/python -m pip freeze > requirements.txt  
# venv/bin/python -m pip uninstall -r requirements.txt -y

