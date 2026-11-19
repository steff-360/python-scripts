"""
Herramientas para consumir APIs REST.
- GET con manejo de errores y reintentos
- POST con autenticacion por token
- Paginacion automatica
"""

import time
import requests
from typing import Any


def get_with_retry(url: str, headers: dict = None, max_retries: int = 3, delay: float = 1.0) -> dict:
    """Realiza un GET con reintentos automaticos en caso de fallo."""
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            if attempt == max_retries - 1:
                raise
            print(f'Intento {attempt + 1} fallido: {e}. Reintentando...')
            time.sleep(delay * (attempt + 1))


def paginated_get(base_url: str, headers: dict = None, page_param: str = 'page') -> list[Any]:
    """Obtiene todos los resultados de un endpoint paginado."""
    results = []
    page = 1

    while True:
        url = f'{base_url}?{page_param}={page}&per_page=100'
        data = get_with_retry(url, headers=headers)

        if not data:
            break

        if isinstance(data, list):
            results.extend(data)
            if len(data) < 100:
                break
        else:
            results.append(data)
            break

        page += 1

    return results


if __name__ == '__main__':
    # Ejemplo: obtener repos publicos de un usuario de GitHub
    headers = {'Accept': 'application/vnd.github.v3+json'}
    repos = paginated_get('https://api.github.com/users/steff-360/repos', headers=headers)
    for repo in repos:
        print(f"{repo['name']} - Stars: {repo['stargazers_count']}")
