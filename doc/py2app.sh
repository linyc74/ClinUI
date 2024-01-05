VERSION=v0.0.0 &&
py2applet \
  --packages=cffi \
  --iconfile=./icon/logo.ico \
  --make-setup ./ClinUI.py &&
python setup.py py2app &&
cp ./lib/libffi.8.dylib ./dist/ClinUI.app/Contents/Frameworks/ &&
mv ./dist/ClinUI.app ./ &&
zip -r ClinUI-mac-${VERSION}.zip ClinUI.app &&
rm -r build dist setup.py ClinUI.app
