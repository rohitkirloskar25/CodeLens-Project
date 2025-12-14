pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        VENV_DIR = '.venv'
    }

    stages {

        stage('Setup Python Environment') {
            steps {
                sh '''
                    python3 -m venv ${VENV_DIR}
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install google-generativeai
                '''
            }
        }

        stage('Generate Tests') {
            steps {
                sh '''
                    . ${VENV_DIR}/bin/activate
                    python generate_tests.py > generated_tests.txt
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
