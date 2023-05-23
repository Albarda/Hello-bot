pipeline {
    agent {
    kubernetes {
      yaml '''
        apiVersion: v1
        kind: Pod
        spec:
          containers:
          - name: jenkins-agent
            image: kubealon/jenkins-docker-agent:latest
            namespace: jenkins
            tty: true
            command:
            - "/bin/sh"
            args:
            - "-c"
            - "while true; do echo 'jenkins-agent running...'; sleep 30; done"
        '''
        }
    }
    options {
        skipDefaultCheckout(true)
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'Github-cred',
                        passwordVariable: 'pass',
                        usernameVariable: 'user'
                    ),
                ]) {
                   // sh 'minikube start'
                    sh 'eval $(minikube -p minikube docker-env)'
                    sh """
                        docker build -f Dockerfile -t kubealon/alon-bot-python:${env.BUILD_NUMBER} .
                    """
                    sh """
                        docker build -f Dockerfile-nginx -t kubealon/alon-bot-nginx:${env.BUILD_NUMBER} .
                    """
                }
            }
        }

        stage('push') {
            options {
                timeout(time: 10, unit: 'MINUTES')
            }
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        passwordVariable: 'dockerPass',
                        usernameVariable: 'dockerUser'
                    ),
                ]) {
                    sh """
                        docker push kubealon/alon-bot-python:${env.BUILD_NUMBER}
                    """
                    sh """
                        docker push kubealon/alon-bot-nginx:${env.BUILD_NUMBER}
                    """
                }
            }
        }

        stage('Deploy to Minikube') {
            steps {
                script {
                    sh 'kubectl config use-context minikube'
                    sh 'kubectl apply -f alon-bot-python-deployment.yaml'
                    sh 'kubectl apply -f alon-bot-python-service.yaml'
                    sh 'kubectl apply -f alon-bot-python-hpa.yaml'
                    sh 'kubectl apply -f alon-bot-release-pvc.yaml'
                    sh 'kubectl apply -f alon-bot-nginx-deployment.yaml'
                    sh 'kubectl apply -f alon-bot-nginx-service.yaml'
                    sh 'kubectl apply -f alon-bot-pvc.yaml'
                    sh 'kubectl apply -f alon-bot-ingress.yaml'
                }
            }
        }
    }

    post {
        always {
            sh 'docker system prune -af'
         //   sh 'minikube stop'
        }
    }
}
