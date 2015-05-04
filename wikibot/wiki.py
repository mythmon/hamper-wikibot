from hamper.interfaces import ChatCommandPlugin, Command
import requests as re
import json
import os

class WikiBot(ChatCommandPlugin):
    name = 'wikibot'

    class TestCommand(Command):
        regex = 'wiki (.+)'

        def command(self, bot, comm, groups):
            """
            !wiki <query> -> wiki summary of <query>
            """
            query = groups[0]
            bot.reply(comm, (self.summary(query, comm)))

        def summary(self, query, comm):
            """Returns wikipedia summary of <query>
            Uses wikipedia api to grab the first <280 characters of <query>
            article (or lets you know the query is ambigious) and appends a
            clickable url at the end.
            """
            # Makes the api call
            r = re.get('https://en.wikipedia.org/w/api.php?format=json&action=query&prop=extracts&exintro=&explaintext=&titles='+query)
            # loads r.text into an object
            p = json.loads(r.text)
            # pageid is needed to grab the info of a page, it's an api thing
            pageid = p['query']['pages'].keys()[0]
            # extract is the top content of a given wiki page
            extract = p['query']['pages'][pageid]['extract']
            # generates psuedo-slugified url
            url = 'https://en.wikipedia.org/wiki/'+query.replace(' ','_')
            # if the article introduction is longer than 280 charcters it
            # shortens it so you don't get wikibot spam
            try:
                return (comm['user']+': '+extract[:280].replace(os.linesep,'\ ')+'[...] :: URL: '+url)
            except:
                return (comm['user']+': '+extract.replace(os.linesep,'\ ')+' :: URL: '+url)
