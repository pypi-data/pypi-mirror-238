# deutils
deutils offeres a set of commonly used python fuctions for use with Glue Jobs and Lambda.

# Functions

## get_secret(secret_name, region):
This function allows the look up of a sceret from aws secrets manager. It returns the key value pairs in a dictionary object.

## delogging
Several small helper functions for formatting logs. Right now its simple prints but it will extend to write to 
CloudWatch.

## s3_helper
The functions aggregate base functions into composite calls. For instance combining get_secret with connect_to_ftp. 
The new function get_ftp_connection_from_secret takes a secret as an input and returns a ftp connection to minimise
lines of code in the users call.

When you need to build a layer: https://awstip.com/create-aws-lambda-layers-using-cloud-9-694895903ca5

### Change Log:
| User       | Date       | Comment                                                                     |
|------------|------------|-----------------------------------------------------------------------------|
| ffortunato | 11/01/2023 | Describing Overall package.        |
  

[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)