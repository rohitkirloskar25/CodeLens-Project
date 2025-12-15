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
                echo "$GEMINI_API_KEY"
            }
        }

        stage('Read Code') {
            steps {
                echo 'Reading last uploaded (changed) code...'

                sh '''
                    echo "=========== LAST UPLOADED FILES ==========="

                    FILES=$(git diff --name-only HEAD~1 HEAD)

                    for file in $FILES; do
                        if [ -f "$file" ]; then
                            echo "\\n--- File: $file ---"
                            cat "$file"
                        fi
                    done

                    echo "============= END OF CODE ================="
                '''
            }
        }

        stage('Generate Tests') {
            steps {
                echo "Generating Tests"
                // intentionally left empty
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Tests"
                // intentionally left empty
            }
        }

        stage('Finish') {
            steps {
                echo 'Done... End of program'
            }
        }
    }
}
