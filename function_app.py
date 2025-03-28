import azure.functions as func
from PortmanTrigger.http_trigger import http_trigger
from PortmanTrigger.timer_trigger import timer_trigger
from PortmanXMLConverter.main import main as emswe_xml_converter

app = func.FunctionApp()

# Register HTTP Trigger
app.route(route="http-trigger", auth_level=func.AuthLevel.FUNCTION)(http_trigger)

# Register Timer Trigger
app.schedule(schedule="0 */15 * * * *", arg_name="portmanTimer", run_on_startup=True)(timer_trigger)

# Register XML Converter
app.route(route="emswe-xml-converter", auth_level=func.AuthLevel.FUNCTION)(emswe_xml_converter)