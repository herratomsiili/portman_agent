import azure.functions as func
from PortmanTrigger.http_trigger import http_trigger_main
from PortmanTrigger.timer_trigger import timer_trigger_main

app = func.FunctionApp()

# Register HTTP Trigger
app.route(route="http-trigger", auth_level=func.AuthLevel.FUNCTION)(http_trigger_main)

# Register Timer Trigger
app.schedule(schedule="0 */5 * * * *", arg_name="myTimer", run_on_startup=True)(timer_trigger_main)
