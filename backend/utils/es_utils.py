from elasticsearch import AsyncElasticsearch

from backend.config import ES_HOST, ES_PORT


def get_es_client():
    return AsyncElasticsearch(f'http://{ES_HOST}:{ES_PORT}/')
