CREATE TABLE `Customer_Reviews` (
  `review_id` int NOT NULL,
  `customer_id` int DEFAULT NULL,
  `review_text` text,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Employee_Salaries` (
  `employee_id` int NOT NULL,
  `employee_name` varchar(255) DEFAULT NULL,
  `salary` float DEFAULT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Product_Categories` (
  `category_id` int NOT NULL,
  `category_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Sales_Region` (
  `region_id` int NOT NULL,
  `region_name` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`region_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `Supplier_Information` (
  `supplier_id` int NOT NULL,
  `supplier_name` varchar(255) DEFAULT NULL,
  `contact_email` varchar(255) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`supplier_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `customers` (
  `id` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `employees` (
  `id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `age` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `inventory` (
  `id` int DEFAULT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `quantity` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `orders` (
  `order_id` int DEFAULT NULL,
  `order_date` date DEFAULT NULL,
  `customer_id` int DEFAULT NULL,
  `product_id` int DEFAULT NULL,
  `employee_id` int DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


CREATE TABLE `products` (
  `id` int DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `price` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;


INSERT INTO Customer_Reviews (review_id, customer_id, review_text, rating) VALUES
(1, 101, 'Great product! Will buy again', 5),
(2, 102, 'Good quality product', 4),
(3, 103, 'Disappointed with the product', 2);

INSERT INTO Employee_Salaries (employee_id, employee_name, salary) VALUES
(1, 'John Doe', 60000.0),
(2, 'Jane Smith', 65000.0),
(3, 'Emily Johnson', 70000.0);

INSERT INTO Product_Categories (category_id, category_name) VALUES
(1, 'Electronics'),
(2, 'Clothing'),
(3, 'Home Decor');

INSERT INTO Sales_Region (region_id, region_name, country) VALUES
(1, 'North Region', 'USA'),
(2, 'South Region', 'USA'),
(3, 'West Region', 'USA');

INSERT INTO Supplier_Information (supplier_id, supplier_name, contact_email, country) VALUES
(1, 'ABC Electronics', 'info@abc.com', 'USA'),
(2, 'XYZ Clothing', 'info@xyz.com', 'USA'),
(3, 'HomeStyle Furnishings', 'info@homestyle.com', 'USA');

INSERT INTO customers (id, name, email) VALUES
(1, 'Alice', 'alice@example.com'),
(2, 'Bob', 'bob@example.com'),
(3, 'Eva', 'eva@example.com');

INSERT INTO employees (id, name, age) VALUES
(1, 'Michael', 30),
(2, 'Emma', 25),
(3, 'Emily Turner', 28),
(4, 'David Wilson', 35);

INSERT INTO inventory (id, product_name, quantity) VALUES
(1, 'Laptop', 10),
(2, 'T-shirt', 50),
(3, 'Cushions', 30);

INSERT INTO orders (order_id, order_date, customer_id, product_id, employee_id) VALUES
(1, '2023-01-15', 1, 1, 1),
(2, '2023-02-20', 2, 2, 2),
(3, '2023-03-15', 3, 3, 1);

INSERT INTO products (id, name, price) VALUES
(1, 'Laptop', 1200.0),
(2, 'T-shirt', 25.0),
(3, 'Cushions', 35.0);