# Installation

Detta kapitel beskriver närmare hur man installerar och sätter upp en server utifrån den programvara som skapats i projektet.

Det finns olika sätt för att installera en av de olika typer av servrar som finns tillgängliga. Antingen laddar du ner skivavbildningen, [ISO]-filen,
av installationsmediet från en distributionsserver eller, om du är en avancerad användare, så bygger du en egen avbild från källkoden som också distribueras. Detta gäller som regel, men med ett undantag. Brandväggen som använts inom projektet ingår inte i paketeringen, utan den kan istället laddas ner från brandväggsprojektet pfsense egen webbplats.

## Installera en server

Nedanstående flödesdiagram visar grafiskt översiktligt de olika stegen som behövs för att hämta programvaran, utföra de olika momenten för att installera och konfigurerar servern samt börja använda den. Vi har i själva paketeringen förenklat och automatiserat för att så få steg som möjligt skall behövas för att komma igång.

![Flödesdiagram för att installera och använda programvaran](images/install_flow.png "Flödesdiagram för att installera och använda programvaran.")

Första steget med att installera en server är att ha tillgång till själva installationsfilen, vanligtvis en så kallad [ISO]-fil.
Information om var och hur installations-filen kan hämtas finns på <https://www.informationssakerhet.se>.  

För att installera en server måste datorn startas upp från antingen DVD:n eller USB-stickan. Om du inte använder en fysisk server kan det räcka med alternativet att direkt starta den virtuella servern från ISO-filen.

Om du behöver omvandla den hämtade filen till en USB-sticka eller en DVD-skiva, varifrån installationen görs,
följ instruktionerna för det som finns i kapitlet [Skapa installationsmedia].

För att starta datorn från det valda mediet kan det räcka med att starta den direkt med mediet istoppat i CD/DVD-läsaren eller i USB-anslutningen. Om du stöter på problem, kan det bero på en mängd olika saker, exempelvis att

* datorn du försöker installera på är inställd att inte stödja att starta ifrån annat än hårddisken
* datorn inte vill starta från ett osäkert lagringsmedia.

Sådana här inställningar kan justeras så att systemet i stället startas från den nya temporära startdisken. Ibland kan man behöva konfigurera datorns inställningar för BIOS eller UEFI. Hur detta görs skiljer sig från tillverkare till tillverkare och datorserie till datorserie. Se instruktioner från aktuell leverantör av datorn hur detta ska göras.

### Installationsförfarande

OBS! I nedanstående beskrivning är det enbart hårddiskinställningarna som *måste* sättas upp i första steget. Övriga inställningar går att ändra senare.

Vid uppstart från mediet kommer en meny att visas med de olika installationstyperna enligt bilden nedan.

![Uppstartsmeny vid installationsstart](images/installation_val_av_server.png "Uppstartsmeny vid installationsstart.")  

  1. Med tangentbordets piltangenter går det att stega till den servertyp som ska installeras.

  2. Efter att vald servertyp är markerad, tryck på knappen *enter/return*.

Datorn kommer nu att ladda installationen och efter en liten stund kommer nedanstående meny att visas där installationsspecifika val kan göras.

![Konfigurationsval under installationen, övre delen](images/installation_val_av_sprak.png "Konfigurationsval under installationen, övre delen.")

  3. Under rubriken **LOKALISERING** är svenska förvalt, men det är möjligt att ändra till ett annat språk om så önskas.  

  4. Under rubriken **PROGRAMVARA** är det också förvalt, dessa val ska **inte** ändras.

Beroende på den aktuella datorn och skärmens upplösning som används kan hela bilden visas eller vara *rullbar*.

  5. Längst ner finns rubriken **SYSTEM** och där **måste** val göras för att installationen ska kunna fortsätta.

![Konfigurationsval under installationen, undre delen](images/installation_val_av_disk_nat.png "Konfigurationsval under installationen, undre delen.")

Som bilden visar, är alternativet "installationsmål" markerat med ett utropstecken och en text om att de förinställda parametrarna som satts för installationen i övrigt inte gäller för detta alternativ. Installationsmålet är den eller de hårddiskar som ska användas som system- och startdisk när systemet väl installerats klart. För dessa hårddiskar måste du manuellt gå in i installationsverktyget och ändra vissa inställningar för hur du vill använda disken.

*OBS. Vi har valt detta alternativ - att installationen stannar och ber om manuella handgrepp av två orsaker. 1. För att ge användaren en chans att bestämma hur systemets diskar ska vara uppsatta. 2. För att ge användaren en chans att ångra sig ifall det visar sig att något fel uppstått, exempelvis att installationen håller på att utföras på fel dator eller mot fel disk.*

  6. Klicka på **INSTALLATIONSMÅL**. Menyn i bilden nedan kommer då att visas.  

