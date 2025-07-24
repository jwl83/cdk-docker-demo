import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_ecr_assets as _ecr_assets,
    aws_ecr as _ecr,
)
import cdk_ecr_deployment as ecrdeploy
from constructs import Construct

class CdkDockerDemoStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        TAG_NAME = "stable"

        # Destination ECR repository
        ecr_repo = _ecr.Repository(
            self,
            "CdkEcrRepo",
            repository_name="cdk-docker-demo",
        )

        # Create a Docker image asset from the source directory
        image_asset = _ecr_assets.DockerImageAsset(
            self,
            "CDKDockerImageSrc",
            directory="src",
            platform=_ecr_assets.Platform.LINUX_AMD64,
            asset_name="cdk-docker-demo--asset-name",
        )

        # Copy from cdk docker image asset to another ECR.
        ecrdeploy.ECRDeployment(
            self,
            "CDKDockerImageDeployment",
            src=ecrdeploy.DockerImageName(image_asset.image_uri),
            dest=ecrdeploy.DockerImageName(f"{ecr_repo.repository_uri}:{TAG_NAME}"), 
        )

        hello_handler = _lambda.DockerImageFunction(
            self,
            'HelloDockerHandler',
            # code=_lambda.DockerImageCode.from_ecr(
            #     repository=image_asset.repository,
            #     tag_or_digest=image_asset.image_tag,
            #     cmd=["cdk_docker_demo.hello.handler"],
            # )
            code=_lambda.DockerImageCode.from_ecr(
                repository=ecr_repo,
                tag_or_digest=ecr_repo.repository_uri_for_tag(TAG_NAME),
                cmd=["cdk_docker_demo.hello.handler"],
            ),
        )

        _apigateway.LambdaRestApi(
            self,
            'Endpoint',
            handler=hello_handler,
        )
