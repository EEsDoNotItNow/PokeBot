pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'virtualenv .env'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}