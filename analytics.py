from fastapi import HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from models import InstanceDataORM
from schemas import InstanceData, AnalyticsRequestParams, InstancesVolumeAnalyticsResult


def store_instances_data(session: Session, reserved_instances: [InstanceData]) -> [InstanceData]:
    """
    Consumes and array of JSON objects from AWS API as a parameter, converts it into
    an array pydantic classes to return and also creates an array of models to store in the DB
    :param session: DB session
    :param reserved_instances: and array of JSON object retrieved from AWS API
    :return: a list of InstanceData objects
    """
    try:
        for instance in reserved_instances:
            instance_data_orm = InstanceDataORM()
            instance_data_orm.from_pydantic(instance)
            session.add(instance_data_orm)

        session.commit()
        return reserved_instances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def get_instance_volume_analytics(session: Session, instance_type: str,
                                  date: str) -> InstancesVolumeAnalyticsResult:
    """
    Retrieves a collection of Min Max and Average values for the number of instances for a select date.
    1. counts the number of instances matching the criteria for each distinct timestamp
    2. calculates min max and average over the day based on the total count for each (1)

      :param session: database session.
      :param instance_type: instance type, e.g. m5.large.
      :param date: date to perform the aggregation for.
      :return: InstancesVolumeAnalyticsResult
    """
    subquery = session.query(
        func.count().label('total_count')
    ).filter(
        InstanceDataORM.instance_type == instance_type,
        func.date(InstanceDataORM.timestamp) == date
    ).group_by(
        func.date_trunc('hour', InstanceDataORM.timestamp)
    ).subquery()

    result = session.query(
        func.min(subquery.c.total_count).label('min_count'),
        func.max(subquery.c.total_count).label('max_count'),
        func.avg(subquery.c.total_count).label('avg_count')
    ).first()

    request_params = AnalyticsRequestParams(
        instance_type=instance_type,
        specific_date=date
    )

    return InstancesVolumeAnalyticsResult(
        params=request_params,
        min_count=int(result.min_count) if result.min_count else 0,
        max_count=int(result.max_count) if result.max_count else 0,
        avg_count=float(result.avg_count) if result.avg_count else 0.0
    )


def get_ranked_m5_instances(session: Session, specific_date: str) -> list[str]:
    """
    Retrieving and ranking the m5 family (part of it) instances based on the variability of the offering volume across
    the snapshots taken every 30 minutes within a selected date. Variability is calculated as a delta between minimum
    and maximum offered instances of the specific type on the market

    :param session: Database session
    :param specific_date: date for which we are performing the liquidity analysis
    :return: list of ranked instances from most liquid to least liquid
    """
    m5_instance_types = ['m5.large', 'm5.xlarge', 'm5.2xlarge', 'm5.4xlarge', 'm5.12xlarge', 'm5.24xlarge']

    # Dictionary to store the min-max delta (liquidity)
    differences = {}

    for instance_type in m5_instance_types:
        result = get_instance_volume_analytics(session, instance_type, specific_date)

        # Calculate the naive `liquidity`
        delta = result.max_count - result.min_count

        differences[instance_type] = delta

    # Sort the results based on the delta in descending order
    ranked_results = sorted(differences.items(), key=lambda x: x[1], reverse=True)

    return ranked_results
