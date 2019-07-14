#  Project 4 - Item Catalog

Item Catalog is a catalog website designed as part of the Udacity Web Full Stack Nanodegree.

# About

This is the fourth project in the Full Stack Nanodegree. It consists in developing a website where users
can execute all CRUD (Create, Read, Update and Delete) operations on a list of itens within a variety of categories.
User authentication and authorization also has to be implemented. RESTful endpoints are also defined to serve
users data as JSON. Third-party authentication with Google or Facebook, as well as libraries such as Flask, 
Bootsrap, Jinja2, and SQLite were employed during development.

The project rubric can be found [here](https://review.udacity.com/#!/rubrics/2216/view)

# Skills used in this project

* Python
* HTML
* CSS
* Bootstrap
* Flask
* Jinja2
* SQLAlchemy
* Toastr
* OAuth
* Flask-Dance

# Executing the project

1. Make sure you have [Vagrant](https://www.vagrantup.com/downloads) and 
[Virtual Box](https://www.virtualbox.org/wiki/Downloads) installed in your machine.

2. Clone the [fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository.

3. Run ```vagrant up``` from the vagrant folder of the newly cloned repository to configure your VM.

4. Clone this repository, and replace the ```catalog``` folder in the 
[fullstack-nanodegree-vm](https://github.com/udacity/fullstack-nanodegree-vm) repository with this
repository contents.

5. Run ```pip install -r requirements.txt``` from the ```catalog``` folder to install the necessary libs.

6. Run ```vagrant ssh``` to login into the VM.

7. Navigate to the ```catalog``` folder inside the VM and run ```python database_setup.py``` to create the database
and then ```python populate_database.py``` to populate it with some data.

8. To sart the server, run ```python app.py```.

9. The server will be accessible from the address http://localhost:5000.



