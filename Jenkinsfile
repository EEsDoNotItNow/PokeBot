pipeline {
    agent { dockerfile true }
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