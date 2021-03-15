# Licensiering och tillgång till programvaran

Detta kapitel beskriver licenskrav, licensformer och andra formella saker som
behövs för att uppfylla olika krav som ställs för att kunna förpacka och
tillhandahålla dessa programpaket.

### Programpaket som inte tillåter distribution

När vi inte kunnat avgöra licensformen eller där licensformen inte tillåter direkt återdistribution av programvaran, finns textbeskrivningar i distributionen som beskriver hur en användare själv kan
hämta dessa moduler eller programpaket och installera i denna modul, vilket är
acceptabelt enligt licensmodellerna.

## Licenser

En central licens som förekommer i de flesta programpaket som ingår i denna programdistribution är Gnu Public License (GPL) version 2 samt version 3. Dessa licenser finns närmare beskrivna här: [gnulicens].

### Efterlevnad av GPL-krav

För att följa de krav som Gnu Public Licenses (GPL) och varianter därav (t.ex. LGPL)
har, främst krav på tillgänglighet av källkoden, kommer denna att göras tillgänglig för allmänheten genom distribution via publika kanaler, till exempel [GitHub](https://github.com/CS-CY/skydd-ics) och via länkar på [informationssakerhet.se](https://www.informationssakerhet.se).

## Egenutvecklad kod

Paketeringen innehåller mer än enbart programvara skapad av andra parter. De skript och de
program som vi utvecklat som en del av detta projekt är släppt under GPL-licens, vilket innebär
att vem som helst får ta del av, modifiera och vidaredistribuera källkoden så länge de vidareför dessa licenskrav
i ytterligare led mot andra personer och parter.

## Egenutvecklad dokumentation

Den dokumentation som är framtagen för detta projekt (exempelvis denna text) är fritt tillgänglig under
[Creative Commons](https://creativecommons.org/licenses/by/4.0/legalcode) Attribution 4.0 International.

Denna licens ger fria möjligheter att vidaredistribuera och att använda dokumentationen.

## Distribution

Nedan redovisas och listas olika programpaket och programdistributioner med tillhörande licenser.

### Centos Linux

CenOS och dess olika beståndsdelar består till stor del av operativsystemets kärna (Linuxkärnan), systemkommandon och verktyg, kodbibliotek, konfigurationsfiler, subsystem och applikationer. Merparten, om inte alla dessa, är licensierade under GPL. Förutom att programvarulicensen är GPL, finns följande tillägg rörande just namnet CentOS:

Från [centoslicens]

```
	You may use the Word Mark, but not the Logos, to truthfully describe
	the origin of the software that you are providing but not the software
	itself, where what you are distributing is modified official CentOS
	source code or is a build compiled from modified official CentOS
	source code.

	You may say, for example: “This software is derived from the source code
	for the CentOS distribution.” However, you may not say that the software
	is CentOS.
```
<https://www.centos.org/>


### Icinga

Larm- och övervakningsprogramvaran Icinga ingår i paketeringen. Icinga är licensierad enligt
GPL version 2.
```
	License  
	Icinga 2 and the Icinga 2 documentation are licensed under the terms
	of the GNU General Public License Version 2. You will find a copy of
	this license in the LICENSE file included in the source package.
```

För det grafiska gränssittet används icingaweb2 som även den är licenserad enligt GPL verision 2.  
<https://icinga.com/>  
<https://icinga.com/docs/icinga2/latest/#license>  
<https://github.com/Icinga/icinga2/blob/master/COPYING>
<https://github.com/Icinga/icingaweb2/blob/master/COPYING>

### Snort
Snort ägs av Cisco och består av två huvudkomponenter. Dessa är detekteringsprogramvaran och en uppsättning regler. Reglerna är uppdelade i *Community Snort Rules* och *Proprietary Snort Rules*.  
Detekteringsprogramvaran och *Community Snort Rules* är [GPL]-licensierad enligt version 2. *Proprietary Snort Rules* är inte inkluderade i denna paketering då de lyder under en annan licensmodell som bland annat kräver användarregistrering.  
<https://www.snort.org/>  
<https://www.snort.org/license>  
<https://www.snort.org/downloads/#rule-downloads>

### Quickdraw
Quickdraw är en samling protokollbeskrivningar, regler och IDS/IPS-specifika beskrivningar av ICS/SCADA-protokoll.
Samlingen är framtagen av företaget DigitalBond och är släppt under så kallad MIT-licens, vilket ger stora friheter
att använda, ändra och vidaredistribuera reglerna. För mer detaljerad information, se [quickdrawlicense].
```
	The MIT License (MIT)

	Copyright (c) 2015 Digital Bond

	Permission is hereby granted, free of charge, to any person obtaining a copy
	of this software and associated documentation files (the "Software"), to deal
	in the Software without restriction, including without limitation the rights
	to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
	copies of the Software, and to permit persons to whom the Software is
	furnished to do so, subject to the following conditions:

	The above copyright notice and this permission notice shall be included in all
	copies or substantial portions of the Software.

	THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
	IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
	FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
	AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
	LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
	OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
	SOFTWARE.
```
https://github.com/digitalbond/Quickdraw-Snort  
https://github.com/digitalbond/Quickdraw-Snort/blob/master/LICENSE

### Snorby

Programvaran *Snorby* som ingår som en komponent i IDS-lösningen Snort är licensierad enligt GPL version 3.
Det medför därmed inga problem att vidaredistribuera snorbykomponenten i plattformen.  
För mer information, se [snorbylicens].

```
	Snorby - All About Simplicity.

	Copyright (c) 2013 Threat Stack, Inc (support@threatstack.com)

	Snorby is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	Snorby is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with Snorby.  If not, see <http://www.gnu.org/licenses/>.

	Neither the names of Licensor, nor the names of any contributors to
	the Original Work, nor any of their trademarks or service marks, may
	be used to endorse or promote products derived from this Original Work
	without express prior permission of the Licensor. No license is granted
	to the trademarks of Licensor even if such marks are included in the
	Original Work.

	The above copyright notice and this permission notice shall be included
	in all copies or substantial portions of the Software. Not limited to but
	including the Software's footer, Web URL and Author Names.

	**Notice**
	The snorby source code is 100% free and open source however we use highcharts
	for metrics and reporting. Please make sure you review the
	[highcharts](http://www.highcharts.com) licensing in detail
	[here](http://www.highcharts.com/license). The license above
	only applies to snorby source code (contact the Dustin Willis
	Webber if you have futher questions).
```
<https://github.com/Snorby/snorby>  
<https://github.com/Snorby/snorby/blob/master/LICENSE>

**Highcharts**  
Snorby innehåller en komponent kallad "highcharts" från Highsoft som är licensierad enligt Creative Common
Attribution Non-commercial för redistribution i icke vinstdrivande syfte. För mer information, se [CCBYNC3].  

**När kan jag använda den icke kommersiella licensen?**  
Den icke kommersiella licensen är tillgänglig för:

  * statligt finansierade skolor
  * universitet
  * icke vinstdrivande organisationer
  * studenter
  * individer som använder mjukvaran för personligt bruk, testning och demonstration  

Denna licens inkluderar inte kommersiellt bruk av Highsoft-mjukvaran för ovannämnda aktörer.  
Highsofts mjukvara är inte avgiftsfri för kommersiell användning eller användning i statlig verksamhet.

Läs mer om licenser för highcharts för att ta reda på vilken licensform som gäller för dig:  
<https://shop.highsoft.com/highcharts>  
<https://www.highcharts.com/license>  
<https://shop.highsoft.com/faq>  

Om det är så att du behöver köpa en licens men av någon anledning inte har möjlighet till det går det att antingen deaktivera highcharts eller deaktivera Snorby. Se avsnittet [Viktigt att veta om Snorby och Highcharts] i kapitlet [IDS server] i dokumentationen för hur det går till.

### Barnyard

Programvaran Barnyard som ingår som en komponent i IDS-lösningen Snort är licensierad enligt GPL2.
Det medför därmed inga problem att vidaredistribuera Barnyardkomponenten i plattformen.

För mer information, se [barnyardlicens].  
<https://github.com/firnsy/barnyard2>
<https://github.com/firnsy/barnyard2/blob/master/LICENSE>

### Tcpdump

Vi har använt oss av programvaran tcpdump för att kunna spela in nätverkstrafik.
Tcpdump använder sig av en så kallad *3-clause BSD license*, vilket är en väldigt
öppen och flexibel mjukvarulicens.

För detaljinformation om programvarans licensbestämmelser, se [tcpdumplicens].  
<http://www.tcpdump.org/>  
<http://www.tcpdump.org/license.html>  

### OSA ikoner

Flera av diagrammen i dokumentationen använder sig av ikoner från OSA [Icon Library](https://www.opensecurityarchitecture.org/cms/library/icon-library). OSA tillhandahåller ikonerna och övrigt material på <https://www.opensecurityarchitecture.org> enligt 	[Creative Commons](https://creativecommons.org/licenses/by-sa/3.0/) share-alike.
För mer information se [OSA-licens](https://www.opensecurityarchitecture.org/cms/about/license-terms).

\clearpage
