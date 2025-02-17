import sys
import os
import logging
import azure.functions as func

# Ensure parent-dir is in the Python module search path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

from portman import main as portman_main

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        portman_main(req)
        return func.HttpResponse(
             "Portman function triggered successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
