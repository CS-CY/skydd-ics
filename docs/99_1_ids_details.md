# Bilaga. Byggdetaljer för IDS-Server

Den här bilagan beskriver i mer detaljnivå vad som behöver göras för att kunna bygga den IDS-funktion som skapats. Det finns två syften med bilagan: (1) att fungera som dokumentation för det arbete som lagts ner, men kanske viktigare (2) att fungera som instruktion för de som vill göra ändringar, utökningar eller på annat sätt återskapa samma grundförutsättningar för att kunna bygga de programpaket som ingår i IDS-lösningen.

## Snort

Snort har inte sina paketfiler för Linux CentOS i något repository. Det innebär att uppdateringar måste laddas ner direkt från deras hemsida: <https://snort.org/>. För att uppdatera **IDS-Servern** räcker det med att ladda ner RPM:erna *snort* och *daq* från <https://snort.org/#centos>, kopiera dem till **IDS-servern** och köra följande i en [Terminal] som *root*-användare i den katalogen dit filerna kopierades:

```
    rpm -i snort*.rpm daq*.rpm
```

### Snort-regler

Det medföljer inga regler till Snort-paketen utan de måste laddas ner separat. Vi har därför paketerat med två grupperingar av regler med denna
installation: Community-regler från Snort och ICS/SCADA-reglerna från Quickdraw. Community-reglerna är en samling regler som vanliga användare av Snort har
skickat in. Dessa regler passar inte alltid i alla miljöer men i en relativt tyst ICS/SCADA-miljö borde de aldrig larma då de flesta reglerna är
skrivna för Internet och kontorsmiljöer. Quickdraw-reglerna däremot är utvecklade specifikt för att larma om trafik mot SCADA-system. Dessa regler
har några variabler som måste justeras för att de inte ska larma på normal trafik. Nedan följer ett exempel:

```
    alert tcp $MODBUS_CLIENT any -> $MODBUS_SERVER 502 ( \
        flow:from_client, established; \
        content:"|00 00|"; \
        offset:2;  \
        depth:2; \
        content:"|08 00 04|"; \
        offset:7; \
        depth:3; \
        msg:"SCADA_IDS: Modbus TCP - Force Listen Only Mode"; \
        reference:url,digitalbond.com/tools/quickdraw/modbus-tcp-rules; \
        classtype:attempted-dos; \
        sid:1111001; \
        rev:2; \
        priority:1; \
    )

```

MODBUS_CLIENT och MODBUS_SERVER är variabler som sätts i filen: **/etc/snort/snort.conf**. Dessa variabler bör ändras så att de reflekterar verkligheten i den miljö där IDS-servern sitter.

Det går att registrera sig på Snorts hemsida för att få tillgång till fler regler och sedan få uppdateringar till dessa automatiskt.

## Barnyard2

Barnyard2 är den process som läser från *Snort*s loggar och stoppar in dem i en databas. Den finns inte som paket utan
den har för denna server laddats ner från <https://github.com/firnsy/barnyard2/releases>. Den har sedan kompilerats
enligt följande:

```
    $ tar xvzf barnyard2-v2-1.13.tar.gz
    $ cd barnyard2-2-1.13/
    $ /configure --with-mysql --with-mysql-libraries=/usr/lib64/mysql/
    $ make -j4
```

Sedan har den resulterande binären, vars SHA256-checksumma är

    e803874cdc0dd8a6f6edd5d6a5473ec5cda793793f4dbeae8b09b7a9371821c9

kopierats in under filkatalogen **/usr/local/bin/**.

## Snorby

**Snorby** klonades direkt från sin master-branch eftersom de har gjort flera säkerhetsfixar där sedan sin senaste release. För
att få exakt samma version som användes för IDS-servern, använd följande instruktioner:

```
    $ git clone https://github.com/Snorby/snorby
    $ cd snorby
    $ git checkout 5a3a33cf496b66be7ef4bd7d3cce0a996e1d2112
```

**Snorby** har ett beroende på [Ruby] version 1.9.x vilket innebär att det inte går att använda den Ruby-version som följer
med **CentOS 7**. Dessutom behövs det då en annan webbserverversion och tillhörande modul för [Passenger].
En lösning på detta är att använda färdiga byggen från [Software Collections]. Installera följande
RPM-paket för att få tillgång till dessa:

```
    # yum install scl-utils
    $ export RHSCL=https://www.softwarecollections.org/en/scls/rhscl/
    $ wget $RHSCL/v8314/epel-7-x86_64/download/rhscl-v8314-epel-7-x86_64.noarch.rpm
    $ wget $RHSCL/ruby193/epel-7-x86_64/download/rhscl-ruby193-epel-7-x86_64.noarch.rpm
    $ wget \
       $RHSCL/rh-passenger40/epel-7-x86_64/download/rhscl-rh-passenger40-epel-7-x86_64.noarch.rpm
    $ wget $RHSCL/httpd24/epel-7-x86_64/download/rhscl-httpd24-epel-7-x86_64.noarch.rpm
    $ sudo rpm -i rhscl*.rpm
```

Sedan går det installera de nödvändiga paketen genom följande:

```
    $ sudo yum install -y v8314 ruby193 ruby193-ruby-devel
    $ sudo yum install -y rh-passenger40 rh-passenger40-ruby193 httpd24
```

Efter detta steg går det att fortsätta med **Snorby**-installationen. Flytta snorby-katalogen till webbkatalogen, till exempel **/var/www/html/snorby**, gå in i katalogen och justera följande:

1. Ändra i Gemfile: "gem 'rake', '0.9.2'" till "gem 'rake', '>0.9.2'".
2. Ändra i Gemfile.lock: "rake (0.9.2)" till "rake (0.9.2.2)".

För att få ner de Ruby-paket som **Snorby** behöver måste du dessutom göra följande (fortfarande stående i samma katalog):

```
    # yum install -y git
    # yum install -y ruby193-ruby-devel
    # yum install -y gcc-c++-4.8.3-9.el7.x86_64
    # yum install -y libxml2-devel libxslt-devel
    # yum install -y mariadb-devel
    # bundle install --deployment
    # RAILS_ENV=production bundle exec rake snorby:setup
```

Utöver dessa steg behöver dess databas, login och lösenord konfigureras vilket görs i **config/snorby_config.yml** och **config/database.yml**.

## Databasen

Under kickstart-installationen genererades det nya lösenord till databasanvändarna *root* och *snort*. Dessa sparas i **/root/.mariadb_pass** respektive **/etc/snort/.mariadb_pass** med filrättigheterna satta så att enbart rätt användare får läsa dem. För att koppla sig till databasen som *root*:

```
    # mysql -uroot -p$(</root/.mariadb_pass)
```

## Systemd

Vi har under **/etc/systemd/system/** skapat [systemd]-servicefiler vilka används av systemet för att starta
och stoppa de installerade tjänsterna.

* snort@.service, används av NetworkManager för att starta och stoppa *snort* på rätt nätverkskort.
* barnyard2.service, används av systemd för att starta *barnyard2* efter att *MySQL* startat.
* snorby.service, används av systemd för att starta *Snorby* efter att *barnyard2* startat. Detta skript använder sig i sin tur av två skript vi skrivit **/var/www/html/snorby/**: snorby-start och snorby-stop.
