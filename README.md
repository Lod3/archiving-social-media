# archiving-social-media
Holds all scripts and or documentation related to social media archiving including related pilot projects 

## Inhoud

* [facebook](facebook/): bevat een script om profielfoto's te downloaden van Facebookaccounts waar je de identifier van hebt. Meer informatie vind je in de [README](facebook/README.md). Het bevat ook een onafgewerkt script om identifiers van Facebookaccounts geautomatiseerd te valideren. Op basis van naam en woonplaats zal het script controleren of het account wel van de juiste persoon is.
* [linkedin](linkedin/): bevat een script om profielfoto's te downloaden van LinkedInaccounts waar je de identifier van hebt. Meer informatie vind je in de [README](linkedin/README.md)
* [twitter](twitter/): bevat scripts om profielfoto's te downloaden van Twitteraccounts waar je de identifier van hebt.
* [find_social_media_accounts.py](find_social_media_accounts.py) is een script om geautomatiseerd socialemediaprofielen op Twitter, Facebook, LinkedIn en Instagram van politici te zoeken via Google. Het script vereist een CSV met minstens de kolommen 'volledige naam', 'QID', 'gemeente' en 'partij'.
* [clean_photos.py](clean_photos.py) is een script dat via gezichtsdetectie nagaat of de gevonden foto's een portret zijn. De resultaten worden neergeschreven in een CSV.
*[sample-data](sample-data/) bevat een sample waarmee je de verschillende scripts kan testen.

Voor vragen en problemen kan je een issue aanmaken.

