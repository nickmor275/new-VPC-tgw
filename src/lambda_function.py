# Any code, applications, scripts, templates, proofs of concept, documentation
# and other items provided by AWS under this SOW are "AWS Content,"" as defined
# in the Agreement, and are provided for illustration purposes only. All such
# AWS Content is provided solely at the option of AWS, and is subject to the
# terms of the Addendum and the Agreement. Customer is solely responsible for
# using, deploying, testing, and supporting any code and applications provided
# by AWS under this SOW.
#
# (c) 2019 Amazon Web Services

import os
import logging
import json
import boto3
import cfnresponse
import urllib3
from botocore.exceptions import ClientError

# Instanciate low level boto3
client = boto3.resource('ec2')

# Configure logging
LOGGER = logging.getLogger(__name__)
DEBUG_MODE = os.getenv('DEBUG_MODE', 'true')
if DEBUG_MODE == 'true':
    LOGGER.setLevel(logging.DEBUG)
else:
    LOGGER.setLevel(logging.INFO)


def lambda_handler(event, context):
    """ Lambda Function for command execution """
    LOGGER.info("Received event: " + json.dumps(event, indent=2))

    request_type = event['RequestType']
    if request_type == 'Create':
        _create_route(event, context)
    elif request_type == 'Delete':
        _delete_route(event, context)
    elif request_type == 'Update':
        _update_route(event, context)


def _create_route(event, context):
    status = cfnresponse.FAILED
    data = {}
    physical_resource_id = None

    try:
        # Retrieve data from event
        RouteTableId = event['ResourceProperties']['RouteTableId']
        DestinationCidrBlock = event['ResourceProperties']['DestinationCidrBlock']
        TransitGatewayId = event['ResourceProperties']['TransitGatewayId']

        LOGGER.info("Boto3 version: " + boto3.__version__)
        LOGGER.info("DestinationCidrBlock: " + DestinationCidrBlock)
        LOGGER.info("RouteTableId: " + RouteTableId)
        LOGGER.info("TransitGatewayId: " + TransitGatewayId)

        route_table = client.RouteTable(RouteTableId)
        route_table.create_route(
            DestinationCidrBlock=DestinationCidrBlock,
            TransitGatewayId=TransitGatewayId,
        )

        if route_table:
            # Set status and physical id
            status = cfnresponse.SUCCESS
            physical_resource_id = f"{RouteTableId}-{DestinationCidrBlock}-{TransitGatewayId}"

            # Set output data
            data = {
                "ResourceId": f"{RouteTableId}-{DestinationCidrBlock}-{TransitGatewayId}"
            }

    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=physical_resource_id)

def _update_route(event, context):
    return _create_route(event, context)

def _delete_route(event, context):

    status = cfnresponse.FAILED
    data = {}
    physical_resource_id = None

    try:
        # Retrieve data from event
        RouteTableId = event['ResourceProperties']['RouteTableId']
        DestinationCidrBlock = event['ResourceProperties']['DestinationCidrBlock']
        TransitGatewayId = event['ResourceProperties']['TransitGatewayId']

        route = client.Route(RouteTableId, DestinationCidrBlock)
        route.delete()

        if route:
            # Set status and physical id
            status = cfnresponse.SUCCESS
            physical_resource_id = f"{RouteTableId}-{DestinationCidrBlock}-{TransitGatewayId}"

            # Set output data
            data = {
                "ResourceId": f"{RouteTableId}-{DestinationCidrBlock}-{TransitGatewayId}"
            }

    except BaseException as ex:
        LOGGER.exception(ex)

    finally:
        cfnresponse.send(event=event, context=context, responseStatus=status, responseData=data,
                         physicalResourceId=physical_resource_id)
