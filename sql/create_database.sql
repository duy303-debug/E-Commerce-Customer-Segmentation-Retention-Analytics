
CREATE DATABASE ecommerce;
GO

USE ecommerce;
GO

CREATE SCHEMA ec;
GO

-- 1. CUSTOMERS
CREATE TABLE ec.customers
(
    customer_id   INT           NOT NULL PRIMARY KEY,
    full_name     NVARCHAR(100),
    email         NVARCHAR(255),
    phone         VARCHAR(20),
    gender        NVARCHAR(10),
    date_of_birth DATE,
    city          NVARCHAR(100)
);
GO

-- 2. PRODUCTS
CREATE TABLE ec.products
(
    product_id   INT            NOT NULL PRIMARY KEY,
    product_name NVARCHAR(200)  NOT NULL,
    category     NVARCHAR(100),
    unit_price   DECIMAL(12,2)  NOT NULL,
    unit_cost    DECIMAL(12,2)  NOT NULL,

    CONSTRAINT CK_products_unit_price
        CHECK (unit_price > 0),

    CONSTRAINT CK_products_unit_cost
        CHECK (unit_cost >= 0)
);
GO

-- 3. ORDERS
CREATE TABLE ec.orders
(
    order_id      INT           NOT NULL PRIMARY KEY,
    customer_id   INT           NOT NULL,
    order_date    DATETIME    NOT NULL,
    payment_method NVARCHAR(50),
    order_status  NVARCHAR(30),

    CONSTRAINT FK_orders_customers
        FOREIGN KEY (customer_id)
        REFERENCES ec.customers(customer_id)
);
GO

-- 4. ORDER_ITEMS
CREATE TABLE ec.order_items
(
    order_item_id INT           NOT NULL PRIMARY KEY,
    order_id      INT           NOT NULL,
    product_id    INT           NOT NULL,
    quantity      INT           NOT NULL,
    unit_price    DECIMAL(12,2) NOT NULL,
    cost          DECIMAL(12,2) NOT NULL,

    CONSTRAINT FK_order_items_orders
        FOREIGN KEY (order_id)
        REFERENCES ec.orders(order_id),

    CONSTRAINT FK_order_items_products
        FOREIGN KEY (product_id)
        REFERENCES ec.products(product_id),

    CONSTRAINT CK_order_items_quantity
        CHECK (quantity > 0),

    CONSTRAINT CK_order_items_unit_price
        CHECK (unit_price > 0),

    CONSTRAINT CK_order_items_cost
        CHECK (cost >= 0)
);
GO
