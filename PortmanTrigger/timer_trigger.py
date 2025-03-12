import logging
import azure.functions as func
from PortmanTrigger.portman import main as portman_main

def timer_trigger_main(myTimer: func.TimerRequest) -> None:
    logging.info("Timer trigger function triggered.")
    
    portman_main()
    
    logging.info("Timer trigger function executed.")
