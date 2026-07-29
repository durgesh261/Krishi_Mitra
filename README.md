# 🌱 Krishi Mitra

An AI-powered agriculture assistance platform that helps farmers make informed decisions by providing crop recommendations, agricultural insights, and easy access to farming-related information.

## 📌 Overview

Krishi Mitra is designed to support farmers with modern technology by offering intelligent recommendations and a simple, user-friendly interface. The platform aims to improve productivity by helping users select suitable crops, access farming guidance, and manage agricultural information efficiently.

## ✨ Features

* 🔐 Secure user authentication and authorization
* 🌾 Crop recommendation and agricultural guidance
* 👤 Farmer profile management
* 📊 Dashboard for viewing recommendations and updates
* 🗄️ Database integration for storing user and crop information
* 🌐 RESTful backend architecture
* 📱 Responsive and easy-to-use interface

## 🛠️ Tech Stack

### Backend

* Java
* Spring Boot
* Spring Security
* Spring Data JPA
* Hibernate

### Database

* MySQL

### Frontend

* HTML
* CSS
* Bootstrap
* Thymeleaf

### Tools

* Git
* GitHub
* Maven
* IntelliJ IDEA / Eclipse

## 🏗️ Project Architecture

```
Client
   │
   ▼
Spring Boot Application
   │
   ├── Authentication
   ├── Crop Recommendation Module
   ├── Farmer Management
   ├── Service Layer
   ├── Repository Layer
   ▼
MySQL Database
```

## 📂 Project Structure

```
src
├── controller
├── service
├── repository
├── model
├── dto
├── config
├── security
├── resources
│   ├── templates
│   ├── static
│   └── application.properties
└── main
```

## 🚀 Getting Started

### Prerequisites

* Java 17 or later
* Maven
* MySQL
* Git

### Installation

1. Clone the repository.

```bash
git clone https://github.com/durgesh261/Krishi_Mitra.git
```

2. Navigate to the project folder.

```bash
cd Krishi-Mitra
```

3. Configure the MySQL database in `application.properties`.

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/krishi_mitra
spring.datasource.username=your_username
spring.datasource.password=your_password
```

4. Build the project.

```bash
mvn clean install
```

5. Run the application.

```bash
mvn spring-boot:run
```

6. Open your browser.

```
http://localhost:8080
```

## 🎯 Future Enhancements

* AI-based disease detection using crop images
* Weather forecast integration
* Market price prediction
* Fertilizer recommendation system
* Multilingual support
* Mobile application
* AI chatbot for farming assistance

## 📸 Screenshots

Add screenshots of the following pages:

* Login Page
* Dashboard
* Crop Recommendation Page
* Farmer Profile
* Admin Dashboard

## 👨‍💻 Author

**Durgesh Kanjariya**

* GitHub: https://github.com/durgesh261
* LinkedIn: https://linkedin.com/in/durgesh-kanjariya-389a91252

## 📄 License

This project is available for educational and learning purposes. Feel free to fork, explore, and contribute.
