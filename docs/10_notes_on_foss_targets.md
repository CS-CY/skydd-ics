# Sammanställning av de olika servertyperna
Det här är en sammanställning av de olika varianter av servrar som går att installera med hjälp av de guider och instruktioner som finns tillgängliga i detta paket.

Alla installationsmoment är gjorda så att själva installationen är så automatiserad som möjligt.
För de installationer där manuell konfiguration behövs är det antingen av säkerhetsrelaterade skäl eller av den enkla
anledningen att det måste ske en anpassning till den aktuella nätverksmiljön.

Nedan beskrivs på ett mer övergripande sätt de olika typer av tjänster och servrar som ingår.

## Logginsamlingsserver

Den här servertypen är till för att samla in loggar (spårdata) från andra datorer. En loggserver är mycket användbar både för felsökning och vid incidenthantering. Dessutom kan en dedikerad, extern loggserver krävas för att ingen ska kunna missbruka en server. Det går att lösa genom att vanliga
serveradministratörer inte får åtkomst till den centrala loggservern.

![Principskiss loggserver.](images/overview-logserver.png "Översikt och principskiss för en loggserver.")

En enkel loggserver klarar att ta emot och samla in loggar från andra system. Den ser också till att loggmeddelanden finns tillgängliga över tid
genom att spara ner dem på disk. För vissa ändamål kan det krävas en mer avancerad server för att kunna ha bättre
kontroll av de händelser som sker i en miljö. Dock är den här servertypen en mycket bra start ifall det inte finns någon central loggserver.


## Nätverksinspelningsserver

Den här servertypen är till för att på ett enkelt sätt kunna spela in nätverkstrafik och spara information om den. För att spela in trafik så kopplar man in en nätverkskabel till den nätverksport där inspelning ska ske. För att relevant trafik ska komma till den aktuella porten behövs antingen en nätverkstapp eller en switch som är konfigurerad med en så kallad *monitoreringsport* eller *SPAN-port*.

![Principskiss nätverksinspelningsserver.](images/overview-networkrecorder1.png "Översikt och principskiss för en nätverksinspelningsserver.")

## IDS-server

Den här servertypen är till för att kunna agera på beteenden i nätverk genom att lyssna på och analysera nätverkstrafik för att hitta signaturer eller mönster som tyder på intrång, policyöverträdelser, med mera.
Servern ansluts på en sådan nättopologisk plats att den kan se nätverkstrafik där det finns behov av larm vid onormala beteenden. Detta kan ske genom att exempelvis koppla nätverksporten till en så kallad *monitoreringsport* eller *SPAN-port*.

![Principskiss intrångsdetekteringssystem.](images/overview-ids2.png "Översikt och principskiss för en IDS.")

## Nätverksinspelningsserver och IDS-server

Den här servertypen är en kombination av nätverksinspelningsserver och IDS-server. Den innehåller samtliga funktioner som finns i de båda servertyperna. För dokumentation se respektive avsnitt för de ingående servertyperna.  

*Om denna installation väljs finns det ett känt varningsmeddelande som kommer efter första inloggningen då både servertyperna försöker öppna dokumentation genom att starta Firefox. Denna varning kan ignoreras.*

## Larmserver

Den här servertypen är till för att kunna övervaka andra servar, andra infrastrukturkomponenter samt
de tjänster som finns på dem. Den kan till exempel upptäcka och larma om att  lagringsutrymmet
håller på att ta slut och att lasten på servern (hur nedtyngd servern är) är för hög.

![Principskiss larmserver.](images/overview-alarmserver.png "Översikt och principskiss för en övervaknings- och larmserver.")

Installationen av servern i sig är automatisk, men för att funktionen ska kunna vara verkningsfull, krävs att den konfigureras mot den miljö som ska övervakas.

## Brandvägg för SCADA- och ICS-miljö

