pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install Pipfile'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}