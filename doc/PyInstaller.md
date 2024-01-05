```PowerShell
pip install PyInstaller

pyinstaller --icon="icon/logo.ico" --add-data="icon;icon" ClinUI.py

rm -r build
rm *.spec
```
