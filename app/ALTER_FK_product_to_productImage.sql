ALTER TABLE MStore_v1.Product 
    ADD CONSTRAINT fk_product_to_ProductImage
    FOREIGN KEY(productImage_id) REFERENCES MStore_v1.ProductImage(id);