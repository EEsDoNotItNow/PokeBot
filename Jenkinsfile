pipeline {
    agent { dockerfile true }
    stages {
        stage('Setup') {
            steps {
                sh 'echo Setup complete!'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}