pipeline {
    agent any

    environment {
        FLASK_PORT = '5001'
        WIREMOCK_PORT = '9090'
    }

    stages {
        stage('Get Code') {
            steps {
                git branch: 'master', url: 'https://github.com/escribano89/helloworld'
                echo "Current workspace: ${env.WORKSPACE}"
                bat 'dir "%WORKSPACE%"'
            }
        }

        stage('Unit Tests') {
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        where python
                        set PYTHONPATH=%WORKSPACE%
                        python -m coverage run --branch --source=app --omit=app\\_init.py,app\\api.py -m pytest --junitxml=result-unit.xml test\\unit
                    '''
                }
                junit "result*.xml"
            }
        }

        stage('Coverage') {
            steps {
                bat '''
                    python -m coverage report
                    python -m coverage xml
                '''

                catchError(buildResult: 'UNSTABLE', stageResult: 'UNSTABLE') {
                    cobertura coberturaReportFile: 'coverage.xml',
                            conditionalCoverageTargets: '100,80,90',
                            lineCoverageTargets: '100,85,95'
                }
            }
        }

        stage('Static') {
            steps {
                bat 'flake8 --exit-zero --format=pylint app >flake8.out'
                recordIssues tools: [flake8(name: 'Flake8', pattern: 'flake8.out')], 
                            qualityGates: [[threshold: 8, type: 'TOTAL', unstable: true], 
                                            [threshold: 10, type: 'TOTAL', unstable: false]] 

            }
        }

        stage('Security') {
            steps {
                bat '''
                    bandit --exit-zero -r . -f custom -o bandit.out --msg-template "{abspath}:{line}: [{test_id}]: {msg}"
                '''
                recordIssues tools: [pyLint(name: 'Bandit', pattern: 'bandit.out')], 
                    qualityGates: [[threshold: 2, type: 'TOTAL', unstable: true], 
                                    [threshold: 4, type: 'TOTAL', unstable: false]]
            }
        }

        stage('Performance') {
            steps {
                echo "Starting Flask..."
                bat '''
                    set FLASK_APP=app\\api.py
                    set PYTHONPATH=%WORKSPACE%
                    start /B python -m flask run --port=%FLASK_PORT%
                '''
    
                echo "Comprobando flask..."

                retry(3) {
                    bat 'curl -s http://127.0.0.1:%FLASK_PORT% || exit 1'
                }
                bat '''
                    C:\\Users\\escribano\\Downloads\\apache-jmeter-5.6.3\\apache-jmeter-5.6.3\\bin\\jmeter -n -t test\\jmeter\\test-plan.jmx -f -l flask.jtl
                '''
                perfReport sourceDataFiles: 'flask.jtl'
                
            }
        }
    }
}
