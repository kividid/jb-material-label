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
                script {
                def buildImage = docker.build("test-image")
                println "New image, " + buildImage.id
                }
            }
        }
        stage('Push container') {
            steps {
                script {
                    buildImage.push()
                }
            }
        }
    }
}