-- Database: MStore_v1

-- DROP DATABASE IF EXISTS "MStore_v1";
SET search_path TO MStore_v1;
CREATE DATABASE "MStore_v1"
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LC_COLLATE = 'Finnish_Finland.1252'
    LC_CTYPE = 'Finnish_Finland.1252'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

COMMENT ON DATABASE "MStore_v1"
    IS 'Music Store v1 db';

CREATE TABLE MStore_v1.Customer (
    id SERIAL NOT NULL PRIMARY KEY,
    Store_id INT NOT NULL,
    custoName VARCHAR(50) NOT NULL UNIQUE,
    custoPassw VARCHAR(20) NOT NULL UNIQUE,
    custoEmail VARCHAR(50) DEFAULT NULL,
    custoPhone VARCHAR(20) DEFAULT NULL,
    custoStatus BOOLEAN DEFAULT FALSE, -- loyalty card owner or not
    custoBlocked BOOLEAN DEFAULT FALSE
    --FOREIGN KEY(Store_id) REFERENCES MStore_v1.Store(id)
);

CREATE TABLE MStore_v1.Store (
    id SERIAL NOT NULL PRIMARY KEY,
    storeManagerName VARCHAR(50) NOT NULL UNIQUE,
    storeManagerPssw VARCHAR(20) DEFAULT NULL,
    storeName VARCHAR(40) NOT NULL,
    storeTaxId VARCHAR(16) NOT NULL UNIQUE,
    storePhone VARCHAR(20) NOT NULL UNIQUE,
    storeEmail VARCHAR(25) NOT NULL UNIQUE,
    storeAddress VARCHAR(40) NOT NULL UNIQUE,
    storeLogoUrl VARCHAR(140) DEFAULT NULL, -- Link to the actual image file
    storeManager_id INT
    --FOREIGN KEY(storeManager_id) REFERENCES MStore_v1.Customer(id)
);

CREATE TABLE MStore_v1.ProductGroup (
    id SERIAL NOT NULL PRIMARY KEY,
    Store_id INT NOT NULL,
    prodGroupName VARCHAR(80) NOT NULL UNIQUE,
    prodGrDiscount DECIMAL(10, 2) DEFAULT 0.00, 
	-- percent of discount per group
    prodGrVatPercent DECIMAL(10, 2) DEFAULT 0.00, 
	-- Percent of Value Added Tax of group
    -- Cumulative monthly saldo fields for one year (3 times 12 fields)
    monthlySales_01 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyDiscounts_01 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyTaxes_01 DECIMAL(10, 2) DEFAULT 0.00,
    monthlySales_02 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyDiscounts_02 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyTaxes_02 DECIMAL(10, 2) DEFAULT 0.00,
    -- Repeat for all 12 months
    monthlySales_12 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyDiscounts_12 DECIMAL(10, 2) DEFAULT 0.00,
    monthlyTaxes_12 DECIMAL(10, 2) DEFAULT 0.00
    --FOREIGN KEY(Store_id) REFERENCES MStore_v1.Store(id)
);

CREATE TABLE MStore_v1.ShoppingCart (
    id SERIAL NOT NULL PRIMARY KEY,
    cartStore_id INT NOT NULL, -- ID of the MusicStore
    cartCustomer_id INT NOT NULL,
    cartStatus BOOLEAN DEFAULT FALSE, -- status of the cart: open/closed/delivered
    cartVat FLOAT DEFAULT 0.00, -- Amount of Value Added Taxes
    cartDiscount FLOAT DEFAULT 0.00,
    cartTotal FLOAT DEFAULT 0.00, -- Total sum of items – discounts + VAT
    cartPaymentBank VARCHAR(30) NOT NULL,
    cartCardInfo VARCHAR(30) DEFAULT NULL,
    cartCurrentTime TIMESTAMP NOT NULL, -- used for receipt and campaign manag.
    cartEditedTime TIMESTAMP NOT NULL, -- edited and saved time
    cartPurchasedTime TIMESTAMP NOT NULL,
    cartDeliveryTime TIMESTAMP NOT NULL,
    cartDeliveryMethod VARCHAR(50) NOT NULL,
    cartProd_1_id INT,
    cartProd_2_id INT,
    cartProd_3_id INT,
    cartProd_4_id INT,
    cartProd_5_id INT,
    cartProd_6_id INT,
    cartProd_7_id INT,
    cartProd_8_id INT,
    cartProd_9_id INT,
    cartProd_10_id INT,
    cartProd_11_id INT,
    cartProd_12_id INT
    --FOREIGN KEY(cartStore_id) REFERENCES MStore_v1.Store(id),
    --FOREIGN KEY(cartCustomer_id) REFERENCES MStore_v1.Customer(id),
    --FOREIGN KEY(cartProd_1_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_2_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_3_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_4_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_5_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_6_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_7_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_8_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_9_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_10_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_11_id) REFERENCES MStore_v1.Product(id),
    --FOREIGN KEY(cartProd_12_id) REFERENCES MStore_v1.Product(id)
);

CREATE TABLE MStore_v1.Product (
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
    --FOREIGN KEY(productGroup_id) REFERENCES MStore_v1.ProductGroup(id),
    --FOREIGN KEY(productImage_id) REFERENCES MStore_v1.ProductImage(id)
);

CREATE TABLE ProductImage (
    id SERIAL NOT NULL PRIMARY KEY,
    prodImageName VARCHAR(60) NOT NULL,
    prodImageType VARCHAR(4) DEFAULT '.PNG',
    prodImageResHori INT NOT NULL,
    prodImageResVert INT NOT NULL,
    prodImage_url VARCHAR(120) NOT NULL -- Link to the actual image file
);