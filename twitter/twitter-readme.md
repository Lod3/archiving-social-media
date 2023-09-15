### Twarc

Twarc gebruiken om usernames te zoeken op basis van de mandaten lijst, voornaam achternaam. 
Gebruikersnamen in de lijst mogen geen spaties bevatten en line endings moeten LF zijn. 


`twarc2 users --usernames usernames2.txt > users.jsonl`




### Troubleshooting
#### CRLF to LF 
Met vim:
` vim usernames2.txt -c "set ff=unix" -c ":wq" # dos to unix `

### Tools
Collectie van tools nog te bekijken if it works

https://github.com/Altimis/Scweet

https://github.com/bisguzar/twitter-scraper
