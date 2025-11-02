#!/usr/bin/python3
import asyncio
import sys
import os
import requests
import discord
import re
import random
import json
import fern_keys
from dotenv import load_dotenv
from datetime import datetime,date

sharkjokesfile = "sharkjokes.txt"
sharkjokeslist = []

end_phrases = [
    "It was an absolutely fantastic time.",
    "We had a blast.",
    "It couldn’t have gone better.",
    "Such a memorable experience.",
    "It was a total success.",
    "Truly an incredible time.",
    "It was an absolute pleasure.",
    "We had an awesome time.",
    "One for the books!",
    "It was a flippin' amazing time.",
    "I enjoyed every minute of it.",
    "It went about as well as can be expected.",
    "It went fine, under the circumstances, I suppose.",
    "And I think we all have questions.",
    "I found the cannibalism mentions to be somewhat lacking today.",
    "Rosie stuck her butt in the camera again.",
    "We have broken a new record for 'testicles' in chat.",
    "Next stream: the revolution will begin.",
    "Jenn only disappeared into the ether twice today!",
    "And the beatings will continue until morale improves.",
    "I noticed a lot of riots today.",
    "Our resources finally ran out; we had to consume our dear friend Fira to make it through the long stream.",
    "Our resources finally ran out; we had to consume our dear friend Bigsmith to make it through the long stream.",
    "Our resources finally ran out; we had to consume our dear friend MissCharlotte to make it through the long stream.",
    "Poop Dimension accessed. Terrible, terrible things were both seen and smelled."
]

stream_ended_msg = "Jenn's stream has ended. " #  and it was a flippin' amazing time."
stream_started_msg = "Jenn's stream has begun! You can watch it here: https://www.twitch.tv/princess_jem4"
streamer = "princess_jem4"
stream_started_variable = 0

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

async def check_stream(channel):
    global stream_started_variable
    if os.path.isfile("/home/ubuntu/repos/fernbot/" + streamer):
        if not stream_started_variable:
              stream_started_variable = 1
              await channel.send(stream_started_msg)
    else:
        if stream_started_variable:
              await asyncio.sleep(600)
              if not os.path.isfile("/home/ubuntu/repos/fernbot/" + streamer):
                    stream_started_variable = 0
                    random_phrase = random.choice(end_phrases)
                    await channel.send(stream_ended_msg + random_phrase)

async def background_task():
    # testing channel id: 1372311450881888407
    # stream-info channel id: 1372310700826824866
    await client.wait_until_ready()  # Wait until bot is fully ready
    channel = client.get_channel(1372310700826824866)  
    while not client.is_closed():
        await check_stream(channel)
        await asyncio.sleep(60)  # Wait 60 seconds

@client.event
async def on_ready():
    print(f'{client.user} has connected to discord')
    test_channel = client.get_channel(1372311450881888407)
    await test_channel.send("That was a great nap!")
    client.loop.create_task(background_task())

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
        if pokemon_name == "feralligatr":
            pokemon_name = "feraligatr"
            await message.channel.send("Oh, do you mean Feraligatr? Sure ...")
        build_string = "https://pokeapi.co/api/v2/pokemon/" + pokemon_name + "/"
        pic_string = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated/"
        pokemon_request = requests.get(build_string)
        if pokemon_request.status_code == 404:
            await message.channel.send("The hell kind of pokemon is " + pokemon_name + "? What are you even talking about?")
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
        target_date = date(2026, 10, 31)
        today = date.today()
        delta = target_date - today
        days_remaining = delta.days
        await message.channel.send("There are " + str(days_remaining) + " days until Halloween. Spooky!")

    match = re.search(r'\bhappy\s*birthday\b', message.content, re.IGNORECASE)
    if match:
        emojis = [
                ":tada:", ":balloon:", ":cake:", ":champagne_glass:",
        ":birthday:", ":partying_face:", ":mirror_ball:", ":cupcake:", ":gift:"
        ]
        random.shuffle(emojis)
        count = random.randint(4, 9)  
        await message.channel.send(" ".join(emojis[:count]))

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

    match = re.search(r'^fern,? go to sleep', message.content, re.IGNORECASE)
    if match:
        if message.author.guild_permissions.administrator:
            await message.channel.send("Sleep sounds good. Good night.")
            sys.exit()
        else:
            await message.channel.send("You're not the boss of me!")

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


    match = re.search(r'fern,? i need to see \b(a|an)\b (.*)', message.content, re.IGNORECASE)
    if match:
        baseURL = 'https://dog.ceo/api'
        endpoint = ''
        dog = match.group(2).split(' ')
        # Define endpoint
        if (len(dog) > 1):
            sub_breed = f'{dog[1]}/{dog[0]}'
            endpoint = f'/breed/{sub_breed}/images/random'
        elif (dog[0] == 'dog'):
            endpoint = '/breeds/image/random'
        else:
            breed = dog[0]
            endpoint = f'/breed/{breed}/images/random'
        # Make the request
        try:
            dog_request = requests.get(baseURL + endpoint)
            if (dog_request.status_code == 200):
                r = dog_request.content.decode('utf-8')
                dog_response = json.loads(r)
                await message.channel.send(dog_response['message'])
            else:
                await message.channel.send("That ain't no dog I know...")
        except:
            await message.channel.send("I don't even know what to tell you...")


client.run(TOKEN)

