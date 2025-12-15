pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {

        stage('Change Filter') {
            steps {
                script {
                    sh '''
                        git diff --name-only HEAD~1 HEAD > changed_files.txt || true
                        grep '^src/main/' changed_files.txt > changed_sources.txt || true
                    '''

                    def changes = readFile('changed_sources.txt').trim()
                    if (!changes) {
                        echo "No changes in src/main/. Skipping pipeline."
                        currentBuild.result = 'NOT_BUILT'
                        env.RUN_PIPELINE = "false"
                    } else {
                        env.RUN_PIPELINE = "true"
                        echo "Changed source files:"
                        echo changes
                    }
                }
            }
        }

        stage('Prepare Source Code') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            steps {
                sh '''
                    echo "=========== MODIFIED FILES ===========" 
                    cat changed_sources.txt
                    echo "====================================="

                    echo "=========== SOURCE CODE (CONSOLE) ===========" 
                    echo "=========== SOURCE CODE ===========" > uploaded_code.txt

                    while read file; do
                        if [ -f "$file" ]; then
                            echo ""
                            echo "----- FILE: $file -----"
                            cat "$file"
                            echo "-----------------------"

                            echo "\\n--- File: $file ---" >> uploaded_code.txt
                            cat "$file" >> uploaded_code.txt
                        fi
                    done < changed_sources.txt

                    echo "=========== END ===================" >> uploaded_code.txt
                '''

                stash includes: 'uploaded_code.txt, changed_sources.txt', name: 'source-code'
            }
        }

        stage('Generate Tests') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                unstash 'source-code'

                sh '''
                    pip install --upgrade pip
                    pip install google-generativeai

                    mkdir -p src/test

                    while read SOURCE_FILE; do
                        BASENAME=$(basename "$SOURCE_FILE")
                        NAME="${BASENAME%.*}"
                        EXT="${BASENAME##*.}"
                        TEST_FILE="src/test/${NAME}Tests.${EXT}"

                        echo ""
                        echo "===== GENERATING TEST FOR: $SOURCE_FILE ====="

                        python generate_tests.py "$SOURCE_FILE" > "$TEST_FILE"

                        echo "----- GENERATED TEST CODE ($TEST_FILE) -----"
                        cat "$TEST_FILE"
                        echo "-------------------------------------------"
                    done < changed_sources.txt
                '''

                stash includes: 'src/test/**', name: 'generated-tests'
            }
        }

        stage('Push Tests to GitHub') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            steps {
                unstash 'generated-tests'
                withCredentials([
                    usernamePassword(
                        credentialsId: 'github-creds',
                        usernameVariable: 'GIT_USER',
                        passwordVariable: 'GIT_TOKEN'
                    )
                ]) {
                    sh '''
                        git config user.name "admin"
                        git config user.email "admin@codelens.com"

                        while read SOURCE_FILE; do
                            BASENAME=$(basename "$SOURCE_FILE")
                            NAME="${BASENAME%.*}"
                            EXT="${BASENAME##*.}"
                            TEST_FILE="src/test/${NAME}Tests.${EXT}"

                            if [ -f "$TEST_FILE" ]; then
                                echo "Adding $TEST_FILE"
                                git add "$TEST_FILE"
                            else
                                echo "Test file not found: $TEST_FILE"
                            fi
                        done < changed_sources.txt

                        git status

                        git commit -m "Auto-generate unit tests for src/main changes" \
                            || echo "No changes to commit"

                        git push https://$GIT_USER:$GIT_TOKEN@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }

        stage('Run Tests') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            agent {
                docker {
                    image 'python:3.11-slim'
                    args '-u root'
                }
            }
            steps {
                unstash 'generated-tests'
                unstash 'source-code'

                sh '''
                    echo "====================================="
                    echo "========== RUNNING TESTS =========="
                    echo "====================================="

                    pip install --upgrade pip

                    export PYTHONPATH=$PYTHONPATH:$(pwd)

                    TEST_EXIT_CODE=0
                    while read SOURCE_FILE; do
                        BASENAME=$(basename "$SOURCE_FILE")
                        NAME="${BASENAME%.*}"
                        EXT="${BASENAME##*.}"
                        TEST_FILE="src/test/${NAME}Tests.${EXT}"

                        if [ -f "$TEST_FILE" ]; then
                            echo ""
                            echo "--- Executing $TEST_FILE ---"
                            python "$TEST_FILE" || TEST_EXIT_CODE=1
                        else
                            echo "Warning: Test file not found for $SOURCE_FILE."
                        fi
                    done < changed_sources.txt

                    if [ $TEST_EXIT_CODE -ne 0 ]; then
                        echo "====================================="
                        echo "!!! UNIT TESTS FAILED !!!"
                        echo "====================================="
                        exit 1
                    else
                        echo "====================================="
                        echo "✅ ALL UNIT TESTS PASSED ✅"
                        echo "====================================="
                    fi
                '''
            }
        }

        stage('Finish') {
            steps {
                echo "Finish stage intentionally left empty"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'uploaded_code.txt, src/test/*',
                             allowEmptyArchive: true
        }
    }
}
