# Verifiera media

All data som laddas ner från en obetrodd källa bör verifieras för att få en garanti på att det är korrekt version som har laddats ner. Ibland går det att ladda ner kod över [TLS] vilket ger en garanti på att det som laddas ner verkligen kommer från rätt källa. I många fall laddas programvara ner över klartext-protokoll och då finns en risk att det nedladdade blir manipulerat. För att undvika det använder många [TLS] på den sida där de presenterar data och där visar de även en eller flera kryptografiska checksummor som sedan kan verifieras när själva filen har laddats ner från exempelvis ett öppet bibliotek som hanterar lagring och bandbreddstillgången.

#### Verifiera i Linux
Öppna en terminal och skriv kommandona:

1. ```sha256sum pfSense-LiveCD-2.2.5-RELEASE-amd64.iso.gz```
2. ```cat pfSense-LiveCD-2.2.5-RELEASE-amd64.iso.gz.sha256```

Säkerställ att resultatet i de båda kommandona har samma långa textsträng.

![Verifiera SHA256 i Linux.](images/verify_sha_linux.png "Verifiera SHA256 i Linux.")

#### Verifiera i Mac OS X
Öppna en terminal och skriv kommandona:

1. ```shasum -a 256 pfSense-LiveCD-2.2.5-RELEASE-amd64.iso.gz```
2. ```cat pfSense-LiveCD-2.2.5-RELEASE-amd64.iso.gz.sha256```

Säkerställ att resultatet i de båda kommandona har samma långa textsträng.

![Verifiera SHA256 i OS X.](images/verify_sha_osx.png "Verifiera SHA256 i OS X.")

#### Verifiera i Windows
Windows har tyvärr inte som standard lika enkla sätt för att verifiera kryptografiska checksummor som Mac OS X och Linux. För att verifiera i Windows måste du först ladda ned programvara för checksummeuträkning.

1. Ladda ner [Get-FileHash.ps1] från Microsoft.
2. Starta en kommandotolk.
  a. Välj start / kör
  b. Skriv ```cmd``` och tryck enter/retur. Då öppnas en kommandotolk där skriver du följande:
3. ```powershell -ExecutionPolicy Bypass```
4. ```..\\Get-FileHash.ps1```
5. ```Get-FileHash -Path filsökväg -Algorithm SHA256 | Format-List```
6. Jämför checksumman i resultat med den som nedladdningssidan visar.

![Verifiera SHA256 i Windows.](images/verify_sha_win.png "Verifiera SHA256 i Windows.")
