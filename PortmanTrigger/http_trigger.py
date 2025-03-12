import logging
import azure.functions as func
from PortmanTrigger.portman import main as portman_main

def http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('HTTP-trigger function processed a request.')

    portman_main(req)
    return func.HttpResponse("Portman function triggered successfully.", status_code=200)
