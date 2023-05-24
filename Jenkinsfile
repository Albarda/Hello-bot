pipeline {
    agent {
    kubernetes {
      serviceAccount 'jenkins'
      yaml '''
        apiVersion: v1
        kind: Pod
        metadata:
          labels:
            jenkins: "slave"
        spec:
          containers:
          - name: jenkins-agent
            image: kubealon/jenkins-docker:1.6
            command:
            - "/bin/sh"
            args:
            - "-c"
            - "while true; do echo 'jenkins-agent running...'; sleep 30; done"
            env:
            - name: KUBECONFIG
              value: /home/jenkins/.kube/config
            tty: true
          volumes:
          - name: kubeconfig
            secret:
              secretName: my-kubeconfig
          volumeMounts:
          - name: kubeconfig
            mountPath: /home/jenkins/.kube/config
            readOnly: true
            subPath: config
        '''
        }
    }
    options {
        skipDefaultCheckout(true)
        timestamps()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        disableConcurrentBuilds()
    }
            environment {
    PATH = "$PATH:/home/jenkins/bin"
        }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }



        stage('Install kubectl') {
  steps {
    script {
      sh '''
        curl -LO https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl
        chmod +x ./kubectl
        mkdir -p ~/bin
        mv ./kubectl ~/bin/
        echo 'export PATH=$PATH:~/bin' >> ~/.bashrc
        . /home/jenkins/.bashrc
      '''
    }
  }
}




        stage('Deploy to Minikube') {
            steps {
                script {
                   // sh 'kubectl config use-context minikube'
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
