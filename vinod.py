pipeline {
    agent any

    environment {
        IMAGE_NAME = "vipolink-local"
        CONTAINER_NAME = "vipolink-local-container"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/guptavinodqwerty-cyber/vipolink.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                docker build -t $IMAGE_NAME .
                '''
            }
        }

        stage('Run Application') {
            steps {
                sh '''
                docker rm -f $CONTAINER_NAME || true
                docker run --name $CONTAINER_NAME $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo "✅ Local CI/CD completed successfully"
        }
        failure {
            echo "❌ Local CI/CD failed"
        }
    }
}
