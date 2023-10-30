# loggi

logger boilerplate with dataclass models for parsing

## Installation

Install with:

<pre>
pip install loggi
</pre>



## Usage

<pre>
>>> import loggi
>>> logger = loggi.getLogger("demo", "logs") 
</pre>
The file "demo.log" will be created inside a folder named "logs" in the current directory.<br>

loggi wraps the logging level mapping so the log level can be set without importing the logging module
<pre>
>>> logger.setLevel(loggi.DEBUG)
</pre>
Also loggi imports the logging module when it's initialized, so all logging module features can be utilized without explicity importing logging yourself
<pre>
>>> print(loggi.logging.getLevelName(loggi.INFO))
INFO
</pre>
loggi uses the format `{level}|-|{date}|-|{message}` where date has the format `%x %X`
<pre>
>>> logger.info("yeehaw")
</pre>
produces the log
<pre>
INFO|-|10/26/23 18:48:30|-|yeehaw
</pre>
loggi also contains two dataclasses: `Log` and `Event`.<br>
A `Log` object contains a list of `Event` objects that can be loaded from a log file (that uses the above format).<br>
Each `Event` contains `level: str`, `date: datetime`, `message: str` fields.
<pre>
>>> log = loggi.load_log("logs/demo.log")
>>> print(log)
INFO|-|10/26/23 18:48:30|-|yeehaw
>>> print(log.num_events)
1
>>> print(log.events[0].level)
INFO
</pre>
`Log` objects can be added together.<br>
Useless examples:
<pre>
>>> log += log
>>> print(log)
INFO|-|2023-10-26 18:48:30|-|yeehaw
INFO|-|2023-10-26 18:48:30|-|yeehaw
</pre>
New, filtered `Log` objects can be created using the `filter_dates`, `filter_levels`, and `filter_messages` functions.
<pre>
>>> from datetime import datetime, timedelta
>>> log = loggi.load_log("realistic_log.log")
</pre>
Filtering for events between 24 and 48 hours ago:
<pre>
>>> filtered_log = log.filter_dates(datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1))
</pre>
Filtering for events with critical and error levels:
<pre>
>>> filtered_log = log.filter_levels(["CRITICAL", "ERROR"])
</pre>
Filtering for events whose message contains "yeehaw", but not "double yeehaw" or "oopsie":
<pre>
>>> filtered_log = log.filter_messages(["*yeehaw*"], ["*double yeehaw*", "*oopsie*"])
</pre>
The filtering methods can be chained:
<pre>
>>> log_slice = log.filter_dates(datetime.now() - timedelta(days=2), datetime.now() - timedelta(days=1)).filter_levels(["CRITICAL", "ERROR"])
</pre>
When adding `Log` objects, the `chronosort()` function can be used to reorder the events by date:
<pre>
>>> log = filtered_log + log_slice
>>> log.chronosort()
</pre>
`log` now contains all critical and error level events between 24 and 48 hours ago,
as well as events from anytime of any level with "yeehaw" in the message, but not "double yeehaw" or "oopsie".


