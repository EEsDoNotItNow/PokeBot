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
                sh 'python3 --version'
            }
        }
    }
}