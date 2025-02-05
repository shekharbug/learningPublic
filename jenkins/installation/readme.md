# Installation of Jenkins on Docker:

## 1) installation of docker

## 2) Prerequisites
### Minimum hardware requirements:
### 256 MB of RAM
### 1 GB of drive space (although 10 GB is a recommended minimum if running Jenkins as a Docker container)

## 3) Downloading and running Jenkins in Docker
### Use the recommended official jenkins/jenkins image from the Docker Hub repository.
### However, this image doesn’t contain Docker CLI, and is not bundled with the frequently used Blue Ocean plugins and its features.
### To use the full power of Jenkins and Docker, you may want to go through the installation process described below.

### 3.1) Create a bridge network in Docker
 #### $ docker network create jenkins
