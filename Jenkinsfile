pipeline {
    agent {
        kubernetes {
            label 'alon-bot-pod'
            defaultContainer 'jnlp'
            yamlFile '/home/ec2-user/Hello-bot/alon-bot-pod.yaml' // Replace this with the path to your pod YAML file
        }
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh 'docker build -t alon-bot:latest .'
            }
        }

        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker tag alon-bot:latest kubealon/alon-bot:latest' // Replace 'your-docker-registry' with your actual Docker registry
                    sh 'docker push kubealon/alon-bot:latest' // Replace 'your-docker-registry' with your actual Docker registry
                }
            }
        }

        stage('Deploy') {
            steps {
                withCredentials([string(credentialsId: 'kubectl-credentials', variable: 'KUBECONFIG_CA')]) {
                    sh '''
                    export KUBECONFIG=~/.kube/config
                    kubectl config use-context my-context
                    kubectl config set-credentials jenkins --certificate=$KUBECONFIG_CA
                    kubectl config set-context --current --namespace=jenkins

                    # Apply Kubernetes manifests
                    kubectl apply -f Hello-bot/alon-bot-python-deployment.yaml
                    kubectl apply -f Hello-bot/alon-bot-python-service.yaml
                    kubectl apply -f Hello-bot/alon-bot-hpa.yaml
                    kubectl apply -f Hello-bot/alon-bot-pvc.yaml

                    # Apply nginx and ingress manifests
                    # kubectl apply -f Hello-bot/alon-bot-nginx-configmap.yaml
                    kubectl apply -f Hello-bot/alon-bot-nginx-deployment.yaml
                    kubectl apply -f Hello-bot/alon-bot-nginx-service.yaml
                    kubectl apply -f Hello-bot/alon-bot-ingress.yaml
                    '''
                }
            }
        }
    }
}
