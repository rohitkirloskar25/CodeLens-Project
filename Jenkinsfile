pipeline {
    agent any

    triggers {
        githubPush()
    }

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
                        echo "No changes in src/main/. Exiting pipeline early."
                        currentBuild.result = 'NOT_BUILT'
                        return
                    }

                    echo "Source files changed:"
                    echo changes
                }
            }
        }

        stage('Prepare Source Code') {
            when {
                expression { fileExists('changed_sources.txt') }
            }
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

        stage('Generate Tests') {
            when {
                expression { fileExists('changed_sources.txt') }
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
                        BASE=$(basename "$SOURCE_FILE")
                        NAME="${BASE%.*}"
                        EXT="${BASE##*.}"
                        python generate_tests.py "$SOURCE_FILE" \
                          > "src/test/${NAME}Tests.${EXT}"
                    done < changed_sources.txt
                '''
            }
        }

        stage('Push Tests') {
            when {
                expression { fileExists('src/test') }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'github-creds',
                    usernameVariable: 'GIT_USER',
                    passwordVariable: 'GIT_TOKEN'
                )]) {
                    sh '''
                        git add src/test/
                        git commit -m "Auto-generate tests" || true
                        git push https://$GIT_USER:$GIT_TOKEN@github.com/rohitkirloskar25/CodeLens-Project.git HEAD:main
                    '''
                }
            }
        }
    }
}
