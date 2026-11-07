pipeline {
    agent any

    environment {
        GITHUB_USER = 'Vania228-star'
        REPO_NAME   = 'documentacion-trazabilidad'
    }

    stages {
        stage('Build') {
            steps {
                echo 'Instalando dependencias del proyecto'
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Ejecutando pruebas unitarias'
                sh 'python3 -m pytest test_app.py -v'
            }
        }

        stage('Generate Documentation') {
            steps {
                echo 'Generando documentación con Doxygen'
                sh 'doxygen Doxyfile'
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
                echo 'Desplegando la aplicación en entorno de prueba'
                sh '''
                    nohup python3 app.py > app.log 2>&1 &
                    sleep 5
                    curl -s "http://localhost:5000/hello?name=Prueba" && echo ""
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completado correctamente. Documentación actualizada.'
        }
        failure {
            echo 'FALLO en el pipeline: revisar etapa y corregir a la brevedad.'
        }
    }
}