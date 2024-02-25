#!/usr/bin/env bash -ex

# Get the account number associated with the current IAM credentials
account=$(aws sts get-caller-identity --query Account --output text)

if [ $? -ne 0 ]; then
    exit 255
fi

region="eu-west-1"

image="dshop"

fullname="${account}.dkr.ecr.${region}.amazonaws.com/${image}:latest"

# Get the login command from ECR and execute it directly
# $(aws ecr get-login-password --region ${region} --no-include-email)
aws ecr get-login-password --region ${region} | docker login --username AWS --password-stdin ${fullname}

# If the repository doesn't exist in ECR, create it.
aws ecr describe-repositories --region ${region} --repository-names "${image}" >/dev/null 2>&1

if [ $? -ne 0 ]; then
    aws ecr create-repository --region ${region} --repository-name "${image}" >/dev/null
fi

# Build the docker image locally with the image name and then push it to ECR
# with the full name.
docker build --platform=linux/amd64 -t ${image} -f Dockerfile .
docker tag ${image} ${fullname}

docker push ${fullname}
