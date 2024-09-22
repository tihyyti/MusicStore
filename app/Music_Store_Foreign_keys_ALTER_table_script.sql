
SET search_path TO mstore_v1;
ALTER TABLE MStore_v1.Customer 
    ADD CONSTRAINT fk_customer_to_store 
	FOREIGN KEY(Store_id) REFERENCES MStore_v1.Store(id);

ALTER TABLE MStore_v1.Store 
    ADD CONSTRAINT fk_manager_to_customer
	FOREIGN KEY(storeManager_id) REFERENCES MStore_v1.Customer(id);

ALTER TABLE MStore_v1.ProductGroup 
	ADD CONSTRAINT fk_ProdGroup_to_Store
    FOREIGN KEY(Store_id) REFERENCES MStore_v1.Store(id);

ALTER TABLE MStore_v1.ShoppingCart 
    ADD CONSTRAINT fk_cart_to_store
    FOREIGN KEY(cartStore_id) REFERENCES MStore_v1.Store(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cart_to_Customer
    FOREIGN KEY(cartCustomer_id) REFERENCES MStore_v1.Customer(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_1_to_Product
    FOREIGN KEY(cartProd_1_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_2_to_Product
    FOREIGN KEY(cartProd_2_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_3_to_Product
    FOREIGN KEY(cartProd_3_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_4_to_Product
    FOREIGN KEY(cartProd_4_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_5_to_Product
    FOREIGN KEY(cartProd_5_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_6_to_Product
    FOREIGN KEY(cartProd_6_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_7_to_Product
    FOREIGN KEY(cartProd_7_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_8_to_Product
    FOREIGN KEY(cartProd_8_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_9_to_Product
    FOREIGN KEY(cartProd_9_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_10_to_Product
    FOREIGN KEY(cartProd_10_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_11_to_Product
    FOREIGN KEY(cartProd_11_id) REFERENCES MStore_v1.Product(id);
ALTER TABLE MStore_v1.ShoppingCart 
	ADD CONSTRAINT fk_cartProd_12_to_Product
    FOREIGN KEY(cartProd_12_id) REFERENCES MStore_v1.Product(id);

ALTER TABLE MStore_v1.Product 
    ADD CONSTRAINT fk_product_to_ProductGroup
    FOREIGN KEY(productGroup_id) REFERENCES MStore_v1.ProductGroup(id);
ALTER TABLE MStore_v1.Product 
	ADD CONSTRAINT fk_product_to_ProductImage
    FOREIGN KEY(productImage_id) REFERENCES MStore_v1.ProductImage(id);
