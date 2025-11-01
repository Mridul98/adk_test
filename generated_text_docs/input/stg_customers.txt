## Overview  
This model cleans raw customer data by trimming and formatting names, normalizing email addresses, converting timestamps to dates, and ensuring an active status flag. It filters out records with invalid email formats and outputs a tidy customer table.

## Tables Involved  
- **raw.customers**: Source table containing unprocessed customer information.

## Columns Used  
**raw.customers**:  
- `raw.customers.customer_id` – Unique identifier for the customer.  
- `raw.customers.first_name` – Customer's first name; trimmed and capitalized in the output.  
- `raw.customers.last_name` – Customer's last name; trimmed and capitalized in the output.  
- `raw.customers.email` – Email address; lowercased and filtered to include only rows containing “@”.  
- `raw.customers.region` – Customer region; trimmed and capitalized in the output.  
- `raw.customers.created_at` – Creation timestamp; converted to a date in the output.  
- `raw.customers.is_active` – Active status flag; defaults to TRUE if NULL.

## Logic Explanation  
1. **CTE `cleaned`**  
   - **Source**: `raw.customers`.  
   - **Filters**: Keeps only rows where `email` contains an “@” character.  
   - **Transformations**:  
     - `first_name` and `last_name` are trimmed of whitespace and converted to title case (`INITCAP`).  
     - `email` is converted to lowercase.  
     - `region` is trimmed and title‑cased.  
     - `created_at` is parsed into a date using `TRY_TO_DATE`.  
     - `is_active` is set to `TRUE` when NULL via `COALESCE`.  
   - **Output columns**: `customer_id`, cleaned `first_name`, cleaned `last_name`, cleaned `email`, cleaned `region`, parsed `created_at`, and cleaned `is_active`.  

2. **Final SELECT**  
   - Returns all columns from the `cleaned` CTE, providing a single, cleaned view of customer data.

## Grain of Data  
One row per customer (`customer_id`), representing the cleaned customer record.
