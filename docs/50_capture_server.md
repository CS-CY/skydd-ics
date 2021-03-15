# Nätverksinspelningsserver

Detta kapitel beskriver en server med en särskild säkerhetsfunktion - att kunna spela in och spara nätverkstrafik som den ser via de nätverksanslutningar den har. Servern är en för funktionen speciellt uppsatt Linuxserver som enbart fungerar som nätverksövervakare.

Det här kapitlet går närmare in i hur tjänsten installeras, hur man använder nätverksinspelningarna, ger
förslag på hur detta kan användas för att förbättra säkerheten i ett SCADA/ICS-nät, med mera.

## Översikt

Nätverksinspelningsservern är en tjänst som används för att spara
nätverkstrafik från alla nätverksgränssnitt som servern är ansluten till, det sker med hjälp av [NetworkManager]. Det går
att tänka på den som en eller flera övervakningskameror som är riktad mot ett visst objekt eller i det här fallet nätverk. När det händer något
på nätverket, spelas det in och sparas på serverns hårddisk.

Den inspelade nätverkstrafiken har flera möjliga användningsområden:

  * Vid felsökning av system, applikationer eller nätverk går det att undersöka inspelad trafikdata.
  * Vid en IT-incident går det att gå tillbaka i tid och undersöka olika händelser, genom att analysera nätverksinspelningen som gjorts vid den aktuella tidpunkten för att se om det går att hitta någon relevant trafik i relation till incidenten.
  * Vid prestandaproblem går det att se vilka nättjänster som använder nätet, hur mycket nätverket används, etc.

## Installation av nätverksinspelningsserver

Installationen är till största delen automatiserad och enbart ett fåtal steg måste utföras för att få en fullt fungerande nätverksinspelningsserver.

  1. Starta datorn från installationsmediet som skapats enligt [Skapa installationsmedia].
  2. Installera nätverksinspelningsservern genom att följa instruktionerna i [Installation].

Under installationen av nätverksinspelningsservern går det att konfigurera nätverkskortet direkt med en [link-local] adress för att inte behöva göra den inställningen enligt instruktionerna i kapitlet [Nödvändiga inställningar].
Dessutom går det att konfigurera nätverksinställningarna att automatiskt aktivera nätverkskortet vid uppstart som det beskrivs i installationsguiden. Om båda inställningarna görs behövs kapitlet [Nödvändiga inställningar] utföras.

Notera att beroende på var servern placeras kan mängden data som sparas bli mycket stor. Välj därför en större installationsdisk än vad som är normalt för en server. På så sätt kan trafikdata sparas så länge som möjligt. När disken blir
80 procent full börjar de äldsta inspelningarna automatiskt raderas.

