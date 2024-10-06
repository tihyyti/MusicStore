CREATE TABLE mstore_v1.Product (
    id SERIAL NOT NULL PRIMARY KEY,
    productGroup_id INT NOT NULL,
    productCampaignFlag BOOLEAN DEFAULT FALSE, -- campaign or regular pricing
    productName VARCHAR(100) NOT NULL,
    productDetails TEXT,
    productImage_id INT DEFAULT NULL, -- Links to gear image metadata file
    productsInStore INT DEFAULT NULL,
    productsReserved INT DEFAULT NULL,
    producPurchPrice DECIMAL(10, 2) DEFAULT 0.00,
    productSalesPrice DECIMAL(10, 2) DEFAULT 0.00,
    productCampaignPrice DECIMAL(10, 2) DEFAULT 0.00,
    productDiscount DECIMAL(10, 2) DEFAULT 0.00,
    -- Cumulative daily fields
    dailySales DECIMAL(10, 2) DEFAULT 0.00,
    dailyDiscounts DECIMAL(10, 2) DEFAULT 0.00,
    dailyTaxes DECIMAL(10, 2) DEFAULT 0.00,
    -- Cumulative monthly fields
    monthlySales DECIMAL(10, 2) DEFAULT 0.00,
    monthlyDiscounts DECIMAL(10, 2) DEFAULT 0.00,
    monthlyTaxes DECIMAL(10, 2) DEFAULT 0.00,
    productCampaignStart TIMESTAMP NOT NULL,
    productCampaignEnd TIMESTAMP NOT NULL,
    productCreated TIMESTAMP NOT NULL,
    productEdited TIMESTAMP NOT NULL
    --FOREIGN KEY(productGroup_id) REFERENCES ProductGroup(id)
);
CREATE TABLE mstore_v1.ShoppingCartProduct (
    cart_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT DEFAULT 1,
    PRIMARY KEY (cart_id, product_id),
    FOREIGN KEY (cart_id) REFERENCES mstore_v1.ShoppingCart(id),
    FOREIGN KEY (product_id) REFERENCES mstore_v1.Product(id)
);
-- Create an index on product code
CREATE INDEX idx_product_code ON mstore_v1.product (id);
-- Create a composite index on product code and product name
CREATE INDEX idx_product_code_name ON mstore_v1.product (id, productname);
-- Index on price
CREATE INDEX idx_product_price ON mstore_v1.product (productsalesprice);
-- Index on discount
CREATE INDEX idx_product_discount ON mstore_v1.product (productdiscount);
-- Index on storage amount
CREATE INDEX idx_product_storage ON mstore_v1.product (productsinstore);
-- Index on customer ID in the Customer table
CREATE INDEX idx_customer_id ON mstore_v1.customer (id);
CREATE INDEX idx_customer_name ON mstore_v1.Customer (custoName);
CREATE INDEX idx_customer_email ON mstore_v1.Customer (custoEmail);
CREATE INDEX idx_customer_last_login ON mstore_v1.Customer (last_login);
-- Index on shopping cart ID in the Shopping Cart table
CREATE INDEX idx_shoppingcart_id ON mstore_v1.shoppingcart (id);
CREATE INDEX idx_shoppingcartproduct_cart_id ON mstore_v1.ShoppingCartProduct (cart_id);
CREATE INDEX idx_shoppingcartproduct_product_id ON mstore_v1.ShoppingCartProduct (product_id);
CREATE INDEX idx_shoppingcartproduct_cart_product ON mstore_v1.ShoppingCartProduct (cart_id, product_id);
-- Composite index on customer ID and product ID in the Shopping Cart table
CREATE INDEX idx_cart_customer_product ON mstore_v1.shoppingcart (id, id);
-- Index on cartCustomer_id for efficient filtering and ordering
CREATE INDEX idx_shoppingcart_cartCustomer_id ON mstore_v1.ShoppingCart (cartCustomer_id);
-- Index on cartStatus for efficient filtering
CREATE INDEX idx_shoppingcart_cartStatus ON mstore_v1.ShoppingCart (cartStatus);
-- Index on cartCurrentTime for efficient ordering
CREATE INDEX idx_shoppingcart_cartCurrentTime ON mstore_v1.ShoppingCart (cartCurrentTime);



