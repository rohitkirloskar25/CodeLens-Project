pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {
        stage('Build') {
            steps {
                echo 'Building project...'
            }
        }

        stage('Generate Tests') {
            steps {
                sh '''
                    python3 generate_tests.py > generated_tests.txt
                '''
            }
        }

        stage('Ending') {
            steps {
                echo 'Done... End of program'
            }
        }
    }
}
