pipeline {
    agent { dockerfile true } //{ additionalBuildArgs '--no-cache'}  if we wanted to be slower!

    environment {
        LC_ALL = 'C.UTF-8'
        LANG = 'C.UTF-8'
    }

    stages {
        stage('Setup') {
            steps {
                sh 'echo Setup complete!'
            }
        }
        stage('Unit testing') {
            steps {
                withCredentials([string(credentialsId: 'CLIENT_TOKEN', variable: 'CLIENT_TOKEN')]) {
                    sh 'echo Test of the $CLIENT_TOKEN'
                }
                sh 'python3 --version'
                sh 'python3 -m unittest -v'
            }
        }
    }
}