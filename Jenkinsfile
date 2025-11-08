pipeline {
    agent any

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
                withCredentials([usernamePassword(credentialsId: 'dockerhub-token',
                                                 usernameVariable: 'DOCKER_USER',
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
                        docker build -t $IMAGE_NAME:$IMAGE_TAG .
                        docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
            }
        }
    
    }

}