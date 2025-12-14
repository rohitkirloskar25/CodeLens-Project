pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/rohitkirloskar25/CodeLens-Project.git'
            }
        }

        stage('Build') {
            steps {
                echo 'Building project...'
                // Example:
                // sh 'mvn clean package'
                // sh 'npm install'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                // sh 'mvn test'
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying...'
            }
        }
    }
}
