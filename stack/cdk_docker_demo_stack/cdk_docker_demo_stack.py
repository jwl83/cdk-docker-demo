from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as _apigateway,
    aws_ecr_assets as _ecr_assets,
)
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

        hello_handler = _lambda.DockerImageFunction(
            self,
            'HelloDockerHandler',
            code=_lambda.DockerImageCode.from_image_asset(
                directory="src",
                cmd=["cdk_docker_demo.hello.handler"],
                platform=_ecr_assets.Platform.LINUX_AMD64,
                asset_name="data-api"
            ),
        )

        _apigateway.LambdaRestApi(
            self,
            'Endpoint',
            handler=hello_handler,
        )
