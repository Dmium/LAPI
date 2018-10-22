# LazyAPI


Vulnerable to CSRF don't use in production


# Usage

1. Start a mongodb server

2. Put in the URI in the MONGO_URI field of "lazyAPIconfig.py"

3. Run setup.sh (or setup.bat on Windows)

4. Use the api at localhost:5000

5. Send api calls using the url '/<project>/<type>' followed by standard rest calls


# Endpoints

This uses rails standard rest api calls:

https://guides.rubyonrails.org/routing.html#crud-verbs-and-actions
