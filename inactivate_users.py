import procore_cpg_app_authentication as pca
import procore_api_calls as pac
import pandas as pd
import datetime
import pytz
from pprint import pprint

''' This script removes any users from the company directory which 
    have not logged in within the past year or who have never logged in.'''

credentials, base_url = pca.get_oauth_access()

active_users = pac.get_company_active_users(credentials['access_token'], base_url)
pprint(active_users)
utc = pytz.UTC
one_year_ago = datetime.datetime.now() - datetime.timedelta(days=1*365)

one_year_ago = utc.localize(one_year_ago)

users_to_remove = []
for user in active_users:

    new_date = pd.to_datetime(user['last_login_at'])

    if isinstance(new_date, type(None)) == False:
        if new_date < one_year_ago:
            # user hasn't logged in in over a year, removing them
            users_to_remove.append(user)
    else:
        # user has never logged in
        created_date = pd.to_datetime(user['created_at'])
        if created_date < one_year_ago:
            # users account was not created in the last year
            users_to_remove.append(user)


company_id = pac.get_company_id(credentials['access_token'], base_url)

payload = {'updates':[]}
for index, user in enumerate(users_to_remove):
    id = user['id']
    payload['updates'].append({'id': user['id'], 'is_active': False})
    if index % 50 == 0:
        pac.inactivate_user(credentials['access_token'], base_url, company_id, payload)
        payload = {'updates':[]}
        print(f'{round(index / len(users_to_remove), 2) * 100}% done')

pac.inactivate_user(credentials['access_token'], base_url, company_id, payload)






