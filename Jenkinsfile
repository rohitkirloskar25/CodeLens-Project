pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {

        stage('Setup Environment') {
            steps {
                echo 'Skipping Python setup (not needed yet)'
            }
        }

        stage('Read Code') {
            steps {
                echo 'Reading last uploaded (changed) code...'

                sh '''
                    echo "=========== LAST UPLOADED FILES ==========="

                    if git rev-parse HEAD~1 >/dev/null 2>&1; then
                        FILES=$(git diff --name-only HEAD~1 HEAD)
                    else
                        FILES=$(git ls-files)
                    fi

                    for file in $FILES; do
                        if [ -f "$file" ]; then
                            echo "\\n--- File: $file ---"
                            cat "$file"

                            # Persist code for later stages
                            echo "\\n--- File: $file ---" >> uploaded_code.txt
                            cat "$file" >> uploaded_code.txt
                        fi
                    done

                    echo "============= END OF CODE ================="
                '''
            }
        }

        stage('Generate Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                echo "Generating Tests from uploaded code..."

                sh '''
                    python --version

                    echo "===== CODE SENT TO TEST GENERATOR ====="
                    cat uploaded_code.txt
                    echo "======================================"

                    TEST_OUTPUT=$(python generate_tests.py uploaded_code.txt)

                    echo "===== GENERATED TEST CASES ====="
                    echo "$TEST_OUTPUT"
                    echo "================================"
                '''
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Tests"
            }
        }

        stage('Finish') {
            steps {
                echo 'Done... End of program'
            }
        }
    }
}
