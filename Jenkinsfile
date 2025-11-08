pipeline {
    agent any

    environment {
        DOCKER_USER = amanoj23   // Jenkins credentials: username
        DOCKER_PASS = credentials('dockerhub-token')      // Jenkins credentials: PAT
    }

    stages {
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/aratim23/Devops-Assignment2-2024TM93091.git',
                        credentialsId: 'github-https-token'
                    ]]
                ])
            }
        }

        stage('Build & Test') {
            steps {
                script {
                    sh '''
                        python3 -m venv ACEestFitness/venv
                        . ACEestFitness/venv/bin/activate
                        pip install --upgrade pip
                        pip install --force-reinstall -r requirements.txt
                        export PYTHONPATH=$PWD/ACEestFitness
                        pytest ACEestFitness/tests --maxfail=1 --disable-warnings -v
                        deactivate
                    '''
                }
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                script {
                    // Get short Git commit hash for tagging
                    def gitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    def imageName = "aceestfitness:${BUILD_NUMBER}-${gitHash}"

                    echo "Building Docker image: ${imageName}"

                    // Login to DockerHub securely
                    sh """
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    """

                    // Build Docker image incrementally using BuildKit
                    sh """
                        DOCKER_BUILDKIT=1 docker build \
                            --tag ${imageName} \
                            --file Dockerfile \
                            .
                    """

                    // Push image to DockerHub
                    sh "docker push ${imageName}"
                }
            }
        }
    
    }

}