#!/user/bin/env python3 
"""
uniboost.py: This program is used for Rancher purposes.
Requirements: python2.7 or later.
"""

__author__ = "Michael Shobitan"
__copyright__ = "Copyright 2019, BTCS Platform Engineering"
__credits__ = ["Michael Shobitan"]
__license__ = "PFE"
__maintainer__ = "Michael Shobitan"
__email__ = "michael.shobitan@pfizer.com"
__status__ = "Development"
# __version__ = "0.7.3"

import os
import re
import sys
import json
import time
import boto3
import base64
import atexit
import shutil
import urllib3
import argparse
import requests
import warnings
import subprocess
import boto.ec2.autoscale
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

headers = {'Content-type':'application/json'}

def exampleFunc():
    """ 
    Summary line. 
  
    Extended description of function. 
  
    Parameters: 
    arg1 (int): Description of arg1 
  
    Returns: 
    int: Description of return value 
    """

    pass


def latest():
    script = subprocess.Popen(["pip", "install", "uniboost", "-U"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    this_out, this_err = script.communicate()
    return this_out

def clusterInfo(url, key, secret):
    response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
    binary = response.content
    output = json.loads(binary)

    return {'response': response, 'binary': binary, 'output': output}

target_dir = '/opt/pfizer/etc/rancher-api'
this_target_dir = '/opt/pfizer/etc'
full_target_dir = '/opt/pfizer/etc/rancher-api/config_files/'

aws_credentials_file_path = '/opt/pfizer/etc/rancher-api/config_files/rancher2AWSVariables'
with open(aws_credentials_file_path) as json_file:
    aws_credentials_file = json.load(json_file)

def set_env_var(var_name, var_value):
    os.environ[var_name] = var_value
    
def get_env_var(var_name):
    path = os.environ[var_name]
    return path

def file_to_json(json_file):
    with open(json_file, 'r') as handle:
        parsed = json.load(handle)
    return parsed

def jsonPP(json_content):
    response = json.dumps(json_content, indent=4)
    return response

def ppJSON(json_content):
    response = json.dumps(json_content, indent=4, sort_keys=True, default=str)
    return response

def cd(cd_dir):
    os.chdir(cd_dir)

def pwd():
    cwd = os.getcwd()
    return cwd

def file_exist(this_file):
    status = os.path.exists(this_file)
    if(status == True):
        if(os.path.isdir(this_file)):
            file_type = 'directory'
            # print(file_type)
        elif(os.path.isfile(this_file)):  
            file_type = 'file'
            # print(file_type)
        else:
            print("It is a special file (socket, FIFO, device file, etc.)" )
        status = 'exist'
    else:
        file_type = status
        status = status

    return {'file_type': file_type, 'status': status}

def delete_folder(folder_name):
    try:
        os.rmdir(folder_name)
    except OSError:
        print ("NOTE: Deletion of the directory %s failed" % folder_name + "\n")
    else:
        print ("NOTE: Successfully deleted the directory %s" % folder_name)

# def cluster_deletion():
#     env_clusters_url = env_url + "/clusters"
#     # projects_request = UrlRequest(env_clusters_url, key, secret)
#     # output = projects_request.output
        
#     response = requests.get(env_clusters_url, auth=(key, secret), headers=headers, verify=False)
#     binary = response.content
#     output = json.loads(binary)

#     for counter in range(len(output['data'])):
#         cluster_name = output['data'][counter]['name']           
#         if(folder_name == cluster_name):
#             cluster_id = output['data'][counter]['id']
#             cluster_delete_url = "%s/%s" % (env_clusters_url, cluster_id)
#             cluster_delete_url = cluster_delete_url[:4] + 's' + cluster_delete_url[4:]
#             cluster_delete_url = "curl -u \"%s:%s\" -X DELETE -H 'Accept: application/json' '%s'" % (key, secret, cluster_delete_url)
#             p = subprocess.Popen([cluster_delete_url], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#             out, err = p.communicate()

# cluster_detected =  False
# def cluster_detection(url):
#     global cluster_detected
#     url = url + "/clusters"
#     # projects_request = UrlRequest(env_clusters_url, key, secret)
#     # output = projects_request.output
        
#     response = requests.get(url, auth=(key, secret), headers=headers, verify=False)
#     binary = response.content
#     output = json.loads(binary)

#     for counter in range(len(output['data'])):
#         cluster_name = output['data'][counter]['name']           
#         if(folder_name == cluster_name):
#             cluster_id = output['data'][counter]['id']
#             cluster_detected = True
#             print("ERROR: Cluster already exist!")
#             cd(folder_name)
#             shutil.rmtree(folder_name, ignore_errors=True)
#             print('NOTE: Cluster folder cleaning complete')
#             # cluster_deletion()
#             sys.exit()

# cluster_detection()        

# def awsAPIConnection():
#     conn = boto.ec2.autoscale.connect_to_region(get_env_var('AWS_REGION'),
#     aws_access_key_id=get_env_var('AWS_ACCESS_KEY_ID'),
#     aws_secret_access_key=get_env_var('AWS_SECRET_ACCESS_KEY'))
#     return conn

def base64Decoder(coded_string):
    # Ensure the coded_string has correct padding
    missing_padding = len(coded_string) % 4
    if missing_padding:
        coded_string += '=' * (4 - missing_padding)
    try:
        decoded_string = base64.b64decode(coded_string).decode('utf-8', 'ignore')
        return decoded_string
    except Exception as e:
        print('Failed to decode base64 string: {}'.format(e))
        raise  # re-raise the exception to propagate it up the call stack

def awsAPIConnection(aws_account): # This one
    os.environ['AWS_ACCESS_KEY_ID'] = base64Decoder(aws_credentials_file[aws_account]['us-east-1']['key'])
    os.environ['AWS_SECRET_ACCESS_KEY'] = base64Decoder(aws_credentials_file[aws_account]['us-east-1']['secret'])
    os.environ['AWS_DEFAULT_OUTPUT'] = "json"
    os.environ['AWS_REGION'] = "us-east-1"
    os.environ['AWS_DEFAULT_REGION'] = "us-east-1"

    conn = boto.ec2.autoscale.connect_to_region(os.environ['AWS_REGION'],
    aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
    aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'])
    return conn

def get_cluster_region(cluster_name, aws_account='330470878083', credentials_file=aws_credentials_file):
    conn = awsAPIConnection(aws_account)

    client = boto3.client('ec2')
    regions = [region['RegionName'] for region in client.describe_regions()['Regions']]
   
    regionData = {}
    for region in regions:
        regionData.update( {region : []} )

    for region in regions:
        try:
            eks = boto3.client(
                'eks',
                aws_access_key_id = base64Decoder(credentials_file[aws_account][region]['key']),
                aws_secret_access_key = base64Decoder(credentials_file[aws_account][region]['secret']),
                region_name=region
            )

            try:
                def describeClusterEKS():
                    response = eks.describe_cluster(name=cluster_name)
    
                    return region
    
                clusters_region = describeClusterEKS()
            except:
                pass
        except KeyError as e:
            # handle key errors you want
            if e.args[0] in regions:
                # print(e.args[0])
                # print('handled!')
                pass
            # reraise the exception if not handled
            else:
                raise
        except TypeError as e:
            pass

    return clusters_region

# Global variable to hold the client object
client = None
def connect_to_aws_service(service_name, region_name='us-east-1', aws_account='330470878083', credentials_file=aws_credentials_file):
    global client  # Declare client as global so we can replace it
    
    aws_access_key_id = base64Decoder(credentials_file[aws_account][region_name]['key'])
    aws_secret_access_key = base64Decoder(credentials_file[aws_account][region_name]['secret'])

    try:
        try:
            session = boto3.Session(
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key,
                region_name=region_name
            )
            client = session.client(service_name)
        except:
            # client = boto3.client(service_name, region_name=region_name)
            client = boto3.client(
                service_name,
                region_name = region_name,
                aws_access_key_id = aws_access_key_id,
                aws_secret_access_key = aws_secret_access_key
            )
        return client
    except Exception as e:
        # print(f'Failed to create client for {service_name}: {e}')
        print('Failed to create client for {}: {}'.format(service_name, e))
        raise

def eks():
    eks = boto3.client('eks')
    return eks

def describe_cluster(eks, cluster):
    response = eks.describe_cluster(
        name=cluster
    )
    return response

def cloudformation():
    cloudformation = boto3.client('cloudformation')
    return cloudformation

def describe_stack(cloudformation, cluster):
    stack_name = "%s-eks-worker-nodes" % (cluster)
    response = cloudformation.describe_stacks(
        StackName=stack_name,
    )
    return response

def describe_stack_dynamically(cloudformation, cluster):
    response = cloudformation.describe_stacks()
    try:
        responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
        allResponses = [response, responseMore]
    except:
        allResponses = [response]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)
    
    clusterStackNames.append(allStackData[0])
    stacksINFO.append(allStackData[1])
    
    # if(len(clusterStackNames > 0)):
    if(clusterStackNames):
        return {'clusterStackNames': clusterStackNames, 'stacksINFO': stacksINFO}
    
    response = cloudformation.describe_stacks()
    responseMore = cloudformation.describe_stacks(NextToken=response['NextToken'])
    allResponses = [response, responseMore]

    clusterStackNames = []
    stacksINFO = []
    def aggregateAllStackInfo(response):
        clusterStackNames = []
        stacksINFO = []
        if(sys.version_info > (3, 0)):
            for counter in range(len(response['Stacks'])): # Python3.6
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))
        else:
            for counter in xrange(len(response['Stacks'])): # Python2.7
                stackName = response['Stacks'][counter]['StackName']
                if(cluster in stackName):
                    clusterStackNames.append(stackName)
                    # print(response['Stacks'][counter])
                    stacksINFO.append(response['Stacks'][counter])
                    # print(json.dumps(response['Stacks'][counter], indent=4, sort_keys=True, default=str))

        # print(clusterStackNames)
        return clusterStackNames, stacksINFO

    for thisResponse in allResponses:
        allStackData = aggregateAllStackInfo(thisResponse)
        # print(allStackData)
        clusterStackNames.append(allStackData[0])
        stacksINFO.append(allStackData[1])

    clusterStackNames = [x for x in clusterStackNames if x != []]
    clusterStackNamesCleaned = []
    for stack in clusterStackNames:
        stack = stack[0]
        # print(stack)
        clusterStackNamesCleaned.append(stack)
    # print(clusterStackNamesCleaned)

    stacksINFO = [x for x in stacksINFO if x != []]
    stacksINFOCleaned = []
    for stack in stacksINFO:
        stack = stack[0]
        # print(stack)
        stacksINFOCleaned.append(stack)
    # print(stacksINFOCleaned)
    
    return {'clusterStackNames': clusterStackNamesCleaned, 'stacksINFO': stacksINFOCleaned}

