The CPSC5330 Docker Image

* The files in bda_class_image are the files used to construct the image. 
  They are there for your interest.  If you are pulling the image from DockerHub, you won't use them
* The script run-image starts an interactive terminal container with the class image, using the bash shell
* The script run-image-with-mount allows you to create a mount point between a folder on your
    computer and a directory in the Docker image.  In class I will use this mount point to work with
    programs and files that are in the course Github repository, so you can access those files through GitHub.
    You will need to change variables in that script to run it yourself