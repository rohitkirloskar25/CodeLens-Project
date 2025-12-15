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
                        fi
                    done

                    echo "============= END OF CODE ================="
                '''
            }
        }

        stage('Generate Tests') {
            steps {
                echo "Generating Tests"
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
