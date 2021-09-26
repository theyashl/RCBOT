from trakt import Trakt
from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
import tmdbsimple as tmdb
import datetime
import requests


tmdb.API_KEY = '44ec5f422b554212fb8bd83da7323142'
Trakt.configuration.defaults.client(
        id="46fa1c789a7e019574e4946af5824546f05e7dece99f5384bfaeb1c0641bb051"
    )


@run_async
def air(bot: Bot, update: Update):
    KEY = '44ec5f422b554212fb8bd83da7323142'
    res = "*Airing Shows:*\n\n"
    tv = tmdb.TV()
    response = []
    for i in range(1, 3):
        response.append(tv.airing_today(timezone="IST", page=i))
    data = []
    for i in response:
        for j in i['results']:
            if j['original_language'] in ["en", "hi", "te", "mr", "ta", "ml"]:
                data.append(j)
    res = "*Shows Airing Today:*\n\n"
    del response
    for i in data:
        res += i['name'] + " (_"
        try:
            req = requests.get(
                "https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key={key}".format(
                    tv_id=i['id'], key=KEY)).json()['results']
            for p in req['IN']['flatrate']:
                res += p['provider_name']
        except KeyError as e:
            res += "NA"
        res += "_)\n"

    try:
        COVER = "https://www.themoviedb.org/t/p/original"+data[0]['backdrop_path']
    except:
        COVER = "https://scontent.fnag1-1.fna.fbcdn.net/v/t1.6435-9/102459297_105404194547552_1607624959242791968_n.jpg?_nc_cat=102&ccb=1-5&_nc_sid=e3f864&_nc_ohc=wxphiccOyAwAX9aMvNC&_nc_ht=scontent.fnag1-1.fna&oh=602a2002ebd85747cbfad534de6414d3&oe=6151A4FC"
    del data
    update.effective_message.reply_photo(
        COVER,
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@run_async
def otv(bot: Bot, update: Update):
    res = "*Ongoing TV Shows*\n\n"
    tv = tmdb.TV()
    response = tv.on_the_air()
    for j in response['results']:
        res += j['name'] + "\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


@run_async
def umovie(bot: Bot, update: Update):
    res = "*Upcoming Movies:*\n\n"
    mov = tmdb.Movies()
    response = mov.upcoming()
    for j in response['results']:
        if datetime.datetime.strptime(j['release_date'], "%Y-%m-%d") > datetime.datetime.today():
            res += j['title'] + ", " + j['release_date'] + "\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)

@run_async
def trendingm(bot: Bot, update: Update):
    res = "*Trending Movies:*\n\n"
    items = Trakt['movies'].trending()
    for i in range(10):
        res += items[i].title + " (" + str(items[i].year) + ")\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)

@run_async
def trendings(bot: Bot, update: Update):
    res = "*Trending Shows:*\n\n"
    items = Trakt['shows'].trending()
    for i in range(10):
        res += items[i].title + " (" + str(items[i].year) + ")\n"

    update.effective_message.reply_text(res, parse_mode=ParseMode.MARKDOWN)


AIR_HANDLER = DisableAbleCommandHandler("air", air)
dispatcher.add_handler(AIR_HANDLER)


OTV_HANDLER = DisableAbleCommandHandler("otv", otv)
dispatcher.add_handler(OTV_HANDLER)


UMOVIE_HANDLER = DisableAbleCommandHandler("umovie", umovie)
dispatcher.add_handler(UMOVIE_HANDLER)


TRENDINGS_HANDLER = DisableAbleCommandHandler("trendings", trendings)
dispatcher.add_handler(TRENDINGS_HANDLER)

TRENDINGM_HANDLER = DisableAbleCommandHandler("trendingm", trendingm)
dispatcher.add_handler(TRENDINGM_HANDLER)
