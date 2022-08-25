#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from 'aws-cdk-lib';
import { CellmapDBStack } from '../lib/cellmap-db-stack';
import { CellmapAPILambdaStack } from '../lib/lambda-stack';
const app = new cdk.App();
const dbstack = new CellmapDBStack(app, 'cellmap-rds', {});
new CellmapAPILambdaStack(app,
    'cellmap-fastapi-lambda',
    {vpc: dbstack.vpc, lambdaToRDSProxyGroup: dbstack.lambdaToRDSProxyGroup
    }
    );