Det går att montera en till disk för sparande av trafikdata. Men observera då att de existerande [SELinux]-reglerna är inställda så att [tcpdump] enbart kan skriva i **/home/tcpdump/**.

## Nödvändiga inställningar

Efter en installation behöver de nätverkskort där trafik ska spelas in, aktiveras i [NetworkManager]. Det görs
enklast genom menyn uppe i högra hörnet.

![NetworkManager ikon.](images/networkmanager_bar.png "NetworkManager Inställningar.")

Samtliga nätverkskort som är aktiva kommer som standard att spela in trafik automatiskt när servern är startad.
Det räcker med att ställa in *Link-Local Only* på det önskade nätverkskortet för att trafik ska spelas in. Sätt inte ut en IP-adress på nätverkskortet eftersom det av säkerhetsskäl är bra att maskinen inte är nåbar från andra nätverk.

![NetworkManager interface.](images/networkmanager_link.png "NetworkManager Link-Local på ett interface.")

## Användning

Det här kapitlet går närmare in på hur man använder sig av nätinspelningsserverns olika möjligheter.

### Sökning i inspelad nätverkstrafik

En användabar funktion är att kunna söka efter textsträngar i den nätverkstrafik som spelats in.

Genom att starta webbläsaren och gå till URL <http://127.0.0.1/dump> går det att söka i de
existerande nätverksdumparna direkt på servern. Hur denna sökfunktion ser ut går att se på nästa bild.

![Sökning i inspelad nätverkstrafik.](images/trafikvy-sok.png "Sökning i inspelad nätverkstrafik.")

Bakom kulisserna använder sig sökfunktionen av verktyget [ngrep], ett program för att kunna tolka
innehållet i nätverksinspelningar, för att kunna välja ut de dumpar som är intressanta.

![Sökning i inspelad nätverkstrafik, utan att träffa på sökt information.](images/trafikvy-sok-no-hit.png "Sökning i inspelad nätverkstrafik, utan att träffa på sökt information.")

### Analys av inspelad nätverkstrafik med Chaosreader

När en inspelad trafikdump valts ut, går det att antingen packa upp den direkt på servern
med hjälp av verktyget [Chaosreader] som kan förstå nätverkstrafik, eller titta på den med webbläsare.

Nedanstående bild visar hur det ser ut i webbläsaren när man får upp en lista över filer med
inspelad nätverkstrafik. På bilden klickar vi på knappen "packa upp" för att ta upp och
visa filinnehållet i verktyget *Chaosreader*.

![Klicka på knappen "packa upp" för att titta på en trafikinspelning med hjälp av verktyget Chaosreader.](images/trafikvy-analysera-trafik.png "ÖVersikt inspelad trafik.")

Nästa bild visar hur det ser ut i webbläsaren när Chaosreader har analyserat den inspelade
nätverkstrafiken och visar upp en lista över trafikdata och nätverksströmmar.

![Översiktsbild i verktyget Chaosreader.](images/chaosreader-overview.png "Chaosreader översikt.")

Nästa bild visar en detaljvy när verktyget Chaosreader har avkodat nätverkstrafiken och visar
upp den i webbläsaren. I exemplet ser vi hur en HTTP-ström har avkodats och vi ser den blåa frågan
och den röda färgen som är satt på svaret.

![Detaljbild när verktyget Chaosreader har avkodat nätverkstrafik.](images/chaosreader-details.png "Chaosreader detaljvy.")

Det går också att hämta hem hela trafikdumpen och använda andra verktyg, till exempel [Wireshark], på en lokal dator för att göra en annan analys.

### Analys av inspelad nätverkstrafik med Wireshark

En annan metod för att avkoda inspelad nätverkstrafik är att använda verktyget [Wireshark],
som har stöd för att tolka många olika nätverksprotokoll på detaljnivå. Verktyget Wireshark
medföljer paketeringen.

Nästföljande bild visar var i menyerna man hittar verktyget Wireshark.

![Detaljbild över när verktyget Wireshark ska startas.](images/wireshark-startup-pic1.png "Wireshart uppstart.")

Nedanstående bild visar när verktyget Wireshark har startats igång och använts för att avkoda nätverkstrafik.

![Detaljbild över när verktyget Wireshark har startat.](images/wireshark-startup-pic2.png "Wireshark detaljvy.")

Nedanstående bild visar filväljaren. Notera den röda rektangeln som visar var någonstans i filträdet som filerna
finns undansparade, det vill säga */home/tcpdump/*. Du måste gå runt i filträdet för att komma dit och lista filerna.

![Detaljbild över när verktyget Wireshark ska ladda en inspelningsfil.](images/wireshark-select-file.png "Wireshark detaljvy för filval.")

Nedanstående bild visar när filen med den inspelade nätverkstrafiken är inläst i verktyget Wireshark. Här kan nätverkstrafiken analyseras i detalj.

![Detaljbild när verktyget Wireshark har avkodat nätverkstrafik.](images/wireshark-overview-pic1.png "Wireshark detaljvy.")

*Det bör noteras att den version av Wireshark som finns tillgänglig för CentOS är 1.x. Den senaste versionen av Wireshark,
är inte tillgänglig som en del av CentOS supporterade standardpaket. Senare versioner har en del förbättringar i stödet för att avkoda protokoll, inte minst vad det gäller möjligheten att avkoda Siemens S7-protokoll.*  

## Detaljbeskrivning

Denna server använder verktyget [tcpdump] för att spela in trafik på de nätverksgränssnitt som är uppe enligt [NetworkManager]. När [NetworkManager] märker att ett gränssnitt är uppe triggas ett event som i sin tur får [Systemd] att starta en tcpdump-instans
på det gränssnitt som kom upp.

En konsekvens av detta är att en inspelning avslutas, och sparas ner till en färdig fil,
i samband med att nätverksgränssnittet stängs ner, exempelvis med när man kopplar ur en nätverkskabel.
Detta kan vara bra att känna till om man direkt vill kunna analysera senast inspelad
trafik.

### Vart inspelad nätverkstrafik sparas

De inspelade nätverkstrafik-dumparna hamnar i filkatalogen **/home/tcpdump/**. För att filer
som ska öppnas i analysverktyg ska ha en hanterbar storlek är inspelningsfunktionen satt att
hacka upp inspelad nätverkstrafik i filer av fix storlek. Det innebär i praktiken att inspelningsfiler
roteras automatiskt när de blir 100MB stora.

Namnet på loggarna följer mönstret

```
	gränssnitt-datum-och-tid-när-gränssnittet-kom-upp.pcap
```
och när de roteras adderas en siffra till namnet.

Till exempel skulle en fil som heter *eno77744-2016-01-01.pcap* bli *eno77744-2016-01-01.pcap1*.

### Hur gamla nätverksinspelningar hanteras  

Ett skript som vi utvecklat och som används för att bättre kontrollera insamlade filer vid namn *reaper.py*
körs vid start och ansvarar för att partitionen där dumparna läggs alltid har plats över för att kunna rotera en dump.
Blir hårddisken full, tar reaper-skriptet bort de äldsta filerna automatiskt. Det innebär att denna server ska kunna stå igång i flera år utan att någon behöver logga in och rensa bort gamla dump-filer på grund av att hårddisken blivit full.

### Säkerhet för att skydda systemet från angrepp och fel i inspelningsfunktionen

Säkerhetsmekanismen *[SELinux]*, som är ett sätt att med hårda säkerhetsinställningar styra ett exekverande
program, används för att låsa ner *tcpdump* så att detta inte kan skriva någon annanstans än just under
filkatalogen **/home/tcpdump**. Detta är ett sätt att kunna försäkra sig mot att eventuella gömda eller
framtida säkerhetshål i tcpdump kan missbrukas och bli till säkerhetsproblem mot själva servertjänsten.

