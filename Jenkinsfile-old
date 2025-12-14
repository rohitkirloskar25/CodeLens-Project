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
                expression { fileExists('src/test/python') }
            }
            steps {
                echo 'Testing Python code...'
                sh '''
                    set -e
                    echo "Python version:"
                    python3 --version
                    
                    # Install dependencies (if any)
                    if [ -f src/test/python/requirements.txt ]; then
                        pip install --break-system-packages -r src/test/python/requirements.txt
                    else
                        pip install --break-system-packages pytest
                    fi

                    # Add project root to PYTHONPATH so imports like "from src..." work
                    export PYTHONPATH=$PYTHONPATH:$(pwd)
                    
                    # Run tests
                    pytest src/test/python --maxfail=1 --disable-warnings -q
                '''
            }
        }
    }
}
