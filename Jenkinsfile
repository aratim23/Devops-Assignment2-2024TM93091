pipeline {
    agent any

    environment {
        VERSIONS = "ACEestFitness"
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
                    // Create virtual environment inside ACEestFitness
                    sh """
                        python3 -m venv ACEestFitness/venv
                        source ACEestFitness/venv/bin/activate
                        pip install --upgrade pip
                        pip install --force-reinstall -r requirements.txt
                    """

                    // Run pytest from inside ACEestFitness
                    sh """
                        cd ACEestFitness
                        ../venv/bin/pytest tests --maxfail=1 --disable-warnings -v
                    """
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
