"""
********************************************************************************
File:		deUtils/delogging/delogging.py
Name:		delogging
Purpose:	Logg to all sorts of different places.
Author:		ffortunato
Date:		20220401
********************************************************************************
"""

#imports

# Public Packages
from datetime import  timedelta, date, datetime
from datadog import initialize, api
import time

"""
********************************************************************************
Name:		log_to_console
Purpose:	Log to all sorts of different places.
Example:	log_to_console(__name__,'Info','I\'m good enough.')
Parameters:    
Called by:	
Calls:          
Errors:		
Author:		ffortunato
Date:		20220401
********************************************************************************
"""


def log_to_console(function_name, message_type, message):

    current_time = datetime.today().strftime('%Y-%b-%d %H:%M:%S')

    try:
        # print(current_time + ',' + function_name + ',' + message_type + ',' + message)
        print(current_time, ',', function_name, ',', message_type, ',', message)
    except Exception as e:
        print("Unable to Log!", e)

"""
********************************************************************************
Name:		datadogSendMetric
Purpose:	Log to all sorts of different places.
Example:	datadogSendMetric(__name__,'Info','I\'m good enough.')
Parameters:    
Called by:	
Calls:          
Errors:		
Author:		ffortunato
Date:		20220401
********************************************************************************
"""

def datadogSendMetric(api_key, app_key, job_name, env, success):
    options = {
        "api_key": api_key,
        "app_key": app_key,
    }

    initialize(**options)

    now = int(time.time())
    tags = [f'success:{success}', 'department:EIM', f'jobname:{job_name}', f'env:{env.lower()}']
    metrics = [{'metric': 'kaena.glue_job_runs', 'type': 'count', 'points': [(now, 1)], 'tags': tags}]
    api.Metric.send(metrics=metrics)

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
ffortunato  04/14/2022  Initial Iteration.
ffortunato  11/01/2023  Adding Data Dog logging.

*******************************************************************************
"""