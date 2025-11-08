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
                dir("${WORKSPACE}") {  // ensure we're in workspace root
                sh """
                    # 1. Create virtual environment inside ACEestFitness
                    python3 -m venv ACEestFitness/venv

                    # 2. Upgrade pip and install dependencies
                    ACEestFitness/venv/bin/pip install --upgrade pip
                    ACEestFitness/venv/bin/pip install -r requirements.txt

                    # 3. Set PYTHONPATH to ACEestFitness so tests can import the module
                    export PYTHONPATH=$PWD

                    # 4. Run pytest from the ACEestFitness folder
                    ACEestFitness/venv/bin/pytest ACEestFitness/tests --maxfail=1 --disable-warnings -v
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
