This is the back-end code built for the Award project "TeleVital" that won CODE19 Hackathon organised by The MJ Foundation.
### Note:

1) The database credentials given are dummy values.
2) Citation for mathematical algo : [Paper Link](http://ieeexplore.ieee.org/document/6959086).

### What it does

1) The code expects a frame and performs certain mathematical operations to calculate the oxygen concentration in the blood.
2) Image should contain a finger at an approximate distance of 3-5 cm from the camera.
3) It writes the data on to the firebase database.

In the demo site, the server is simply flipping the image horizontally. You could imagine it doing something more sophisticated (e.g. applying some filters), but obviously I was too lazy to implement anything cool.

### Demo

To see the demo, you can check out the project website : [TeleVital](https://televital-monitor.web.app/).

#### Optional

- setup heroku (`brew install heroku`)
- Use a python virtualenv

#### Required
- `git clone https://github.com/routrohan/spo2-omachack.git
- `pip install -r requirements.txt`

### Run locally

IF YOU HAVE HEROKU:
- `heroku local`
IF NOT:
- `python3 app.py`

- in your browser, navigate to localhost:5000

### Deploy to heroku

- `git push heroku master`
- heroku open

### Common Issues

If you run into a 'protocol not found' error, see if [this stackoverflow answer helps](https://stackoverflow.com/questions/40184788/protocol-not-found-socket-getprotobyname).
