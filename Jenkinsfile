pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

        stage('Build') {
            steps {
                echo 'Building project...'
                // Example:
                // sh 'mvn clean package'
                // sh 'npm install'
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
