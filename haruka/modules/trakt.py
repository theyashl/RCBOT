from trakt import Trakt
from haruka import dispatcher, MESSAGE_DUMP, LOGGER
from haruka.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.ext import run_async

Trakt.configuration.defaults.client(
        id="46fa1c789a7e019574e4946af5824546f05e7dece99f5384bfaeb1c0641bb051"
    )

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



TRENDINGS_HANDLER = DisableAbleCommandHandler("trendings", trendings)
dispatcher.add_handler(TRENDINGS_HANDLER)

TRENDINGM_HANDLER = DisableAbleCommandHandler("trendingm", trendingm)
dispatcher.add_handler(TRENDINGM_HANDLER)
