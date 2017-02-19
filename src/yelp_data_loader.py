#!/usr/bin/python
# -*- coding: utf-8 -*-


import argparse
from spark_connector import SparkConnector

def main(filename, cores):
    sc = SparkConnector(cores)
    sc.load_tables_from_tar(filename)
    query = "SELECT city, count(*) as cnt_business FROM business group by 1 order by 2 desc limit 10"
    print("\nTop 10 Business Cities:\n")
    sc.run_query(query)
    query = "SELECT b.name, count(*) as cnt_brand FROM business b join review r using(business_id) " + \
            "group by 1 order by 2 desc limit 10" 
    print("Top 10 Popular Businesses by brand name:\n")
    sc.run_query(query)
    query = "with city_count as (SELECT city, count(*) as cnt FROM business group by 1) " + \
            "select b.name as business_name, b.city, count(*) as ratings_total, avg(r.stars) as avg_rating " + \
            "from city_count as base LEFT JOIN city_count as c on (c.cnt > base.cnt) join business b " + \
            "ON (base.city = b.city) JOIN review r ON(b.business_id = r.business_id) " + \
            "WHERE c.cnt IS NULL GROUP BY 1,2 ORDER BY 3 DESC LIMIT 10"
    print("Top 10 Popular Businesses in most popular city:\n")
    sc.run_query(query)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Populate YELP data from a local tar archive' +
                        ' to a local Spark instance and run some queries on it')
    parser.add_argument('-f', '--filename', help='filename of the local tar file to load',
                        required=True)
    parser.add_argument('-c', '--cores', help='number of cores to use for Spark', required=True)
    args = parser.parse_args()
    file_name = args.filename.strip()
    cores = args.cores.strip()
    main(file_name, cores)
