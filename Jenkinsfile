pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup') {
            steps {
                sh 'wget https://downloads.lambdatest.com/tunnel/v3/linux/64bit/LT_Linux.zip'
                sh 'sudo apt-get install -y zip unzip'
                sh 'unzip -o LT_Linux.zip'
                sh 'chmod +x LT'
                sh '''
                  set -e # Exit on error
                  ./LT --user YOUR_LAMBDATEST_USERNAME --key YOUR_LAMBDATEST_ACCESS_KEY --tunnelName jenkins-tunnel # Corrected command
                '''
                sh 'sleep 10'
            }
        }
        stage('Test') {
            steps {
                sh '''
                  set -e
                  # Check if port 8081 is in use (Linux example)
                  if netstat -tulnp | grep :8081; then
                    echo "Port 8081 is in use. Trying to kill the process..."
                    lsof -i :8081 | awk 'NR==2 {print $2}' | xargs kill -9  # Find and kill the process
                    sleep 5 # Give it time to release the port
                    if netstat -tulnp | grep :8081; then
                      echo "Failed to kill process on port 8081. Using a different port."
                      python3 -m http.server 8082 # Try a different port
                    else
                      python3 -m http.server 8081 # Retry on the original port
                    fi
                  else
                    python3 -m http.server 8081
                  fi
                '''
                sh 'sleep 5'
                sh 'python3 test_sample_todo_app.py'
                sh 'pkill -f http.server'
                sh 'sleep 10'
                sh '''
                  set -e
                  curl -X DELETE http://127.0.0.1:8000/api/v1.0/stop # Verify the port!
                '''
            }
        }
        post {
            always {
                sh 'pkill -f LT'
            }
        }
    }
}