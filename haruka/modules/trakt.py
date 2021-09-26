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
def sinfo(bot: Bot, update: Update):
    message = update.effective_message
    res = ""
    # /sinfo 1234
    sid = message.text[7:]
    show = tmdb.TV(sid)
    info = show.info()

    res += "Title: *{name}* ({year})".format(name=info['name'], year=str(info['first_air_date']).split("-")[0])
    res += "\n\nTagline: " + info['tagline']
    res += "\n\nGenres: "
    for g in info['genres']:
        res += g['name'] + " "
    res += "\n\nOverview: " + info['overview']
    res += "\n\nRecent Episode: " + info['last_episode_to_air']['name'] + " (S{s}E{e})".format(
        s=info['last_episode_to_air']['season_number'],
        e=info['last_episode_to_air']['episode_number'])
    res += "\n\nRecommendations:\n"
    recs = show.recommendations()
    recs = recs['results'][:5]
    for r in recs:
        res += "\n" + "[" + r['name'] + "](https://t.me/share/url?url=/sinfo%20{sid})".format(sid=r['id'])

    POSTER = "https://www.themoviedb.org/t/p/original" + info['poster_path']
    del show
    del info
    del recs
    update.effective_message.reply_photo(
        POSTER,
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True
    )


@run_async
def air(bot: Bot, update: Update):
    KEY = '44ec5f422b554212fb8bd83da7323142'
    res = "*Shows Airing Today:*\n\n"
    tv = tmdb.TV()
    response = []
    for i in range(1, 3):
        try:
            response.append(tv.airing_today(timezone="IST", page=i))
        except:
            res += "Sorry, there's been connection error!\nPlease Try again later (After 15-20 minutes.)"
            break
    data = []
    for i in response:
        for j in i['results']:
            if j['original_language'] in ["en", "hi", "te", "mr", "ta", "ml"]:
                data.append(j)
    del response
    for i in data:
        res += "[" + i['name'] + "](https://t.me/share/url?url=/sinfo%20{sid})".format(sid=i['id']) + " (_"
        try:
            req = requests.get(
                "https://api.themoviedb.org/3/tv/{tv_id}/watch/providers?api_key={key}".format(
                    tv_id=i['id'], key=KEY)).json()['results']
            for p in req['IN']['flatrate']:
                res += p['provider_name']
        except KeyError as e:
            res += "NA"
        res += "_)\n"

    del data
    update.effective_message.reply_text(
        res, parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=False
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


SINFO_HANDLER = DisableAbleCommandHandler("sinfo", sinfo)
dispatcher.add_handler(SINFO_HANDLER)

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
