from flask import Flask, request, render_template, url_for, redirect
import requests, jsonify

app = Flask(__name__)

API_KEY = 'kKvfT+ITNHE5ouovhYk4QQ==EAWuwdych4jyqJVY'

@app.route('/', methods=['POST','GET'])
def index():
  if request.method == 'POST':
    longitude = request.form['longitude']
    latitude = request.form['latitude']
    date = request.form['date']

    api2_url = f'https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}&date={date}'

    response = requests.get(api2_url)
    data = response.json()

    sunrise = data['results']['sunrise']
    sunset = data['results']['sunset']

    return redirect(url_for('results', sunrise=sunrise, sunset=sunset))
  
  return render_template('index.html')


@app.route('/results', methods=["POST",'GET'])
def results():
  sunrise = request.args.get('sunrise')
  sunset = request.args.get('sunset')

  return render_template('results.html', sunrise=sunrise, sunset=sunset)


@app.route("/longlat/<city>/<state>/<date>",methods=['GET','POST'])
def longlat(city,state,date):
  if request.method == "GET":

    #api1
    country = 'US'
    api_url = f'https://api.api-ninjas.com/v1/geocoding?city={city}&state={state}&country={country}'

    response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
    data = response.json()

    latitude = data[0]['latitude']
    longitude = data[0]['longitude']

    #api2

    api2_url = f'https://api.sunrisesunset.io/json?lat={latitude}&lng={longitude}&date={date}'

    response2 = requests.get(api2_url)
    data2 = response2.json()

    return data2

if __name__ == '__main__':
   app.run(debug=True)