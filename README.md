# Surveillance Anomaly Object Detection Project

## Workflows

    - constants
    - config_entity
    - artifact_entity
    - components
    - pipeline
    - app.py


## Jenkins 

This project involves setting up a CI/CD pipeline using Jenkins, Docker, and AWS services for automated deployment. The project includes a web application that is deployed on an AWS EC2 instance using Docker containers, and the build process is managed by Jenkins. This README will guide you through the setup, configuration, and deployment processes.


## Table of Contents
    - [Prerequisites](#prerequisites)
    - [Jenkins Setup](#jenkins-setup)
    - [Docker Deployment](#docker-deployment)
    - [GitHub Actions Integration](#github-actions-integration)
    - [Cleanup](#cleanup)

## Prerequisites
    - AWS Account
    - Jenkins Server
    - GitHub Repository
    - Docker
    - AWS CLI
    - Access to EC2 instance

## Jenkins Setup
1. **Upgrade Necessary Tools**
    ```bash
    # Upgrade tools as needed
    ```

2. **Configure AWS CLI**
    ```bash
    aws configure
    ```

3. **Set Up Elastic IP**
    - Go to the AWS Management Console.
    - Navigate to the EC2 dashboard.
    - Allocate a new Elastic IP and associate it with your EC2 instance.

4. **Configure Jenkins**
    - Open Jenkins and go to `Manage Jenkins` > `Manage Plugins` to install required plugins.
    - Go to `Manage Jenkins` > `Configure System` and set up your Jenkins URL.
    - Configure credentials in Jenkins:
    - Go to `Manage Jenkins` > `Manage Credentials` and add your AWS credentials.
    - Add GitHub secrets:
    - Navigate to your GitHub repository.
    - Go to `Settings` > `Secrets and variables` > `Actions`.
    - Add new secrets for Jenkins URL, username, and token.

5. **Create and Configure Jenkins Job**
    - Create a new Jenkins job for your project.
    - Configure the job to use your GitHub repository.
    - Set up build triggers and actions according to your project requirements.

 
# Project Setup and Deployment

## Jenkinsfile

The `Jenkinsfile` defines the stages and steps for the CI/CD pipeline using Jenkins. It includes:

### 1. **Continuous Integration**
   - **Purpose:** Lint the code and run unit tests.
   - **Commands:**
     ```groovy
     echo "Linting repository"
     echo "Running unit tests"
     ```

### 2. **Login to ECR**
   - **Purpose:** Authenticate Docker with Amazon Elastic Container Registry (ECR).
   - **Commands:**
     ```groovy
     sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com'
     ```

### 3. **Build Image**
   - **Purpose:** Build a Docker image tagged with `latest`.
   - **Commands:**
     ```groovy
     sh 'docker build -t ${ECR_REPOSITORY}:latest .'
     ```

### 4. **Push Image**
   - **Purpose:** Push the Docker image to ECR.
   - **Commands:**
     ```groovy
     sh 'docker push ${ECR_REPOSITORY}:latest'
     ```

### 5. **Continuous Deployment**
   - **Purpose:** Deploy the application on a remote EC2 instance.
   - **Commands:**
     ```groovy
     sshagent(['ssh_key']) {
       sh "ssh -o StrictHostKeyChecking=no -l ubuntu 3.218.21.247 'cd /home/ubuntu/ && wget https://raw.githubusercontent.com/snehsuresh/yolo-end-to-end/develop/docker-compose.yml && export IMAGE_NAME=${ECR_REPOSITORY}:latest && aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.us-east-1.amazonaws.com && docker compose up -d '"
     }
     ```

### 6. **Post Actions**
   - **Purpose:** Clean up unused Docker resources.
   - **Commands:**
     ```groovy
     sh 'docker system prune -f'
     ```

## GitHub Actions Workflow (`main.yaml`)

The `main.yaml` file is a GitHub Actions workflow that mirrors the Jenkinsfile but is used for GitHub Actions CI/CD pipelines. It performs the same stages: Continuous Integration, Login to ECR, Build Image, Push Image, and Continuous Deployment.

## EC2 Setup Script

### 1. **General EC2 Setup**
   - **Commands:**
     ```bash
     sudo apt update 
     sudo apt-get update 
     sudo apt upgrade -y
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     sudo usermod -aG docker $USER
     newgrp docker
     sudo apt install awscli -y
     aws configure
     ```

### 2. **Jenkins EC2 Setup**
   - **Commands:**
     ```bash
     sudo apt update 
     sudo apt install openjdk-8-jdk -y
     curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io.key | sudo apt-key add -
     sudo sh -c 'echo deb http://pkg.jenkins.io/debian-stable binary/ > /etc/apt/sources.list.d/jenkins.list'
     sudo apt update
     sudo apt install jenkins -y
     sudo systemctl start jenkins
     sudo systemctl enable jenkins
     sudo systemctl status jenkins
     curl -fsSL https://get.docker.com -o get-docker.sh
     sudo sh get-docker.sh
     sudo usermod -aG docker $USER
     sudo usermod -aG docker jenkins
     sudo apt install awscli -y
     aws configure
     sudo systemctl restart jenkins
     sudo cat /var/lib/jenkins/secrets/initialAdminPassword
     ```
