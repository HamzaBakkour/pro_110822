pipeline{
    agent {label 'host'}
     environment {
      PATH="/Users/alexa/Desktop/pro_110822/pro_110822_venv_11/Scripts:$PATH"
    }
   
    stages{

        stage ('Download dependices'){
            steps{
                withPythonEnv('/Users/alexa/Desktop/pro_110822/pro_110822_venv_11/Scripts/python')
                    {
                    bat '''
                    cd C:/Users/alexa/Desktop/pro_110822
                    py -m pip install -r requirements.txt
                    '''
                    }
                }
            }
   
        stage('Unit test'){
            steps{
                catchError(buildResult: 'FAILURE', stageResult: 'FAILURE'){
                    script{
                    def cmd = new StringBuilder()
                    cmd.append(" cd C:/Users/alexa/Desktop/pro_110822 ")  
                    cmd.append("  & py -m jenkins_pipline_tests_runner ")
                    def test_result = bat(
                        returnStdout: true,
                        script: "${cmd.toString()}")
                    echo test_result
                    
                    
                    publishHTML (target: [
                        reportDir: '/Users/alexa/Desktop/pro_110822/reports/unittest',
                        reportFiles: 'unittest_pro_110822.html',
                        reportName: "Unittest Report"
                        ])
                    
                    def result_string = test_result.toString()
                    def finished_with = result_string.split("RESULT:")[1] 
                    
                    echo "Finished with ${finished_with}"
                    
                    trimmed_result = finished_with.trim()
                    
                    
                    if (trimmed_result.equals("SUCESS")){
                        bat "exit 0"
                        }
                        
                    else if (trimmed_result.equals("FAILED")){
                        bat "exit -1"
                    }
                    else {
                        echo ("$Running unittest retuned: {trimmed_result}. Which is UNKNOWN result. Known results are: SUCESS and FAILED.")
                        bat "exit -1"
                            }
                        }
                    }
                }
            }
        
        stage('Coverage test'){
            steps{
                    bat '''
                    cd C:/Users/alexa/Desktop/pro_110822
                    coverage run -m unittest discover
                    coverage html
                    '''
                    publishHTML (target: [
                    reportDir: '/Users/alexa/Desktop/pro_110822/htmlcov',
                    reportFiles: 'index.html',
                    reportName: "Coverage Report"
                    ])
            }
        }
        
       stage('Build executable'){
        steps{
                    bat '''cd C:/Users/alexa/Desktop/pro_110822
                            py -m build_exe 0.%BUILD_NUMBER%
                            '''
            }
        }

    }
}