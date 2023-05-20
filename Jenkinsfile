pipeline {
    agent {
        kubernetes {
            // Spin up a Pod to execute the pipeline steps
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
                // Execute your build steps here...
            }
        }
        stage('Test') {
            steps {
                // Execute your testing steps here...
            }
        }
        stage('Deploy') {
            steps {
                // Execute your deployment steps here...
            }
        }
    }
}
