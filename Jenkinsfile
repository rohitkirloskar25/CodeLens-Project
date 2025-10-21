pipeline {
    agent any
    tools {
        maven 'jenkins-maven'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Java') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                echo 'Building Java project with Maven...'
                sh 'mvn -B -DskipTests clean package'
            }
        }

        stage('Test Java') {
            when {
                expression { fileExists('pom.xml') }
            }
            steps {
                sh 'mvn test'
            }
        }

        stage('Test Python') {
            when {
                expression { fileExists('src/main/python') || fileExists('src/test/python') }
            }
            steps {
                echo 'Testing Python code...'
                sh '''
                    python3 --version
                    if [ -f requirements.txt ]; then
                        pip install -r requirements.txt
                    fi
                    if [ -d src/test/python ]; then
                        pytest src/test/python --maxfail=1 --disable-warnings -q
                    fi
                '''
            }
        }
    }
}
