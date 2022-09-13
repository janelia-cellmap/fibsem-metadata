import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as cdk from 'aws-cdk-lib';
import { CfnOutput } from 'aws-cdk-lib';


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
      natGateways: 1,
      maxAzs: 3,
      subnetConfiguration: [
        {
          name: 'public-subnet',
          subnetType: ec2.SubnetType.PUBLIC,
          cidrMask: 24,
        },
        {
          name: 'private-isolated-subnet',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
          cidrMask: 24,
        },
        {name: 'private-subnet',
        subnetType: ec2.SubnetType.PRIVATE_WITH_NAT,
        cidrMask: 24}
      ],
    });


    // We need this security group to allow our proxy to query our MySQL Instance
    const dbConnectionGroup = new ec2.SecurityGroup(this,
      'Proxy to DB Connection', {
      vpc: this.vpc
    });

    this.lambdaToRDSProxyGroup = new ec2.SecurityGroup(this,
      'Lambda to RDS Proxy Connection', {
      vpc: this.vpc
    });

    const DbBastionHostGroup = new ec2.SecurityGroup(this,
      'Security group for db admin instance', {
      vpc: this.vpc,
      allowAllOutbound: true
    });

    DbBastionHostGroup.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'ssh from anywhere');
    //DbBastionHostGroup.addIngressRule(ec2.Peer.ipv4('206.241.0.254/32'), ec2.Port.tcp(22), 'ssh access from janelia workstation');
    
    dbConnectionGroup.addIngressRule(dbConnectionGroup, ec2.Port.tcp(dbPort), 'allow db connection');
    dbConnectionGroup.addIngressRule(this.lambdaToRDSProxyGroup, ec2.Port.tcp(dbPort), 'allow lambda connection');
    dbConnectionGroup.addIngressRule(DbBastionHostGroup, ec2.Port.tcp(dbPort), 'allow admin instance connection')

    const dbInstance = new rds.DatabaseInstance(this, 'db-instance', {
      vpc: this.vpc,
      vpcSubnets: {
        subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
      },
      engine: rds.DatabaseInstanceEngine.postgres({
        version: rds.PostgresEngineVersion.VER_13_7,
      }),
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.M5,
        ec2.InstanceSize.LARGE,
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


    const DbBastionHost = new ec2.Instance(this, 'cellmap-db-admin-instance', {
      instanceType: ec2.InstanceType.of(
        ec2.InstanceClass.BURSTABLE2,
        ec2.InstanceSize.MICRO),
      machineImage: ec2.MachineImage.latestAmazonLinux(),
      vpc: this.vpc,
      keyName: 'ec2_bennettd',
      vpcSubnets: {subnetType: ec2.SubnetType.PUBLIC},
      securityGroup: DbBastionHostGroup
    }
    )

    new cdk.CfnOutput(this, 'dbEndpoint', {
      value: dbInstance.instanceEndpoint.hostname,
      exportName: 'dbEndpoint'
    });


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

    new CfnOutput(this, 'dbAdminIP', {
      value: DbBastionHost.instance.attrPublicIp,
      exportName: 'dbAdminIP'
    })

  }
}
