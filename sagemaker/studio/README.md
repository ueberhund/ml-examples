# SageMaker Studio CloudFormation template

This template shows how to set up a SageMaker Studio via CloudFormation. 

- [sagemaker-studio-setup-novpc.yml](sagemaker-studio-setup-novpc.yml) - this shows how to set up SageMaker Studio in PublicInternetOnly mode.
- [sagemaker-studio-setup-vpconly.yml](sagemaker-studio-setup-vpconly.yml) - this shows how to set up SageMaker Studio in VpcOnly mode. 


There's a lot here, so some thoughts:

- While this template does create everything you need, please note that behind the scenes SageMaker creates an EFS volume for Studio users. You don’t explicitly create this EFS volume, so just be aware that it exists.
- The template spins up SageMaker Studio in VpcOnly mode or PublicInternetOnly mode, depending on which template you pick. Becuase of this, I also spin up a simple VPC. All VPC resources are in the “VPC Resources” section, so it should be pretty easy to delete this and use your own VPC.
- For the VpcOnly template: there are a number of VPC endpoints required for SM Studio to work properly. Note that I’m only allowing access to a single S3 bucket. Speaking of which, the sample bucket I created (in the “S3 Bucket” section) can be deleted, but I built it to demonstrate access to this specific bucket via SM Studio.
- You’ll notice the IAM Section is a bit of a doozy. The AmazonSageMakerServiceCatalogProductsUseRole creates a monster set of in-line permissions. These permissions are currently required by SageMaker Studio.
- Finally, you cannot enable SM Studio projects via CloudFormation at this time. You’ll see a custom Lambda that is executed to assign the SageMaker Service Catalog portfolio to our Studio domain.