### Säkerhet för att skydda systemet vid läsning av inspelad trafik

En webbserver, [Apache], är igång och nedlåst med *[SELinux]* så att den enbart
ska kunna läsa i **/var/www** och i **/home/tcpdump** där de inspelade nätverksdumparna ligger.

## Avancerat, nästa steg

Om servern ska spela in en stor mängd trafik kan det vara möjligt att *tcpdump* inte räcker till.
Då är det bättre att byta till [Netsniff-NG] som följer med installationen. Om netsniff ska användas är det möjligt att ändra i
skriptet som startar *tcpdump* i **/etc/NetworkManager/dispatcher.d/99-tcpdump**.


Önskas en "live" bild av trafiken kan man installera [ntop]. Med det verktyget kan
man lättare få en bild av nätverkstrafiken vid tillfället. Samma projekt har även flera andra
verktyg som kompletterar och som ibland kan ersätta de verktyg som är installerad på denna server.

### Åtkomst till webbgränssnitt via nätverket

Som standard går webbgränssnittet enbart att nå via den egna datorn, via lokalt ansluten
skärm och tangentbord. När servern kommer igång startar det grafiska gränssnittet lokalt.
Via denna grafiska miljö kan man via en lokalt startad webbläsare komma åt gränssnittet.
Det går alltså inte att nå webbtjänsten direkt via nätverket. Orsaken till detta är att
standardinstallationen ska   vara så säkert uppsatt som möjligt.

Om det finns behov av att kunna nå nätverksinspelningsservern från en annan dator måste
konfigurationen för webbservern ändras så att den även är åtkomlig på det externa nätverksgränssnittet. För att hindra att den potentiellt känsliga trafiken ska kunna ses av någon obehörig, eller att serven kan nås, och loggas in i, av någon obehörig måste kryptering av webbtrafiken samt autentisering av åtkomst till webbsidan aktiveras.

Nano är namnet på ett textredigeringsprogram som medföljer. Använd nano, vi eller mg efter önskemål.
*För hjälp att förstå hur man använder textredigeringsprogram eller hur man använder sig av terminalprogrammet,
se närmare detaljinformation i kapitlet [Terminal-åtkomst och kommandoraden].*

Förutom att aktivera nätåtkomst till webbserverdelen samt aktivera TLS-kryptering, måste du också öppna brandväggen.
Starta programmet *Terminal* från menyn ”Applications”. Redigera filen **/etc/sysconfig/iptables**. för att tillåta inkommande nätverkstrafik  
Gör det med ett textredigeringsprogram enligt nedanstående exempel:

```
   	      sudo nano /etc/sysconfig/iptables
```

När brandväggsreglerna är ändrade och nedsparade, ladda du om brandväggsreglerna med
kommandot:

```
 	      sudo iptables-restore /etc/sysconfig/iptables
```

### Undantag av nätverkskort för inspelning

För att undanta ett nätverkskort från att användas måste det undantas network manager som är den tjänst som startar funktionen. Det görs enklast genom att i konfigurationsfilen för nätverkskort skriva följande:

> NM_CONTROL=no

i filen

`/etc/sysconfig/network-scripts/ifcfg-"interfacenamn"`

\clearpage
