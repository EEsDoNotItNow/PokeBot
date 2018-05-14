pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'pip install -p'
                sh 'pip freeze'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}