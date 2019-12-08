from multicorn import ForeignDataWrapper
from multicorn.utils import log_to_postgres as log
from requests import get
from requests import post
import logging


class Keycloak(ForeignDataWrapper):
  def __init__(self, options, columns):
    super(Keycloak, self).__init__(options, columns)

    self.batchSize = 500

    self.validate(options, columns)

    self.columns = columns
    # keycloak api call body options
    # url is the base url (e.g. keycloak-server.com)
    self.url = options['url']
    # admin username and password
    self.username = options['username']
    self.password = options['password']
    # name of realm
    self.realm = options['realm']
    # the name of the client
    self.client_id = options['client_id']
    self.grant_type = options['grant_type']
    # you get the client secret from the keycloak client (access type should be "confidential")
    self.client_secret = options['client_secret']
    # organization_id so we can use our foriegn joined table like we did with the old "user" table
    self.organization_id = options['organization_id']

  # validate options
  def validate(self, options, columns):
    if 'organization_id' not in options:
      log(message = 'No org id provided', level = logging.ERROR)

    if 'url' not in options:
      log(message = 'No url provided', level = logging.ERROR)

    if 'username' not in options:
      log(message = 'No username provided', level = logging.ERROR)

    if 'password' not in options:
      log(message = 'No password provided', level = logging.ERROR)

    if 'realm' not in options:
      log(message = 'No realm provided', level = logging.ERROR)

    if 'client_id' not in options:
      log(message = 'No client_id provided', level = logging.ERROR)

    if 'grant_type' not in options:
      log(message = 'No grant_type provided', level = logging.ERROR)

    if 'client_secret' not in options:
      log(message = 'No client_secret provided', level = logging.ERROR)

  # handle error responses
  def handle_error(self, response):
    if response['error_description']:
      error = response['error_description']
    else:
      error = response['error']

    log(message = error, level = logging.ERROR)

  def getUserCount(self):
      token = self.getToken()
      headers = {'Authorization': 'Bearer %s' % token, 'Content-Type': 'application/json'}
      getUserCountURL = '%s/auth/admin/realms/%s/users/count' % (self.url, self.realm)
      userCountResponse = get(getUserCountURL, headers=headers)
      log(message = userCountResponse.text, level = logging.WARNING)
      return userCountResponse.text

  def getUsers(self, batchStart):
      token = self.getToken()
      headers = {'Authorization': 'Bearer %s' % token, 'Content-Type': 'application/json'}
      getUsersURL = '%s/auth/admin/realms/%s/users?first=%s&max=%s' % (self.url, self.realm,batchStart,self.batchSize)
      usersResponse = get(getUsersURL, headers=headers)
      log(message = getUsersURL, level = logging.WARNING)
      usersData = usersResponse.json()
      return usersData

  def getToken(self):
      requestURL = '%s/auth/realms/%s/protocol/openid-connect/token' % (self.url, self.realm)
      requestBody = {
        'username': self.username,
        'password': self.password,
        'client_id': self.client_id,
        'grant_type': self.grant_type,
        'client_secret': self.client_secret
      }
      tokenResponse = post(requestURL, data=requestBody)
      tokenData = tokenResponse.json()

      if 'error' in tokenData:
        self.handle_error(tokenData)
      else:
        # we've got an access token to use in the users request
        token = tokenData['access_token']
        return token

  def execute(self, quals, columns):
    # let get the token followed by the number of users
    userCount = int(self.getUserCount())

    for batchStart in range(1,userCount,self.batchSize):
        log(message = batchStart, level = logging.WARNING)
        usersData = self.getUsers(batchStart)

        if 'error' in usersData:
          self.handle_error(usersData)
        else:
          for entry in usersData:
            entry['organization_id'] = self.organization_id
            yield entry
