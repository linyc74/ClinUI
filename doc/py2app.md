Install `py2app`.

```zsh
pip install py2app
```

Create `setup.py`.
`py2app` does not handle dependency very well.
The `cffi` python package needs to be added manually.

```zsh
py2applet \
  --packages=cffi \
  --iconfile=./icon/logo.ico \
  --make-setup ./ClinUI.py
```

Build the app.

```zsh
python setup.py py2app
```

This x86_64 version of `libffi.8.dylib` was acquired from Anaconda.
It needs to be copied to the app bundle.

```zsh
cp ./lib/libffi.8.dylib ./dist/ClinUI.app/Contents/Frameworks/
```

Run the app from the command line. It can also be run by double clicking the app.

```zsh
dist/ClinUI.app/Contents/MacOS/ClinUI
```

Zip the app.

```zsh
mv ./dist/ClinUI.app ./ && zip -r ClinUI-mac-v0.0.0.zip ClinUI.app
```

Remove unused build files.

```zsh
rm -r build
rm -r dist
rm setup.py
```


