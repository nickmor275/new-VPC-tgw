#!/bin/bash
#EC2RouteTGW_scripts.sh

# Any code, applications, scripts, templates, proofs of concept, documentation
# and other items provided by AWS under this SOW are "AWS Content,"" as defined
# in the Agreement, and are provided for illustration purposes only. All such
# AWS Content is provided solely at the option of AWS, and is subject to the
# terms of the Addendum and the Agreement. Customer is solely responsible for
# using, deploying, testing, and supporting any code and applications provided
# by AWS under this SOW.
#
# (c) 2019 Amazon Web Services

PROFILE_NAME="account2"
TEMPLATE="NewVPCtgw"
TEMPLATE_DEPLOY="$TEMPLATE-deploy"
STACK_NAME="TestVPC"
S3_BUCKET="account2-vpc-tgw-test"
S3_PREFIX="ec2routetgw"

# Parameters
VPCCIDR="10.42.0.0/16"
SNCIDR="10.42.0.0/16"
TGWCIDR1="10.0.0.0/16"
TGWCIDR2="10.20.0.0/16"
TGWCIDR3="10.30.0.0/16"
TGWCIDR4="10.40.0.0/16"
TGWCIDR5="10.50.0.0/16"
TGWCIDR6="10.60.0.0/16"
TGWCIDR7="192.168.128.0/16"
MyTransitGateway="tgw-00d4d654b468abf85"


# Package
aws cloudformation package \
--profile $PROFILE_NAME \
--template-file $TEMPLATE.yml \
--s3-bucket $S3_BUCKET \
--s3-prefix $S3_PREFIX \
--output-template-file $TEMPLATE_DEPLOY.yml

# Deploy
aws cloudformation deploy \
--profile $PROFILE_NAME \
--template-file $TEMPLATE_DEPLOY.yml \
--stack-name $STACK_NAME \
--capabilities CAPABILITY_NAMED_IAM \
--parameter-overrides \
VPCCIDR=$VPCCIDR \
SubnetCIDR=$SNCIDR \
TGWCIDR1=$TGWCIDR1 \
TGWCIDR2=$TGWCIDR2 \
TGWCIDR3=$TGWCIDR3 \
TGWCIDR4=$TGWCIDR4 \
TGWCIDR5=$TGWCIDR5 \
TGWCIDR6=$TGWCIDR6 \
TGWCIDR7=$TGWCIDR7 \
MyTransitGateway=$MyTransitGateway
