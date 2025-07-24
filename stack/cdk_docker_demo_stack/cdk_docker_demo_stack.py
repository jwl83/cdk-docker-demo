import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_ecr_assets as _ecr_assets,
    aws_ecr as _ecr,
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

        # Destination ECR repository
        ecr_repo = _ecr.Repository(
            self,
            "CdkEcrRepo",
            repository_name="cdk-docker-demo",
        )

        # Copy from cdk docker image asset to another ECR.
        ecrdeploy.ECRDeployment(
            self,
            "CDKDockerImageDeployment",
            src=ecrdeploy.DockerImageName(image.image_uri),
            dest=ecrdeploy.DockerImageName(f"{ecr_repo.repository_uri}:stable") 
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

        # TODO: Use this instead of from_image_asset()
        _lambda.DockerImageCode.from_ecr(
            repository=ecr_repo,
            tag="latest",
        )

        _apigateway.LambdaRestApi(
            self,
            'Endpoint',
            handler=hello_handler,
        )
