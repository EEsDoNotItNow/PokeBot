pipeline {
    agent { docker { image 'python:3.6.5' } }
    stages {
        stage('Setup') {
            steps {
                sh 'pipenv install'
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