# Build front end
cd lazyAPI/frontend/lapi/
npm run build
cd ../../../
#Prepare flask env variables
export FLASK_APP=lazyAPI
export FLASK_ENV=development
#Install LAPI backend
pip3 install --user -e .
#Start server
python -m flask run
