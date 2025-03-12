import logging
import azure.functions as func
from PortmanTrigger.portman import main as portman_main

def timer_trigger(portmanTimer: func.TimerRequest) -> None:
    logging.info("Timer-trigger function processed a request.")
    
    portman_main()
    
    logging.info("Portman function triggered successfully.")
