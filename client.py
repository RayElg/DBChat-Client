import time
import simplejson as json
import requests
import mysql.connector
import psycopg2
from quickchart import QuickChart

BASE_URL = "https://gptblocks.co/dbchat/api"


def query_from_payload(payload, conn):
    try:
        query = payload["query"]
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        if result is None:
            return {"res": "OK"}
        return {"res": result, "columns_description": cursor.description}
    except Exception as e:
        if hasattr(conn, "rollback"):
            conn.rollback()
            return {"res": str(e) + ". Transaction rolled back."}
        return {"res": str(e)}


# Currently supports 1 dataset (one y_data col)
def chart_from_payload(payload, conn):
    res = query_from_payload(payload, conn)["res"]
    if isinstance(res, list):
        if (len(res) > 50) or (len(res) == 0):
            return {
                "res": f"Charts must have 1 to 50 rows. Your query returned {len(res)} rows"
            }
        if len(res[0]) != 2:
            return {"res": f"Charts must have exactly 2 columns"}
        x_data = [item[0] for item in res]
        y_data = [item[1] for item in res]

        qc = QuickChart()
        qc.width = 500
        qc.height = 300
        qc.config = {
            "type": payload.get(
                "chart_type", "bar"
            ),  # default to bar chart if not specified in opts
            "data": {
                "labels": x_data,
                "datasets": [
                    {
                        "label": payload.get(
                            "chart_label", "Values"
                        ),  # default to 'Values' if not specified in opts
                        "data": y_data,
                    }
                ],
            },
            "options": {
                "title": {
                    "display": True,
                    "text": payload.get(
                        "chart_title", "Chart Title"
                    ),  # default to 'Chart Title' if not specified in opts
                },
            },
        }
        try:
            qc.config = json.dumps(qc.config)  # Avoids type errors. Using simplejson instead of json for its Decimal type support
        except Exception as e:
            return {"res": f"failed to convert data to a chart: {e}. Hint: cast queried columns to string or number types."} # Some data types are still not JSON encodable

        return {"image_url": qc.get_url()}
    else:
        return {"res": f"non-chartable response from query: {res}"}


def get_db_tool_calls(runId, threadId, api_header):
    results = requests.post(
        f"{BASE_URL}/db_tool_calls",
        json={"runId": runId, "threadId": threadId},
        headers={"Authorization": api_header},
    )
    if results.status_code == 200:
        return results.json()
    else:
        return None


def poll_for_runs(context, api_header):
    results = requests.get(
        f"{BASE_URL}/poll?context={context}", headers={"Authorization": api_header}
    )
    if results.status_code == 200:
        return results.json()
    else:
        return None


def submit_tool_calls(runId, threadId, outputs, api_header):
    succ = requests.post(
        f"{BASE_URL}/submit_tool_calls",
        json={"runId": runId, "threadId": threadId, "outputs": outputs},
        headers={"Authorization": api_header},
    )
    if succ.status_code == 200:
        return True
    else:
        print(succ.text)
        print("Was not successful")
        return None


def user_loop(audit, conn, context, api_header):
    while True:
        res = poll_for_runs(context, api_header)
        if res:
            for run in res:
                tool_calls = get_db_tool_calls(
                    run["runId"], run["threadId"], api_header
                )
                if tool_calls:
                    tool_results = []
                    for toolcall in tool_calls:
                        print(toolcall["query"])
                    if (
                        audit
                        and input("Are you sure you want to execute these? (Y/n) ")
                        != "Y"
                    ):
                        print("Rejecting...")
                        for toolcall in tool_calls:
                            tool_res = {
                                "tool_call_id": toolcall["call_id"],
                                "output": str(
                                    {"res": "Query manually declined by user"}
                                ),
                            }
                            tool_results.append(tool_res)
                        submit_tool_calls(
                            run["runId"], run["threadId"], tool_results, api_header
                        )
                    else:
                        for toolcall in tool_calls:
                            call_res = (
                                query_from_payload(toolcall, conn)
                                if toolcall.get("function_called", "execute_query")
                                == "execute_query"
                                else chart_from_payload(toolcall, conn)
                            )
                            tool_res = {
                                "tool_call_id": toolcall["call_id"],
                                "output": str(call_res),
                            }
                            tool_results.append(tool_res)
                        submit_tool_calls(
                            run["runId"], run["threadId"], tool_results, api_header
                        )
        time.sleep(1)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true", help="Enable audit mode")

    parser.add_argument("--postgres", action="store_true", help="Use postgres connection")
    parser.add_argument("--mysql", action="store_true", help="Use MYSQL connection")

    parser.add_argument("--database", type=str, help="Database name")
    parser.add_argument("--user", type=str, help="DB Username")
    parser.add_argument("--password", type=str, help="DB password")
    parser.add_argument("--host", type=str, help="DB host")
    parser.add_argument("--port", type=str, help="DB port")
    parser.add_argument("--base-url", type=str, help="Base URL for GPTBlocks")
    parser.add_argument("--api-header", type=str, help="API header")
    parser.add_argument("--context", type=str, help="Context for DBChat - i.e. which client is this host connected to")
    args = parser.parse_args()

    if not (args.postgres ^ args.mysql):
        raise ValueError("Please select exactly one of --postgres or --mysql")

    DB_DATABASE = args.database or input("Enter database name: ")
    DB_USER = args.user or input("Enter DB username: ")
    DB_PASSWORD = args.password or input("Enter DB password: ")
    HOST = args.host or input("Enter DB host: ")
    DB_PORT = args.port or input("Enter DB port")
    BASE_URL = args.base_url or BASE_URL
    API_HEADER = args.api_header or input("Enter API header: ")
    CONTEXT = "DBChat:" + (args.context or "DEFAULT")

    def connect_to_mysql():
        cnx = mysql.connector.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=HOST,
            database=DB_DATABASE,
            port=DB_PORT,
        )
        return cnx

    def connect_to_postgres():
        cnx = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=HOST,
            database=DB_DATABASE,
            port=DB_PORT,
        )
        return cnx

    conn = connect_to_mysql() if args.mysql else connect_to_postgres()

    user_loop(args.audit, conn, CONTEXT, API_HEADER)
