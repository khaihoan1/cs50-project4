# cs50-project4

## This is my work for CS50 Web Programming with Python and JavaScript course's [Project 4 - Network](https://cs50.harvard.edu/web/2020/projects/4/network/)

You can quickly run this webapp using Docker container, as following steps:
- Clone this repo > https://github.com/khaihoan1/cs50-project4
- Change into root of the repo, docker-compose up the webapp:

    <code>docker-compose up -d</code>
- Now you have a container for the webapp linked with a Postgresql container, you need to migrate to have the right tables for the operation:

    <code>docker-compose run webapp python manage migrate</code>

Now, you have the webapp running