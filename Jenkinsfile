pipeline {
    agent any
    options {
        buildDiscarder(logRotator(numToKeepStr: '3'))
    }
    stages {
        stage('Get latest repo'){
          steps {
              checkout scm

          }  
        }
        stage('Build docker') {
            steps {
                sh 'docker build -t labels:latest'
            }
        }
    }
}