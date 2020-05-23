#!groovy

// https://rahmonov.me/posts/continuous-integration-and-continous-deployment-for-django-app-with-jenkins/
// https://www.ionutgavrilut.com/2019/jenkins-pipelines-sh-source-not-found/

node {

    try {
        stage 'Checkout'
            checkout scm

            sh 'git log HEAD^..HEAD --pretty="%h %an - %s" > GIT_CHANGES'
            def lastChanges = readFile('GIT_CHANGES')
            slackSend color: "warning", message: "Started `${env.JOB_NAME}#${env.BUILD_NUMBER}`\n\n_The changes:_\n${lastChanges}"

        stage 'Test'
            sh 'python3.8 -m venv ./venv'
            sh 'source venv/bin/activate'
            sh 'pip3 install -r requirements.txt'
            sh 'python3.8 manage.py jenkins --enable-coverage'


        stage 'Deploy'
            sh './deployment/deploy_prod.sh'

        stage 'Publish results'
            slackSend color: "good", message: "Build successful: `${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"
    }

    catch (err) {
        slackSend color: "danger", message: "Build failed :face_with_head_bandage: \n`${env.JOB_NAME}#${env.BUILD_NUMBER}` <${env.BUILD_URL}|Open in Jenkins>"

        throw err
    }

}