Den brandvägg som valts heter pfsense. Den är en mogen och beprövad lösning som sedan tidigare har en färdig paketering.
Pfsense har också många säkerhetsfunktioner, exempelvis inbyggt stöd för skydd mot överlastningsattacker, loggning av trafik,
möjlighet att sättas upp i klustrat högtillgänglighetsläge, normalisering (tvätt) av överförda nätverkspaket, med mera.

Eftersom Pfsense sedan tidigare har en paketering har den inte ompaketerats. För den här servertypen har dock en installations- och användarguide på svenska framställts.

Nedanstående bild visar hur en brandvägg fungerar i princip. I datorsammanhang och i IT-säkerhetssammanhang är en brandvägg
en kontrollfunktion med filtrerings- och spårbarhetsmöjlighet som styr datortrafik som passerar mellan olika nätverk. Bilden visar
att viss typ av trafik, den gröna pilen, släpps igenom brandväggen medan den brandgula pilen visar trafik som blockeras från att
passera brandväggen. Förekomsten av blockerad eller genomsläppt trafik kan loggas och därmed bli spårdata som går att analysera,
sammanställa och ta fram rapporter eller statistik från.

![Principskiss brandvägg.](images/overview-firewall1.png "Översikt och principskiss för en brandvägg.")

Nästa bild visar att en brandvägg kan bestå av flera anslutningspunkter. Vissa mer okontrollerade nät finns på en sida och ett internt nätverk - i detta fall ett processkontrollnät finns på den andra sidan som här kallas "insidan" och ett eller flera så kallade DMZ-nät som sitter i den demilitariserade zonen.

![Principskiss brandvägg - uppdelning av in- och utsida samt DMZ-nät.](images/overview-firewall2.png "Översikt och principskiss för en brandvägg.")

I geografiskt utspridda organisationer, till exempel elbolag med lokalkontor, olika anläggningar för distribution och produktion, med mera, kan det finnas behov av att installera flera interna brandväggar för att dela upp nätverket i mindre delar som har åtkomstbegränsningar
från varandra. Nästa bild visar översiktligt behovet av att dela in ett koncernnät i olika delar, där de olika process-, ICS- eller SCADA-miljöerna
är utseparerade från det sammanhållande koncernnätet. Detta för att skydda processnäten från obehörig åtkomst eller misstag med it-teknik som kan
påverka tillgänglighet och produktion.

![Principskiss brandvägg - användning av flera interna brandväggar för olika nät.](images/overview-firewall3.png "Översikt och principskiss för en brandvägg.")

Notera att eftersom Pfsense inte ompaketerats hämtas själva installationsfilen ner från tillverkaren på adress [pfsensedl].

## Placering av de olika säkerhetslösningarna

Det finns många alternativ på var i ett nät en komponent kan vara placerad. Vad som är rätt beror på hur det aktuella nätverket ser ut. Ibland kan det även vara bra att gör en ny design på nätverket för att uppnå bättre säkerhet. För att visa hur de olika komponenterna skulle kunna ge en bättre kontroll och säkerhet utan att påverka den aktuella designen används i exemplet nedan en fiktiv nätverksmiljö som inte är designad utifrån säkerheten.

![Enkel nätverksdesign.](images/exempel-utan-skydd.png "Enkel nätverksdesign.")

Med en nätverksmiljö som den ovanstående beskrivna är det möjligt att med relativt
små medel, till exempel de gratisverktyg som erbjuds i den här paketeringen, bygga in säkerhetskomponenter som kan förbättra säkerheten och kontrollen i nätverket
avsevärt.

![Enkel nätverksdesign med skydd.](images/exempel-med-skydd.png "Enkel nätverksdesign med skydd.")

Kostnaden för att uppnå det förstärka skyddet, med hjälp av de extra komponenterna och de extra skydd som dessa kan ge,
bör ställas i relation till arbetsinsatser och investeringar. Om man till exempel lyckas återanvända en redan existerande
dator, om gammal hårdvara återanvänds, och till detta lägger någon dag eller en veckas arbete, kan det i många fall vara en god investering som kan ge en mycket bra utdelning.

\clearpage
