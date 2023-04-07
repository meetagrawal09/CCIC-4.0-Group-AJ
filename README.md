# CCIC 4.0 - Group-AJ

## Team Members 
- Meet Agrawal ([@meetagrawal09](https://github.com/meetagrawal09)) 
- Lankesh Purekar ([@ravanlankesh](https://github.com/ravanlankesh))

## Prerequisites
Before you can use this project, you will need to have Python and pip installed on your system. If you don't already have them installed, you can download the latest version of Python from the [Python website](https://www.python.org/) and use pip to install it.

## Setting up a Virtual Environment

It is recommended to set up a virtual environment for this project to ensure that the dependencies and packages installed for this project do not conflict with any other packages on your system. To set up a virtual environment, navigate to the root directory of the project and run the following command:

    python -m venv env

This will create a new virtual environment called  `env`.

To activate the virtual environment, run the following command:

* For Linux based systems: 

      source env/bin/activate

* For Windows based systems:

      ./env/Scripts/activate
    
Your virtual environment is now active, and any packages you install will be isolated to this environment.

## Installation

To install the required dependencies for this project, run the following command:

    pip install -r requirements.txt

This will install all of the packages listed in the `requirements.txt` file.

## Usage

To run the `build_reports` script, navigate to the `TaskQueue` directory of the project and run the following command:

    python build_report.py
    
This will execute the `build_reports` script and generate the necessary reports.
