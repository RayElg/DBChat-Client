import time
import requests
import mysql.connector

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
        return result
    except Exception as e:
        return {"res": str(e)}


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
    results = requests.get(f"{BASE_URL}/poll?context={context}", headers={"Authorization": api_header})
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
                            call_res = query_from_payload(toolcall, conn)
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

    parser.add_argument("--mysql-database", type=str, help="MySQL database name")
    parser.add_argument("--mysql-user", type=str, help="MySQL username")
    parser.add_argument("--mysql-password", type=str, help="MySQL password")
    parser.add_argument("--host", type=str, help="MySQL host")
    parser.add_argument("--base-url", type=str, help="Base URL")
    parser.add_argument("--api-header", type=str, help="API header")
    parser.add_argument("--context", type=str, help="Context for DBChat - i.e. which client is this host connected to")
    args = parser.parse_args()

    MYSQL_DATABASE = args.mysql_database or input("Enter MySQL database name: ")
    MYSQL_USER = args.mysql_user or input("Enter MySQL username: ")
    MYSQL_PASSWORD = args.mysql_password or input("Enter MySQL password: ")
    HOST = args.host or input("Enter MySQL host: ")
    BASE_URL = args.base_url or BASE_URL
    API_HEADER = args.api_header or input("Enter API header: ")
    CONTEXT = "DBChat:" + (args.context or "DEFAULT")

    def connect_to_mysql():
        cnx = mysql.connector.connect(
            user=MYSQL_USER, password=MYSQL_PASSWORD, host=HOST, database=MYSQL_DATABASE
        )
        return cnx

    mysql_connection = connect_to_mysql()

    user_loop(args.audit, mysql_connection, CONTEXT, API_HEADER)
