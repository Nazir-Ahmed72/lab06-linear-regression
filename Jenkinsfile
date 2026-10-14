pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
        disableConcurrentBuilds()
        timeout(time: 150, unit: 'SECONDS')
    }

    triggers {
        githubPush()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build') {
            steps {
                sh '''
                    set -eu
                    docker compose config --quiet
                    docker compose down --remove-orphans
                    docker compose pull
                    docker compose up -d --wait --wait-timeout 90

                    curl --fail --silent --show-error \
                      "http://127.0.0.1:5000/predict?x1=2&x2=3&x3=1"
                '''
            }
        }
    }

    post {
        success {
            echo 'Prediction API is running on port 5000.'
        }

        failure {
            sh '''
                docker compose ps || true
                docker compose logs --tail=100 || true
            '''
        }
    }
}
