# Assignment
Repository for assignment

## Arquitectura
- Step Functions:
  - Lambda de descarga diaria
  - Bucket que recibe el CSV 
  - Fargate (contenedor) de transformacion e insercion en la base de datos RDS
- VPC con subnets publicas

## Suposiciones
- Esta funcion es unica y no tomara como parametros fuentes de datos distintas, solo la url de data de incendios
- El archivo de incidentes no crece demasiado dia a dia (el original conteniendo data desde 2003 pesa 200 MB)

## Decisiones de implementacion
- Se usara el ID de incidencia como indicador ascendente de la vigencia del dataset. 
- El tamaño del archivo diario permite procesarlo de manera serverless sin necesidad de un cluster de procesamiento.
- Se usara la libreria Pandas + SQLAlchemy para insertar los registros diarios
- Se usaran dos schemas:
  - Analytics: Schema para consumo de usuarios finales y herramientas de BI
  - Staging: Schema de carga de paso, sin coerciones de tipos de datos

# Modelo de Datos
- Se identificaron 1 tabla fact y dos tablas de dimension
  - Incidentes (Fact): Contiene la informacion de performance de la unidad de bomberos (tiempos de respuestas, personal asignado) y datos del incidente respecto a ayuda a personas
  - Geografia (Dimension): Contiene la informacion geografica de los incidentes
  - Buildings (Dimension): Contiene la informacion de afectacion de los edificios del incidente, y sus caracteristicas.

