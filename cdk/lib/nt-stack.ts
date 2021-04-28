import * as cdk from '@aws-cdk/core';
import * as s3 from '@aws-cdk/aws-s3';
import * as lambda from '@aws-cdk/aws-lambda';
import * as ec2 from '@aws-cdk/aws-ec2';
import * as ecs from "@aws-cdk/aws-ecs";
import * as sfn from '@aws-cdk/aws-stepfunctions';
import * as tasks from '@aws-cdk/aws-stepfunctions-tasks';
import * as rds from "@aws-cdk/aws-rds";
import { Duration } from '@aws-cdk/core';

export class NTStack extends cdk.Stack {
  readonly sourceBucket: s3.Bucket;
  readonly fnFetchData: lambda.Function;
  readonly vpc: ec2.IVpc;
  readonly demoDb: rds.IDatabaseInstance;
  readonly workflowStateMachine: sfn.StateMachine;

  constructor(scope: cdk.Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.vpc = ec2.Vpc.fromLookup(this, 'VPC', {
      vpcId: 'vpc-0f3982b122493722a'
    });

    this.sourceBucket = new s3.Bucket(this, 'sourceBucket', {
      versioned: false
    });

    this.demoDb = rds.DatabaseInstanceBase.fromDatabaseInstanceAttributes(this, 'demoDb', {
      instanceEndpointAddress: process.env.DB_HOST || '',
      instanceIdentifier: 'nt-database',
      port: 5432,
      securityGroups: [ec2.SecurityGroup.fromLookup(this, 'db-sg','sg-0e673d12ba4f84628')],
    })

    this.fnFetchData = new lambda.Function(this, 'fnFetchData', {
      code: lambda.Code.fromAsset('../src/fetch'),
      handler: 'fetch.lambda_handler',
      runtime: lambda.Runtime.PYTHON_3_8,
      memorySize: 1024,
      timeout: Duration.minutes(15),
      environment: {
        FIRE_DATA_URL: "https://data.sfgov.org/api/views/wr8u-xric/rows.csv",
        S3_DATA_BUCKET: this.sourceBucket.bucketName
      }
    });

    this.sourceBucket.grantWrite(this.fnFetchData);

    const cluster = new ecs.Cluster(this, "ecsCluster", {
      containerInsights: true,
      vpc: this.vpc,
    });

    const taskDefinition = new ecs.FargateTaskDefinition(this, 'FargateTask', {
      cpu: 1024,
      memoryLimitMiB: 4096
    });

    this.sourceBucket.grantReadWrite(taskDefinition.taskRole);

    const containerDefinition = taskDefinition.addContainer('Container', {
      image: ecs.ContainerImage.fromAsset('../src/load/'),
      logging: ecs.LogDriver.awsLogs({
        streamPrefix: 'Container'
      }),
      environment: {
        S3_DATA_BUCKET: this.sourceBucket.bucketName
      },
      cpu: 1024,
      memoryLimitMiB: 4096
    });

    // Step Functions workflow
    const fetchDatatask = new tasks.LambdaInvoke(this, 'FetchDataTask', {
      lambdaFunction: this.fnFetchData
    })

    const loadDataTask = new tasks.EcsRunTask(this, 'RunFargate', {
      cluster: cluster,
      taskDefinition: taskDefinition,
      integrationPattern: sfn.IntegrationPattern.RUN_JOB,
      launchTarget: new tasks.EcsFargateLaunchTarget(),
      assignPublicIp: true,
      containerOverrides: [
        {
          containerDefinition: containerDefinition,
          environment: [
            {name: 'DB_HOST', value: process.env.DB_HOST || ''},
            {name: 'DB_USER', value: process.env.DB_USER || ''},
            {name: 'DB_PASS', value: process.env.DB_PASS || ''}
          ]
        }
      ]
    });

    const workflowDefinition = fetchDatatask.next(loadDataTask);

    this.workflowStateMachine = new sfn.StateMachine(this, 'StateMachine', {
      definition: workflowDefinition
    });

  }
}
