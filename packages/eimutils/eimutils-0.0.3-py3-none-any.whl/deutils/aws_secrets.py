"""
*******************************************************************************
File: aws_secrets.py

Purpose: Gets secret values from AWS Secrets.

Dependencies/Helpful Notes :

*******************************************************************************
"""
# Use this code snippet in your app.
# If you need more information about configurations or implementing the sample code, visit the AWS docs:
# https://aws.amazon.com/developers/getting-started/python/

import boto3
import json
from botocore.exceptions import ClientError
import base64

"""
*******************************************************************************
Function: get_secret

Purpose: Gets AWS secret data.

Parameters:
     secret_name - AWS secret name from the account the process is running in
                   that contains the db connection information.  

Calls:

Called by:

Returns: dictionary of secret values

*******************************************************************************
"""


def get_secret(secret_name):
    
    #ToDo: Pass region name as a parameter.
    region_name = "us-west-2"
    
    # Create a Secrets Manager client
    try:
        session = boto3.session.Session()
        client = session.client(
            service_name='secretsmanager',
            region_name=region_name
        )
    except Exception as e:
        print(__name__, ' :: ', e)
        raise e

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            print(__name__, ' :: ', e)
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            print(__name__, ' :: ', e)
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            print(__name__, ' :: ', e)
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            print(__name__, ' :: ', e)
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            print(__name__, ' :: ', e)
            raise e
        else:
            print(__name__, ' :: ', e)
            raise e
    except Exception as e:
        print(__name__, ' :: ', e)
        raise e
    """
    else:
        get_secret_value_response = "Failed to get secret"
    """
    """
    else:
        # Decrypts secret using the associated KMS key.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
    """
    # Your code goes here.

    connection_parms = json.loads(get_secret_value_response["SecretString"])

    return connection_parms

def getSecrets(srcPS, srcArn):
    print(
        "============================================\nParameters and Secrets\n============================================\n")
    if srcPS == "params":
        try:
            print("SSM Parameters Store Checks")
            # latest_string_token = ssm.StringParameter.value_for_string_parameter(self, srcKey)
            # latest_string_token = ssm.StringParameter.value_for_string_parameter(self, srcKey, srcVer)
            # secure_string_token = ssm.StringParameter.value_for_secure_string_parameter(self, srcSecret, srcVer)
        except:
            print("An error occurred")
    elif srcPS == "secrets":
        secret_name = srcArn  # "eim_de_poc_exakeys"
        region_name = "us-west-2"
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager', region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        except ClientError as e:
            if e.response['Error']['Code'] == 'DecryptionFailureException':
                print("Secrets Manager can't decrypt the protected secret text using the provided KMS key.")
                raise e
            elif e.response['Error']['Code'] == 'InternalServiceErrorException':
                print("An error occurred on the server side.")
                raise e
            elif e.response['Error']['Code'] == 'InvalidParameterException':
                print("You provided an invalid value for a parameter")
                raise e
            elif e.response['Error']['Code'] == 'InvalidRequestException':
                print("You provided a parameter value that is not valid for the current state of the resource.")
                raise e
            elif e.response['Error']['Code'] == 'ResourceNotFoundException':
                print("We can't find the resource that you asked for.")
                raise e
        else:
            if 'SecretString' in get_secret_value_response:
                print("Retrieving Secret String")
                secret = get_secret_value_response['SecretString']
                return secret
            else:
                print("Retrieving Secret Binary")
                decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
                return decoded_binary_secret
    else:
        print("Please either use 'params' or 'secrets'")

"""
*******************************************************************************
Change History:

Author		Date		Description
----------	----------	-------------------------------------------------------
ffortunato  11/1/2023   + new flavor of get secrets: getSecrets(srcPS, srcArn):
*******************************************************************************
"""