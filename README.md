## Overview
The project is realized using Django and DRF. The endpoints are documented and testable at `/docs` and `/redoc`.

Each product can have 0..n stock items tied to itself. Each product can be tied to 0..n labels. The labels are indepentend from the products.

The code is inside a django app called `products`, which exposes the following urls:
- `products/`: Retrieves the paginated list of the products, with the products ordered by the related stock min price. Also allows creation.
- `products/{pk}`: Retrieves the specified product. Allows updates and deletes.
- `products/{pk}/stock`: Retrieves the stock for a given product. Allows the creation of new stock items for the given product.
- `products/{pk}/stock/{pk}`: Retrieves the specified stock for the given product. Allows updates and deletes. 
- `products/{pk}/labels`: Retrieves the labels tied to the given product. Allows the addition of new labels to the given product.
- `products/{pk}/labels/{pk}`: Retrieves the specified label for the given stock. Allows the removal of the specified label from the given product.
- `labels/`: Retrieves all labels, paginated. Allows creation.
- `labels/{pk}`: Retrieves the specified label. Allows updates and deletes.

### Data import
In `products/scripts` a `import.py` script is provided to retrieve the data from the provided URL and import it into the database. The script can be run with the `runscript` command, as shown in the "Running" section. It uses pydantic for validation.

### Database
The dbms is sqlite for simplicity.

### Running
From inside the repo directory, run:
```
pip install -r requirements.txt
python manage.py runscript products.scripts.import
python manage.py runserver
```
### Testing
From inside the repo directory, run:
```
python manage.py test
```