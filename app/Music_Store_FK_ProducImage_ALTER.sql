-- Step 1: Drop the existing foreign key constraint
ALTER TABLE MStore_v1.Product
DROP CONSTRAINT fk_product_to_productimage;

-- Step 2: Add the new foreign key constraint
ALTER TABLE MStore_v1.Product
ADD CONSTRAINT fk_product_to_producimage
FOREIGN KEY (productimage_id) REFERENCES MStore_v1.Productimage(id);
ALTER TABLE Store
ADD last_login DATE;

ALTER TABLE Customer
ADD last_login DATE;