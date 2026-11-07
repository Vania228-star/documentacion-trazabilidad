pipeline {
    agent any

    environment {
        GITHUB_USER = 'Vania228-star'
        REPO_NAME   = 'documentacion-trazabilidad'
    }

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    stages {

        stage('Build') {
            steps {
                echo '=== Etapa 1: BUILD - Instalar dependencias ==='
                sh '''
                    pip3 install --break-system-packages -r requirements.txt
                    python3 -c "import flask, pytest; print('Dependencias instaladas OK')"
                '''
            }
        }

        stage('Test') {
            steps {
                echo '=== Etapa 2: TEST - Pruebas unitarias ==='
                sh '''
                    python3 -m pytest test_app.py -v --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit 'test-results.xml'
                }
            }
        }

        stage('Generate Documentation') {
            steps {
                echo '=== Etapa 3: GENERATE DOCUMENTATION - Doxygen ==='
                sh '''
                    doxygen Doxyfile
                    test -f docs/html/index.html
                    echo "Documentacion HTML generada correctamente"
                '''
            }
        }

        stage('Version Control') {
            steps {
                echo '=== Etapa 4: VERSION CONTROL - Publicar docs en Git ==='
                withCredentials([usernamePassword(credentialsId: 'github-creds', usernameVariable: 'GIT_USER', passwordVariable: 'GIT_PASS')]) {
                    sh '''
                        git config user.name "Jenkins"
                        git config user.email "jenkins@ci.local"
                        git add docs/
                        git add test-results.xml 2>/dev/null || true
                        if git diff --cached --quiet; then
                            echo "Documentacion actualizada. Nada que commitear."
                        else
                            git commit -m "docs: actualizacion automatica de documentacion [skip ci]"
                            git push https://${GIT_USER}:${GIT_PASS}@github.com/Vania228-star/documentacion-trazabilidad.git HEAD:main
                        fi
                    '''
                }
            }
        }

        stage('Deploy') {
            steps {
                echo '=== Etapa 5: DEPLOY - Entorno de pruebas ==='
                sh '''
                    pkill -f "python3 app.py" || true
                    nohup python3 app.py > app.log 2>&1 &
                    sleep 5
                    curl -s "http://localhost:5000/hello?name=Prueba"
                    echo ""
                '''
            }
        }
    }

    post {
        success {
            echo "Pipeline completado - Build #${BUILD_NUMBER} exitoso"
        }
        failure {
            echo "FALLO en el pipeline - Revisar build #${BUILD_NUMBER}"
        }
        always {
            archiveArtifacts artifacts: '**/test-results.xml, docs/html/**', allowEmptyArchive: true
        }
    }
}