# Netflix-Style Serverless Platform (AWS + Terraform)

## Overview
Deployed a scalable serverless video platform using AWS and Infrastructure as Code.

## Architecture
- API Gateway + Lambda for backend services
- S3 + CloudFront for content delivery
- RDS (PostgreSQL) for metadata
- Redis for caching
- SQS for async processing

## Key Features
- CI/CD pipeline for Terraform
- Modular infrastructure
- Performance monitoring with CloudWatch

## What I Learned
- Designing reproducible environments
- Structuring cloud systems for scale
- Automating deployments

## How to Run
(terraform init / plan / apply)

## Prereqs
- AWS CLI configured
- AWS SAM CLI installed
- Python 3.11

## Build & deploy
```bash
sam build
sam deploy --guided

