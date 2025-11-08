pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = credentials('dockerhub-creds') // Jenkins credentials ID
        DOCKERHUB_USERNAME = "amanoj23"
        APP_NAME = "aceestfitness"
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
                    // Get short Git commit hash
                    def gitCommit = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    
                    // Create unique Docker image tag using build number + git commit
                    def imageTag = "${env.BUILD_NUMBER}-${gitCommit}"
                    def fullImageName = "${DOCKERHUB_USERNAME}/${APP_NAME}:${imageTag}"
                    
                    echo "Building Docker image: ${fullImageName}"
                    
                    // Build the Docker image
                    sh "docker build -t ${fullImageName} ."
                    
                    // Login to Docker Hub
                    sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u ${DOCKERHUB_CREDENTIALS_USR} --password-stdin"
                    
                    // Push uniquely tagged image
                    sh "docker push ${fullImageName}"
                    
                    // Optionally, tag and push 'latest'
                    def latestImage = "${DOCKERHUB_USERNAME}/${APP_NAME}:latest"
                    sh "docker tag ${fullImageName} ${latestImage}"
                    sh "docker push ${latestImage}"
                }
            }
        }

    }
}
