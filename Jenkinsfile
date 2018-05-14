pipeline {
    agent { dockerfile true }
    stages {
        stage('Setup') {
            steps {
                sh 'pipenv install'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}