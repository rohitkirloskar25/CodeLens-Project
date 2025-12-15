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
                    echo "=========== LAST UPLOADED FILES ===========" > uploaded_code.txt

                    if git rev-parse HEAD~1 >/dev/null 2>&1; then
                        FILES=$(git diff --name-only HEAD~1 HEAD)
                    else
                        FILES=$(git ls-files)
                    fi

                    for file in $FILES; do
                        if [ -f "$file" ]; then
                            echo "\\n--- File: $file ---" >> uploaded_code.txt
                            cat "$file" >> uploaded_code.txt
                        fi
                    done

                    echo "============= END OF CODE =================" >> uploaded_code.txt
                '''
                // Save the file for use in Docker container
                stash includes: 'uploaded_code.txt', name: 'uploaded-code'
            }
        }

        stage('Generate Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                // Retrieve stashed code
                unstash 'uploaded-code'
                echo "Generating Tests from uploaded code..."
                sh '''
                    python --version
                    echo "===== CODE SENT TO TEST GENERATOR ====="
                    cat uploaded_code.txt
                    echo "======================================"

                    # Run test generator if script exists
                    if [ -f generate_tests.py ]; then
                        TEST_OUTPUT=$(python generate_tests.py uploaded_code.txt)
                        echo "===== GENERATED TEST CASES ====="
                        echo "$TEST_OUTPUT"
                        echo "================================"
                    else
                        echo "generate_tests.py not found!"
                    fi
                '''
            }
        }

        stage('Push Code to GitHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_TOKEN')]) {
                    sh '''
                        git config user.name "admin"
                        git config user.email "admin@codelens.com"

                        git add uploaded_code.txt
                        git commit -m "Add uploaded_code.txt from Jenkins" || echo "No changes to commit"
                        git push https://$GIT_USER:$GIT_TOKEN@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo "Running Tests..."
                // Add commands to actually run tests if needed
            }
        }

        stage('Finish') {
            steps {
                echo 'Done... End of pipeline'
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'uploaded_code.txt', allowEmptyArchive: true
        }
    }
}
