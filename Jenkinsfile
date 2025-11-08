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
                script {
                    // Get short commit hash for tagging
                    def gitHash = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
                    def imageTag = "amanoj23/aceestfitness:${env.BUILD_NUMBER}-${gitHash}"

                    // Enable Docker BuildKit for incremental build and caching
                    withEnv(["DOCKER_BUILDKIT=1"]) {

                    // Login to DockerHub safely
                    withCredentials([usernamePassword(credentialsId: 'dockerhub', 
                                                 usernameVariable: 'DOCKER_USER', 
                                                 passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    '''
                    }

                    // Build the Docker image
                    sh "docker build --progress=plain -t ${imageTag} ."

                    // Push the Docker image
                    sh "docker push ${imageTag}"
                }
            }
        }
    }


    }
}
