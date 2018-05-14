pipeline {
    agent { dockerfile true } //{ additionalBuildArgs '--no-cache'}  if we wanted to be slower!

    stages {
        stage('Setup') {
            steps {
                sh 'echo Setup complete!'
            }
        }
        stage('build') {
            steps {
                withCredentials([string(credentialsId: 'CLIENT_TOKEN', variable: 'CLIENT_TOKEN')]) {
                    sh 'Test of the $CLIENT_TOKEN'
                }
                sh 'python3 --version'
            }
        }
    }
}