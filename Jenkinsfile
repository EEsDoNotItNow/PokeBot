pipeline {
    agent { docker { image 'debian:stable' } }
    stages {
        stage('Setup') {
            steps {
                sh 'apt-get install -y make build-essential libssl-dev zlib1g-dev'
                sh 'apt-get install -y libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm'
                sh 'apt-get install -y libncurses5-dev  libncursesw5-dev xz-utils tk-dev'
            }
        }
        stage('build') {
            steps {
                sh 'python --version'
            }
        }
    }
}