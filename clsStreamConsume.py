##############################################
#### Written By: SATYAKI DE               ####
#### Written On: 26-Jul-2021              ####
#### Modified On 08-Sep-2021              ####
####                                      ####
#### Objective: Consuming Streaming data  ####
#### from Ably channels published by the  ####
#### playIOTDevice.py                     ####
####                                      ####
##############################################

import json
from clsConfigClient import clsConfigClient as cf
import requests
import logging
import time
import pandas as pd
import clsL as cl
import base64

# Initiating Log class
l = cl.clsL()
df_conv = pd.DataFrame()

class clsStreamConsume:
    def __init__(self):
        self.appType = cf.conf['appType']
        self.ably_id = str(cf.conf['ABLY_ID'])
        self.ably_url = str(cf.conf['ABLY_READ_URL'])
        self.channel_name = str(cf.conf['CHANNEL_NAME'])

    def conStream(self, varVa, debugInd):
        try:
            appType = self.appType
            ably_id = self.ably_id
            ably_url = self.ably_url
            channel_name = self.channel_name

            var = varVa
            debug_ind = debugInd

            df = pd.DataFrame()
            temp_df = pd.DataFrame()
            corrected_data = ''

            response = ''
            value = ''

            url = ably_url

            # Headers including the Authorization
            headers = {
                'Authorization': f'Basic ' + base64.b64encode(ably_id.encode('utf-8')).decode('utf-8'),
                'Content-Type': appType,
            }

            # Keep the program running to listen for messages.
            # In real applications, consider a more robust way to manage the lifecycle.
            # Make the GET request to fetch the history
            response = requests.get(url, headers=headers)

            # Check the response
            data = json.loads(response.text)

            # Check if the data is a list
            if isinstance(data, list):
                # Iterate over each item in the list
                for item in data:
                    # If the item is a dictionary, you can then iterate over its key-value pairs
                    if isinstance(item, dict):
                        for key, value in item.items():
                            print(f'Key: {key}, Value: {value}')
                            if key == 'data':
                                value = value.replace("'", '"')
                                corrected_data = value
                    else:
                        # If the item is not a dictionary, handle accordingly (e.g., print it)
                        print(item)
            elif isinstance(data, dict):
                # If the data is a dictionary, iterate over its key-value pairs
                for key, value in data.items():
                    print(f'Key: {key}, Value: {value}')
                    if key == 'data':
                        value = value.replace("'", '"')
                        corrected_data = value
            else:
                # If the data is neither a list nor a dictionary, handle accordingly
                print(data)

            parsed_dict = json.loads(corrected_data)
            temp_df = pd.DataFrame.from_dict(parsed_dict, orient='index')
            df = pd.concat([df, temp_df], ignore_index=True)

            return df

        except Exception as e:

            x = str(e)
            print('Error: ', x)

            logging.info(x)

            # This will handle the error scenaio as well.
            # Based on that, it will capture the old events
            # from cache.

            df = pd.DataFrame()

            return df
