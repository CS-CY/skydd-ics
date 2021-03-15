# Några kommentarer om hårdvara och hårdvarukrav

Detta kapitel beskriver kort några av de förutsättningar som krävs för att kunna använda funktionerna och att sätta upp servrar.

En av tankarna är att man ska kunna installera programmen på såväl gammal utrustning som på nyköpt. Det ska fungera lika bra att kunna bygga en budgetlösning med sina gamla datorer som att införskaffa nya servrar.

## Hårdvaruarkitektur

För de hårdvaruarkitekturer vi stödjer (Intel, AMD) finns det ett antal grundläggande hårdvarukrav rörande prestanda, storlek med mera framtagna. Dessa egenskaper, miniminivåer samt rekommenderade nivåer finns  närmare beskrivna i detta dokument.

Som regel är dock den hårdvara som är tänkt målmiljö en Intelbaserad dator av PC-typ av modernt snitt. Mer information om arkitekturkrav beskrivs i följande kapitel.

## Fysisk eller virtuell hårdvara
Programvarudistributionen har installerats och testats på både virtuell och fysisk hårdvara.

Många av de paket och funktioner som levereras i detta installationspaket har funktioner, till exempel nätverksinspelningsfunktion, som fungerar bäst på fysisk hårdvara eftersom de kräver åtkomst till Ethernet-portar på ett sådant sätt som kan vara problematiskt i en virtuell miljö.

En del andra funktioner och uppsättningarna av programvarudistributionen, såsom enkel loggserver, fungerar lika bra på virtuell som fysisk hårdvara.

## 32- och 64-bitars hårdvara

Intel har haft 64-bitarsversioner av sina CPU:er sedan i början av 2000 (2003 närmare bestämt). Likaså finns det 32-bitars och 64-bitarsversioner av det operativsystem, [Linux](http://www.linux.org/), som vi har valt att använda i projektet. Modern hård- och mjukvara är bättre anpassad till att använda 64-bitarsversionerna. Vi har också valt att dra en gräns för hur gammal hårdvara vi kan stödja. Därför har vi valt att bara skapa 64-bitarsversioner av de programpaket som vi tagit fram.

## Primärminnesutrymme

De paketerade systemen kräver 1GB RAM-minne för att fungera. Mer minne är dock att rekommendera, gärna 4 eller 8GB.

## Lagringsutrymme
Det går att installera systemet på så små diskar som 20GB men eftersom de flesta system bygger på
att samla in data är det rekommenderat att ha betydligt mycket mer i lagringsutrymme. Vilken storlek som behövs avgörs av hur mycket data det är tänkt att samla in i de olika systemen.

## CD och DVD eller USB-masslagring
Det går att används såväl DVD och USB-minnen för att skapa en installationsdisk. Denna installationsdisk används sedan för att installera
systemet på en hårddisk för permanent användning av programvaran. För installation på en virtuell dator går det bra att använda
ISO-filen direkt i det virtualiseringsprogram som används.

## Nätverksanslutning

Alla komponenter (loggserver, IDS-server, larmserver, nätverksinspelningsserver, brandvägg) kräver
nätverksanslutningar för att vara användbara i verkliga scenarion, detta eftersom de oftast har ett behov
av att inhämta trafik eller få saker skickade till sig via nätverket.

Testerna har utförts med virtuell och fysisk hårdvara där Ethernetkort har använts. Testerna gjordes mot Ethernetkopplingar med 10Mbit- och 100Mbit-anslutningar.

\clearpage
