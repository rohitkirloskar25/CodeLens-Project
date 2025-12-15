pipeline {
    agent any

    environment {
        GEMINI_API_KEY = credentials('GEMINI_API_KEY')
        SOURCE_DIR = 'src/main/'
        TEST_DIR   = 'src/test/'
    }

    triggers {
        githubPush()
    }

    stages {

        stage('Change Filter') {
            steps {
                script {
                    def changedFiles = sh(
                        script: "git diff --name-only HEAD~1 HEAD || true",
                        returnStdout: true
                    ).trim()

                    echo "Changed files:\n${changedFiles}"

                    def sourceFiles = changedFiles
                        .split('\n')
                        .findAll { it.startsWith(env.SOURCE_DIR) }

                    if (sourceFiles.isEmpty()) {
                        echo "No changes in ${env.SOURCE_DIR}. Skipping pipeline."
                        currentBuild.result = 'NOT_BUILT'
                        error("Pipeline stopped – no relevant changes")
                    }

                    writeFile file: 'changed_sources.txt',
                              text: sourceFiles.join('\n')

                    echo "Source files to process:\n${sourceFiles.join('\n')}"
                }
            }
        }

        stage('Prepare Source Code') {
            steps {
                sh '''
                    echo "=========== SOURCE CODE ===========" > uploaded_code.txt

                    while read file; do
                        if [ -f "$file" ]; then
                            echo "\\n--- File: $file ---" >> uploaded_code.txt
                            cat "$file" >> uploaded_code.txt
                        fi
                    done < changed_sources.txt

                    echo "=========== END ===================" >> uploaded_code.txt
                '''

                stash includes: 'uploaded_code.txt, changed_sources.txt',
                      name: 'source-code'
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
                unstash 'source-code'

                sh '''
                    pip install --upgrade pip
                    pip install google-generativeai

                    mkdir -p ${TEST_DIR}

                    while read SOURCE_FILE; do
                        BASENAME=$(basename "$SOURCE_FILE")
                        NAME="${BASENAME%.*}"
                        EXT="${BASENAME##*.}"

                        TEST_FILE="${TEST_DIR}${NAME}Tests.${EXT}"

                        echo "Generating test for $SOURCE_FILE → $TEST_FILE"

                        python generate_tests.py "$SOURCE_FILE" > "$TEST_FILE"

                        echo "Generated:"
                        cat "$TEST_FILE"
                        echo "--------------------------------"
                    done < changed_sources.txt
                '''
            }
        }

        stage('Push Tests to GitHub') {
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

                        git add ${TEST_DIR}
                        git commit -m "Auto-generate unit tests for src/main changes" || echo "No changes to commit"

                        git push https://${GIT_USER}:${GIT_TOKEN}@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    for test in ${TEST_DIR}*Tests.*; do
                        echo "Running $test"
                        python "$test" || exit 1
                    done
                '''
            }
        }

        stage('Finish') {
            steps {
                echo "Pipeline completed successfully"
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'uploaded_code.txt, src/test/**/*',
                             allowEmptyArchive: true
        }
    }
}
