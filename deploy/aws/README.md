# AWS Deployment Mapping

This folder documents how the local MLOps demo maps to a production AWS design without claiming prior production ownership of AWS infrastructure.

## Suggested architecture

1. **S3** — versioned training data and model artifacts.
2. **SageMaker Training** — run `python -m src.train` in a managed training job.
3. **SageMaker Model Registry** — register approved model versions and metrics.
4. **ECR** — store the Docker image.
5. **SageMaker Endpoint or ECS/Fargate** — serve the FastAPI inference container.
6. **CloudWatch** — logs, latency, error-rate and infrastructure metrics.
7. **SageMaker Model Monitor** — input/data-quality monitoring.
8. **EventBridge + Step Functions / SageMaker Pipelines** — scheduled or condition-based retraining.
9. **IAM** — least-privilege access between training, registry, storage and serving components.

## Production checks

- separate training, validation and production datasets
- immutable model/version metadata
- automated unit/integration tests before deployment
- health endpoint and rollback strategy
- data-drift and model-performance thresholds
- retraining only after evaluation against the current production model and a baseline
- secret management outside source control

## Interview explanation

> I have not claimed production AWS ownership in my CV. I built the project cloud-ready so I can explain how the same training, serving and monitoring components would map to SageMaker, S3, ECR and CloudWatch. My strongest hands-on experience is Python, forecasting, data validation and software engineering, and I am extending that experience into MLOps/cloud deployment.


<!-- BEGIN FOLDER GUIDE -->
## Folder guide

A mapping from the local forecasting components to possible AWS services. Read the existing guide for its stated implementation scope.

[Parent folder](../) · [Repository overview](../../README.md) · [All projects](https://github.com/zahramardani/ML2PP-Artifacts/blob/main/PROJECTS.md)

This directory currently contains its README only. The existing text above explains the intended role of this documentation area.

<!-- END FOLDER GUIDE -->
