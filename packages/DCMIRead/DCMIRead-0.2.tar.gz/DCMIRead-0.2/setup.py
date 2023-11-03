import setuptools

#Si tienes un readme
with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='DCMIRead',  #nombre del paquete
     version='0.2', #versión
     scripts=['DCMIRead/dicom_reader.py'] , #nombre del ejecutable
     author="Jorge Felix Martinez", #autor
     author_email="jorgito16040@gmail.com", #email
     description="A package to read and normalize DICOM images", #Breve descripción
     long_description=long_description,
     long_description_content_type="text/markdown", #Incluir el README.md si lo has creado
     url="https://github.com/WiseGeorge/DCMIRead", #url donde se encuentra tu paquete en Github
     packages=setuptools.find_packages(), #buscamos todas las dependecias necesarias para que tu paquete funcione (por ejemplo numpy, scipy, etc.)
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
) 
