import psycopg2
from psycopg2 import OperationalError

from db import config

config_file = 'db/db_config.ini'
db = 'pump-db'
db_config = config.get_db_info(config_file, db)


def ingest(response):
    db_conn = None
    try:
        with psycopg2.connect(**db_config) as db_conn:
            with db_conn.cursor() as db_cursor:
                offerings = 0
                offers_with_prices = 0

                for offering in response["ReservedInstancesOfferings"]:
                    offerings += 1

                    search_query = "SELECT * FROM instance_offerings WHERE reserved_instances_offering_id = %s;"
                    search_values = (offering['ReservedInstancesOfferingId'],)
                    db_cursor.execute(search_query, search_values)

                    instance_offering = db_cursor.fetchone()
                    if instance_offering is None:
                        insert_query = ("INSERT INTO instance_offerings ("
                                        "duration, "
                                        "fixed_price, "
                                        "instance_type, "
                                        "product_description, "
                                        "reserved_instances_offering_id, "
                                        "usage_price, "
                                        "currency_code, "
                                        "instance_tenancy, "
                                        "marketplace, "
                                        "offering_class, "
                                        "offering_type) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                                        )

                        db_cursor.execute(insert_query, get_instance_offering_insert_values(offering))

                        # Reload
                        db_cursor.execute(search_query, search_values)
                        instance_offering = db_cursor.fetchone()

                    if len(offering['PricingDetails']) > 0:
                        offers_with_prices += 1

                        search_query = 'SELECT pd.* FROM pricing_details pd WHERE instance_offering_id = %s;'
                        search_values = (instance_offering[0],)
                        db_cursor.execute(search_query, search_values)

                        pricing_details = db_cursor.fetchone()
                        if pricing_details is None:
                            insert_query = ('INSERT INTO pricing_details (count, price, instance_offering_id) '
                                            'VALUES (%s, %s, %s);')
                            insert_values = (
                                offering['PricingDetails'][0]['Count'],
                                offering['PricingDetails'][0]['Price'],
                                instance_offering[0]
                            )
                            db_cursor.execute(insert_query, insert_values)
                        else:
                            update_query = ('UPDATE pricing_details '
                                            'SET count = %s, price = %s '
                                            'WHERE instance_offering_id = %s;')
                            update_values = (
                                offering['PricingDetails'][0]['Count'],
                                offering['PricingDetails'][0]['Price'],
                                instance_offering[0]
                            )
                            db_cursor.execute(update_query, update_values)

            return offerings, offers_with_prices

    except OperationalError:
        print("Error connecting to database")
    finally:
        if db_conn:
            db_conn.close()


def get_instance_offering_insert_values(offering: dict):
    return (
        offering["Duration"],
        offering["FixedPrice"],
        offering["InstanceType"],
        offering["ProductDescription"],
        offering["ReservedInstancesOfferingId"],
        offering["UsagePrice"],
        offering["CurrencyCode"],
        offering["InstanceTenancy"],
        offering["Marketplace"],
        offering["OfferingClass"],
        offering["OfferingType"]
    )


def rank(instance_type: str):
    return 'hi'
