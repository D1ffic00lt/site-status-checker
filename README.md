<h1 align="center">Site Status Checker</h1>
<h2 align="center">Console application for monitoring the status of sites from a .csv file</h2>

## Task
> You got a job as a system administrator in a small office. Your responsibilities include monitoring the health of multiple sites. You have successfully set up a server status mail notification from the hosting, but it turned out that this is not enough. And you decide to develop a small application in Python so that it sends you messages in case any of the sites becomes unavailable for any reason.

## Implementation
> - The application performs all necessary checks
> - The application works offline, informs when there is no Internet access
> - The application performs input checks
> - The application performs all necessary checks every hour

## Project structure, files and directories

### Files and directories

| Name                                                       | Description                                                                                                                                           |
|------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| [checker](checker)                                         | All main program code                                                                                                                                 |
| [checker/units](checker/units)                             | Custom errors, handlers and csv file readers                                                                                                          |
| [checker/units/controller.py](checker/units/controller.py) | Single site request handler                                                                                                                           |
| [checker/units/exceptions.py](checker/units/exceptions.py) | Custom errors                                                                                                                                         |
| [checker/&#95;&#95;init&#95;&#95;.py](checker/__init__.py) | Main project initialization file                                                                                                                      |
| [checker/config.py](checker/config.py)                     | Application configuration (regular expressions, log formats, etc.)                                                                                    |
| [checker/display.py](checker/display.py)                   | Web part of the application, responsible for outputting data to the console                                                                           |
| [app.py](app.py)                                           | Code (in some cases an example) that performs the function of deploying an application                                                                |
| [requirements.txt](requirements.txt)                       | Libraries required to use the application                                                                                                             |
| [Dockerfile](Dockerfile)                                   | Docker application image                                                                                                                              |
| [run.sh](run.sh)                                           | a bash script that deploys and executes a docker container if docker is available (otherwise, the library is installed and the app.py starts working) |

### Structure

```
.
├── checker
│   ├── units             
│   │   ├── __init__.py        
│   │   ├── controller.py
│   │   ├── exceptions.py
│   │   ├── exceptions.py
│   │   └── reader.py
│   ├── __init__.py
│   ├── config.py
│   ├── display.py
│   └── sitestatuschecker.py 
├── app.py
├── run.sh
├── README.md
├── .gitignore
├── Dockerfile
├── LICENCE.md
├── .dockerignore
└── requirements.txt
```

## Installation and launch
### Bash script (universal meth, almost...)

Bash scripts are almost everywhere (even in windows, sort of...)

When testing with this script, I managed to run the program on both Unix and Windows.

Run command:
```
bash run.sh
```

The script checks for the presence of docker on the computer and, depending on the result, launches 2 options:

> - Build and run the docker image
> - Installing all the necessary libraries from the requirements.txt, running the app.py python script

The entire code of the script can be found [here](run.sh)

### Docker
[Docker](https://www.docker.com)  is an open platform for developing, delivering and operating applications. Docker is designed to get your applications up and running faster. With Docker, you can decouple your application from your infrastructure and treat your infrastructure as a managed application. Docker helps you deploy your code faster, test faster, deploy applications faster, and reduce the time between coding and running code. Docker does this with a lightweight container virtualization platform, using processes and utilities to help manage and host your applications.

At its core, Docker allows you to run almost any application safely isolated in a container. Secure isolation allows you to run many containers on the same host at the same time. The lightweight nature of the container, which runs without the overhead of a hypervisor, allows you to get more out of your hardware.

#### Running the docker image
1. install docker on your computer
2. run docker (it is important that it starts completely)
3. Enter the command in the console
```bash
docker build --no-cache -t sitestatuschecker . && run -it sitestatuschecker
```
4. Wait for the end of the program build
5. Everything is ready to use!

### Python (3.10+)

__It is very important that the python version >= 3.10, otherwise the application will not work__

It is also possible to run through a regular python

1. In the console from the project directory, write the command
```
pip3 install -r requirements.txt
```
2. Wait for all libraries to be installed and send the command to the console from the bot directory
```
python3 app.py
```
3. Everything is ready to use!

## Exceptions

```
SSCException                  # Basic custom error
├── CSVReaderException        # Error while reading file         
│   ├── DataInvalidFormat     # Error in data format from .csv file  
│   └── FileInvalidFormat     # Critical file reading error (wrong extension, etc.)
├── CheckerException          # More warning than error (no access to IP address, TCP or HTTPS ports closed, etc.)
└── InternetConnectionError   # Internet connection error
```

## Example
```
[2023-03-12 18:12:58] [INFO]: Enter filename (csv): test.csv
[2023-03-12 18:13:01] [INFO]: Ignore errors in csv? (Y/N): y
[2023-03-12 18:13:02] [INFO]: Print errors? (Y/N): y
[2023-03-12 18:13:02] [INFO]: Worker created
[2023-03-12 18:13:02] [INFO]: Check starting...
[2023-03-12 18:13:02] [ERROR]: host must be not None
[2023-03-12 18:13:02] [INFO]: continue...
[2023-03-12 18:13:04] [INFO]: host: localhost	|	ip: 127.0.0.1	    |	RTT: 0.102 ms	  |	port: ???	|	multy ip: False
[2023-03-12 18:13:09] [INFO]: host: yandex.ru	|	ip: 5.255.255.50	|	RTT: 51.219 ms	|	port: ???	|	multy ip: True
[2023-03-12 18:13:09] [INFO]: host: yandex.ru	|	ip: 5.255.255.55	|	RTT: 51.934 ms	|	port: ???	|	multy ip: True
[2023-03-12 18:13:09] [INFO]: host: yandex.ru	|	ip: 77.88.55.66	  |	RTT: 53.820 ms	|	port: ???	|	multy ip: True
[2023-03-12 18:13:09] [INFO]: host: yandex.ru	|	ip: 77.88.55.70	  |	RTT: 49.834 ms	|	port: ???	|	multy ip: True
[2023-03-12 18:13:10] [WARNING]: ip is not success (last.fm)
[2023-03-12 18:13:13] [WARNING]: ip is not success (140.82.112.3)
[2023-03-12 18:13:15] [WARNING]: cant get host name by address
[2023-03-12 18:13:15] [INFO]: Check completed!
```
