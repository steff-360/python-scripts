# Merge profundo de diccionarios (sin sobrescribir niveles anidados)
def deep_merge(base: dict, override: dict) -> dict:
    result = base.copy()
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

config_base = {'db': {'host': 'localhost', 'port': 5432}, 'debug': False, 'timeout': 30}
config_env  = {'db': {'host': 'prod.db.com', 'ssl': True}, 'debug': True}
print(deep_merge(config_base, config_env))
# {'db': {'host': 'prod.db.com', 'port': 5432, 'ssl': True}, 'debug': True, 'timeout': 30}