![Val av hårddisk som installation ska ske på](images/installation_val_av_disk.png "Val av hårddisk som installation ska ske på.")

  7. Välj *den hårddisk* som installationen ska ske på. I exemplet på bilden så finns det en hårddisk i en virtuell dator som är vald.  

  8. Välj *klar* uppe i högra hörnet om partitioneringen ska ske automatiskt.  

För en mer avancerad installation kan en manuell partitionering vara ett bättre alternativ. Dock är det konfigurationsvalet utanför vad som beskrivs i den här installationsguiden.

CentOS beskriver mer i sin dokumentation under kapitlet [Partitionering] hur det kan ske. Genom att exempelvis ha en egen partition för /var/log går det att få ett skydd mot att loggar fyller hela disken med effekten att systemet blir instabilt, i synnerhet för logservern.

  9. Om hårddisken inte är tom måste det bekräftas att all data skrivs över genom att klicka på knappen *Återvinn utrymme*. Om det görs kommer tidigare data att skrivas över och den informationen kommer inte att kunna återskapas

![Radera hårddiskutrymme](images/installation_val_av_disk_bekrafta.png "Radera hårddiskutrymme.")

Efter att du valt återvinn utrymme kommer det dyka upp ytterligare en dialogruta, som ser ut som nedanstående exempelbild.

![Töm hårddisken](images/installation_val_av_disk_radera.png "Töm hårddisken.")

  10. I denna meny välj *Delete all* för att kunna göra en ny installation på hårddisken.

  11. Välj sedan *Reclaim space*.

Nu är valet för att sätta upp hårddisken för installation klar. Du kommer därefter tillbaka till huvudmenyn.

Väl tillbaka i den första menyn måste även nätverksinställningar ställas in innan installationen kan påbörjas.

  12. Välj menyn **NÄTVERK & VÄRDNAMN**.

![Nätverkskonfiguration](images/installation_val_av_nat.png "Nätverkskonfiguration.")

  13. I den här menyn måste nätverkskortet aktiveras genom att du klickar på *av*-knappen. Nätverkskortet blir nu aktiverat men IP-adressen måste också konfigureras.

*OBS! Den här menysidan kan se annorlunda ut än den förevisade bilden, främst om ett nätverkskort saknas i datorn eller om en nätverkssladd inte är ansluten. Om den är annorlunda, felsök för att hitta felet så att du kan avsluta nätverksinställningarna.*

  14. Om datorn tillhör en specifik domän ska du skriva domännamnet tillsammans med datorns egna namn i rutan **Värdnamn**.

  15. Klicka på knappen **Konfigurera** för att konfigurera IP-adresser.

En meny kommer fram där det finns flera flikar att välja på beroende på vilken konfiguration som behöver utföras för att servern ska fungera i det nätverket där den ska användas.

  16. I fliken **Inställning för IPv4** går det att sätta IPv4 adresser. Om du ska använda DHCP kan du låta programmet göra inställningen automatiskt vilket är det förvalda alternativet. Om i stället en fast IP-adress ska användas ska metod ändras till *Manuell* enligt bilden nedan, en del installationstyper kräver att det åtminstone är konfigurerat med en så kallad link-local-adress.

![IP konfiguration.](images/installation_val_av_nat_ipv4.png "IP konfiguration.")

I tabellen **Adresser** ska du skriva in information om IP-adressen enligt följande:  

A. **Adress** sätts till den IP-adress som ska användas.  
B. **Nätmask** sätts till den nätmask som ska användas i det aktuella nätverket.  
C. **Gateway** sätts till den *gateway/default route* som behövs om kommunikation ska ske till andra IP-nätverk än det lokala för den aktuella nätmasken.

Om DNS används skrivs namnservrarnas IP-adresser in i rutan **DNS-servrar**.  
När alla val är klara avslutar du med att klicka på **Spara**-knappen.

  17. I fliken **Allmänt** kan du välja om den aktuella konfigurationen ska vara aktiverad efter uppstart. Klicka därefter på knappen **Spara**.

Markera checkrutan som heter *Anslut automatiskt till detta nätverk när det är tillgängligt* enligt bilden nedan om du vill att konfigurationen som är satt ska vara aktiv när datorn startar.

![IP-konfiguration.](images/installation_val_av_nat_ipv4_enable.png "Aktivera IP konfiguration.")

Om den aktuella datorn har flera nätverkskort behöver du konfigurera alla nätverkskort om all nätverksfunktionalitet ska vara aktiverad vid uppstart.

När alla val för IP-konfigurationen är klara avslutar du konfigurationen genom att klicka på knappen KLAR i övre högra hörnet.

Nu är alla val gjorda och installationen kan påbörjas.  

**OM DET FINNS NÅGON DATA LAGRAD PÅ HÅRDDISKEN SOM ÄR VALD FÖR INSTALLATIONEN KOMMER DEN ATT SKRIVAS ÖVER OCH DET ÄR INTE MÖJLIGT ATT ÅNGRA ELLER ÅTERSKAPA DEN.**

