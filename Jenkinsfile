pipeline {
    agent { dockerfile true } //{ additionalBuildArgs '--no-cache'}  if we wanted to be slower!

    environment {
        LC_ALL = 'C.UTF-8'
        LANG = 'C.UTF-8'
        temp = "${GIT_URL}".replaceAll("\\.git","")
        myGitURL = "${temp}/commit/${GIT_COMMIT}"
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
                sh './run_unittests.sh'
            }
        }
        stage('Post Analysis') {
            steps{
                script {
                    sh 'flake8 --exit-zero'
                    if ( GIT_BRANCH == 'master' || GIT_BRANCH == 'development' ){
                        echo "We are on ${GIT_BRANCH}, and will accept _zero_ pep8 errors!"
                        maxPepFails = '0'
                    } else {
                        echo "We are on ${GIT_BRANCH}, allow pep errors"
                        maxPepFails = ''
                    } 

                    step([$class: 'WarningsPublisher',
                        canRunOnFailed: true,
                        consoleParsers: [
                            [parserName: 'pep8']
                        ],
                        defaultEncoding: '',
                        excludePattern: '',
                        failedNewAll: '',
                        failedTotalAll: maxPepFails,
                        healthy: '',
                        includePattern: '',
                        messagesPattern: '',
                        unHealthy: '',
                        useDeltaValues: true,
                        useStableBuildAsReference: true
                    ])
                }
            }
        }
    }
    post {
        always {
            script {
                if (env.GIT_COMMIT != env.GIT_PREVIOUS_SUCCESSFUL_COMMIT) {
                    discordSend description: "Jenkins Pipeline Build: ${GIT_BRANCH}#${env.BUILD_ID}\n\nResult: ${currentBuild.currentResult}", link: "${myGitURL}", footer: 'Have a nice build!', successful: currentBuild.resultIsBetterOrEqualTo('SUCCESS'), title: "${GIT_COMMIT}", webhookURL: 'https://discordapp.com/api/webhooks/445449456117219328/wRdFW4QjHKSoA-5Kt16gFCNdVVGeBAo9eOo63saSD2s9IB1BFNfT65s5zjDCVvx-Whcc'
                }
            }
        }
    }
}
