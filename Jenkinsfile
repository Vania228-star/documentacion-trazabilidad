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
                echo 'Subiendo la documentación generada al repositorio'
                sh '''
                    git config user.name "Jenkins"
                    git config user.email "jenkins@ci.local"
                    git add docs/
                    git diff --cached --quiet || git commit -m "docs: actualización automática de documentación [skip ci]"
                    git push origin HEAD:main || echo "Sin cambios que subir"
                '''
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