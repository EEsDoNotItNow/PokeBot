pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install --user -r requirements.txt'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}