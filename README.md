Behöver köra skapa en databasplats och döpa den till frivilligt. i config.py kan man ändra vilken url databasen ska ha.

Mellan midnatt och 06 kommer scriptet för att skicka mail med mistänksamma transaktioner. Det seedas inga sådana transaktioner vid uppstart men skapa några. 
Har lämnat en utkommenterad funktion för att köra scriptet 1 gång. Den är dock inte testad sen vanliga scriptet fungerat.


Alla moduler som används kan man installera med:
"pip install -r requirements.txt"

Unittest kan köras med:
"python3 -m unittest scripts.unittest"
