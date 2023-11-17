from rapid_latex_ocr import LatexOCR
import tempfile

image_resizer_path = 'models/image_resizer.onnx'
encoder_path = 'models/encoder.onnx'
decoder_path = 'models/decoder.onnx'
tokenizer_json = 'models/tokenizer.json'

def run_latex_ocr(image_data):
    model = LatexOCR(image_resizer_path=image_resizer_path,
                encoder_path=encoder_path,
                decoder_path=decoder_path,
                tokenizer_json=tokenizer_json)
    # Convert image data to an image file
    with tempfile.NamedTemporaryFile(delete=False) as tmpfile:
        tmpfile.write(image_data)
        tmpfilepath = tmpfile.name

    with open(tmpfilepath, "rb") as f:
        data = f.read()
    result, elapse = model(data)
    return result