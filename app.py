#!/usr/bin/env python3
import os

from aws_cdk import (
    App,
    aws_s3 as _s3,
    app_staging_synthesizer_alpha as _synth,
)

from cdk_docker_demo_stack.cdk_docker_demo_stack import CdkDockerDemoStack


app = App(
    default_stack_synthesizer=_synth.AppStagingSynthesizer.default_resources(
        app_id="cdk-docker-demo-app",
        staging_bucket_encryption=_s3.BucketEncryption.S3_MANAGED,
    )
)

CdkDockerDemoStack(app, "CdkDockerDemoStack",
    # If you don't specify 'env', this stack will be environment-agnostic.
    # Account/Region-dependent features and context lookups will not work,
    # but a single synthesized template can be deployed anywhere.

    # Uncomment the next line to specialize this stack for the AWS Account
    # and Region that are implied by the current CLI configuration.

    #env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

    # Uncomment the next line if you know exactly what Account and Region you
    # want to deploy the stack to. */

    #env=cdk.Environment(account='123456789012', region='us-east-1'),

    # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
    )

app.synth()
