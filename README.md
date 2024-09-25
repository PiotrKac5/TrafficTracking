# Traffic Tracking
Web application tracking and counting vehicles live from one of intersections in Cracow.
</br>

https://github.com/user-attachments/assets/b6ac1bbb-709c-4cb4-8447-1ceacc7b36bd

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Features](#features)
- [How It Works](#how-it-works)
- [Technical Details](#technical-details)
- [License](#license)

## About the Project
Web app used to track and count vehicles at an intersection in Cracow. 
</br> </br>
At home page client receives live-time video of the
*[intersection](https://go.toya.net.pl/25-kamery/14022-krakow/444414022167-zbigniewa-herberta-trasa-lagiewnicka/play)* after processing.
*(There is about 1 to 3 minutes delay compared to the live camera feed.)* All processing is done by using **YOLOv10s** model trained on custom dataset and **OpenCV** library.
It includes applying bounding boxes on tracked vehicles, predicted type of vehicle and confidence of prediction. In addition center of each vehicle is shown as circle. 
When vehicle appears near one of the red lines, the counter is increased and color of the line changes to green. Counter at top left of video is zeroed after every 15min.
The app tracks vehicles only in designated regions of the image, achieved by applying a **mask** to each video frame. 
The mask can be viewed in the "About" section of the website.
</br></br>

https://github.com/user-attachments/assets/1c49fb8d-668e-47d4-9038-a01a724cfcfe

</br></br>
By clicking on plots you can explore plots of how many cars there was at certain time range. *Note: If monthly plots lack data, it means the server hasn't been running long enough.*
*Warning!!! When running app locally plots will be generated from sample data prepared by ChatGPT* 
</br></br>
![image](https://github.com/user-attachments/assets/40850e88-6f19-4c8b-8f85-15f8d49b0739)
</br>
<p align="center">
Sample plot
</p>

</br> </br>
In about section on website you can watch sample video and add/remove **mask** to see in what regions of image vehicles are tracked.
</br></br>
![image](https://github.com/user-attachments/assets/fd7ecd9d-84ec-4b62-9249-2eda746a2179)

</br> </br>
**This project is designed for educational and non-comercial use only.**

## Getting Started
### Prerequisites
- **Docker**: Make sure Docker is installed on your system. Follow [this guide](https://docs.docker.com/get-docker/) to install Docker on your platform.
- **GPU Support** (optional but recommended): For better performance, it's recommended to enable GPU support in Docker. You can find instructions for setting up
[NVIDIA Docker](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/install-guide.html).

## Usage
### 1. Clone the repo
```
git clone https://github.com/pkacprzak5/TrafficTracking.git
```

### 2. Navigate to repository path
```
cd <your-path>/TrafficTracking
```

### 3. Download dependencies and run app in Docker
```
docker-compose up --build
```

### 4. Explore application
After everything is set up correctly visit ```http://localhost:80``` to interact with web application.

## Features
- Real-time video processing
- Plotting historical data
- Microservice architecture
- GPU support

## How It Works
1. The app downloads video from of the specified intersection in Cracow from [ToyaGO](https://go.toya.net.pl/25-kamery/14022-krakow/444414022167-zbigniewa-herberta-trasa-lagiewnicka/play).
2. **Mask** is added to video before processing it.
3. The video is processed using the YOLOv10s model to detect and classify vehicles.
4. Vehicles crossing designated lines are counted and displayed in real-time.
5. Each frame is published through redis from microservice to backend.
6. Backend sends each frame through WebSockets to client.
7. Buffer on frontend is created to ensure no stuttering.
8. The data is stored and used to generate historical traffic plots.

## Technical Details
The Traffic Tracking application uses a microservice-based architecture with the following key components:

### 1. **Frontend**
- Built using React for user interaction and video display.

### 2. **Backend**
- Built using Flask and Flask-SocketIO for real-time video processing and communication.

### 3. **Video Processing Engine**
- Python-based video processing engine using **OpenCV** for image manipulation and the *custom-trained* **YOLOv10s** model for vehicle detection.

### 4. **Redis**
- Redis is used as a message broker for communication between services and for caching real-time data.

### 5. **Docker**
- The entire application is containerized using Docker, with Docker Compose managing the services.
- **GPU Support**: Optional GPU acceleration can be enabled using NVIDIA Docker for faster video processing.

## License
Distributed under the MIT License. See ```LICENSE``` for more information.
