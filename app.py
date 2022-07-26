from flask import Flask, jsonify
import json
import os.path
import pandas as pd
from lib.calender import generate_calendar_from_events
from lib.api import fetch_events_for_commission_abbr, fetch_active_commissions

app = Flask(__name__)

@app.route("/commissies/<commission>.ics")
def commission_calendar(commission):
    events = fetch_events_for_commission_abbr(commission)
    calendar = generate_calendar_from_events(events)

    return app.response_class(
        calendar.serialize(), 
        mimetype='text/calendar'
    )


@app.route("/commissies")
def commissions():
    commissions = fetch_active_commissions()

