apoxz.org
=========

The redesign of the APO XZ public website.

Introduction
------------

This repository is meant to aid in the collaboration between developers of the
new APO XZ public website. The website should be primarily data-driven and
allow an ease of updating the content for empowered users that are not familar
with web technologies.

Developer Setup
---------------

The recommended approach for developers to test locally is to create a virtual
machine and use git and a receive hook to automatically update the code in their
test environment and restart necessary processes in the environment.

1. Check out this project to your local machine.
2. Create a new Ubuntu Server 12.04 virtual machine.
3. When creating a user, choose "ubuntu" as the username and "tiger" as the password.
4. At the end of the installation process, choose to install only the SSH package.
5. After installation, obtain the IP address of the virtual machine and SSH into it.
6. Use SFTP to copy the web_setup.sh script in this project to the ubuntu user's home directory.
7. Make the script executable and execute the script as root (```chmod 755 web_setup.sh; sudo ./web_setup.sh```).
8. The script will prompt you to create a new database user. Create a user with the username "root" and password "tiger".
9. Toward the end, the script will prompt you for the database password. Enter "tiger".
10. On your local machine, navigate to the directory of this project.
11. Add the virtual machine as a remote repository to the git project. ```git remote add dev-apoxz ssh://ubuntu@ip.of.v.m/opt/apoxz.org.git```
12. Syncronize the revision history from the project to the remote repository. ```git push dev-apoxz +master:refs/heads/master```
13. To push new code that you have committed locally: ```git push dev-apoxz```