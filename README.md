# API YaMDb

Review, rate, discuss — engage with your favorites!

## Description

Enhance your application's user interaction with our versatile API, specifically designed for effortless integration and powerful capabilities. Collect and manage user reviews on various works across categories such as Books, Movies, and Music. Though the works themselves are not hosted on YaMDb, our API provides a platform for users to share their opinions and rate the works.

Administrators have the exclusive ability to add works, categories, and genres, ensuring a well-curated database. Users can then leave text reviews and rate works on a scale from one to ten, contributing to an aggregate rating for each work. To maintain fairness, each user is allowed only one review per work.

In addition to reviews, our API supports commenting, allowing users to engage in discussions about the reviews. This creates a dynamic community where opinions and discussions flourish. Only authenticated users can participate in reviewing, commenting, and rating, ensuring a reliable and engaged user base.

With our API, you can effortlessly deliver a rich, interactive experience, encouraging users to share their insights and engage in meaningful conversations.

## Getting Started

### List of used technologies

* `Python`
* `Django REST Framework`
* `Django ORM`
* `SQLite`

### Dependencies

You can find all used packages in `requirements.txt` file.

### Installation

Use the following commands in your terminal to prepare your project for local lauch and modification.

* Creating local copy of the project
```
git clone https://github.com/ArtemMaksimov-trial/api_yamdb.git
```
* Creating virtual environment from the root folder `.../api_yamdb`
```
python -m venv venv
```
* Activating a virtual environment
```
source venv/Scripts/activate
```
* Setting up of the required dependencies
```
pip install -r requirements.txt
```
* Switching to an internal folder `.../api_yamdb/api_yamdb`
```
cd api_yamdb
```
* Creating and applying of necessary migrations
```
python manage.py makemigrations
python manage.py migrate
```
* Importing .csv fixtures
```
python manage.py import_data
```
* Creating superuser
```
python manage.py createsuperuser
```
* Running of the local server
```
python manage.py runserver
```

Now you are ready to use our API through any of web or desktop platform for your choice!

## Contact

Artem Maksimov - [@ovienrait](https://t.me/ovienrait) - [nirendsound@gmail.com](https://nirendsound@gmail.com)

Project Link: [API YaMDb](https://github.com/ArtemMaksimov-trial/api_yamdb.git)