pipeline {
    agent any

    stages {
        stage('Setup Python Dependencies') {
            steps {
                sh '''
                    python3 -m pip install --user google-generativeai
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building project...'
            }
        }

        stage('Generate Tests') {
            steps {
                withCredentials([string(credentialsId: 'GEMINI_API_KEY', variable: 'GEMINI_API_KEY')]) {
                    sh '''
                        python3 generate_tests.py > generated_tests.txt
                    '''
                }
            }
        }

        stage('Ending') {
            steps {
                echo 'Done... End of program'
            }
        }
    }
}
