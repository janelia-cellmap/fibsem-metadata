import * as cdk from 'aws-cdk-lib';
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import apigw = require('@aws-cdk/aws-apigatewayv2-alpha');
import {HttpLambdaIntegration} from "@aws-cdk/aws-apigatewayv2-integrations-alpha"

interface CellmapAPILambdaStackProps extends cdk.StackProps {
    vpc: ec2.Vpc
    lambdaToRDSProxyGroup: ec2.SecurityGroup
}

export class CellmapAPILambdaStack extends cdk.Stack {
    constructor(scope: cdk.App, id: string, props: CellmapAPILambdaStackProps) {
    super(scope, id, props);

    const secretName = cdk.Fn.importValue('secretName');
    const dbEndpoint = cdk.Fn.importValue('dbEndpoint');
    const dbPort = cdk.Fn.importValue('dbPort');
    const dbName = cdk.Fn.importValue('dbName');

    const secret = rds.DatabaseSecret.fromSecretNameV2(this, 'cellmap-api-lambda-rds-secret', secretName);
         
    const apiLambda = new lambda.Function(this,
        'api-lambda',
        {
          vpc: props.vpc,
          securityGroups: [props.lambdaToRDSProxyGroup],
          runtime: lambda.Runtime.PYTHON_3_9,
          handler: 'fibsem_metadata/lambda.handler',
          code: lambda.Code.fromAsset('../artifact.zip'),
          environment: {
            DB_HOST: dbEndpoint,
            DB_PORT: dbPort,
            DB_NAME: dbName,
            SECRET_NAME: secretName
          }
        }
    );

    let api = new apigw.HttpApi(this, 'Endpoint', {
      defaultIntegration: new HttpLambdaIntegration("lambda-proxy", apiLambda)
    });

   new cdk.CfnOutput(this, 'HTTP API Url', {
     value: api.url ?? 'Something went wrong with the deploy'
   });
  }
    
}
