#!/usr/bin/env node
import 'source-map-support/register';
import * as cdk from '@aws-cdk/core';
import { NTStack } from '../lib/nt-stack';


const PROJECT_TAG = 'nt-assignment';

const app = new cdk.App();
const props = {tags: {project: PROJECT_TAG}}

new NTStack(app, 'NTStack', props);
