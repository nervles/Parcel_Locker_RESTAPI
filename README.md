# Parcel Locker REST API

Welcome to the Parcel Locker REST API repository! This project showcases a fully functional parcel locker system powered by IoT technology and RESTful API communication. The parcel locker system is designed to securely store and manage packages, allowing users to conveniently retrieve their items upon authentication. 

### I was inexperienced when I did this so there are few shortcomings such as some variables in code are named in polish instead of english. But it's fully functional and I think easy to make.

## Features

- **IoT Device Integration:** The parcel locker utilizes an ESP32 microcontroller to manage the locking mechanism and monitor server variables.
- **RESTful API Communication:** Communication between the parcel locker and the server is established through RESTful API endpoints.
- **User Registration:** Users are required to register before using the parcel locker system.
- **Package Notification:** Upon receiving a package, registered users are notified via email with instructions to retrieve their items.
- **QR Code Access:** A QR code printed on the front doors allows easily send a package (You don't have to look for link its in qr code).

## Case
<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/665e8a17-2ddb-4c08-9e0c-a19d1df887fd" width=500 height=400> <img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/57a0c7fc-1dca-4a0b-9090-bc80a5c81d76" width=500 height=400>
<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/b33e4c1a-9e5b-4377-94ec-7c270138530f" width=500 height=400> <img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/14811229-851f-4c73-9bc3-322d98c96950" width=500 height=400>

## Hardware Components

The parcel locker system comprises the following hardware components:

- Electric Lock (Handmade by someone else)
- 5V Relay
- Step-Up Converter
- Step-Down Converter
- ESP32 Microcontroller
- Power Supply (6A, 15V)

## Wiring

This is a prototype diagram of wiring for this project. Later one another DC/DC converter was added but diagram was not updated.

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/a12256ba-157f-49ac-b70c-705bc6f41385" width=700 height=500>

Here is final wiring

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/4fb3137d-77c7-498c-bb7b-d2fb9a1091cb" width=500 height=600>

## How It Works

1. **User Registration:** Users must register with the system to utilize the parcel locker service. [Link](https://paczkomat.pythonanywhere.com/webpostuser)

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/2b50cbc2-17e6-43e5-9e2f-88318cf22b57" width=400 height=400>

2. **Package Sending:** Registered users can send packages through the system by accessing the website via the QR code on front doors or this link. You can see the list of users on [Link](https://paczkomat.pythonanywhere.com/web/users) and send it here [Link](https://paczkomat.pythonanywhere.com/web/sendpackage).
### After sending the package the parcel locker opens

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/fb06f545-0aeb-4117-a1cf-7cf16fe8a921" width=400 height=400>

3. **Package Notification:** Upon successful package delivery, users receive an email notification informing them of the arrival.
4. **Package Retrieval:** To retrieve the package, users follow the link provided in the email and input the corresponding password.

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/0d65e93e-12c0-4125-add9-d04a2153bfe7" width=600 height=200>

5. **Parcel Locker Access:** Upon successful authentication, the parcel locker opens, allowing users to collect their packages.

Please note that some variables within the code may be in Polish due to initial development stages, but they are easily understandable.

## Deployment

The parcel locker system is deployed on [PythonAnywhere.com](https://www.pythonanywhere.com/) for seamless access and functionality. The diagram of database uploaded on server. Original names of variables are in brackets and that is how they are in code but i translated them.

<img src="https://github.com/nervles/Parcel_Locker_RESTAPI/assets/130153131/8cbb63cf-781d-4f4c-bdc4-6a927effc2d2" width=700 height=300>


Thank you for exploring the Parcel Locker REST API project! If you have any questions or suggestions, feel free to reach out.

**Disclaimer:** The electric lock used in this project was handmade, and details about its specifications are not available. The power supply has been selected so that lock would function properly.


