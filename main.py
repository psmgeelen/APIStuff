import cProfile
import logging
from APIStuff import APIStuff

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    handlers=[
        logging.FileHandler("example1.log"),
        logging.StreamHandler()
    ])
logger = logging.getLogger()

api_without_pagination = "https://reqres.in/api/users?page2"
api_with_pagination = "https://reqres.in/api/users"

results = APIStuff(logger=logger).get_data_form_API(
    endpoint=api_without_pagination,
    method='sync',
    pagination=False
)
print([item for item in results])

results = APIStuff(logger=logger).get_data_form_API(
    endpoint=api_with_pagination,
    method='async',
    pagination=True
)
print([item for item in results])

results = APIStuff(logger=logger).get_data_form_API(
    endpoint=api_with_pagination,
    method='parallel',
    pagination=True
)
print([item for item in results])
