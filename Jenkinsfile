pipeline {
    agent any

    environment {
        VERSIONS = "ACEestFitness-V1.0 ACEestFitness-V1.1 ACEestFitness-V1.2.1"
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
                    def versions = env.VERSIONS.split()
                    for (version in versions) {
                        dir(version) {
                            sh """
                               python3 -m venv venv
                               . venv/bin/activate
                               pip install -r requirements.txt
                               pytest || exit 1
                               deactivate
                            """
                        }
                    }
                }
            }
        }

        stage('Package Artifacts') {
            steps {
                script {
                    def versions = env.VERSIONS.split()
                    for (version in versions) {
                        dir(version) {
                            sh "tar czf ../${version}.tar.gz *"
                        }
                    }
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: '*.tar.gz', fingerprint: true
                }
            }
        }
    }
}
