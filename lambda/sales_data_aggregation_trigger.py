import psycopg2
import os
import configparser
import pymysql
from decimal import Decimal


def load_configs():
    config = configparser.ConfigParser()
    config.read('db_config.ini')
    return config


def get_redshift_conn(config):
    print("Connecting to Redshift")
    try:
        conn = psycopg2.connect(
            host=config['host'],
            dbname=config['dbname'],
            user=config['user'],
            password=config['password'],
            port=int(config['port']),
            sslmode='require'
        )
        print("Connection successful")
        return conn
    except Exception as e:
        print("Connection failed:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }


def get_rds_conn(config):
    print("Connecting to RDS")
    try:
        conn = pymysql.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            port=int(config['port'])
        )
        print("Connection successful")
        return conn
    except Exception as e:
        print("Connection failed  rds:", str(e))
        return {
            'statusCode': 500,
            'body': str(e)
        }


def fetchall_from_rds(rds_cur, query):
    rds_cur.execute(query)
    return rds_cur.fetchall()


def insert_into_redshift(rs_cur, query, data):
    return 'SUCCESS'


def lambda_handler(event, context):
    config = load_configs()

    print(config['mysql']['host'])

    rs_con = get_redshift_conn(config['redshift'])
    rds_con = get_rds_conn(config['mysql'])

    rds_cur = rds_con.cursor()

    query_1 = """SELECT
                    t.team_id,
                    t.team_name,
                    SUM(s.sale_amount) AS total_sales,
                    CASE
                        WHEN SUM(s.sale_amount) >= t.monthly_target  THEN 'Achieved'
                        ELSE 'Not Achieved'
                    END AS target_status
                FROM mooninsurance_db.integration s
                JOIN mooninsurance_db.agents a ON s.agent_id = a.agent_id
                JOIN mooninsurance_db.teams t ON a.team_id = t.team_id
                GROUP BY t.team_id, t.team_name
                ORDER BY total_sales DESC;"""

    query_2 = """SELECT
                    p.product_id,
                    p.product_name,
                    p.product_target_sales,
                    SUM(s.sale_amount) AS total_sales,
                    CASE
                        WHEN SUM(s.sale_amount) >= p.product_target_sales THEN 'Achieved'
                        ELSE 'Not Achieved'
                    END AS target_status
                FROM mooninsurance_db.integration s
                JOIN mooninsurance_db.products p ON s.product_id = p.product_id
                GROUP BY p.product_id, p.product_name, p.product_target_sales
                ORDER BY total_sales DESC;"""

    query_3 = """SELECT
                    b.branch_id,
                    b.branch_name,
                    b.monthly_target,
                    SUM(s.sale_amount) AS total_sales,
                    CASE
                        WHEN SUM(s.sale_amount) >= b.monthly_target THEN 'Achieved'
                        ELSE 'Not Achieved'
                    END AS target_status
                FROM mooninsurance_db.integration s
                JOIN mooninsurance_db.agents a ON s.agent_id = a.agent_id
                JOIN mooninsurance_db.branches b ON a.branch_id = b.branch_id
                GROUP BY b.branch_id, b.branch_name, b.monthly_target
                ORDER BY total_sales DESC;"""

    query_1_result = fetchall_from_rds(rds_cur, query_1)
    query_2_result = fetchall_from_rds(rds_cur, query_2)
    query_3_result = fetchall_from_rds(rds_cur, query_3)

    insert_query_1 = """INSERT INTO public.best_performing_team_metrics
                        (team_id, team_name, sale_amount, target_status)
                        VALUES ({}, {}, {}, {})"""

    insert_query_2 = """INSERT INTO public.product_sales_aggregated
                        (product_id, product_name, target_sales, total_sales, target_status)
                        VALUES ({}, {}, {}, {}, {})"""

    insert_query_3 = """INSERT INTO public.branch_sales_aggregated
                        (branch_id, branch_name, target_sales, total_sales, target_status)
                        VALUES ({}, {}, {}, {}, {})"""

    rs_cur = rs_con.cursor()

    rs_cur.execute("TRUNCATE TABLE public.best_performing_team_metrics")
    for data in query_1_result:
        print(data)
        rs_cur.execute(insert_query_1.format(data[0], f"'{data[1]}'", data[2], f"'{data[3]}'"))

    rs_cur.execute("TRUNCATE TABLE public.product_sales_aggregated")
    for data in query_2_result:
        print(data)
        rs_cur.execute(insert_query_2.format(data[0], f"'{data[1]}'", data[2], data[3], f"'{data[4]}'"))

    rs_cur.execute("TRUNCATE TABLE public.branch_sales_aggregated")
    for data in query_3_result:
        print(data)
        rs_cur.execute(insert_query_3.format(data[0], f"'{data[1]}'", data[2], data[3], f"'{data[4]}'"))

    rs_con.commit()
    rs_cur.close()

    return {
        'statusCode': 200
    }