Klicka på **Starta installationen** för att installera den valda servern.

Installationen kommer nu att starta och en ny meny kommer att visas enligt bilden nedan.

![Installationsförfarandet.](images/installation_val_av_paborjad.png "Installationsförfarandet.")

Det finns två menyval i den här vyn och den ena knappen för ROOT-lösenord går det inte att trycka på.  
Det är knappen för att sätta root-lösenordet, det vill säga lösenordet för att få högsta behörighet på servern. Lösenordet är en slumpmässig sträng på 32 tecken. För att få högre behörighet eller ändra root-lösenordet kan kommandot *sudo* användas enligt de instruktioner som beskriver hur terminalen fungerar efter att installationen är slutförd.  

Det andra menyvalet är till för att skapa användarkonton, det ska **inte** göras i det här skedet utan görs efter att installationen är slutförd. 

Nu är det bara att vänta på att installationen slutförs. När den är klar kommer servern att startas om. Säkerställ att datorn startar från hårddisken och inte installationsmediet.

När datorn har startat om kommer den att visa några grafiska fönster där du måste göra de sista valen. Det första som ska göras är att lägga till ett adminstratörskontot. Klicka på **USER CREATION**

![Skapa konto.](images/installation_post_first.png "Skapa konto.")

Nu är det dags att skapa ett användarkonto för att kunna använda servern.  

![Kontokonfiguration.](images/installation_post_konto.png "Kontokonfiguration.")

Fyll i samtliga rutor för att skapa ett konto och tillhörande lösenord.

  * **Full name** är det beskrivande namnet för konto som skapas
  * **User name** är det namnet som används vid inloggning till servern.
  * **Checkbox** *Make this user administrator* ska vara ibockad för att ge första användaren administrativa rättigheter. Denna användaren kan då även skapa ytterliggare konton.
  * **Checkbox** *Require a password to use this account* ska vara ibockad för att tvinga fram att lösenord används.
  * **Password** är det lösenordet som används för att logga in med det valda användarnamnet. Lösenordet ska vara avancerat och slumpat så att ingen obehörig kan gissa sig till det eller vare sig manuellt eller maskinellt kunna pröva sig fram till korrekt lösenord.
  * **Confirm password** Här ska du fylla i samma lösenord som du matade in i *Lösenordsrutan* för att säkerställa att det valda lösenordet inte har stavats fel.

Klicka på **Klar** i övre högra hörnet för att fortsätta.

När kontot är skapat är det bara att klicka på **SLUTFÖR KONFIGURATIONEN**.

I detta läge går det nu att logga in med användarnamnet och lösenordet som sattes i det tidigare steget.

En välkomstmeny kommer att komma fram enligt bilden nedan.  

![Val av språk.](images/installation_post_sprak.png "Val av språk.")

I det första steget kan språkvalet än en gång konfigureras, svenska är förvalt och det går bra att klicka på **Nästa** för att fortsätta.

I denna meny går det också att välja tangentbordstyp.

![Val av tangentbord.](images/installation_post_tangentbord.png "Val av tangentbord.")

Svenskt [qwerty]-tangentbord är förvalt och det går bra att klicka på **Nästa** för att fortsätta.  

  
![Val av sekretess.](images/installation_post_platstjanster.png "Val av sekretess.")

Platstjänster är förvalt och bör avaktivers då inga installationer kräver denna funktion. Klicka på **PÅ**-knappen för att stänga av funktionen.

![Molntjänster.](images/installation_post_moln.png "Molntjänster.")

Här behövs inga molntjänster och det går bra att klicka på **Hoppa över**.

Installationen är nu klar.

![Slutför konfigurationen.](images/installation_post_klar.png "Slutför konfigurationen.")

Starta den aktuella server, som nu är färdiginstallerad, genom att klicka på knappen **Börja använda CentOS Linux**.  

Nu är allt klart och det går att börja använda eller ytterligare konfigurera den aktuella serverinstallationen enligt vidare instruktioner för aktuell installation.
Den användare som skapades är redan inloggad.

## Avancerad säkerhetskonfiguration
Samtliga installationier bygger på Linux och det är möjligt att konfigurera operativsystemet för att utöka säkerheten ytterliggare genom olika typer av härdningar. Flera av de olika teknikerna som kan göras finns inte med som standard i installationen då dessa ofta har beroenden på miljön där servern ska placeras.

Det går exempelvis att ändra kärnparametrar(eng. kernel parameters) för att begränsa olika funktioner. För att undvika olika typer av nätverksattacker genom s.k. spoofing kan även systemets ARP-tabell hårdkodas för att säkerställa att korrekt server kommunicerar med den aktuella installationen.

Om inte IPv4 och IPv6 ska användas bör endast det aktuella protokollet vara aktivt.

\clearpage
