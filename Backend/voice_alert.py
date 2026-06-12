import threading
import os
import time

# GLOBAL FLAG

is_speaking = False

# INTERNAL VOICE FUNCTION

def run_voice(message):

    global is_speaking

    # PREVENT MULTIPLE VOICES

    if is_speaking:

        return

    is_speaking = True

    try:

        # REPEAT ALERT 3 TIMES

        for i in range(3):

            os.system(

                f'say "{message}"'
            )

            time.sleep(1)

    except Exception as e:

        print(

            "Voice Error:",

            e
        )

    finally:

        is_speaking = False

# MAIN FUNCTION

def speak_alert(message):

    thread = threading.Thread(

        target=run_voice,

        args=(message,)
    )

    thread.daemon = True

    thread.start()