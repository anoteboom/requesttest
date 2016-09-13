# requesttest
testscript to show executionscript deadline exceeded


the libraries mentioned in requiremnets are copied to the \lib folder


The apps script contains the following code:


function fastResponse() {
  Utilities.sleep(1000);
}

function slowResponse() {
  Utilities.sleep(65000);
}


Executing the slowresponse, will cause the following error to be shown in the logging:

START SCRIPT_ID: Mb1NoXuAiAH93g5Xo7WSNr0eDcafZ4rz6 BODY: {'function': 'slowResponse', 'parameters': [], 'devMode': True}
URL being requested: POST https://script.googleapis.com/v1/scripts/Mb1NoXuAiAH93g5Xo7WSNr0eDcafZ4rz6:run?alt=json (/base/data/home/apps/e~requesttest-143307/20160913t120946.395609801631616532/lib/googleapiclient/discovery.py:822)
SCRIPT RESULTS:
('ERROR occured:', <type 'exceptions.Exception'>, ' - ', HTTPException('Deadline exceeded while waiting for HTTP response from URL: https://script.googleapis.com/v1/scripts/Mb1NoXuAiAH93g5Xo7WSNr0eDcafZ4rz6:run?alt=json',))



