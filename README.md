# Sirius Bandy
## Generellt
Instruktioner kring hur man hanterar all kod. 

Koden är skriven i Python 3.9.5

### Använda paket
```
pandas
pptx
```

## Datainsamling
Datainsamlingen kan startas genom:
```
from get_data import Game
g = Game('sirius', 'edsbyn')
g.collector_raw('20221121 sirius edsbyn halvlek 1')
```

### Händelser
Följande händelser och eventuella underhändelser är vi intresserade av:
* **skott** - bollen skjuts mot mål
  * **utanför** - skottet missar mål och går till utkast
  * **räddning** - målvakten räddar
  * **täckt** - skottet når inte mål då det täcks undan av spelare
* **skottyp** - notera efter skott för varje avslut
  * **friställande** - friställande passning
  * **inlägg** - inläggspassning
  * **utifrån** - skott utifrån
  * **dribbling** - individuell dribbling in i straffområdet
  * **centralt** - centralt anfall med flera spelare
* **mål** - det blir mål
  * **straffområde** - bollen skjuts inifrån straffområdet 
  * **lång** - bollen skjuts utanför straffområdet
  * **fast** - det blir mål på en fast situation (hörna, straff, frislag)
* **bolltapp** - en spelare förlorar bollen "av egen maskin"
  * **tappad** - spelaren tappar bara kontrollen (dålig dribbling)
  * **passförsök** - spelaren försöker sig på en passning och tappar bollen (dålig passning)
* **närkamp** - det uppstår en närkampssituation som vinns av spelare i laget som anges. 
* **brytning** - spelare i laget som anges bryter boll påväg till motståndare.
* **frislag** - domaren dömer frislag
* **hörna** - domaren dömer hörna
* **straff** - domaren dömer straff
* **utvisning** - domaren dömer utvisning
  * **5** - fem minuters utvisning
  * **10** - tio minuters utvisning 
* **inslag** - bollen går ut och det blir inslag
* **utkast** - bollen hamnar hos målvakten
* **avslag** - det blir avslag
* **passning** - ett lag lägger en farlig passning 
  * **straffområde** - "inlägg" från kant in i straffområde
  * **lång** - långboll som går fram
  * **långtapp** - långboll som inte går fram
* **friläge** - spelare får ett friläge
* **offside** - spelar i lag åker offside, motstådarna får bollen
* **resning** - laget i fråga rensar bort bollen, motståndarna får den utan närkamp
* **anfall** - 
  * **direkt** - direkt anfall, en spelare kör
  * **kontring** - samlad kontring, flera spelare
  * **långt** - långt, strukturerat anfall 
* **stop** - halvleken slut, programmet avslutas
* **boll** - laget har bollinnehav
* **timeout** - lag tar timeout. Kan även användas utan lag för valfritt (längre) matchstopp. 

### Synca klockan i collector_raw:
För att ändra tiden i realtid vid datainsamling i ```collector_raw``` (t.ex. om videon pausats).
```
clock MM:SS
```
kommer ändra tiden att matcha input. Notera att vi oftast kommer skapa en fil för varje halvlek så det kan bli konstigt att gå efter matchuret. 

### Clean CSV
Kommer bara fungera ifall Raw CSV slutar med "tid, stop".

För att starta krävs
```
from get_data import Game
g = Game('sirius', 'edsbyn')
g.clean_csv('20221121 sirius edsbyn halvlek 1')
```

### Ask for-metoderna
* Man ska alltid kunna kringgå frågorna genom att ange 0


## Skottinsamling
Starta matchen genom att skriva vad som helst, men gör detta precis när matchen startar. Det som ska anges är lag, anfallstyp, skottyp och utfall. Har lagt till **övrigt** som skotttyp. Använd 0 för att strunta i någon annan typ. 

### Anfallstyper
* **Direkt** -  vi kommer över bollen i ett läge där det finns en rak väg till mål, ofta kan en enskild spelare driva bollen hela vägen från att ha vunnit den till avslut.
* **Samlat** - vi skapar en konting med fler än en spelare. Det är inte en helt rak väg till mål, men anfallet går snabbt och vi vänder aldrig hem.
* **Långt** - anfallet är helt strukturerat, ofta börjar vi på egen planhalva och har tid att vända tillbaka ifall första eller andra läget inte är bra nog.

### Skottyper
* **Friställande** - en längre passning når fram till en anfallspelare i ett läge där denna antingen är fri, eller i ett sådant läge att den snabbt kan ta sig fram till ett skottläge i straffområdet.
* **Inlägg** - bollen passas in i straffområdet från endera kant. 
* **Utifrån** - skott från håll. 
* **Dribbling** - enskild spelare för bollen in i straffområdet och skapar skottläge. Ofta tydligt stark individuell prestation. 
* **Centralt** - ett anfall där flera spelare (ofta två eller tre) driver in bollen centralt i straffområde, ofta genom passningsspel såväl i som utanför straffområdet.
* **Fast** - fast situation. Exempelvis straff, hörna eller frislag. 

### Utfall
* **Mål** - det blir mål.
* **Hörna** - det blir hörna.
* **Annat** - målvaktens boll, bollen lös etc. 