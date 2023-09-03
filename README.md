# Giftly online store

![Giftly Preview](./preview.png)

Giftly is an online store platform with features tailored for both users and administrators.

## Our final project for SDA done by

1) Kaarel - KaarelF
2) Erich - Erjokul
3) Demi - ddemip
4) Natalja - nataljj


This is a website for selling fun little gifts to other people. Gifts are sorted into categories, so there is 
something for everyone.

## Key Features:

- **User and Admin Panels**: While users can view products categorized by main and sub-categories, admins have the privilege to add or delete them.
  
- **Weather Widget**: Shows real-time weather data, specifically the temperature in Tallinn.
  
- **UI Elements**: Includes static Bootstrap files for a responsive and user-friendly design.
  
- **User Account Management**: Allows account creation, profile updates, and account settings.
  
- **Gift Ordering System**: Seamlessly process payments via cards and mobile phones.
  
- **Database**: The platform runs on MySQL.

## Getting Started

Ensure you have [Docker installed](https://docs.docker.com/get-docker/) on your system. Docker is available for Windows, Linux, and macOS.

#### Clone the repository

- If you're using PyCharm:
    1. Click on "Get from VCS".
    2. Enter the repository URL: `https://github.com/ddemip/giftly.git`

- Alternatively, using the terminal or command prompt:
    ```bash
    git clone https://github.com/ddemip/giftly.git
    cd giftly
    ```

### Build and Run the App

1. Using the terminal or command prompt, navigate to the root directory of the project.
2. Build and start the application:
    ```bash
    docker-compose up --build
    ```
3. Once the services are up, the website will be accessible at `http://127.0.0.1:8000`.

## Reporting Issues

If you encounter any bugs or issues, please let us know! We are committed to making continuous improvements to ensure a seamless user experience.