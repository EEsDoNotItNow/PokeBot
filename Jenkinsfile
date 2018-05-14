pipeline {
    agent { dockerfile true } //{ additionalBuildArgs '--no-cache'}  if we wanted to be slower!



    environment {
        LC_ALL = 'C.UTF-8'
        LANG = 'C.UTF-8'
        myGitURL = "${GIT_URL}".replaceAll("\\.git","")
        myGitURL = "${myGitURL}/commit/${GIT_COMMIT}"
    }

    stages {
        stage('Setup') {
            steps {
                sh 'echo ${myGitURL}'
                sh 'echo Setup complete!'

                
            }
        }
        stage('Unit testing') {
            steps {
                withCredentials([string(credentialsId: 'CLIENT_TOKEN', variable: 'CLIENT_TOKEN')]) {
                    sh 'echo Test of the $CLIENT_TOKEN'
                }
                sh 'python3 --version'
                sh 'rm poke.db || true'
                sh 'python3 -m unittest -v'
            }
        }
    }
    post {
        always {
            discordSend description: "Jenkins Pipeline Build: ${GIT_BRANCH}#${env.BUILD_ID}\n\nResult: ${currentBuild.currentResult}", link: "${myGitURL}", footer: 'Have a nice build!', successful: currentBuild.resultIsBetterOrEqualTo('SUCCESS'), title: '${GIT_COMMIT}', webhookURL: 'https://discordapp.com/api/webhooks/445449456117219328/wRdFW4QjHKSoA-5Kt16gFCNdVVGeBAo9eOo63saSD2s9IB1BFNfT65s5zjDCVvx-Whcc'
        }
    }
}