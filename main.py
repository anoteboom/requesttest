#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
from google.appengine.api import users
from oauth2client.appengine import oauth2decorator_from_clientsecrets
from oauth2client.appengine import StorageByKeyName
from google.appengine.ext import deferred
from model import CredentialsModel
from google_api import ScriptService


client_secrets = os.path.join(os.path.dirname(__file__), 'client-secrets.json')

missing_client_secrets_message = 'no client secrets file on app'
scopes = [
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/script.storage',
    'https://www.googleapis.com/auth/forms',
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/plus.me',
    'https://www.googleapis.com/auth/userinfo.email'
]

decorator = oauth2decorator_from_clientsecrets(
    client_secrets,
    scope=scopes,
    message=missing_client_secrets_message)
decorator.user_agent = 'VOGSY'


class MainHandler(webapp2.RequestHandler):
    @decorator.oauth_required
    def get(self, script_function=''):
        user = users.get_current_user()

        google_id = decorator.credentials.id_token['sub']

        # store the user credentials so it can be used in deferred jobs
        storage = StorageByKeyName(CredentialsModel, google_id, 'credentials')
        storage.put(decorator.credentials)
        print 'stored new credentials: ', decorator.credentials.to_json()

        if script_function != '':
            deferred.defer(run_script, google_id, script_function)

        self.response.write('Hello world!' +
                            '<p><a href = "/script/slowResponse" > slow </a></p>'
                            '<p><a href = "/script/fastResponse" > fast </a></p>'
                           )



def run_script(google_id, script_function):
    print google_id
    print "Trying to start ScriptService"
    script_service = ScriptService(google_id)

    response = script_service.run(function=script_function,
                                  dev_mode=True,
                                  parameters=[])
    print response


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    webapp2.Route('/script/<script_function:(.*)>', handler=MainHandler, methods=['GET']),
    (decorator.callback_path, decorator.callback_handler())
], debug=True)
