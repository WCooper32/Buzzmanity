import requests
import time


class Humanity():
    """A connection interface object for the Humanity API"""

    DEBUG = False

    access_token = ''  # Token to access the api
    accessTokenExpirationTime = 0  # State variable for current token expiration time
    accessTokenDuration = 3000  # Life of token in seconds

    userId = ''
    passwd = ''
    clientId = ''
    clientSecret = ''

    # Employeess are referred to as PIs (Prototyping Instructor)
    PIFields = ['id', 'firstname', 'lastname', 'email', 'eid']
    PIs = []

    ME_URL = "https://www.humanity.com/api/v2/me"

    TOKEN_URL = "https://www.humanity.com/oauth2/token.php"

    EMPLOYEES_URL = "https://www.humanity.com/api/v2/employees"
    EMPLOYEE_URL = "https://www.humanity.com/api/v2/employees/{}"

    CLOCKIN_URL = "https://www.humanity.com/api/v2/employees/{}/clockin"
    CLOCKOUT_URL = "https://www.humanity.com/api/v2/employees/{}/clockout"

    ON_NOW_URL = "https://www.humanity.com/api/v2/dashboard/onnow"

    POSITIONS_URL = "https://www.humanity.com/api/v2/positions"
    POSITION_URL = "https://www.humanity.com/api/v2/positions/{}"

    SHIFTS_URL = "https://www.humanity.com/api/v2/shifts"
    SHIFT_URL = "https://www.humanity.com/api/v2/shifts/{}"

    LOCATIONS_URL = "https://www.humanity.com/api/v2/locations"
    LOCATION_URL = "https://www.humanity.com/api/v2/locations/{}"

    PUBLISH_URL = "https://www.humanity.com/api/v2/shifts/publish"

    APPROVE_URL = "https://www.humanity.com/api/v2/shifts/{}/approve"

    def __init__(self, _userId, _passwd, _clientId, _clientSecret):

        self.userId = _userId
        self.passwd = _passwd
        self.clientId = _clientId
        self.clientSecret = _clientSecret

        self.refreshTokenIfNeeded()

        self.fetchPIs()

    """
    Update the token if the old one is expired
    """

    def refreshTokenIfNeeded(self):

        if time.time() > self.accessTokenExpirationTime:
            self.refreshAccessToken()

    """
    Get a new access token
    """

    def refreshAccessToken(self):

        token_data = {'username': self.userId,
                      'password': self.passwd,
                      'client_id': self.clientId,
                      'client_secret': self.clientSecret,
                      'grant_type': 'password'}

        try:
            resp = requests.post(self.TOKEN_URL, data=token_data)
        except requests.exceptions.ConnectionError:
            print('FAILED TO REFRESH TOKEN- CONNECTION ERROR')
            return

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to retrieve valid token')
            print(resp.json())
        else:
            # Response code was good

            # Update token expiration time
            self.token_expiration = time.time() + 3000

            # Update token
            self.access_token = resp.json()['access_token']

            if self.DEBUG:
                print('Token refreshed, good until ' +
                      str(self.token_expiration))

        return

    """
    Fetch information about logged in account
    """

    def me(self):
        self.refreshTokenIfNeeded()

        url = self.ME_URL

        payload = {'access_token': self.access_token}

        resp = requests.get(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to fetch ME information')
            print(resp.json())

        else:
            # print(resp.json()['data'])
            pass

        return resp.json()['data']

    """
    Fetch an updated list of employees
    """

    def fetchPIs(self):
        self.refreshTokenIfNeeded()

        # Blank the list of PIs before refilling
        self.PIs = []

        payload = {'access_token': self.access_token}

        if self.DEBUG:
            print('Fetching list of PIs...')
        resp = requests.get(self.EMPLOYEES_URL, params=payload)

        employeeData = resp.json()['data']

        # Sample of full dataset
        # print(employeeData[0])

        if self.DEBUG:
            print('Recieved data for ' + str(len(employeeData)) + ' PIs')

        # Extract PI records filtered for only PIFields
        for e in employeeData:
            # Once per employee record

            # Create a blank new dict for the PI record
            currentPI = {}

            # Populate fields of new PI record
            for fieldName in self.PIFields:
                currentPI[fieldName] = e[fieldName] if type(e) == dict else ''

            self.PIs.append(currentPI)

    """
    Search for a PI
        Non-case sensitive
        All fields are searched for query string
    """

    def searchPIs(self, searchText):
        if self.DEBUG:
            print('Searching for "' + searchText.lower() + '"')

        results = []

        # Iterate over PI records searching
        for thisPI in self.PIs:
            # Once per PI

            # Iterate over the PI record fields
            for thisField in self.PIFields:
                # Once per PI field

                # None check
                if(thisPI[thisField] is not None):
                    # Allows non-None fields

                    if searchText.lower() in thisPI[thisField].lower():

                        # print(str(thisPI))
                        results.append(thisPI)

                        break

        if self.DEBUG:
            print('Search matched ' + str(len(results)) + ' PIs')

        return results

    """
    Clockin a PI
    """

    def clockinPI(self, PI_id):
        self.refreshTokenIfNeeded()

        url = self.CLOCKIN_URL.format(PI_id)

        if self.DEBUG:
            print('Posting clockin for id=' + str(PI_id))
            print(' URL: ' + url)

        payload = {'access_token': self.access_token}

        resp = requests.post(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to clockin employee ' + str(PI_id))
            print(resp.json())

        else:
            if resp.json()['error'] == 'Not a valid location!':
                print('================================================')
                print('ADD THIS AS A VALID CLOCKIN LOCATION ON HUMANITY')
                print('================================================')
                # TODO throw custom error here
            elif resp.json()['error'] == 'Not a valid timeframe!':
                print('Can''t login now - no shift')
                # TODO throw custom error here
            print('Clocked in ' + str(PI_id))

        return

    """
    Clockout a PI
    """

    def clockoutPI(self, PI_id):
        self.refreshTokenIfNeeded()

        url = self.CLOCKOUT_URL.format(PI_id)

        if self.DEBUG:
            print('Posting clockout for id=' + str(PI_id))
            print(' URL: ' + url)

        payload = {'access_token': self.access_token}

        resp = requests.put(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to clockout employee with id=' + str(PI_id))
            print(resp.json())

        else:
            print('Clocked out ' + str(PI_id))

        return

    """
    Update PI buzzcard id
    We are storing buzzcard_id in the eid field on the humanity API
    """

    def updateEmployeeBuzzcardId(self, PI_id, buzzcard_id):
        self.refreshTokenIfNeeded()

        url = self.EMPLOYEE_URL.format(PI_id)

        payload = {'access_token': self.access_token}

        body = {'eid': str(buzzcard_id)}

        resp = requests.put(url, params=payload, data=body)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to update buzzcard employee with id=' +
                  str(PI_id) + ' buzzcard = ' + str(buzzcard_id))
            print(resp.json())

        else:
            if self.DEBUG:
                print('Updating eid for id ' + str(PI_id))
                print(resp.json()['data']['eid'])

        # Update PI information
        self.fetchPIs()

        return

    """
    Lookup PI id from buzzcard id
    """

    def getPIFromBuzzcard(self, buzzcard_id):
        buzzcard_id = str(buzzcard_id)

        # Iterate and find it
        for p in self.PIs:
            if(str(p['eid']) == str(buzzcard_id)):
                return p

        # Failed to find a match
        return None

    """
    Get List of PIs on now
    """

    def getOnNow(self):
        self.refreshTokenIfNeeded()

        url = self.ON_NOW_URL

        payload = {'access_token': self.access_token}

        resp = requests.get(url, params=payload,)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to retrieve PIs on now')
            print(resp.json())
        else:
            # if self.DEBUG:
            data = resp.json()['data']
            if len(data) == 0:
                print('Nobody is on now')
            else:
                print(str(len(data)) + ' PIs on now')
            for i in data:
                print(' ' + str(i['employee_id']) + ' ' +
                      str(i['employee_name']) + ' is on now')
            return resp.json()['data']

        return

    """
    Check if a specific PI is on now
    """

    def isOnNow(self, PI_id):
        self.refreshTokenIfNeeded()

        onNow = self.getOnNow()

        for PI in onNow:
            if str(PI['employee_id']) == str(PI_id):
                return True

        return False

    """
    Create a new position
    """

    def createPosition(self, positionName, location_id):
        self.refreshTokenIfNeeded()

        url = self.POSITIONS_URL

        payload = {'access_token': self.access_token}

        body = {
            'name': str(positionName),
            'location': str(location_id)
        }

        resp = requests.post(url, params=payload, data=body)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to create position ' + str(positionName))
            print(resp.json())
        else:
            # if self.DEBUG:
            print("Created position \"" + str(positionName) +
                  "\" with id " + str(resp.json()['data']['id']))
            return resp.json()['data']

        return resp.json()

    """
    Delete a position
    """

    def deletePosition(self, position_id):
        self.refreshTokenIfNeeded()

        url = self.POSITION_URL.format(str(position_id))

        payload = {'access_token': self.access_token}

        resp = requests.delete(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to delete position with id ' + str(position_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print('Deleted position ' + str(position_id))
            return resp.json()['data']

        return resp.json()

    """
    Create a shift
    """

    def createShift(self,
                    start_time,
                    end_time,
                    start_date,
                    end_date,
                    position_id):
        self.refreshTokenIfNeeded()

        url = self.SHIFTS_URL

        payload = {'access_token': self.access_token}

        body = {
            'start_time': str(start_time),
            'end_time': str(end_time),
            'start_date': str(start_date),
            'end_date': str(end_date),
            'schedule': str(position_id)
        }

        resp = requests.post(url, params=payload, data=body)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to delete position with id ' + str(position_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print("Created shift " + str(resp.json()['data']['id']))
            return resp.json()['data']

        return resp.json()

    """
    Add Employee to Shift
    """

    def addEmployeeToShift(self,
                           shift_id,
                           employee_id):
        self.refreshTokenIfNeeded()

        url = self.SHIFT_URL.format(shift_id)

        payload = {'access_token': self.access_token}

        body = {
            'add': str(employee_id)
        }

        resp = requests.put(url, params=payload, data=body)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to add employee ' +
                  str(employee_id) + ' to shift ' + str(shift_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print('Added employee ' + str(employee_id) +
                  ' to shift ' + str(shift_id))
            return resp.json()['data']

        return resp.json()

    """
    Delete a shift
    """

    def deleteShift(self, shift_id):
        self.refreshTokenIfNeeded()

        url = self.SHIFT_URL.format(str(shift_id))

        payload = {'access_token': self.access_token}

        resp = requests.delete(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to delete shift with id ' + str(shift_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print('Deleted shift with id ' + str(shift_id))
            return resp.json()['data']

        return resp.json()

    """
    Publish a shift
    """

    def publishShift(self, shift_id):
        self.refreshTokenIfNeeded()

        url = self.PUBLISH_URL

        payload = {
            'access_token': self.access_token,
            # 'shifts':"\"" + str(shift_id) + "\""
            'shifts': str(shift_id)
        }

        resp = requests.get(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to publish shift ' + str(shift_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print(resp.json()['data'])
            return resp.json()['data']

        return resp.json()

    """
    Approve a shift
    """

    def approveShift(self, shift_id):
        self.refreshTokenIfNeeded()

        url = self.APPROVE_URL.format(shift_id)

        payload = {
            'access_token': self.access_token
        }

        resp = requests.post(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to approve shift ' + str(shift_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print('Approved shift ' + str(shift_id))
            return resp.json()['data']

        return resp.json()

    """
    Create a location
    """

    def createLocation(self,
                       name):
        self.refreshTokenIfNeeded()

        url = self.LOCATIONS_URL

        payload = {'access_token': self.access_token}

        body = {
            'name': str(name),
            'type': str(1)
        }

        resp = requests.post(url, params=payload, data=body)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to create location ' + str(name))
            print(resp.json())
        else:
            # if self.DEBUG:
            print("Created location \"" + str(name) +
                  "\" with id " + str(resp.json()['data']['id']))
            return resp.json()['data']

        return resp.json()

    """
    Delete a Location
    """

    def deleteLocation(self, location_id):
        self.refreshTokenIfNeeded()

        url = self.LOCATION_URL.format(str(location_id))

        payload = {'access_token': self.access_token}

        resp = requests.delete(url, params=payload)

        if resp.status_code != 200:
            # This means something went wrong
            print('Failed to delete location with id ' + str(location_id))
            print(resp.json())
        else:
            # if self.DEBUG:
            print("Deleted location " + str(location_id))
            return resp.json()['data']

        return resp.json()
