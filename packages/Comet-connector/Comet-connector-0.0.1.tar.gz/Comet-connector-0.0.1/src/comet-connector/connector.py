# Base
import pandas as pd
import requests
from pandas import json_normalize

def getResults(list_token_api):

  URL_API_BASE = "https://latam.analyticom.de/data-backend/api/public/areports/run"

  registros = pd.DataFrame()
  bandera=1000
  page=0
  
  for token_api in list_token_api:
    API_KEY = token_api
    
    params_json={'API_KEY':API_KEY}
    data_json={'API_KEY':API_KEY}

    while(bandera==1000):
      url='/'+str(page)+'/1000/'
      # objJson = getResults('/'+str(page)+'/1000/',{'API_KEY':API_KEY},{'API_KEY':API_KEY})
      response_data=''
      try:
          str_url = URL_API_BASE + url
          headersAPI = {'accept': 'application/json'}

          if data_json != {} and params_json!={}:
            response=requests.get(str_url,headers=headersAPI,params=params_json,data=data_json)
            response_data=response.json()
          elif data_json != {}:
            response=requests.get(str_url,headers=headersAPI,data=data_json)
            response_data=response.json()
          elif params_json != {}:
            response=requests.get(str_url,headers=headersAPI,params=params_json)
            response_data=response.json()
          else:
            response=requests.get(str_url,headers=headersAPI)
            response_data=response.json()

          if 'error' in response_data:
              raise Exception(f"{response_data['error']['message']}")
      except Exception as error:
          print(f"ERROR {error} in API {URL_API_BASE}")
          print(f"ERROR in API {URL_API_BASE}")

      objJson = response_data
    
      ed = json_normalize(objJson['results'])
      bandera=len(ed)
      page=page+1
      registros = pd.concat([registros,ed])

  return registros





# list_token_api = ['4687741a14aad7a49c56ed37efaff4f719c8df4e88007b5c2d8e91dd6e29b7f4f208c8e3e6b8aba6883d579fb8c3c717dd79e2e4e51275139839ef5ba7251a8f']
# df_results = getResults(list_token_api)