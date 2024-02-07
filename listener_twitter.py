import socket 
import tweepy
import os
from dotenv import load_dotenv

load_dotenv()



HOST = 'localhost'
PORT = int(os.getenv('PORT'))
s = socket.socket()
s.bind((HOST, PORT))
print(f'Aguardando conexao na porta:{PORT}')

s.listen(5)
connection, address = s.accept()
print(f'Rebendo solicitacao de {address}')
token  = os.getenv('bearer_token')
keyword = 'cristo'

class GetTweets(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        print('='*50)
        connection.send(tweet.text.encode('utf-8', 'ignore'))

printer = GetTweets(token)
printer.add_rules(tweepy.StreamRule(keyword))
printer.filter()
connection.close()