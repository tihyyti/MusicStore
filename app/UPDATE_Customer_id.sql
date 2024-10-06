DELETE FROM mstore_v1.Customer WHERE id = 1;
DELETE FROM mstore_v1.Customer WHERE id = 2;
DELETE FROM mstore_v1.Customer WHERE id = 3;
DELETE FROM mstore_v1.Customer WHERE id = 4;
UPDATE mstore_v1.ShoppingCart
SET cartcustomer_id = 1
WHERE cartcustomer_id = 33;
UPDATE mstore_v1.ShoppingCart
SET cartcustomer_id = 2
WHERE cartcustomer_id = 34;
UPDATE mstore_v1.ShoppingCart
SET cartcustomer_id = 3
WHERE cartcustomer_id = 35;
UPDATE mstore_v1.ShoppingCart
SET cartcustomer_id = 4
WHERE cartcustomer_id = 36;




