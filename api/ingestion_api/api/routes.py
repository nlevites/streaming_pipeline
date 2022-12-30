import json
from datetime import datetime
from uuid import UUID, uuid4

import boto3
import structlog
from fastapi import APIRouter, Header

from api.ingestion_api.config import config
from api.ingestion_api.models import CreatePOIRequest, CreateResponse, PersonOfInterest

logger = structlog.get_logger()
api_router: APIRouter = APIRouter(prefix="/api/v1")
STREAM_NAME = config.stream_name

kinesis_client = boto3.client(
    "kinesis", endpoint_url=config.stream_host, region_name="us-west-2"
)


@api_router.post("/poi", status_code=201, response_model=CreateResponse)
async def create(
    body: CreatePOIRequest,
    user_id: UUID = Header(),
) -> CreateResponse:
    poi_id = str(uuid4())
    bound_logger = logger.bind(user_id=user_id, poi_id=poi_id)

    # TODO REQUEST AUTH SERVICE
    bound_logger.debug("authenticating user")

    bound_logger.info("creating person of interest")
    poi = PersonOfInterest(
        poi_id=poi_id, date_received=datetime.utcnow().timestamp(), **body.dict()
    )
    kinesis_client.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(poi.dict(), default=str),
        PartitionKey="default_partitionkey",
    )
    bound_logger.info("created person of interest")

    return CreateResponse(id=str(poi_id))
