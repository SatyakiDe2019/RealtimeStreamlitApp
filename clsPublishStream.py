###############################################################
####                                                       ####
#### Written By: Satyaki De                                ####
#### Written Date:  26-Jul-2021                            ####
#### Modified Date: 08-Sep-2021                            ####
####                                                       ####
#### Objective: This script will publish real-time         ####
#### streaming data coming out from a hosted API           ####
#### sources using another popular third-party service     ####
#### named Ably. Ably mimics pubsub Streaming concept,     ####
#### which might be extremely useful for any start-ups.    ####
####                                                       ####
###############################################################

#from ably import AblyRest
import logging
import json
import base64

from random import seed
from random import random

import json
import math
import random
import requests

from clsConfigClient import clsConfigClient as cf

# Disbling Warning
def warn(*args, **kwargs):
    pass

import warnings
warnings.warn = warn

seed(1)

# Global Section

logger = logging.getLogger('ably')
logger.addHandler(logging.StreamHandler())

#ably_id = str(cf.conf['ABLY_ID'])


#ably = AblyRest(ably_id)
#channel = ably.channels.get('sd_channel')
#channel.attach()

# End Of Global Section

class clsPublishStream:
    def __init__(self):
        self.appType = cf.conf['appType']
        self.ably_id = str(cf.conf['ABLY_ID'])
        self.ably_url = str(cf.conf['ABLY_URL'])

    def pushEvents(self, srcJSON, debugInd, varVa):
        try:
            ably_id = self.ably_id
            ably_url = self.ably_url

            url = ably_url + ably_id

            appType = self.appType

            #headers = {'Content-Type': appType}
            headers = {'Authorization': 'Basic ' + base64.b64encode(ably_id.encode()).decode(),
            'Content-Type': appType,}

            # The message you want to publish, including the event name and data
            message = {
                'name': 'saty_event',  # The event name you want to use
                'data': srcJSON
            }


            # Capturing the inbound dataframe
            jdata_fin = json.dumps(message)

            print('IOT Events: ')
            print(str(jdata_fin))

            # Publish rest of the messages to the sd_channel channel
            #channel.publish('event', jdata_fin)
            response = requests.request("POST", url, headers=headers, data=jdata_fin)

            jdata_fin = ''
            message = ''

            #channel.detach()

            return 0

        except Exception as e:

            x = str(e)
            print(x)

            logging.info(x)

            #channel.detach()

            return 1
