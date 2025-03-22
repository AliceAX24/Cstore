# C/C++ Package Manager
This project is a simple client-server application for managing C/C++ libraries. It allows users to upload, download, and search for libraries. The server stores the libraries, and the client interacts with the server to perform operations.

## Table of Contents
1. [Installation](#Installation)
2. [Features](#Features)
3. [Contact](#Contact)

# Installation
## Prerequisites
Python 3.6 or higher
pip (Python package manager)

# Steps
## Download the main file to run here:
curl -o cstore.py cstore.servehttp.com:8080/download

## Install dependencies:
Ensure that this libraries exists.
requests, hashlib, webbrowser, json

# Run the client:
To start the client, run:
python Cstore.py
The client provides a command-line interface with the following commands:

## create_account:
Prompts for an email and password to create a new account.

## login:
Prompts for an email and password to log in.

## upload:
Prompts for the path to a folder. The folder's structure will be uploaded to the server.

## download:
Prompts for the name of the library to download. The library will be downloaded and extracted to the current directory.

## search:
Prompts for a search term. Returns a list of libraries matching the search term.

## exit:
Exits the client.

# Features
User Authentication: Users can create accounts and log in to upload and download libraries.

Library Management: Users can upload, download, and search for libraries.

Folder Structure Preservation: Uploaded libraries retain their folder structure.

Daily Upload Limit: Users are limited to 3 uploads per day to prevent abuse.

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.

Create a new branch for your feature or bugfix.

Commit your changes.

Submit a pull request.

# Contact
For questions or support, please contact:

Your Name: alice.schifelbein.caetano@gmail.com

GitHub: AliceAX24
