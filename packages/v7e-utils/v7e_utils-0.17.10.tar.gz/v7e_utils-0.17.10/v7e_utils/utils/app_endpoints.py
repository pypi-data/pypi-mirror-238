from django.urls import URLPattern, URLResolver
from django.urls import get_resolver
from typing import List, Generator


def list_urls(list:List[URLResolver|URLPattern], base_path:str='')->Generator[str, Generator, Generator]:
    """
        Construye los endpoins a partir de las URLResolver y URLPattern de Django.

        Args:
            list (List[URLResolver|URLPattern]): Lista de URLResolver o URLPattern de Django.
            base_path (str): Path base de los endpoints.

        Returns:
           Generator : Funcion generadora con los endpoints construidos.
    """
    if not list:
        return
    l = list[0]
    str_pattern = str(l.pattern)
    match_pattern = not str_pattern.endswith('/(?P<pk>[^/.]+)/$') and \
                    (str_pattern.endswith('/$') or str_pattern.endswith('/'))
    if isinstance(l, URLPattern) and match_pattern:
        # l.callback tiene el view
        str_pattern = str_pattern.replace('^', '').replace('/$', '/').replace('(?P<pk>[/.]+)', '<pk>')
        yield f"/{base_path}{str_pattern}"
    elif isinstance(l, URLResolver):
        yield from list_urls(l.url_patterns, f"{base_path}{str(l.pattern)}")
    yield from list_urls(list[1:], base_path)


def list_urlresolver(list:List[URLResolver|URLPattern])->Generator[None, str, Generator]:
    """
        Obtiene los URLResolver que pertenezcan a las apps del proyecto.

        Args:
            list (List[URLResolver|URLPattern]): Lista de URLResolver de Django.

        Returns:
            Generator : Funcion generadora con los URLResolver.
    """
    if not list:
        return
    r = list[0]
    if isinstance(r, URLResolver) and '.api.urls' in str(r.urlconf_module):
        yield r
    yield from list_urlresolver(list[1:])


def get_endpoints(exclude:List[str]=[])->List[str]:
    """
        Obtiene una lista de los endpoints pertenecientes a las aplicaciones del proyecto.

        Args:
            exclude (List[str]): Lista de endpoits a descartar para el resultado.

        Returns:
            list[str]: La lista de los endpoints pertenecientes a las aplicaciones del proyecto.
    """
    urls_resolve = list(list_urlresolver(get_resolver().url_patterns))
    endpoints = list(list_urls(urls_resolve))
    if exclude:
        for endpoint in exclude:
            endpoint = endpoint.replace(' ', '')
            if endpoint in endpoints:
                endpoints.remove(endpoint)
    return endpoints