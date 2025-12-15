pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        RUN_PIPELINE = "false"
    }

    stages {

        /* -------------------------------------------------------
           CHECKOUT (REQUIRED)
        ------------------------------------------------------- */
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* -------------------------------------------------------
           FILTER: Continue only if src/main changed
        ------------------------------------------------------- */
        stage('Change Filter') {
            steps {
                script {
                    sh '''
                        if [ -z "$GIT_PREVIOUS_SUCCESSFUL_COMMIT" ]; then
                            git diff --name-only HEAD > changed_files.txt
                        else
                            git diff --name-only $GIT_PREVIOUS_SUCCESSFUL_COMMIT $GIT_COMMIT > changed_files.txt
                        fi

                        grep '^src/main/' changed_files.txt > changed_sources.txt || true
                    '''

                    def changes = readFile('changed_sources.txt').trim()

                    if (changes) {
                        env.RUN_PIPELINE = "true"
                        echo "✅ Changes detected in src/main/:"
                        echo changes
                    } else {
                        echo "⏭ No changes in src/main/. Pipeline will be skipped."
                    }
                }
            }
        }

        /* -------------------------------------------------------
           PREPARE SOURCE CODE
        ------------------------------------------------------- */
        stage('Prepare Source Code') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            steps {
                sh '''
                    echo "=========== SOURCE CODE ===========" > uploaded_code.txt

                    while read file; do
                        [ -f "$file" ] && cat "$file" >> uploaded_code.txt
                    done < changed_sources.txt

                    echo "=========== END ===================" >> uploaded_code.txt
                '''

                stash includes: 'uploaded_code.txt, changed_sources.txt',
                      name: 'source-code'
            }
        }

        /* -------------------------------------------------------
           GENERATE TESTS
        ------------------------------------------------------- */
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
                    pip install google-generativeai
                    mkdir -p src/test

                    while read SOURCE_FILE; do
                        BASENAME=$(basename "$SOURCE_FILE")
                        NAME="${BASENAME%.*}"
                        EXT="${BASENAME##*.}"
                        TEST_FILE="src/test/${NAME}Tests.${EXT}"

                        echo "Generating test: $TEST_FILE"
                        python generate_tests.py "$SOURCE_FILE" > "$TEST_FILE"
                    done < changed_sources.txt
                '''
            }
        }

        /* -------------------------------------------------------
           PUSH GENERATED TESTS
        ------------------------------------------------------- */
        stage('Push Tests to GitHub') {
            when {
                expression { env.RUN_PIPELINE == "true" }
            }
            steps {
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

                        git add src/test/
                        git commit -m "Auto-generate unit tests for src/main changes" || true

                        git push https://$GIT_USER:$GIT_TOKEN@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }

        /* -------------------------------------------------------
           RUN TESTS (INTENTIONALLY EMPTY)
        ------------------------------------------------------- */
        stage('Run Tests') {
            echo "Starting to run Tests"
        }

        /* -------------------------------------------------------
           FINISH (INTENTIONALLY EMPTY)
        ------------------------------------------------------- */
        stage('Finish') {
            steps {
                echo "Pipeline finished"
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
