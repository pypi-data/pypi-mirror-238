import signal
import logging

shutdown_requested = False

def signal_handler(signum, frame):
    logging.info(f"Signal handler called with signal {signum}")
    global shutdown_requested
    shutdown_requested = True

def get_shutdown_requested():
    return shutdown_requested


signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGINT, signal_handler)