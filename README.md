# Welcome to Docker Manipulation APIs

All APIs in this repository aim to manage pods running under service in Kubernetes. This repository is implemented to facilitate our agent in Reinforcement Learning (RL) from [Adaptive Autoscaler Repository](https://github.com/natnicha/master-thesis-auto-scaler).

Docker Manipulation APIs are implemented by [Python](https://www.python.org/), using [Docker SDK](https://docs.docker.com/reference/api/engine/sdk/)
and [Kubernetes Client](https://kubernetes.io/docs/reference/using-api/client-libraries/). This service is designed to centralize and streamline
communication with services on Kubernetes, thereby preventing circular dependencies in software architecture, and making maintenance easier.

## Built With

[<img src="https://www.python.org/static/img/python-logo.png" height="50">](https://www.python.org/) [<img src="https://cdn.freebiesupply.com/logos/large/2x/docker-logo-png-transparent.png" height="50">](https://docs.docker.com/reference/api/engine/sdk/) [<img src="https://juststickers.in/wp-content/uploads/2018/11/kubernetes-wordmark.png" height="50">](https://kubernetes.io/docs/reference/using-api/client-libraries/) [<img src="https://flask.palletsprojects.com/en/stable/_images/flask-horizontal.png" height="50">](https://flask.palletsprojects.com/en/stable/)

<img src="https://img.shields.io/badge/Test-Pass-green"> <img src="https://img.shields.io/badge/Secuiry-Pass-blue">

## Routes Information
Using [Flask](https://flask.palletsprojects.com/en/stable/), these following APIs are implemented.

1. **GET /pod**: This service provides clients with detailed and real-time information about the state of Pods in the system. It includes key performance metrics such as CPU and memory utilization percentages, which help assess the resource consumption and efficiency of each Pod. Additionally, the service reports the current number of active or running Pods, offering insights into the overall health and scale of the deployment.

2.  **POST /pod/confirm**: Similar to the GET /pod API, this API retrieves all relevant information and additionally terminates Pods that are not in a ’running’ status. In our study, the following statuses are considered unsatisfactory: 
- Pending - This status occurs when at least one primary container is initiated successfully, but the Pod is not yet fully operational.
- CrashLoopBackOff - This indicates the Pod is stuck in a restart loop due to an overloaded or incorrectly requested configuration. 
- ImagePullbackOff - This occurs when a container in the Pod fails to pull the required image from a container registry.
- Terminating - This status signifies that the Pod is scheduled for deletion but has not yet been fully removed from the node. By terminating Pods in these unsatisfactory states, we ensure that only active and healthy Pods remain. 

    This approach helps confirm that all operational Pods are ready, thereby facilitating the agent’s ability to learn and perform effectively.

1. **POST /pod/scale/in**: This API specifies a number of online Pods in the cluster and facilitates scaling in by reducing the number of Pods by one. Scaling-in refers to the process of decreasing the cluster size by terminating
one Pod, thereby freeing up resources when demand decreases. The scaling operation is constrained within a defined range, with a minimum of 1 Pod and a maximum of 5 Pods allowed.

1. **POST /pod/scale/out**: Similar to the POST /pod/scale/in API, this API specifies a number of online Pods in the cluster and facilitates scaling by adding one additional Pod. The scaling operation is designed to increase the number of Pods incrementally, with a limit on the number of Pods that can be scaled within the cluster. Specifically, the scaling is constrained within a range of 1 to 5 Pods, ensuring that the cluster remains within manageable limits.

2. **GET /app/stat**: Similar to the previous API, GET /pod, this API retrieves all relevant Pod information while also performing service testing, specifically following a scaling event. After gathering the necessary data, this API executes the Reward Feedback JMeter file. The JMeter file simulates traffic and captures performance metrics, which are then used to evaluate the system’s responsiveness post-scaling. Subsequently, the API calculates key performance indicators, specifically the average latency and packet drop percentage, which are crucial for RL reward computations. These metrics provide essential feedback that helps refine the agent’s decision-
making process, guiding it toward optimal scaling actions.


6. **POST /metrics**: This API collect metrics from the target application inlcuding CPU percentage, memory, online pods and total pods at a moment every, approximaltly, 0.2 seconds. This route has been specifically designed and implemented to provide dedicated support for thesis writing and the subsequent analysis of results.

7. **POST /pod/set-pod-count/<pod_count>**: This API has been implemented to enable administrators to manually configure the number of pods in the system. This feature is designed to provide a quick and effective solution for addressing unexpected issues or resource imbalances, ensuring system stability and performance. By allowing administrators to adjust pod counts as needed, this API helps maintain control over the system's scaling behavior, especially during times when automated scaling might not respond adequately to certain challenges or disruptions.

## Getting Started
To start and test the service, follow the below instruction.

### Starting the service
To run this service, go to a subfolder named `server`, and run the service by flask using the following command.
```
cd .\server\
```

```
flask run -p 6000
```


### Testing
You can simply test if your service is running success fully by opening a browser with the following website [http://localhost:6000/](http://localhost:6000/). If the service is running, you should see `Hello, World!` in the browser.


For further testing the service, use your prefer choices of API testing platforms, for example, [Postman](https://www.postman.com/). Then, use the above information for routes to make requests, for example, [http://localhost:6000/pod](http://localhost:6000/pod).

## Contributing
If you have any suggestion that would make our website looks better or more convenience, please fork the repo and create a merge requeste. You can also simply open an issue with the tag "enhancement". Don't forget to give the project a star! Thank you again!

1. Fork the Project
2. Create your Feature Branch
    ```
    git checkout -b feature/AwesomeFeature
    ```
3. Commit your Changes
    ```
    git commit -m 'Add some AwesomeFeature'
    ```
4. Push to the Branch
    ```
    git push origin feature/AwesomeFeature
    ```
5. Open a Pull Request

## Acknowledgment
The authors would like to express our sincere gratitude to Dr. habil. Julien Vitay, thesis supervisor from the professorship of Artificial Intelligence (Informatik) at Technische Universitat at Chemnitz, for his expert guidance, unwavering support, and valuable feedback throughout the research and writing process.

We also wish to express our heartfelt appreciation to M.Sc. Florian Zimmer, our research mentor and project advisor from [Fraunhofer-Institut fur Software- und Systemtechnik (ISST)](https://www.isst.fraunhofer.de/). His generous investment of time and effort in providing regular, detailed feedback at every stage of the project was invaluable. Additionally, his insightful advice and guidance were crucial in helping us navigate and overcome the challenges encountered throughout this study. 

Importantly, we would like to gratefully acknowledge the computing time made available to them on the high-performance computer Barnard and Alpha at the, Nationales Hochleistungsrechnen, NHR Center, at Zentrum f¨ur Informationsdienste und Hochleistungsrechnen (ZIH), at Technische Universit¨at Dresden. This center is jointly supported by the Federal Ministry of Education and Research and the state governments participating in the [NHR](www.nhr-verein.de/unsere-partner).

## Project Contributor & Support
This project is exclusively contributed by Natnicha Rodtong. For inquiries, feel free to contact me via [ResearchGate](https://www.researchgate.net/profile/Natnicha-Rodtong) or [email](nat.rodtong@gmail.com).

## Disclaimer
This repository is a component of a master's thesis titled `Adaptive Horizontal Pod Autoscaling (AHPA) Based on Reinforcement Learning in Kubernetes for Machine Learning`. The thesis explores advanced techniques for improving the scalability and efficiency of machine learning workloads in Kubernetes environments using reinforcement learning-based approaches for adaptive horizontal pod autoscaling. The research was conducted at [Laboratory of Artificial Intelligence, Technische Universität Chemnitz (TU Chemnitz)](https://www.tu-chemnitz.de/informatik/KI/index.php.en), Germany, as part of the requirements for completing the Master’s program. 

### Important Notes:
1. No Warranty: This project is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties of merchantability, fitness for a particular purpose, or non-infringement.
2. Limitation of Liability: The authors or contributors shall not be held liable for any claim, damages, or other liability arising from the use, misuse, or inability to use the content within this repository.
3. Third-Party Dependencies: This repository may rely on external libraries or tools that are subject to their own licenses. Please ensure compliance with those licenses when using this project.