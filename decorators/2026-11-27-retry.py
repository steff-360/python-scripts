# Decorator: reintentar una funcion N veces ante excepciones
import time, functools

def retry(max_attempts=3, delay=1.0, exceptions=(Exception,)):
    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except exceptions as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Intento {attempt} fallido: {e}. Reintentando en {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=0.5)
def unstable_request():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Timeout")
    return "OK"
