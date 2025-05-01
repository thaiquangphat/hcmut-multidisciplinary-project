from adafruit import pushing_command

def detect_and_push(prediction):
    """Handle the prediction and push to Adafruit."""
    try:
        if prediction == 'none':
            return 'none'
        
        adadevice, command = prediction.split('_')
        value = command.upper()

        return pushing_command(adadevice, value)
    except Exception as e:
        print(f"Error in detect_and_push: {e}")
        raise 