## DBChat Client

DBChat is an AI-assistant program integrated with a database client. This project (DBChat Client) is the client that connects to the [GPTBlocks](https://gptblocks.co/dbchat) endpoint to handle assistant-requested SQL queries.

Postgres & MySQL compatible databases are supported.

### Example

```
$ python client.py --mysql --database=mydatabase --user myuser --password mypassword --host localhost --port 3306 --context mysql
Enter API header: Basic sk_...


SELECT e.name AS employee_name, SUM(p.price) AS total_revenue
FROM employees e
JOIN orders o ON e.id = o.employee_id
JOIN products p ON o.product_id = p.id
GROUP BY e.name
ORDER BY total_revenue DESC;
```

![Web Example](./webexample.png)

[Youtube Demo](https://www.youtube.com/watch?v=F2pkt9w0Er4)



### Usage

To run the DBChat Client, use the following command:

```bash
python client.py [--mysql][--audit] [--database <database>] [--user <username>] [--password <password>] [--host <host>] [--port <port>] [--base-url <base_url>] [--context <identifier_for_client>] [--api-header <header>]
```



### Testing Locally

A docker-compose environment has been supplied that installs prerequisites & starts a local mysql server for testing. The contained DBChat container is configured to use the local mysql container.

Ensure you have docker-compose installed, and run the following commands
```bash
export GPTBLOCKS_API_KEY=<YOUR KEY FROM GPTBLOCKS>
docker-compose build && docker-compose up
```

After both containers have started, you may proceed by chatting on gptblocks.

### Arguments

The DBChat Client accepts the following arguments:

* `--mysql`: Flag to connect using MySQL. Mutually exclusive with --postgres.
* `--postgres`: Flag to connect using Postgres. Mutually exclusive with --mysql.
* `--audit`: Enable audit mode. This mode allows you to approve or deny SQL queries before execution.
* `--database <database>`: The name of the DB database to connect to. If not provided, the client will prompt for the database name.
* `--user <username>`: The username for the DB connection. If not provided, the client will prompt for the username.
* `--password <password>`: The password for the DB connection. If not provided, the client will prompt for the password.
* `--host <host>`: The host for the DB connection. If not provided, the client will prompt for the host.
* `--port <port>`: The port for the DB connection.  If not provided, the client will prompt for the port.
* `--base-url <base_url>`: The base URL for the GPTBlocks endpoint. If not provided, the client will use the default value.
* `--context <identifier_for_client>`: The identifier for this client. When users use your DBChat, this is how they will specify the desired client to send queries to.
* `--api-header <header>`: The API header for authentication. If not provided, the client will prompt for the header.

### Acquiring API Header

To acquire an API key from your user page at gptblocks.co/user, follow these steps:

1. Go to gptblocks.co/user and log in to your account.
2. Navigate to your user page.
3. Locate the API key section.
4. Generate or copy your API key.

The API Header should be in the following format:

```
Basic sk_abcdefghi
```

### Usage Tips

* The assistant performs best when you start the conversation with a request to list tables, and to then describe the schemas for the tables.

* For databases containing sensitive or production data, the user provided to the client should have limited perms

* Try asking the AI to generate views or markdown reports for you

* For an always-online client, set up a small EC2 instance connected to your data warehouse

### Todo

* [x] Integrate with OpenAI, mysql
* [x] Integrate more databases to expand the client's compatibility.
* [ ] Develop a cloud version of the client that can be self-hosted or used as a service.
* [ ] Add support for code execution, DBT (Data Build Tool), and other related functionalities.
* [x] Per-database context
* [ ] Improved framework for by-context & by-user function calling
