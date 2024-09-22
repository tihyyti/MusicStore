-- Insert data into Store table
INSERT INTO MStore_v1.Store (id, storeManagerName, storeManagerPssw, storeName, storeTaxId, storePhone, storeEmail, storeAddress, storeLogoUrl, storeManager_id)
VALUES 
(1,'John Doe', 'password123', 'Vintage Instruments Store', 'TAX1234567890', '123-456-7890', 'vintage@store.com', '123 Vintage St, Music City', 'http://example.com/logo1.png', NULL),
(2,'Jane Smith', 'password456', 'Modern Instruments Store', 'TAX0987654321', '098-765-4321', 'modern@store.com', '456 Modern Ave, Music City', 'http://example.com/logo2.png', NULL);

-- Insert data into Customer table
INSERT INTO MStore_v1.Customer (id, store_id, custoName, custoPassw, custoEmail, custoPhone, custoStatus, custoBlocked)
VALUES 
(1, 1, 'Alice', 'alicepass', 'alice@example.com', '111-222-3333', TRUE, FALSE),
(2, 1, 'Bob', 'bobpass', 'bob@example.com', '222-333-4444', FALSE, FALSE),
(3, 2, 'Charlie', 'charliepass', 'charlie@example.com', '333-444-5555', TRUE, FALSE),
(4, 2, 'Dave', 'davepass', 'dave@example.com', '444-555-6666', FALSE, TRUE);

-- Insert data into ProductGroup table
INSERT INTO MStore_v1.ProductGroup (id, Store_id, prodGroupName, prodGrDiscount, prodGrVatPercent, monthlySales_01, monthlyDiscounts_01, monthlyTaxes_01, monthlySales_02, monthlyDiscounts_02, monthlyTaxes_02, monthlySales_12, monthlyDiscounts_12, monthlyTaxes_12)
VALUES 
(1,1, 'Vintage Guitars', 10.00, 5.00, 1000.00, 100.00, 50.00, 1200.00, 120.00, 60.00, 1500.00, 150.00, 75.00),
(2,1, 'Vintage Accessories', 5.00, 5.00, 500.00, 25.00, 25.00, 600.00, 30.00, 30.00, 700.00, 35.00, 35.00),
(3,2, 'Modern Guitars', 15.00, 10.00, 2000.00, 300.00, 200.00, 2200.00, 330.00, 220.00, 2500.00, 375.00, 250.00),
(4,2, 'Modern Accessories', 10.00, 10.00, 1000.00, 100.00, 100.00, 1200.00, 120.00, 120.00, 1500.00, 150.00, 150.00);

--Insert data into ProductImage table
INSERT INTO MStore_v1.ProductImage (id, prodImageName, prodImageType, prodImageResHori, prodImageResVert, prodImage_url)
VALUES 
(1,'Vintage Fender Stratocaster', '.PNG', 800, 600, 'http://example.com/images/stratocaster.png'),
(2,'Vintage Gibson Les Paul', '.PNG', 800, 600, 'http://example.com/images/lespaul.png'),
(3,'Modern Yamaha Pacifica', '.PNG', 800, 600, 'http://example.com/images/pacifica.png'),
(4,'Modern Ibanez RG', '.PNG', 800, 600, 'http://example.com/images/ibanez.png');

-- Insert data into Product table
INSERT INTO MStore_v1.Product (id,productGroup_id, productCampaignFlag, productName, productDetails, productImage_id, productsInStore, productsReserved, producPurchPrice, productSalesPrice, productCampaignPrice, productDiscount, dailySales, dailyDiscounts, dailyTaxes, monthlySales, monthlyDiscounts, monthlyTaxes, productCampaignStart, productCampaignEnd, productCreated, productEdited)
VALUES 
(1,1, FALSE, 'Vintage Fender Stratocaster', 'A classic vintage guitar from the 1960s.', 1, 10, 2, 1500.00, 2000.00, 1800.00, 10.00, 500.00, 50.00, 25.00, 1000.00, 100.00, 50.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
(2,1, TRUE, 'Vintage Gibson Les Paul', 'A legendary guitar known for its rich sound.', 2, 5, 1, 2000.00, 2500.00, 2200.00, 15.00, 600.00, 60.00, 30.00, 1200.00, 120.00, 60.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
(3,2, FALSE, 'Modern Yamaha Pacifica', 'A versatile modern guitar for all genres.', 3, 20, 5, 300.00, 500.00, 450.00, 5.00, 200.00, 20.00, 10.00, 400.00, 40.00, 20.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', '2024-01-01 00:00:00', '2024-01-01 00:00:00'),
(4,2, TRUE, 'Modern Ibanez RG', 'A high-performance guitar for shredders.', 4, 15, 3, 700.00, 1000.00, 900.00, 10.00, 300.00, 30.00, 15.00, 600.00, 60.00, 30.00, '2024-01-01 00:00:00', '2024-12-31 23:59:59', '2024-01-01 00:00:00', '2024-01-01 00:00:00');

-- Insert data into ShoppingCart table
INSERT INTO MStore_v1.ShoppingCart (id, cartStore_id, cartCustomer_id, cartStatus, cartVat, cartDiscount, cartTotal, cartPaymentBank, cartCardInfo, cartCurrentTime, cartEditedTime, cartPurchasedTime, cartDeliveryTime, cartDeliveryMethod, cartProd_1_id, cartProd_2_id, cartProd_3_id, cartProd_4_id, cartProd_5_id, cartProd_6_id, cartProd_7_id, cartProd_8_id, cartProd_9_id, cartProd_10_id, cartProd_11_id, cartProd_12_id)
VALUES 
(1, 1, 1, FALSE, 50.00, 10.00, 100.00, 'Bank A', 'Card1234', NOW(), NOW(), NOW(), NOW(), 'Courier', 1, 2, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL),
(2, 2, 3, TRUE, 100.00, 20.00, 200.00, 'Bank B', 'Card5678', NOW(), NOW(), NOW(), NOW(), 'Courier', 3, 4, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL);