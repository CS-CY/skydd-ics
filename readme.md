# Samling av säkerhetslösningar byggda på öppen källkod för att skydda eller upptäcka hot i [SCADA]/[ICS]-miljö]

Detta programarkiv innehåller ett antal olika säkerhetslösningar, vissa för att skapa skydd, andra för att kunna fungera som logg/larm/övervakningsservrar, i ICS/SCADA-miljöer. Dessa säkerhetslösningar bygger i grund och botten på fria och öppna programvaror (s.k. [FOSS]).

Lösningen består av ett installations-media varifrån du kan välja att installera olika säkerhetsfunktioner på servrar. Bland de servrar du kan installera så finns exempelvis

* en enkel logginsamlingsserver som tar emot syslog-trafik och har ett enkelt webbgränssnitt för att kunna söka efter strängar i insamlade loggar
* en larmserver som sätts upp som mottagare och hanterare av olika larm från övervakade tjänster och utrustning
* en nätverksinspelnings-nod som kan samla in nätverkstrafik
* en intrångsdetekterings-nod som kan agera på attackmönster på nätverksnivå

## Filstruktur

Filkatalogen **docs/** innehåller dokumentation skriven i markdown för de enskilda servrarna som går att installera, samt tillhörande stöddokumentation. Från denna grunddokumentation kan motsvarande dokumentation i HTML, pdf m.m. skapas. En sammanställd bok, kallad bok.pdf skapas också av alla dokumentationsfilerna.

Filkatalogen **image/** innehåller skript och konfigurationer för att skapa en avbildning som kan skrivas till en DVD eller en USB-minnessticka.

Filkatalogen **pictures/** innehåller bilder som används


# Vägledning för att bygga och använda lösningen


## För att skapa en installationsmedia, en s.k. [ISO]-fil på en dator med CentOS 7:

### Beroenden
* En av följande virtualiseringsmiljöer:
  * [kvm]
  * vmware
  * [virtualbox] - VBoxManage använder sig av Intel VT eller AMD-V och behöver då vara påslaget i BIOS.
* [Vagrant]

### Bygga installationsmedia
1. Hämta källkoden. Detta kan exempelvis göras genom att ladda ner ZIP-filen eller klona med HTTPS.
Länk till ZIP-fil och adress för kloning finns under "Clone or download"-knappen i detta GiHub repository:
![Download](/pictures/klona.jpg)
    ```console
    $ git clone https://github.com/CS-CY/skydd-ics.git
    ```

2. Starta ett terminal-fönster om inte redan gjort under steg 1

3. Gå in i vagrantmappen när källkoden är nedladdad/uppackad
    ```console
    $ cd vagrant
    ```
4. Skapa och konfigurera en gästmaskin med namnet *build* enligt filen *Vagrantfile*
    ```console
    $ vagrant up build
    ```
5. Anslut till den nyskapade virtuella maskinen via SSH
    ```console
    $ vagrant ssh build
    ```
6. Byt till root rättigheter
    ```console
    $ sudo su -
    ```
7. Byt katalog
    ```console
    $ cd /vagrant/image
    ```
8. Välj lämplig URL på http://isoredirect.centos.org/centos/7/isos/x86_64/ för att använda i kommandot nedan. Det är en CentOS 7 iso av typen minimal som ska användas.
    ```console
    $ curl -o centosdvd.iso [url till centos minimal installationsmedia]
    ```
9. Verifiera checksumman enligt https://wiki.centos.org/TipsAndTricks/sha256sum
10. Sätt upp ISO-filen som en enhet i filträdet
    ```console
    $ mount -o loop centosdvd.iso DVD
    ```
11. Ladda ner nödvändiga packet och beroenden
    ```console
    $ ./download_packages.sh
    ```
12. Skapa ISO-fil för installationsmedia
    ```console
    $ ./create_iso.sh
    ```
13. Den byggda iso:n (skydd-ics.iso) finns i katalogen /vagrant/image

### Skapa en bootbar DVD/USB
Se avsnitt *[8.1 Skapa installationsmedia](docs/81_skapa_installations_media.md)*  i [dokumentationen](docs/).


## För att skapa/ändra dokumentation
### Beroenden
* [pandoc]
* texlive
* texlive-latex-extra

### Skapa/ändra
1. I den katalog till vilken du laddat ner filerna, byt till underkatalogen med hjälp av kommandot **cd docs**
2. Ändra i de textfiler eller de bilder som ska ändras
3. I docs-katalogen, skriv **make all** för att bygga dokumentationen och för att testa förändringarna som gjorts


# Att starta upp från installationsmediet (DVD eller USB-sticka) första gången

Sätt in installationsmediet (DVD eller USB) i den dator som du vill använda för att installera dessa program på.
**Notera att hårddisken som sitter i datorn kommer att omformatteras i det fall du väljer att påbörja en installation. All information på den hårddisken kommer att skrivas över**

När man startar en dator från installationsmediet så går det att välja vilken typ av server som ska installeras. Därefter startas en så kallad [kickstart]installation, där installationsförfarandet av grundläggande systemkomponenter och många installationsval är automatiserade.

Se [dokumentationen](/docs/20_installation.md) för ytterligare information kring installation.

## Att starta upp datorn med de nyinstallerade tjänsterna första gången
Efter installationen är färdig, så ombeds du att starta om datorn, denna gång för att starta upp ifrån ditt nyinstallerade system. Ta ut USB-stickan eller DVD-skivan så att datorn inte försöker starta upp därifrån. I samband med omstart så ombeds du skapa en användare med tillhörande lösenord. När detta är klart så är systemet uppstartat och användaren är inloggad.

Om installationen gått enligt plan, så är webläsaren [firefox] automatiskt startad. Startsidan för webbläsaren innehåller ytterliggare
instruktioner för hur just den aktuella installationen används. Om du av misstag stänger ned webbläsaren, starta den på nytt via menyn "Application" -> "Favorites" -> "Firefox".

# Om något fel inträffar

Om installation inte slutfördes eller inte startades kan det vara så att just den datorn inte stöds utav den Linux-distribution som används.
Testa att installera på en annan dator, helst en annan modell och om möjligt en nyare årsmodell.

[kickstart]: https://docs.centos.org/en-US/centos/install-guide/Kickstart2/ "Ett sätt att installera ett operativsystem med programvara automatiskt"

[SCADA]: https://en.wikipedia.org/wiki/SCADA "Datormiljö som används för industriell automation."
[ICS]: https://en.wikipedia.org/wiki/Industrial_control_system "Datormiljö som används för industriell automation."

[FOSS]: https://en.wikipedia.org/wiki/Free_and_open-source_software "Free and Open-Source Software. Samlingsnamn för datorprogram som klassificeras som både fri (tillgänglighen är inte begränsad) och källkoden är tillgänglig för alla och envar att studera, kopiera, modifiera m.m."

[firefox]: https://en.wikipedia.org/wiki/Firefox "Fri webbläsare som har stor spridning i Linuxvärlden."

[ISO]: https://sv.wikipedia.org/wiki/ISO-avbild "En strukturerad fil som innehåller alla filer sammanställda till en stor sammanslagen fil, vilket är en avbildning av en CD/DVD-skiva"

[kvm]: https://www.linux-kvm.org/page/Main_Page "En virtualiseringsmodul i Linuxkärnan."

[virtualbox]: https://www.virtualbox.org/ "Programvara för virtualisering."

[Vagrant]: https://www.vagrantup.com "Verktyg för att konfigurera och hantera miljöer med virtuella datorer."

[pandoc]: https://pandoc.org/ "Verktyg för att konvertera mellan olika textformat"
