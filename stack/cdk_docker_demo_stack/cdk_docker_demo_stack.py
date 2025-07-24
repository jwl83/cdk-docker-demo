import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_ecr_assets as _ecr_assets,
)
from aws_cdk.aws_ecr_assets import DockerImageAsset
import cdk_ecr_deployment as ecrdeploy
from constructs import Construct

class CdkDockerDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # hello_handler = _lambda.Function(
        #     self,
        #     'HelloHandler',
        #     runtime=_lambda.Runtime.PYTHON_3_13,
        #     code=_lambda.Code.from_asset('src/cdk_docker_demo'),
        #     handler='hello.handler',
        # )

        # code_image = _lambda.DockerImageCode.from_image_asset(
        #     directory="src",
        #     cmd=["cdk_docker_demo.hello.handler"],
        #     platform=_ecr_assets.Platform.LINUX_AMD64,
        # ),

        image = DockerImageAsset(self, "CDKDockerImageSrc",
            directory="src",
            # cmd=["cdk_docker_demo.hello.handler"],
            platform=_ecr_assets.Platform.LINUX_AMD64,
        )

        # TODO: Create destination ECR repository if it doesn't exist

        # Copy from cdk docker image asset to another ECR.
        ecrdeploy.ECRDeployment(self, "CDKDockerImageDeployment",
            src=ecrdeploy.DockerImageName(image.image_uri),
            dest=ecrdeploy.DockerImageName(f"{cdk.Aws.ACCOUNT_ID}.dkr.ecr.eu-west-1.amazonaws.com/cdk-docker-demo:latest")
        )

        hello_handler = _lambda.DockerImageFunction(
            self,
            'HelloDockerHandler',
            code=_lambda.DockerImageCode.from_image_asset(
                directory="src",
                cmd=["cdk_docker_demo.hello.handler"],
                platform=_ecr_assets.Platform.LINUX_AMD64,
            ),
        )

        _apigateway.LambdaRestApi(
            self,
            'Endpoint',
            handler=hello_handler,
        )
