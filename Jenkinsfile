pipeline {
  agent any

  environment {
    IMAGE_NAME       = "amanoj23/aceestfitness"   // DockerHub repo
    K8S_NAMESPACE    = "fitness-app"
    DEPLOYMENT_NAME  = "fitness-app"
    CONTAINER_NAME   = "fitness-app-container"
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
          def scannerHome = tool 'SonarScanner'   // Jenkins tool named "SonarScanner"
          withSonarQubeEnv('SonarQube') {         // Jenkins server config named "SonarQube"
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
            echo $DOCKER_PASS | docker login -u $DOCKER_USER --password-stdin
            docker build -t $IMAGE_NAME:$IMAGE_TAG .
            docker push  $IMAGE_NAME:$IMAGE_TAG
          '''
        }
      }
    }

    stage('Deploy to Minikube') {
      steps {
        sh '''
          set -eux
          # Use the minikube context (must exist on this agent)
          kubectl config use-context minikube

          # Ensure namespace exists
          kubectl get ns ${K8S_NAMESPACE} || kubectl create ns ${K8S_NAMESPACE}

          # Update Deployment to the new tag
          kubectl -n ${K8S_NAMESPACE} set image deployment/${DEPLOYMENT_NAME} \
            ${CONTAINER_NAME}=${IMAGE_NAME}:${IMAGE_TAG}

          # (Optional) enforce pulling fresh tag; not strictly needed since tag is unique
          kubectl -n ${K8S_NAMESPACE} patch deployment/${DEPLOYMENT_NAME} \
            --type='merge' -p \
            '{"spec":{"template":{"spec":{"containers":[{"name":"'${CONTAINER_NAME}'","imagePullPolicy":"Always"}]}}}}'

          # Wait for rollout
          kubectl -n ${K8S_NAMESPACE} rollout status deployment/${DEPLOYMENT_NAME}
        '''
      }
    }
  }

  post {
    always {
      sh 'docker logout || true'
    }
  }
}
