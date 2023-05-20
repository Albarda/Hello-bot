pipeline {
    agent {
        kubernetes {
            yaml """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: jnlp
    image: jenkins/jnlp-slave:latest
    args: ['\$(JENKINS_SECRET)', '\$(JENKINS_NAME)']
    volumeMounts:
    - mountPath: /home/jenkins
      name: workspace-volume
  - name: docker
    image: docker:latest
    command:
    - cat
    tty: true
    volumeMounts:
    - mountPath: /var/run/docker.sock
      name: docker-socket
  volumes:
  - name: docker-socket
    hostPath:
      path: /var/run/docker.sock
  - name: workspace-volume
    emptyDir: {}
"""
        }
    }
    stages {
        stage('Build') {
            steps {
                sh 'docker build -t alon-bot:latest .'
            }
        }
        stage('Push') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh 'docker login -u $DOCKER_USER -p $DOCKER_PASS'
                    sh 'docker tag alon-bot:latest kubealon/alon-bot:latest'
                    sh 'docker push kubealon/alon-bot:latest'
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

                    kubectl apply -f Hello-bot/alon-bot-python-deployment.yaml
                    kubectl apply -f Hello-bot/alon-bot-python-service.yaml
                    kubectl apply -f Hello-bot/alon-bot-hpa.yaml
                    kubectl apply -f Hello-bot/alon-bot-pvc.yaml

                    kubectl apply -f Hello-bot/alon-bot-nginx-deployment.yaml
                    kubectl apply -f Hello-bot/alon-bot-nginx-service.yaml
                    kubectl apply -f Hello-bot/alon-bot-ingress.yaml
                    '''
                }
            }
        }
    }
}
