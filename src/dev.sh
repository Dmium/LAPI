cd lazyAPI/frontend/lapi/
npm run watch &
cd ../../../
export FLASK_APP=lazyAPI
export FLASK_ENV=development
pip3 install --user -e .
python -m flask run
