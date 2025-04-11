import azure.functions as func
from PortmanTrigger.http_trigger import http_trigger
from PortmanTrigger.timer_trigger import timer_trigger
from PortmanXMLConverter.xml_converter import xml_converter
from PortmanNotificator.slack_notificator import blob_trigger
from CargoGenerator.cargo_generator import cargo_generator
from VesselDetails.vessel_details import vessel_details

app = func.FunctionApp()

# Register HTTP Trigger
app.route(route="http-trigger", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])(http_trigger)

# Register Timer Trigger
app.schedule(schedule="0 */15 * * * *", arg_name="portmanTimer", run_on_startup=True)(timer_trigger)

# Register XML Converter
app.route(route="emswe-xml-converter", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])(xml_converter)

# Register Blob Trigger for Slack notifications
app.blob_trigger(arg_name="blob", path="emswe-xml-messages/{name}", connection="AzureWebJobsStorage")(blob_trigger)

# Register Cargo Generator
app.route(route="cargo-generator", auth_level=func.AuthLevel.FUNCTION, methods=["POST"])(cargo_generator)

# Register Vessel Details
app.route(route="vessel-details", auth_level=func.AuthLevel.FUNCTION, methods=["GET", "POST"])(vessel_details)
