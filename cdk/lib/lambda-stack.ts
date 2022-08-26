import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as secrets from 'aws-cdk-lib/aws-secretsmanager'
import apigw = require('@aws-cdk/aws-apigatewayv2-alpha');
import {HttpLambdaIntegration} from "@aws-cdk/aws-apigatewayv2-integrations-alpha"

interface CellmapAPILambdaStackProps extends cdk.StackProps {
    vpc: ec2.Vpc
    lambdaToRDSProxyGroup: ec2.SecurityGroup
}

export class CellmapAPILambdaStack extends cdk.Stack {
    constructor(scope: cdk.App, id: string, props: CellmapAPILambdaStackProps) {
    super(scope, id, props);

    const dbSecretName = cdk.Fn.importValue('dbSecretName');
    const dbName = cdk.Fn.importValue('dbName');
    const dbPort = cdk.Fn.importValue('dbPort');
    const dbUserName = cdk.Fn.importValue('dbUserName');
    const dbProxyEndpoint = cdk.Fn.importValue('dbProxyEndpoint');
    
    const apiLambda = new lambda.Function(this,
        'api-lambda',
        {
          vpc: props.vpc,
          securityGroups: [props.lambdaToRDSProxyGroup],
          runtime: lambda.Runtime.PYTHON_3_9,
          handler: 'fibsem_metadata/lambda_handler.handler',
          code: lambda.Code.fromAsset('../artifact.zip'),
          environment: {
            DB_USER: dbUserName,
            AWS_DB_SECRET_NAME: dbSecretName,
            DB_HOST: dbProxyEndpoint,
            DB_PORT: dbPort,
            DB_NAME: dbName,
          }
        }
    );

    // ensure that the lambda has access to the secret
    const secret = secrets.Secret.fromSecretNameV2(this, 'dbSecret', dbSecretName);
    secret.grantRead(apiLambda);
    
    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new HttpLambdaIntegration("lambda-proxy", apiLambda),
      corsPreflight: {
        allowHeaders: [
          'Content-Type',
          'X-Amz-Date',
          'Authorization',
          'X-Api-Key',
        ],
        allowMethods: [
          apigw.CorsHttpMethod.GET,
        ],
        allowOrigins: ['*'],
      },
    },
    );

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
    
}
