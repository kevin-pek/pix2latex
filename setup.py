from setuptools import setup

APP = ['main.py']
DATA_FILES = [(str('models'), ['models/tokenizer.json', 'models/image_resizer.onnx', 'models/encoder.onnx', 'models/decoder.onnx'])]
OPTIONS = {
    'argv_emulation': True,
    'plist': {
        'CFBundleShortVersionString': '0.2.0',
        'LSUIElement': True,
    },
}

setup(
    app=APP,
    name='Latex OCR',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app']
)
