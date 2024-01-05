```PowerShell
pip install PyInstaller

pyinstaller --icon="icon/logo.ico" --add-data="icon;icon" ClinUI.py

Move-Item -Path "dist\ClinUI" -Destination "ClinUI"

$VERSION = "v0.0.0"
Compress-Archive -Path "ClinUI" -DestinationPath "ClinUI-win-$VERSION.zip"

rm -r build ; rm -r dist ; rm -r ClinUI ; rm ClinUI.spec
```
