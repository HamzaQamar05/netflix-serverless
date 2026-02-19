import os, boto3

_cw = boto3.client("cloudwatch")
NS = os.getenv("METRICS_NS", "NetflixServerless")

def put_metric(name: str, value: float, unit="Count"):
    _cw.put_metric_data(
        Namespace=NS,
        MetricData=[{"MetricName": name, "Value": value, "Unit": unit}],
    )
