pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'pip3 install -p Pipfile'
                sh 'pip3 freeze'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}