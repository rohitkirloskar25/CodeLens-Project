pipeline {
    agent any

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
                echo 'Running Java tests...'
                sh 'mvn test'
            }
        }

        stage('Test Python') {
            when {
                expression { fileExists('src/main/python') || fileExists('src/test/python') }
            }
            steps {
                echo 'Testing Python code...'
                // Install dependencies if requirements.txt exists
                sh '''
                if [ -f requirements.txt ]; then
                    pip install -r requirements.txt
                fi
                # Run pytest if tests exist
                if [ -d src/test/python ]; then
                    pytest src/test/python --maxfail=1 --disable-warnings -q
                else
                    echo "No Python tests found."
                fi
                '''
            }
        }
    }

    post {
        always {
            echo 'Build completed.'
        }
        success {
            echo '✅ Build and tests successful!'
        }
        failure {
            echo '❌ Build or tests failed!'
        }
    }
}
