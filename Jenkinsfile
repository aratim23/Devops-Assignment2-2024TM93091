pipeline {
  agent any

  environment {
    IMAGE_NAME       = "amanoj23/aceestfitness"   // DockerHub repo
    K8S_NAMESPACE    = "fitness-app"
    DEPLOYMENT_NAME  = "fitness-app"
    CONTAINER_NAME   = "fitness-app-container"
    // IMAGE_TAG is set in "Prepare" stage: BUILD_NUMBER-shortSHA
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
        sh '''
          set -eux
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

    stage('SonarQube Analysis') {
      steps {
        script {
          def scannerHome = tool 'SonarScanner'    // Jenkins tool named "SonarScanner"
          withSonarQubeEnv('SonarQube') {          // Jenkins server config named "SonarQube"
            sh "${scannerHome}/bin/sonar-scanner"
          }
        }
      }
    }

    stage('Prepare') {
      steps {
        script {
          env.GIT_HASH  = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
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
            set -eux
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            docker build -t $IMAGE_NAME:$IMAGE_TAG .
            docker push  $IMAGE_NAME:$IMAGE_TAG
          '''
        }
      }
    }

    stage('Deploy to Minikube (dockerized kubectl)') {
        steps {
            withCredentials([file(credentialsId: 'kubeconfig-minikube', variable: 'KCFG')]) {
            sh '''
                set -eux

                # Pick a known-good kubectl image; pull explicitly
                KUBEIMG_PRIMARY="registry.k8s.io/kubectl:v1.30.4"
                docker pull "$KUBEIMG_PRIMARY"
                KUBEIMG="$KUBEIMG_PRIMARY"

                # Helper to run kubectl via Docker (NO quotes around ${KCFG}; use --mount)
                DOCKER_KUBECTL="docker run --rm \
                --mount type=bind,source=${KCFG},target=/kubeconfig,readonly \
                -e KUBECONFIG=/kubeconfig \
                $KUBEIMG kubectl"

                # Sanity check: client version & cluster reachability
                $DOCKER_KUBECTL version --client
                $DOCKER_KUBECTL cluster-info

                # Ensure namespace exists
                $DOCKER_KUBECTL get ns ${K8S_NAMESPACE} >/dev/null 2>&1 || \
                $DOCKER_KUBECTL create ns ${K8S_NAMESPACE}

                # Update the deployment image to the fresh tag
                $DOCKER_KUBECTL -n ${K8S_NAMESPACE} set image deployment/${DEPLOYMENT_NAME} \
                ${CONTAINER_NAME}=${IMAGE_NAME}:${IMAGE_TAG}

                # Wait for rollout to complete
                $DOCKER_KUBECTL -n ${K8S_NAMESPACE} rollout status deployment/${DEPLOYMENT_NAME}
            '''
        }
    }
    }

  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}
