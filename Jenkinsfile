pipeline {
    agent {
        docker {
            image 'kubealon/private-course:jenkins-agent'
            args '--user root -v /var/run/docker.sock:/var/run/docker.sock'
        }
    }

    options {
        skipDefaultCheckout(true)
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }

    stages {
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
                    sh """
                        docker build -t kubealon/alon-bot-python-${env.BUILD_NUMBER} .
                    """
                    sh """
                        docker build -t kubealon/alon-bot-nginx-${env.BUILD_NUMBER} .
                    """
                }
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-cred',
                        passwordVariable: 'DOCKERHUB_PASSWORD',
                        usernameVariable: 'DOCKERHUB_USERNAME'
                    )
                ]) {
                    sh """
                        echo $DOCKERHUB_PASSWORD | docker login \
                            --username $DOCKERHUB_USERNAME \
                            --password-stdin
                    """
                    sh """
                        docker push kubealon/alon-bot-python-${env.BUILD_NUMBER}
                    """
                    sh """
                        docker push kubealon/alon-bot-nginx-${env.BUILD_NUMBER}
                    """
                }
            }
        }
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig-file', variable: 'KUBECONFIG')]) {
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
    }
    post {
        always {
            // Cleanup Docker images from the disk
            sh 'docker system prune -af'
        }
    }
}
