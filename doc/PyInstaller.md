Install PyInstaller

```PowerShell
pip install PyInstaller
```

Package as a .exe file

```PowerShell
$VERSION = "v0.0.0"
pyinstaller --clean --onefile --icon="icon/logo.ico" --add-data="icon;icon" ClinUI.py
Move-Item -Path "dist\ClinUI.exe" -Destination "ClinUI-win-$VERSION.exe"
rm -r build ; rm -r dist ; rm ClinUI.spec
```

Package as a folder

```PowerShell
$VERSION = "v0.0.0"
pyinstaller --clean --icon="icon/logo.ico" --add-data="icon;icon" ClinUI.py
Move-Item -Path "dist\ClinUI.exe" -Destination "ClinUI.exe"
Compress-Archive -Path "ClinUI" -DestinationPath "ClinUI-win-$VERSION.zip"
rm -r build ; rm -r dist ; rm -r ClinUI ; rm ClinUI.spec
```
