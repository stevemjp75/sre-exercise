#!/bin/bash

# colour codes for echo
green='\033[0;32m'
yellow='\033[1;33m'
red='\033[0;31m'

# Deployment variables, change as required
IMAGE_NAME="flask-md5"
CONTAINER_NAME="md5-generator"
PORT="80"

# Function to check if the container is running
is_container_running() {
    if [ "$(docker ps -q -f name=${CONTAINER_NAME})" ]; then
        return 0
    else
        return 1
    fi
}

# Function to stop and delete running container
cleanup_containers() {
    if is_container_running; then
        echo -e "${yellow}Container running, stopping ${CONTAINER_NAME}..." 
        docker stop ${CONTAINER_NAME} > /dev/null 2>&1
        echo -e "Deleting ${CONTAINER_NAME}..."
        docker rm ${CONTAINER_NAME} > /dev/null 2>&1
    fi
}

# Function to build new image
build_image() {
    echo -e "${green}Building image: ${IMAGE_NAME}"
    docker build -t ${IMAGE_NAME} .
}

# Function to start container as daemon
start_container() {
    echo -e "${green}Starting ${CONTAINER_NAME}..."
    docker run -d -p ${PORT}:8080 --name ${CONTAINER_NAME} ${IMAGE_NAME} > /dev/null 2>&1
}

# Function to loop until the container is running or 30 sec timeout is reached
wait_for_container() {
    check_count=0
    while [ $check_count -lt 15 ]; do
        if is_container_running; then
            echo -e "${green}Container ${CONTAINER_NAME} is running."
            exit 0
        fi

        # Increment the check counter
        ((check_count++))
        
        # Sleep for 2 seconds
        echo -e "${yellow}Waiting for container ${CONTAINER_NAME} to start..."
        sleep 2
    done

    # If the loop exits, the timeout was reached and the containter did not start
    echo -e "${red}Timeout. Container ${CONTAINER_NAME} failed to start."
    exit 1
}

cleanup_containers
build_image
start_container
wait_for_container
exit $?
