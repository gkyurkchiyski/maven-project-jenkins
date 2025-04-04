pipeline {
    agent any

    environment {
        LT_USERNAME = credentials('lambda_test_username')  // Use Jenkins Credentials for security
        LT_ACCESS_KEY = credentials('lambda_test_access_key')
    }

    stages {
        stage('Setup') {
            steps {
                script {
                    // Download and setup LambdaTest Tunnel
                    sh 'wget https://downloads.lambdatest.com/tunnel/v3/linux/64bit/LT_Linux.zip'
                    sh 'sudo apt-get install -y zip unzip'
                    sh 'unzip -o LT_Linux.zip'
                    sh 'chmod +x LT'
                    
                    // Start the LambdaTest Tunnel in the background
                    sh """
                    ./LT --user ${LT_USERNAME} --key ${LT_ACCESS_KEY} --tunnelName jenkins-tunnel --infoAPIport 8000 &
                    """
                    
                    // Wait until the tunnel is ready
                    def tunnelReady = false
                    retry(5) {
                        sh(script: "curl --silent http://127.0.0.1:8000/api/v1.0/status", returnStdout: true) { 
                            if (it.contains("tunnelStatus\": \"started\"")) {
                                tunnelReady = true
                            }
                        }
                        if (!tunnelReady) {
                            echo "Waiting for the tunnel to be ready..."
                            sleep 10
                        }
                    }

                    if (!tunnelReady) {
                        error "LambdaTest Tunnel failed to start."
                    }
                }
            }
        }

        stage('Test') {
            steps {
                script {
                    // Start HTTP Server
                    sh 'python3 -m http.server 8081 &'

                    // Wait for HTTP server to be ready
                    sh 'sleep 5'  // Optional - Adjust this depending on the server load and startup time

                    // Run your test
                    sh 'python3 test_sample_todo_app.py'

                    // Stop the server
                    sh 'pkill -f "http.server"'
                    
                    // Optionally, ensure the server is stopped properly before moving to the next step
                    sh 'sleep 5'

                    // Stop LambdaTest Tunnel
                    sh 'curl -X DELETE http://127.0.0.1:8000/api/v1.0/stop'
                }
            }
        }
    }

    post {
        always {
            script {
                // Cleanup: Ensure LambdaTest Tunnel is stopped
                sh 'pkill -f "LT" || true'
                // Optionally, perform any other necessary cleanup steps
            }
        }
    }
}