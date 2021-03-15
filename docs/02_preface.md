# Introduktion

## Förord
Skyddspaket ICD/SCADA är en samling mjukvaruverktyg som underlättar för operatörer av industriella informations- och styrsystem att ha en ändamålsenlig informationssäkerhet. Målgrupp för skyddspaketet är de operatörer som i en del av sitt kontinuerliga säkerhetsarbete behöver ett tekniskt verktyg med låg finansiell och kunskapsmässig tröskel.

Avsikten med paketet är att det ska användas som ett instegsprogram för lärande och behovsprövning hos operatörer som i en del av sitt kontinuerliga säkerhetsarbete behöver ett tekniskt verktyg med låg finansiell och kunskapsmässig tröskel. Efter utvärdering kan behovsbilden av mer potenta verktyg och eller analysstöd värderas.

Även leverantörer av programvaror eller tjänster kan använda verktygen som instegsprogram.

Programvarorna som ingår paketet baseras på öppen källkod och finns således tillgängliga för nerladdning var och en för sig. MSB står för paketering, tillgängliggörande och uppdatering och tillför ingen väsentlig funktionalitet.

Programmen/paketet levereras som det är. Det åligger den som installerar att försäkra sig om att funktion, konfiguration etc är den förväntade.

MSB avser hålla programvaran uppdaterad med nya versioner i viss omfattning. Uppdaterade versioner kan hämtas på samma sätt som ursprunglig version. Det åligger användaren att själv bedöma om uppdatering till ny version är nödvändig.

## Bakgrund
Under 2015 initierade Svenska kraftnät, inom ramen för sitt säkerhetshöjande arbete inom den svenska elbranschen, ett projekt för att skapa ett antal säkerhetskomponenter baserade på öppen källkod, alltså fria att använda utan kostnad. Primära målgruppen var svenska elbolag som av ekonomiska eller andra skäl saknar möjlighet att skaffa tekniska skyddsmekanismer. Dessa skulle då kunna skaffa sig ett grundskydd i sina ICS- och SCADA-miljöer samt få tillgång till verktyg för att enkelt och snabbt komma igång med säkerhetshöjande åtgärder.

Svenska kraftnät gav 2014 ut en vägledning om IT-säkerhetsarkitektur. I denna beskrivs ett antal säkerhetskomponenter, säkerhetskontroller och funktionaliteter som bör finnas i en IT-miljö för att hålla en viss nivå av grundskydd. Relationsdiagrammet nedan visar vad IT-säkerhetsarkitektur är för något och hur det i sin tur relaterar till, och i vissa fall styr, andra delar av IT.

Det programpaket som tagits fram – paketering av mjukvara som kan installeras på en PC-server – är tänkt att underlätta för svenska elbolag att upprätta och förvalta en IT-säkerhetsarkitektur, såsom den beskrivs i vägledningen från 2014, med fokus på säkerhetskontroller, det vill säga olika säkerhetsmekanismer och tekniska skydd.

Eftersom detta programpaket är värdefullt även för andra branscher än elbranschen har Myndigheten för samhällsskydd och beredskap (MSB) valt att ansvara för förvaltning och spridning till motsvarande målgrupper inom övriga branscher i Sverige. Målsättningen är att höja säkerhetsnivån hos de bolag som av ekonomiska eller andra skäl saknar möjlighet att på annat vis skaffa tekniska skyddsmekanismer.

![Relationsdiagram mellan olika viktiga begrepp.](images/itsecarch-metamodell.png "Relationsdiagram mellan olika viktiga begrepp.")

Detta dokument beskriver hur man installerar och använder de ingående komponenterna, samt deras syfte och funktionalitet.

## Begränsningar av garantier och ansvar
MSB påtar sig inget ansvar för eventuella skador på användarens hårdvara, mjukvara eller data som kan uppstå till följd av nedladdning, installation och användning av Skyddspaket ICS/SCADA.
Paketet levereras med de ingående delpaketen som är programvaror baserade på öppen källkod. Det åligger den som installerar att försäkra sig om att funktion, konfiguration etc. är den förväntade. Det åligger även användaren att använda de ingående komponenterna i enlighet med dessa komponenters licenser.

MSB avser hålla programvaran uppdaterad med nya versioner i viss omfattning. Uppdaterade versioner kan hämtas på samma sätt som ursprunglig version. Det åligger användaren att själv kontrollera om nya uppdateringar finns och bedöma om uppdatering till ny version är nödvändig. 

MSB tillför dokumentation och ett samlat installationsmedium. MSB tar inget ansvar för programmens kompabilitet med existerande program och system hos användaren eller mellan de ingående komponenterna i paketet. Det åligger användaren att tillse att de system, brandväggar och andra säkerhetsfunktioner som finns inte kommer i konflikt med varandra. MSB tar inget ansvar för de säkerhetsfunktioner som organisationen har i sina system eller andra funktioner som påverkas av detta direkt eller indirekt. MSB tar inget ansvar för eventuella problem som uppstår i användarens system till följd av installationsprocessen av skyddspaketet.

\clearpage
