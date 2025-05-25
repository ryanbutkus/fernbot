#!/usr/bin/python3
import os
import requests
import discord
import re
import random
import json
import fern_keys
from dotenv import load_dotenv
from datetime import datetime

sharkjokesfile = "sharkjokes.txt"
sharkjokeslist = []

TOKEN = fern_keys.TOKEN
stock_token = fern_keys.stock_token
weather_token = fern_keys.weather_token

load_dotenv

headers = {
        'Content-Type': 'application/json',
         'Authorization' : 'Token ' + stock_token
        }

weather_icon_dict = {
    "01d": ":sunny:",
    "01n": ":first_quarter_moon_with_face:",
    "02d": ":white_sun_small_cloud:",
    "02n": ":new_moon:",
    "03d": ":cloud:",
    "03n": ":cloud:",
    "04d": ":white_sun_cloud:",
    "04n": ":cloud:",
    "09d": ":cloud_rain:",
    "09n": ":cloud_rain:",
    "10d": ":cloud_rain:",
    "10n": ":cloud_rain:",
    "11d": ":thunder_cloud_rain:",
    "11n": ":thunder_cloud_rain:",
    "13d": ":snowflake:",
    "13n": ":snowflake:",
    "50d": ":fog:",
    "50n": ":fog:"
}

sharks = open(sharkjokesfile, "r")
for joke in sharks:
  sharkjokeslist.append(joke)

client=discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    match = re.search(r'fern,? weather (.*)', message.content, re.IGNORECASE)
    if match:
        zipcode = match.group(1)
        match = re.search(r'\d\d\d\d\d', message.content)
        if match:
            build_string = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipcode + ",us&appid=" + weather_token
        else:
            build_string = "http://api.openweathermap.org/data/2.5/weather?q=" + zipcode + "&appid=" + weather_token
        dirs = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
        weather_request = requests.get(build_string)
        weather_response = json.loads(weather_request.content)
        humidity = weather_response["main"]["humidity"]
        wind_deg = weather_response["wind"]["deg"]
        wind_speed = weather_response["wind"]["speed"]
        visibility = weather_response["visibility"]
        icon_code = weather_response["weather"][0]["icon"]
        wind_speed_mph = wind_speed * 2.237
        wind_speed_kmh = wind_speed * 3.6
        place = weather_response["name"]
        desc = weather_response["weather"][0]["description"]
        current_temp = weather_response["main"]["temp"]
        ix = round(wind_deg / (360. / len(dirs)))
        wind_dir = dirs[ix % len(dirs)]
        feels_like = weather_response["main"]["feels_like"]
        feels_like_f = int((feels_like - 273.15) * 9/5 + 32)
        feels_like_c = round((feels_like - 273.15), 2)        
        f_temp = int((current_temp - 273.15) * 9/5 + 32)
        c_temp = round((current_temp - 273.15), 2)
        return_response = weather_icon_dict[icon_code] + " " + place + " has " + desc + " with a current temperature of " + str(c_temp) + "C (" + str(f_temp) + "F/" + str(current_temp) + "K), " \
            "but it feels like " + str(feels_like_c) + "C (" + str(feels_like_f) + "F/" + str(feels_like) + "K). Wind is out of the " + wind_dir + " at " + str(int(wind_speed_kmh)) + "KPH " \
            "(" + str(int(wind_speed_mph)) + "MPH). Humidity is " + str(int(humidity)) + "%. Visibility is " + str(int(visibility)) + " meters."
        await message.channel.send(return_response)

    match = re.search(r'(^| )trash($| )', message.content, re.IGNORECASE)
    if match:
        await message.channel.send("Gomibaka!")

    match = re.search(r'fern,? show me .*?(\b[\w-]+\b)\s*$', message.content, re.IGNORECASE)
    if match:
        pokemon_name = match.group(1)
        build_string = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name + "/"
        pic_string = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/"
        pokemon_request = requests.get(build_string)
        if pokemon_request.status_code == 404:
            await message.channel.send("The hell kind of pokemon is that? What are you even talking about?")
        else:
            pokemon_response = json.loads(pokemon_request.content)
            back_match = re.search(r'back', message.content, re.IGNORECASE)
            if back_match:
                pic_string = pic_string + "back/"
            shiny_match = re.search(r'shiny', message.content, re.IGNORECASE)
            if shiny_match:
                pic_string = pic_string + "shiny/"
            pic_string = pic_string + str(pokemon_response["id"]) + ".gif"
            await message.channel.send(pic_string)

    match = re.search(r'fern,? how many days until halloween', message.content, re.IGNORECASE)
    if match:
        target_date = datetime(2025, 10, 31)  
        today = datetime.today()
        delta = target_date - today
        days_remaining = delta.days
        await message.channel.send("There are " + str(days_remaining) + " days until Halloween. Spooky!")

    match = re.search(r'fern,? tell me a (.*) joke', message.content, re.IGNORECASE)
    if match:
        jokeword = match.group(1)
        response = random.choice(sharkjokeslist)
        await message.channel.send(response.replace("shark", jokeword))

    match = re.search(r'fern,? stock (.*)', message.content, re.IGNORECASE)
    if match:
        symbol = match.group(1)
        requestResponse = requests.get("https://api.tiingo.com/iex/?tickers=" + symbol, headers=headers)
        stockresponse = json.loads(requestResponse.content)
        newprice = stockresponse[0]["last"]
        oldprice = stockresponse[0]["prevClose"]
        diff = round(((newprice - oldprice) / oldprice) * 100, 2)
        await message.channel.send("The price of " + stockresponse[0]["ticker"] + " is " + str(stockresponse[0]["last"]) + " (" + str(diff) + "%).")

    match = re.search(r'fern,? tell me number trivia', message.content, re.IGNORECASE)
    if match:
        r = requests.get("http://numbersapi.com/random/trivia")
        response = r.content.decode("utf-8")
        await message.channel.send(response)


    match = re.search(r'fern,? tell me about the number (.*)', message.content, re.IGNORECASE)
    try:
        if match:
            number = match.group(1)
            r = requests.get("http://numbersapi.com/" + number + "/trivia")
            response = r.content.decode("utf-8")
            if re.search(r'Cannot GET', response, re.IGNORECASE) or re.search(r'Invalid URL', response, re.IGNORECASE):
                response = "I'm getting sick of you."
            if re.search(r'missing a fact', response) or re.search(r'unremarkable', response) or re.search(r'boring', response) or re.search(r'uninteresting', response):
                r = requests.get("http://numbersapi.com/" + number + "/math")
                response = r.content.decode("utf-8")
            await message.channel.send(response)
    except:
        await message.channel.send("I'm getting sick of you.")

client.run(TOKEN)

