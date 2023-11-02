"""PySnoo2 Constants."""

# Base Headers
BASE_HEADERS = {
    'User-Agent': 'okhttp/4.7.2',
}

# Snoo API endpoints
SNOO_API_URI = 'https://api-us-east-1-prod.happiestbaby.com'

# OAuth-related
OAUTH_LOGIN_ENDPOINT = SNOO_API_URI + '/us/v3/login'
OAUTH_TOKEN_REFRESH_ENDPOINT = SNOO_API_URI + '/us/v2/refresh/'
OAUTH_CLIENT_ID = 'snoo_client'
OAUTH_SCOPE = ['offline_access']

SNOO_ME_ENDPOINT = SNOO_API_URI + '/us/me/v10/me'
SNOO_DEVICES_ENDPOINT = SNOO_API_URI + '/hds/me/v11/devices'
SNOO_BABY_ENDPOINT = SNOO_API_URI + '/us/me/v10/baby'
SNOO_SESSIONS_LAST_ENDPOINT = SNOO_API_URI + '/ss/me/v10/babies/{}/sessions/last'
SNOO_SESSIONS_AGGREGATED_AVG_ENDPOINT = SNOO_API_URI + '/ss/v2/babies/{}/sessions/aggregated/avg/'
SNOO_SESSIONS_TOTAL_TIME_ENDPOINT = SNOO_API_URI + '/ss/v2/babies/{}/sessions/total-time/'

# Snoo Pubnub Variables
SNOO_PUBNUB_SUBSCRIBE_KEY = "sub-c-97bade2a-483d-11e6-8b3b-02ee2ddab7fe"
SNOO_PUBNUB_PUBLISH_KEY = "pub-c-699074b0-7664-4be2-abf8-dcbb9b6cd2bf"
SNOO_PUBNUB_ORIGIN = "happiestbaby.pubnubapi.com"
SNOO_PUBNUB_AUTH_URL = SNOO_API_URI + '/us/me/v10/pubnub/authorize'

DATETIME_FMT_AGGREGATED_SESSION = '%Y-%m-%d %H:%M:%S.%f'
