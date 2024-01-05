```PowerShell
pip install PyInstaller

pyinstaller --icon="icon/logo.ico" --add-data="icon;icon" ClinUI.py --name=ClinUI-win-v0.0.0

rm -r build
rm *.spec
```
