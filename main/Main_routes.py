from tempfile import template
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from config import Config

main_bp = Blueprint('Main_routes', __name__)

@main_bp.route('/')
def landingPage():
    return render_template("landingPage.html")


@main_bp.route('/about')
def about():
    return render_template('about.html')



@main_bp.route('/firstpage')
def firstpage():
    return render_template('firstpage.html')


