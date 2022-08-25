import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as cdk from 'aws-cdk-lib';


export class CellmapDBStack extends cdk.Stack {
  public readonly vpc: ec2.Vpc
  public readonly lambdaToRDSProxyGroup: ec2.SecurityGroup

  constructor(scope: cdk.App, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    const instanceIdentifier = 'cellmap-db';
    const dbUserName = 'postgres';
    const dbPort = 5432;
    const secretName = `/${id}/rds/creds/${instanceIdentifier}`.toLowerCase();
    const secret = new rds.DatabaseSecret(this,
      'cellmapRDSCredentials',
      {secretName: secretName, username: dbUserName}
      );

    const dbName = 'cellmap';
    
    // create the VPC
    this.vpc = new ec2.Vpc(this, 'cellmap-db-vpc', {
      cidr: '10.0.0.0/16',
      natGateways: 0,
      maxAzs: 3,
      subnetConfiguration: [
        {
          name: 'ingress-subnet',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'rds-subnet',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 28,
        },
      ],
    });


    // We need this security group to allow our proxy to query our MySQL Instance
    let dbConnectionGroup = new ec2.SecurityGroup(this,
      'Proxy to DB Connection', {
      vpc: this.vpc
    });

    this.lambdaToRDSProxyGroup = new ec2.SecurityGroup(this,
      'Lambda to RDS Proxy Connection', {
      vpc: this.vpc
    });

    dbConnectionGroup.addIngressRule(dbConnectionGroup, ec2.Port.tcp(dbPort), 'allow db connection');
    dbConnectionGroup.addIngressRule(this.lambdaToRDSProxyGroup, ec2.Port.tcp(dbPort), 'allow lambda connection');

    const dbInstance = new rds.DatabaseInstance(this, 'db-instance', {
      vpc: this.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE3,
        ec2.InstanceSize.MICRO,
      ),
      credentials: rds.Credentials.fromSecret(secret),
      multiAz: false,
      allocatedStorage: 20,
      maxAllocatedStorage: 35,
      allowMajorVersionUpgrade: false,
      autoMinorVersionUpgrade: true,
      backupRetention: cdk.Duration.days(0),
      deleteAutomatedBackups: true,
      removalPolicy: cdk.RemovalPolicy.DESTROY,
      deletionProtection: false,
      databaseName: dbName,
      securityGroups: [dbConnectionGroup]
    });

    const proxy = dbInstance.addProxy(id + 'proxy', {
      secrets : [secret],
      debugLogging: true,
      vpc: this.vpc,
      securityGroups: [dbConnectionGroup]
    })    

    new cdk.CfnOutput(this, 'dbProxyEndpoint', {
      value: proxy.endpoint,
      exportName: 'dbProxyEndpoint'
    });

    new cdk.CfnOutput(this, 'dbPort', {
      value: dbPort.toString(),
      exportName: 'dbPort'
    });

    new cdk.CfnOutput(this, 'dbName', {
      value: dbName,
      exportName: 'dbName'
    });

    new cdk.CfnOutput(this, 'dbUserName', {
      value: dbUserName,
      exportName: 'dbUserName'
    });

    new cdk.CfnOutput(this, 'dbSecretName', {
      // eslint-disable-next-line @typescript-eslint/no-non-null-asserted-optional-chain
      value: dbInstance.secret?.secretName!,
      exportName: 'dbSecretName'
    });


  }
}
