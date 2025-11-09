pipeline {
    agent any

    environment {
        IMAGE_NAME = "amanoj23/aceestfitness"   // DockerHub repo
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

        stage('SonarQube Analysis') {
            def scannerHome = tool 'SonarScanner';
                withSonarQubeEnv() {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }

        stage('Prepare') {
            steps {
                // Get short Git hash for unique tagging
                script {
                    env.GIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    env.IMAGE_TAG = "${env.BUILD_NUMBER}-${env.GIT_HASH}"
                    echo "Docker Image Tag: ${env.IMAGE_TAG}"
                }
            }
        }

        stage('Docker Build & Push') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'dockerhub-token', 
                    usernameVariable: 'DOCKER_USER', 
                    passwordVariable: 'DOCKER_PASS'
                )]) {
                    sh '''
                        # Login to DockerHub
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin

                        # Build the image incrementally (layers are cached)
                        docker build -t $IMAGE_NAME:$IMAGE_TAG .

                        # Push the uniquely tagged image
                        docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'docker logout'
        }
    }
    
}
