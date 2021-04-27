#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { NTStack } from '../lib/nt-stack';


const PROJECT_TAG = 'nt-assignment';

const app = new cdk.App();


new NTStack(app, 'NTStack', {
  tags: {
    project: PROJECT_TAG
  },
  env: {
    account: process.env.AWS_ACCOUNT,
    region: process.env.AWS_DEFAULT_REGION
  }
});