def cahc(cluster):
    eks = eks()
    clusterINFO = describe_cluster(eks, cluster)
    # Enabled
    privateAccess = clusterINFO['cluster']['resourcesVpcConfig']['endpointPrivateAccess']
    # Disabled
    publicAccess = clusterINFO['cluster']['resourcesVpcConfig']['endpointPublicAccess']

    cloudformation = cloudformation()
    clusterStackINFO = describe_stack(cloudformation, cluster)
    for instance in xrange(len(clusterStackINFO['Stacks'][0]['Parameters'])):
        parameterKey = (clusterStackINFO['Stacks'][0]['Parameters'][instance]['ParameterKey'])
        if(parameterKey == 'PublicIp'):
            # False
            PulicIpValue = (clusterStackINFO['Stacks'][0]['Parameters'][instance]['ParameterValue'])
    
    return {'privateAccess': privateAccess, 'publicAccess': publicAccess, 'PulicIpValue': PulicIpValue}

def times():
    day = time.strftime("%A")
    month = time.strftime("%B")
    date = time.strftime("%d %H:%M:%S")
    year = time.strftime("%Y")

    return {'day': day, 'month': month, 'date': date, 'year': year}

printLogMsg = False
def logger(logFile, logMsg, printLogMsg, newLine):
    """ 
    Logger for calling program. 
    
    Parameters:
    logFile (str): File to be logged to
    logMsg (str): Message to be logged
    printLogMsg (bool): Option to print log message
    newLine (str): Option to prepend newline to the top, both or bottom only
  
    Returns: 
    int: Description of return value 
    """

    if(printLogMsg is True):
        print(logMsg)

    program = sys.argv[0]
    program = program.rsplit('/', 1)[-1]\
    
    if(newLine == 'top'):
        logFile.write('\n' + str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg))    
    elif(newLine == 'both'):
        logFile.write('\n' + str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg) + '\n')   
    elif(newLine == 'bottom'):
        logFile.write(str(program) + " " + str(times()['day'][:3]) + " " + str(times()['month'][:3]) + " " + str(times()['date']) + " " + str(time.tzname[0]) + " " + str(times()['year']) + " - " + str(logMsg) + '\n')