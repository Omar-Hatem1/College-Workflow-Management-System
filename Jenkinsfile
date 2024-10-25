pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/Omar-Hatem1/College-Workflow-Management-System'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build('college-workflow-management-system')
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    docker.image('college-workflow-management-system').inside {
                        sh 'python manage.py test'
                    }
                }
            }
        }
        
        stage('Deploy') {
            steps {
                script {
                    docker.image('college-workflow-management-system').run("-p 8000:8000")
                }
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
