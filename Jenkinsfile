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
                def buildImage = docker.build("test-image")
                //sh 'docker build -t labels:latest .'
            }
        }
    }
}