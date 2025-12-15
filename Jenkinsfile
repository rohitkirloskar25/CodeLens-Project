pipeline {
    agent any

    triggers {
        githubPush()
    }

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
    }

    stages {

        /* -------------------------------------------------------
           CHECKOUT (MANDATORY)
        ------------------------------------------------------- */
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        /* -------------------------------------------------------
           FILTER: Continue ONLY if src/main changed
        ------------------------------------------------------- */
        stage('Change Filter') {
            steps {
                script {
                    sh '''
                        echo "Previous commit: $GIT_PREVIOUS_SUCCESSFUL_COMMIT"
                        echo "Current commit:  $GIT_COMMIT"

                        if [ -z "$GIT_PREVIOUS_SUCCESSFUL_COMMIT" ]; then
                            git diff --name-only HEAD > changed_files.txt
                        else
                            git diff --name-only $GIT_PREVIOUS_SUCCESSFUL_COMMIT $GIT_COMMIT > changed_files.txt
                        fi

                        grep '^src/main/' changed_files.txt > changed_sources.txt || true
                    '''

                    def changes = readFile('changed_sources.txt').trim()
                    if (!changes) {
                        echo "❌ No changes in src/main/. Exiting pipeline."
                        currentBuild.result = 'NOT_BUILT'
                        return
                    }

                    echo "✅ src/main changes detected:"
                    echo changes
                }
            }
        }

        /* -------------------------------------------------------
           PREPARE SOURCE CODE
        ------------------------------------------------------- */
        stage('Prepare Source Code') {
            steps {
                sh '''
                    echo "=========== SOURCE CODE ===========" > uploaded_code.txt
                    while read file; do
                        [ -f "$file" ] && cat "$file" >> uploaded_code.txt
                    done < changed_sources.txt
                '''

                stash includes: 'uploaded_code.txt, changed_sources.txt',
                      name: 'source-code'
            }
        }

        /* -------------------------------------------------------
           GENERATE TESTS
        ------------------------------------------------------- */
        stage('Generate Tests') {
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
                        BASE=$(basename "$SOURCE_FILE")
                        NAME="${BASE%.*}"
                        EXT="${BASE##*.}"
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
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git config user.name "admin"
                        git config user.email "admin@codelens.com"

                        git add src/test/
                        git commit -m "Auto-generate tests for src/main changes" || true
                        git push https://$GIT_USER:$GIT_TOKEN@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }

        /* -------------------------------------------------------
           RUN TESTS
        ------------------------------------------------------- */
        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.11-slim'
                }
            }
            steps {
                sh '''
                    for test in src/test/*Tests.*; do
                        echo "Running $test"
                        python "$test" || exit 1
                    done
                '''
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
