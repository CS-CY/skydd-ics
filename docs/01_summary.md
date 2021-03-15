# Sammanfattning

Detta dokument beskriver ett antal IT-säkerhetskomponenter, deras syfte, installation och användning. Dessa är ursprungligen anpassade för användning hos elbolag i Sverige i deras SCADA- och industriella kontrollsystemsmiljöer, men kan användas även av företag i andra samhällsviktiga branscher med liknande miljöer. Komponenterna är tänkta att fungera som byggklossar för att skapa en nivå av grundskydd. Dokumentationen är på svenska och installationen är förenklad och automatiserad. För att förenkla användningen har de olika funktionerna försetts med integrerade grafiska användargränssnitt. All dokumentation finns även tillgänglig i de installerade servrarna.

De säkerhetsfunktioner som tillhandahålls i programform är:

  * loggserver
  * larmserver
  * nätverksanalysnod
  * intrångsdetekteringssystem

Vidare finns det även dokumentation som beskriver andra säkerhetsfunktioner som inte
tillhandahålls i den här paketeringen. En sådan funktion är en brandvägg, [pfsense],
baserad på öppen källkod.

Var och en av funktionerna och verktygen finns närmare beskrivna i var sitt kapitel i dokumentet. Här beskrivs vilken funktionalitet som erbjuds, hur installation av verktygen utförs, hur verktygen används, med mera.

I kapitlet [Några kommentarer om hårdvara och hårdvarukrav] beskrivs i närmare detalj kraven på den hårdvara där verktygen kan installeras. Den hårdvara som har använts är standardkomponenter, så kallad [COTS]-utrustning, i form av servrar, nätverkskort, etc.

I kapitlet [Licensiering och tillgång till programvaran] beskrivs licenser för programvarornas användande/nyttjande och möjlighet till ändringar, för de olika modulerna som använts. Många av licenserna är så kallade öppna licenser som tillåter att vem som helst har rätt att använda programmen kostnadsfritt och ta del av källkod, göra ändringar samt även kunna vidaredistribuera programmen. Se detta kapitel eller de individuella programpaketen för specifika frågor rörande licenser.

I slutet av dokumentet finns en sammanställning av vanliga frågor och svar
(ibland kallat *FAQ, frequently asked questions*).

Som bilagor till dokumentet finns detaljbeskrivningar för hur de olika programpaketen har kompilerats, konfigurerats och ändrats för att kunna byggas i den skapade miljön.

\clearpage
