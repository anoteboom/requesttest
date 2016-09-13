from oauth2client.appengine import StorageByKeyName
from model import CredentialsModel
import httplib2
from googleapiclient.discovery import build
from google.appengine.api import urlfetch

APPS_SCRIPT_LIBRARY_ID = 'Mb1NoXuAiAH93g5Xo7WSNr0eDcafZ4rz6'


def create_service(service, version, creds=None, timeout=60):
    """Create a Google API service.

    Load an API service from a discovery document and authorize it with the
    provided credentials.

    Args:
      service: Service name (e.g 'mirror', 'oauth2').
      version: Service version (e.g 'v1').
      creds: Credentials used to authorize service.
    Returns:
      Authorized Google API service.
    """
    # Instantiate an Http instance
    http = httplib2.Http(timeout=timeout)

    if creds:
        # Authorize the Http instance with the passed credentials
        creds.authorize(http)

    return build(service, version, http=http)


class ScriptService:
    def __init__(self, google_id):
        storage = StorageByKeyName(CredentialsModel, google_id, 'credentials')
        credentials = storage.get()

        print "Executing script as using credentials:", credentials.to_json()
        urlfetch.set_default_fetch_deadline(180)
        self.script_service = create_service('script', 'v1', credentials, timeout=180)

    def run(self,
            script_id=None,
            function=None,
            parameters=None,
            dev_mode=False):
        if parameters is None:
            parameters = []

        if script_id is None:
            # use default script
            script_id = APPS_SCRIPT_LIBRARY_ID

        body = {'function': function,
                'parameters': parameters,
                'devMode': dev_mode}

        print "START SCRIPT_ID:", script_id, 'BODY:', body

        urlfetch.set_default_fetch_deadline(180)
        try:
            response = self.script_service.scripts().run(body=body, scriptId=script_id).execute()
        except Exception, error:
            response = 'ERROR occured:', Exception, ' - ', error
        except:
            response = 'ERROR occured'

        print 'SCRIPT RESULTS:', response
        return response
