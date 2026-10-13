# Site-brief lachgasholland.nl (nieuwe, landelijke site)
Lees eerst ../p3/BRIEF_TEMPLATE.md (algemene regels en schema's). Merk: "Lachgas Holland". Gebied: heel Nederland, alle twaalf provincies. Bestellen via WhatsApp (noem geen nummer). Aanspreekvorm "je". Betalen: "contant of via Tikkie bij levering". Wet NL: lachgas staat sinds 1 januari 2023 op lijst II van de Opiumwet; verkoop en bezit voor recreatief gebruik zijn verboden met uitzonderingen voor medisch, technisch en voedingsgebruik; verwijs naar https://www.rijksoverheid.nl. Toon: nuchter, vriendelijk maar zakelijk, landelijk (niet alleen Randstad).
Producten: lachgastanks 2KG, 4KG en 10KG (schrijf exact zo), verzegeld geleverd. Geen patronen/crackers (worden niet verkocht), geen exacte afmetingen/gewichten noemen behalve de netto-inhoud (2, 4, 10 kilo N2O).
Levertijd: OVERAL in Nederland "meestal binnen 15 tot 25 minuten" (schrijf het exact zo). Er zijn GEEN zones, banden of verschillen per plaats, provincie of afstand. Noem nooit een langere rijtijd, nooit "verder weg duurt het langer", geen vergelijkingen tussen plaatsen of provincies. Wel toegestaan als voorbehoud: drukte op vrijdag- en zaterdagavond, evenementen, slecht weer, files; dan "laten we het vooraf via WhatsApp weten". Schrijf over "bezorgers in de regio" of "een bezorger in de buurt", nooit over één centraal vertrekpunt.
Toegestane interne links: /bezorggebied/, /bezorggebied/<provincie-slug>/, /lachgas-bezorgen/<plaats-slug>/, /lachgas-tanks/, /lachgas-tanks/2kg/, /lachgas-tanks/4kg/, /lachgas-tanks/10kg/, /informatie/, /informatie/<artikel-slug>/, /service/, /service/<service-slug>/, /veelgestelde-vragen/, /veelgestelde-vragen/<thema-slug>/, /over-ons/, /contact/, /privacy/, /algemene-voorwaarden/. Externe links alleen: https://www.rijksoverheid.nl, https://www.drugsinfo.nl, https://www.trimbos.nl, https://www.jellinek.nl.
Provincie-slugs (HUBS, in deze volgorde; de hub-pagina heet "Provincie", niet "regio"): noord-holland (naam "Noord-Holland"), zuid-holland ("Zuid-Holland"), utrecht ("Utrecht"), noord-brabant ("Noord-Brabant"), gelderland ("Gelderland"), overijssel ("Overijssel"), limburg ("Limburg"), friesland ("Friesland"), groningen ("Groningen"), drenthe ("Drenthe"), flevoland ("Flevoland"), zeeland ("Zeeland"). In de HUBS gebruik je "region"-veld niet; plaatsen verwijzen met "region" naar de provincie-slug.

## Plaatsen (slug | naam | kind | region (provincie-slug) | gemeente)
### Noord-Holland (bestand areas_noord_holland.py)
amsterdam | Amsterdam | stad | noord-holland | Amsterdam
haarlem | Haarlem | stad | noord-holland | Haarlem
zaandam | Zaandam | stad | noord-holland | Zaanstad
alkmaar | Alkmaar | stad | noord-holland | Alkmaar
hilversum | Hilversum | stad | noord-holland | Hilversum
amstelveen | Amstelveen | stad | noord-holland | Amstelveen
hoofddorp | Hoofddorp | stad | noord-holland | Haarlemmermeer
purmerend | Purmerend | stad | noord-holland | Purmerend
hoorn | Hoorn | stad | noord-holland | Hoorn
den-helder | Den Helder | stad | noord-holland | Den Helder
heerhugowaard | Heerhugowaard | stad | noord-holland | Dijk en Waard
beverwijk | Beverwijk | stad | noord-holland | Beverwijk
### Zuid-Holland (bestand areas_zuid_holland.py)
rotterdam | Rotterdam | stad | zuid-holland | Rotterdam
den-haag | Den Haag | stad | zuid-holland | Den Haag
leiden | Leiden | stad | zuid-holland | Leiden
dordrecht | Dordrecht | stad | zuid-holland | Dordrecht
zoetermeer | Zoetermeer | stad | zuid-holland | Zoetermeer
delft | Delft | stad | zuid-holland | Delft
alphen-aan-den-rijn | Alphen aan den Rijn | stad | zuid-holland | Alphen aan den Rijn
gouda | Gouda | stad | zuid-holland | Gouda
schiedam | Schiedam | stad | zuid-holland | Schiedam
vlaardingen | Vlaardingen | stad | zuid-holland | Vlaardingen
spijkenisse | Spijkenisse | stad | zuid-holland | Nissewaard
capelle-aan-den-ijssel | Capelle aan den IJssel | stad | zuid-holland | Capelle aan den IJssel
katwijk | Katwijk | stad | zuid-holland | Katwijk
### Utrecht (bestand areas_utrecht.py)
utrecht | Utrecht | stad | utrecht | Utrecht
amersfoort | Amersfoort | stad | utrecht | Amersfoort
veenendaal | Veenendaal | stad | utrecht | Veenendaal
nieuwegein | Nieuwegein | stad | utrecht | Nieuwegein
zeist | Zeist | stad | utrecht | Zeist
houten | Houten | stad | utrecht | Houten
ijsselstein | IJsselstein | stad | utrecht | IJsselstein
woerden | Woerden | stad | utrecht | Woerden
soest | Soest | dorp | utrecht | Soest
leusden | Leusden | dorp | utrecht | Leusden
### Flevoland en Zeeland (bestand areas_flevoland_zeeland.py)
almere | Almere | stad | flevoland | Almere
lelystad | Lelystad | stad | flevoland | Lelystad
emmeloord | Emmeloord | stad | flevoland | Noordoostpolder
dronten | Dronten | stad | flevoland | Dronten
zeewolde | Zeewolde | dorp | flevoland | Zeewolde
urk | Urk | dorp | flevoland | Urk
biddinghuizen | Biddinghuizen | dorp | flevoland | Dronten
middelburg | Middelburg | stad | zeeland | Middelburg
vlissingen | Vlissingen | stad | zeeland | Vlissingen
goes | Goes | stad | zeeland | Goes
terneuzen | Terneuzen | stad | zeeland | Terneuzen
zierikzee | Zierikzee | stad | zeeland | Schouwen-Duiveland
hulst | Hulst | stad | zeeland | Hulst
tholen | Tholen | stad | zeeland | Tholen
kapelle | Kapelle | dorp | zeeland | Kapelle
### Noord-Brabant (bestand areas_noord_brabant.py)
eindhoven | Eindhoven | stad | noord-brabant | Eindhoven
tilburg | Tilburg | stad | noord-brabant | Tilburg
breda | Breda | stad | noord-brabant | Breda
s-hertogenbosch | 's-Hertogenbosch | stad | noord-brabant | 's-Hertogenbosch
helmond | Helmond | stad | noord-brabant | Helmond
oss | Oss | stad | noord-brabant | Oss
roosendaal | Roosendaal | stad | noord-brabant | Roosendaal
bergen-op-zoom | Bergen op Zoom | stad | noord-brabant | Bergen op Zoom
waalwijk | Waalwijk | stad | noord-brabant | Waalwijk
### Gelderland (bestand areas_gelderland.py)
nijmegen | Nijmegen | stad | gelderland | Nijmegen
arnhem | Arnhem | stad | gelderland | Arnhem
apeldoorn | Apeldoorn | stad | gelderland | Apeldoorn
ede | Ede | stad | gelderland | Ede
doetinchem | Doetinchem | stad | gelderland | Doetinchem
zutphen | Zutphen | stad | gelderland | Zutphen
tiel | Tiel | stad | gelderland | Tiel
harderwijk | Harderwijk | stad | gelderland | Harderwijk
wageningen | Wageningen | stad | gelderland | Wageningen
### Overijssel (bestand areas_overijssel.py)
zwolle | Zwolle | stad | overijssel | Zwolle
enschede | Enschede | stad | overijssel | Enschede
deventer | Deventer | stad | overijssel | Deventer
hengelo | Hengelo | stad | overijssel | Hengelo
almelo | Almelo | stad | overijssel | Almelo
kampen | Kampen | stad | overijssel | Kampen
oldenzaal | Oldenzaal | stad | overijssel | Oldenzaal
hardenberg | Hardenberg | stad | overijssel | Hardenberg
steenwijk | Steenwijk | stad | overijssel | Steenwijkerland
### Limburg (bestand areas_limburg.py)
maastricht | Maastricht | stad | limburg | Maastricht
venlo | Venlo | stad | limburg | Venlo
heerlen | Heerlen | stad | limburg | Heerlen
sittard | Sittard | stad | limburg | Sittard-Geleen
geleen | Geleen | stad | limburg | Sittard-Geleen
roermond | Roermond | stad | limburg | Roermond
weert | Weert | stad | limburg | Weert
kerkrade | Kerkrade | stad | limburg | Kerkrade
venray | Venray | stad | limburg | Venray
landgraaf | Landgraaf | stad | limburg | Landgraaf
### Friesland (bestand areas_friesland.py)
leeuwarden | Leeuwarden | stad | friesland | Leeuwarden
drachten | Drachten | stad | friesland | Smallingerland
sneek | Sneek | stad | friesland | Súdwest-Fryslân
heerenveen | Heerenveen | stad | friesland | Heerenveen
harlingen | Harlingen | stad | friesland | Harlingen
franeker | Franeker | stad | friesland | Waadhoeke
joure | Joure | dorp | friesland | De Fryske Marren
dokkum | Dokkum | stad | friesland | Noardeast-Fryslân
bolsward | Bolsward | stad | friesland | Súdwest-Fryslân
### Groningen en Drenthe (bestand areas_groningen_drenthe.py)
groningen | Groningen | stad | groningen | Groningen
hoogezand | Hoogezand | stad | groningen | Midden-Groningen
veendam | Veendam | stad | groningen | Veendam
stadskanaal | Stadskanaal | stad | groningen | Stadskanaal
delfzijl | Delfzijl | stad | groningen | Eemsdelta
winschoten | Winschoten | stad | groningen | Oldambt
leek | Leek | dorp | groningen | Westerkwartier
appingedam | Appingedam | stad | groningen | Eemsdelta
assen | Assen | stad | drenthe | Assen
emmen | Emmen | stad | drenthe | Emmen
hoogeveen | Hoogeveen | stad | drenthe | Hoogeveen
meppel | Meppel | stad | drenthe | Meppel
coevorden | Coevorden | stad | drenthe | Coevorden
beilen | Beilen | dorp | drenthe | Midden-Drenthe
roden | Roden | dorp | drenthe | Noordenveld
klazienaveen | Klazienaveen | dorp | drenthe | Emmen

## Artikelen (slug | label | onderwerp) — bestand articles_a.py (eerste 7) en articles_b.py (laatste 7)
wat-is-lachgas | Basis | wat N2O is, geschiedenis kort, toepassingen in zorg/techniek/voeding, werking op het lichaam in grote lijnen
is-lachgas-legaal-in-nederland | Regels | Opiumwet lijst II sinds 1-1-2023, uitzonderingen, wat dat betekent voor bezit/verkoop/vervoer, gemeentelijke APV-verboden, bron rijksoverheid.nl
lachgas-regels-per-gemeente | Regels | hoe APV's werken, typen verboden (gebruik op straat/bij evenementen) zonder onjuiste details per gemeente te verzinnen; adviseer de APV van de eigen gemeente te raadplegen; noem dat grote steden als Amsterdam, Rotterdam, Utrecht en Den Haag eigen regels kennen, zonder te beweren wat die precies inhouden
lachgas-en-vitamine-b12 | Gezondheid | mechanisme, klachten, wanneer naar de huisarts
lachgas-bijwerkingen-en-eerste-hulp | Veiligheid | korte- en langetermijneffecten, bevriezingsletsel, wat te doen als iemand onwel wordt, 112
lachgas-en-alcohol | Gezondheid | waarom combineren riskant is, signalen, hulp
lachgas-in-het-verkeer | Regels | rijverbod, hoe politie controleert, gevolgen, alternatieven om thuis te komen
lachgastank-bewaren-en-vervoeren | Praktisch | rechtop, koel, droog, niet in warme auto, verzegeling, lege tank
lege-lachgastank-inleveren | Praktisch | waarom niet bij restafval, milieustraat van de eigen gemeente (algemeen, geen openingstijden verzinnen), wat wij adviseren
lachgas-bij-kou-en-warmte | Praktisch | druk en temperatuur, bevriezing van de kraan, zon en auto, winter
tank-versus-patronen | Producten | verschil tussen een tank en kleine patronen met een cracker, waarom wij alleen tanks bezorgen, veiligheid, afval
lachgas-en-het-milieu | Achtergrond | N2O als broeikasgas (ca. 265-300x CO2 over 100 jaar), bronnen van uitstoot, eigen rol
problematisch-lachgasgebruik-hulp | Hulp | signalen, waarom stoppen lastig is, hulp in Nederland (huisarts, regionale verslavingszorg, Jellinek als tekst en link, drugsinfo.nl), hoe je iemand aanspreekt
geschiedenis-van-lachgas | Achtergrond | Priestley 1772, Davy, tandheelkunde 1844, 20e eeuw, recente regelgeving; feitelijk, met voorzichtigheid bij jaartallen

## Kennisbank-artikelen (slug | label | onderwerp) — bestand articles_kennis.py, plus TOPIC_HUBS "veiligheid-en-gezondheid" en "regels-en-wetgeving" (schema als in ../brabant/articles_kennis.py)
lachgas-en-mentale-gezondheid | Gezondheid | stemming, angst, gewoontevorming, wanneer hulp zoeken
de-dag-na-lachgas | Gezondheid | nawerking, hoofdpijn, tintelingen, wanneer naar de huisarts
feest-thuis-zonder-overlast | Praktisch | buren, geluid, afval, wat te doen als iemand onwel wordt
lachgas-mythes-en-feiten | Basis | misverstanden ontkracht met bronnen
begrippenlijst-lachgas | Basis | termen uitgelegd (N2O, verzegeling, Opiumwet lijst II, APV, B12, milieustraat)
lachgas-op-festivals-en-evenementen | Regels | festivalregels in Nederland algemeen, waarom wij alleen op privéadressen leveren
lachgas-voor-ouders | Hulp | signalen, gesprek, hulp
betrouwbare-lachgas-bezorgservice-herkennen | Praktisch | kenmerken van een betrouwbare service (18+, verzegeld, prijs vooraf, geen vooruitbetaling), rode vlaggen
eerste-keer-lachgas-bestellen | Praktisch | wat je mag verwachten van bestellen tot levering, zonder gebruiksinstructies

## Servicepagina's (slug | label | onderwerp) — bestand services.py (deze 8, elk met precies 3 FAQ) + SERVICE_INDEX + INFO_INDEX (schema als ../brabant/services.py)
spoedbezorging | Spoed | wat snel bestellen vereist van de klant, wat wij doen, wat we niet beloven
nachtbezorging | Nacht | 24/7 bereikbaarheid, hoe nachtlevering gaat, discretie, rustig aanbellen
weekendbezorging | Weekend | drukte vrijdag/zaterdag, slim plannen, zondag
feestdagen-en-evenementen | Feestdagen | Oud en Nieuw, Koningsdag, carnaval in het zuiden, Pride en festivals (algemeen), vooraf reserveren, 18+ en legitimatie blijven gelden
betalen-bij-levering | Betalen | contant of Tikkie, prijs vooraf, geen vooruitbetaling, wat bij een betwiste levering
leeftijdscontrole-18-plus | 18+ | waarom altijd 18+, ID-controle, wat als iemand jonger blijkt, verantwoordelijkheid
bestellen-via-whatsapp | Bestellen | stap voor stap, welke gegevens, bevestiging, wijzigen of annuleren, privacy
bezorgtijden-per-regio | Bezorgtijden | h1 "Bezorgtijden in heel Nederland": één levertijd voor het hele land (meestal 15 tot 25 minuten) dankzij bezorgers in elke regio, wat de tijd kan beïnvloeden (drukte, weer, evenementen), hoe we een tijdvak bevestigen; GEEN zones of banden
## Extra servicepagina's — bestand services_extra.py (elk precies 3 FAQ)
zakelijk-bestellen | Zakelijk | horeca, verenigingen, organisaties; vooraf afstemmen, factuur, vaste contactpersoon; geen prijzen
bezorgvoorwaarden | Voorwaarden | adresvereisten (alleen privéadres), 18+, verzegeling controleren, wanneer wij niet leveren
bestelling-wijzigen-of-annuleren | Wijzigen | hoe wijzigen/annuleren via dezelfde chat, tot wanneer, wat als de koerier al rijdt
veilig-bestellen-oplichting-herkennen | Veilig | nepaanbieders, vooruitbetaling, verzegeling, hoe je ons herkent (zonder nummer te noemen)

## FAQ-thema's (slug): bestellen, bezorgen, betalen, veiligheid, regels (8-12 items elk, geen overlap) — bestand faq_pages.py + FAQ_INDEX + CONTACT + ABOUT (schema als ../brabant/faq_pages.py)
## Tanks + juridisch — bestand tanks_legal.py: TANKS (INDEX + TANKS 2kg/4kg/10kg), TERMS, PRIVACY (schema als ../brabant/tanks_legal.py)
## Kern — bestand core.py: HOME en AREA_INDEX (schema als ../brabant/core.py; HOME "city_slugs" = 12 grote steden uit verschillende provincies); bestand hubs_a.py: HUBS voor noord-holland, zuid-holland, utrecht, noord-brabant, gelderland, overijssel; bestand hubs_b.py: HUBS voor limburg, friesland, groningen, drenthe, flevoland, zeeland. Elke hub: "gemeenten"-tabel met 8-12 belangrijke gemeenten van die provincie (naam, kernen, levertijd "meestal binnen 15 tot 25 minuten"), "places" = alle plaats-slugs van die provincie uit deze brief, "card" ≤120 tekens, 5 FAQ.
