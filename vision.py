from Vision import VNImageRequestHandler, VNRecognizeTextRequest

def run_vision_ocr(image_data):
    # Create a VNImageRequestHandler with the image data
    handler = VNImageRequestHandler.alloc().initWithData_options_(image_data, {})

    # Create a text recognition request
    request = VNRecognizeTextRequest.alloc().init()
    
    # Process the request
    error = None
    success = handler.performRequests_error_([request], error)
    if not success:
        print(f"Failed to perform OCR: {error}")
        return

    # Get the recognized text from the request results
    recognized_text = []
    for result in request.results():
        for textObservation in result.topCandidates_(1):
            recognized_text.append(textObservation.string())
    print('\n'.join(recognized_text))
    return '\n'.join(recognized_text)