# MD5 Hash Generator Service Documentation

## Table of Contents

1. [Overview](#overview)
2. [Deployment](#deployment)
3. [Maintenance](#maintenance)
4. [Accessing the Service](#accessing-the-service)
5. [Additional Information](#additional-information)

---

## Overview

The MD5 Hash Generator Service is a web application that allows users to upload a file and receive an MD5 hash for that file. It is built using Flask and runs inside a Docker container. 

This service uses a simple web interface to facilitate file uploads and display the corresponding MD5 hash and filename as outputs.

## Deployment

### Prerequisites

- An operating system with a bash interpreter such as Linux or WSL2.
- Docker installed on your machine.
- Basic understanding of shell scripting and Docker.

### Steps to Deploy

1. **Clone the Repository**

   ```bash
   git clone https://github.com/stevemjp75/sre-exercise.git
   cd flask-md5
   ```
2. **Deploy the service** 
    
    You may need to give permissions to make the script executable:
    ```bash
    chmod +x deploy.sh
    ```
    Run the script to deploy:

    ```bash
    ./deploy.sh
    ```
    

## Maintenance

1. **Stopping the Service**

    To stop the running container, use:
    ```bash
    docker stop md5-generator
    ```
2. **Starting the service**
    
    To start the container, use:
    
    ```bash
    docker run -d -p 80:8080 --name md5-generator flask-md5
    ```

3. **Removing the Container**

    To remove the container, use:
    ```bash
    docker rm md5-generator
    ```
4. **Viewing Logs**

    To view the logs of the running container, use:
    ```bash
    docker logs md5-generator
    <use -f to follow logs and get a real-time output>
    ```
5. **Rebuilding the Image**

    If you make changes to the app.py or Dockerfile, rebuild the image using:
    ```bash
    docker build -t flask-md5 .
    ```
    Alternatively, and recommened, re-run the ```deploy.sh``` script as above.

6. **Changing the port**
    
    Default ports:
    - Web server: Port 80
    - Python app: Port 8080
    
    To change the web server port you should edit the ```deploy.sh``` script and set the ```PORT``` variable to your requirement:
    ```bash
    PORT="80"
    ```
    Alternatively, you can run the following command to launch a new instance of the containter:
    ```bash
    docker run -d -p <web_listening_port>:8080 --name md5-generator flask-md5
    ```
    To change the Python app port, you need to update the dockerfile to:
     ```
     EXPOSE: <python_app_port_number>
     ```
    You would also need to update the port in the app.py to match the port exposed by docker:
    ```bash
    # Run the Flask application
    if __name__ == '__main__':
    app.run(host='0.0.0.0', port=<python_app_port_number>)
    ```
    Finally, run the ```deploy.sh``` to build and deploy a new image with the updated ports.

 ### General Information

In general, it's better to use the deploy script once you have made any changes. This will build a fresh container with the latest configuration, clean-up the previous version, deploy and start the new one automatically for you.

## Accessing the Service
### Using a Web Browser
1. **Open a Web Browser**

    - Navigate to the IP address or hostname of the machine running the Docker container, using port 80. For example:
      ```bash
      http://localhost:80
       ```
2. **Uploading a File**
    - Use the provided form on the main page to select a file from your local machine.
    - Click the "Upload" button to submit the file.

3. **Receiving the MD5 Hash**
    - After the file is uploaded, the page will display the file name and its MD5 hash.

### From the command line using CURL
1. **Open your terminal and enter:**
    ```bash
    curl -sF "file=@<path_to_file>" http://<IP address or hostname>:80/upload | grep -G -o '<h2[^>]*>.*</h2>'
    ```
    example:
    ```bash
    curl -sF "file=@./app.py" http://localhost:80/upload | grep -G -o '<h2[^>]*>.*</h2>'

    File: app.py
    MD5 Hash: bfa9181a927eebf31962aa92dd901b56
    ```
    
2. **Using the grep**
    - You can omit the grep command at the end of the file but it will return the entire html body, using the grep will extract just the h2 tags used in the response which is the filename and the hash.

## Additional Information

### Dockerfile (```dockerfile```)

The Dockerfile sets up the Docker image with the following steps:
- Uses the python:3.10-slim image as the base.
- Sets the working directory to /app.
- Copies app.py into the container at /app.
- Installs Flask via pip.
- Creates an /uploads directory.
- Exposes port 8080.
- Runs the Flask application (app.py) when the container starts.

### Flask Application (```app.py```)

The Flask application provides:
- Main Page: Displays an HTML form for file uploads and the file name and corresponding MD5 hash from the response.
- Upload Endpoint: Handles file uploads, calculates the MD5 hash, and deletes the file after processing.

### Deployment Script (```deploy.sh```)

The script performs the following tasks:

  - Checks if a container named md5-generator is already running. If it is, the script stops and removes it.
  - Builds a new Docker image named flask-md5.
  - Starts a new container named md5-generator using the built image.
  - Waits for the container to be up and running, with a timeout of 30 seconds.

The deploy script will provide verbose outputs and correct exit codes should you wish to run this using an automation tool such as Jenkins or Ansible.
