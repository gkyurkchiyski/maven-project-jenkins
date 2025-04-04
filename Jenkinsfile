pipeline {
  agent any
  stages {
  stage('Setup') {
    steps {
      sh 'wget https://downloads.lambdatest.com/tunnel/v3/linux/64bit/LT_Linux.zip'
      sh 'sudo apt-get install -y zip unzip''
      sh 'unzip -o LT_Linux.zip'
      sh './LT --user $(LT_USERNAME) --key $(LT_ACCESS_KEY) --tunnelName jenkins-tunnel --infoAPIport 8000 &'
    }
  }

  stage('Test') {
    steps {
      sh 'sleep 5'
      sh 'python3 -m http.server 8081 &'
      sh 'python3 test_sample_todo_app.py'
      sh 'pkill -f "http_server"'
      sh 'sleep 10'
      sh 'curl -X DELETE http://127.0.0.1/api/v1.0/stop'
    }
  }
}
}