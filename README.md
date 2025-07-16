# Installation Guide: 

To run the program, you will need docker installed. 

Installation instructions for all supported operating systems can be found here: 

https://docs.docker.com/engine/install/ 

 

 

1. Cd into team44_project. 

2. Run the following command, “aiVis” provides the tag for the image and can be changed: 

```docker build -t aiVis . ```

If you get a permission denied you can either run the command with sudo or add docker to the appropriate user group.

Instructions can be found here: 

https://docs.docker.com/engine/install/linux-postinstall/ 

3. You can view your currently built images by running: 

```docker images ```

4. Run the following command to start the container 

```docker run -p 8080:80 aiVis ```

5. Navigate to: `localhost:8080` In your internet browser URL bar 

 
## Test CSV

We have provided a CSV in `Example-CSV` to allow you to play around with the website without
needing your own dataset.

## User Manual

A comprehensive user manual can be found [here](https://team44usermanual.netlify.app/)
