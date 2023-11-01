from copy import deepcopy
from typing import Generic

import httpx
import inflection
from patent_client.util import Manager
from patent_client.util import ModelType
from patent_client.util.request_util import get_start_and_row_count

from . import schema_doc
from .api import PtabApi
from .model import PtabDecision
from .model import PtabDocument
from .model import PtabProceeding
from .util import peds_to_ptab

asession = httpx.AsyncClient(verify=False)


class PtabManager(Manager, Generic[ModelType]):
    url = "https://developer.uspto.gov/ptab-api"
    page_size = 25
    instance_schema = None
    api_method = None

    async def _aget_results(self):
        query = deepcopy(self.config.filter)
        query = peds_to_ptab(query)
        query["sort"] = " ".join(inflection.camelize(o, uppercase_first_letter=False) for o in self.config.order_by)
        for start, rows in get_start_and_row_count(self.config.limit, self.config.offset, self.page_size):
            query["start"] = start
            query["rows"] = rows
            page = await self.api_method(**query)
            for doc in page.docs:
                yield doc
            if len(page.docs) < rows:
                break

    async def alen(self):
        page = await self.api_method(**peds_to_ptab(self.config.filter))
        return min(self.config.limit, page.num_found) if self.config.limit else page.num_found

    def allowed_filters(self):
        params = schema_doc["paths"][self.path]["get"]["parameters"]
        return {inflection.underscore(p["name"]): p["description"] for p in params}


class PtabProceedingManager(PtabManager[PtabProceeding]):
    path = "/proceedings"
    primary_key = "proceeding_number"
    api_method = PtabApi.get_proceedings


class PtabDocumentManager(PtabManager[PtabDocument]):
    path = "/documents"
    primary_key = "document_identifier"
    api_method = PtabApi.get_documents


class PtabDecisionManager(PtabManager[PtabDecision]):
    path = "/decisions"
    primary_key = "identifier"
    api_method = PtabApi.get_decisions
