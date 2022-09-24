import requests
import joblib
import asyncio
import httpx  # Replacement library that enables Async requests
import json

class APIStuff(object):

    def __init__(self, logger):
        self.endpoint = None
        self.params = None
        self.pagination = False
        self.method = None  # Options should be parralel, async or sync
        self.logger = logger

    def get_data_form_API(self,
                          endpoint: str,
                          method: str,
                          pagination: bool = False,
                          params: dict = None
                          ):
        """
        This class manages the session in which the requests are handled
        :param endpoint: str
        :param method: str
        :param pagination: bool
        :param params: additional params that can be parsed, is not yet implemented
        :return: results in the form of actual content. Request information like callback status codes are not parsed.
        """
        assert method in ['parallel', 'async',
                          'sync'], "please use the methods 'parallel', 'async' or 'sync' in accordance to your preference"
        self.endpoint = endpoint
        self.params = params
        self.pagination = pagination
        self.method = method

        if self.pagination == True:
            self._make_pages()
            self.logger.info('Pagination Requested: Created pages')

        if self.method == None:
            self.logger.warning("Please initialise class before using method")
        elif self.method == "parallel":
            self.logger.info("Using parallel method")
            results = self._do_parallel()
            yield results
        elif self.method == "sync":
            self.logger.info("Using sync method")
            results = self._do_sync()
            yield results
        elif self.method == "async":
            self.logger.info("Using async method")
            results = asyncio.run(self._do_async())
            yield results

    def _do_sync(self):
        if self.pagination:
            results = []
            for page in self.pages:
                response = requests.get(self.endpoint)
                results.append(response.text)
        else:
            response = requests.get(self.endpoint)
            self.logger.info(f'the response code was: {response.status_code}')
            results = response.content
        return results

    def _do_parallel(self):
        if self.pagination:
            with joblib.parallel_backend('loky'):
                jobs = joblib.Parallel(n_jobs=-1)(
                    joblib.delayed(requests.get)(page)
                    for page in self.pages)
                results = [job.content for job in jobs]
        else:
            response = requests.get(self.endpoint)
            self.logger.info(f'the response code was: {response.status_code}')
            results = response.content
        return results

    async def _do_async(self):
        if self.pagination:
            async with httpx.AsyncClient() as client:
                jobs = (client.get(page) for page in self.pages)
                results = [payload.content for payload in await asyncio.gather(*jobs)]
        else:
            response = requests.get(self.endpoint)
            self.logger.info(f'the response code was: {response.status_code}')
            results = response.content
        return results

    def _make_pages(self):
        response = requests.get(self.endpoint)
        payload = response.content.decode('utf-8')
        total_pages = json.loads(payload)['total_pages']
        assert isinstance(total_pages, int), f"parsing issue, the root.total_pages attribute is not an interger; {total_pages}"
        pages = []
        for page in range(1, total_pages+1):
            pages.append(self.endpoint + f"?page{page}")

        self.pages = pages