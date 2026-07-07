# Personal Finance Manager #

  A Flask-based REST API for managing personal finances with SQLite database, statistical analysis, and linear regression income forecasting.


# Installation #

  1. Clone or Download the Project

  ```bash
  cd Assignment_V2
  ```

  2. Create a Virtual Environment

  **On Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

  **On macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

  3. Install Dependencies

  ```bash
  pip install -r requirements.txt
  ```


# Running the Application #

  1. Start the Flask Server

  ```bash
  python app.py
  ```

  You should see:
  ```
  * Running on http://127.0.0.1:5000
  * Debug mode: on
  ```

  The API is now accessible at `http://localhost:5000`

  **Keep this terminal running!**


# API Endpoints #

  ### Accounts

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | POST | `/accounts` | Create a new account |
  | GET | `/accounts` | List all accounts |
  | GET | `/accounts/<id>` | Get single account |
  | PUT | `/accounts/<id>` | Update account |
  | DELETE | `/accounts/<id>` | Delete account |

  ### Income

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | POST | `/income` | Create income record |
  | GET | `/income` | List all income |
  | GET | `/income?from=YYYY-MM-DD&to=YYYY-MM-DD` | List income with date filter |
  | GET | `/income/<id>` | Get single income record |
  | PUT | `/income/<id>` | Update income |
  | DELETE | `/income/<id>` | Delete income |

  ### Transactions

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | POST | `/transactions` | Create transaction |
  | GET | `/transactions` | List all transactions |
  | GET | `/transactions?from=YYYY-MM-DD&to=YYYY-MM-DD` | List with date filter |
  | GET | `/transactions/<id>` | Get single transaction |
  | PUT | `/transactions/<id>` | Update transaction |
  | DELETE | `/transactions/<id>` | Delete transaction |

  ### Statistics & Forecasting

  | Method | Endpoint | Description |
  |--------|----------|-------------|
  | GET | `/stats/summary` | Get statistical summary |
  | GET | `/stats/summary?from=YYYY-MM-DD&to=YYYY-MM-DD` | Get stats with date filter |
  | GET | `/stats/income_forecast?n_months=3` | Get income forecast |


# API Calls Using Postman
  {{base_url}}: http://localhost:5000

  ## Accounts API

    ### 1. Create Account

      **Method:** `POST`
      **URL:** `{{base_url}}/accounts`
      **Body:**
      ```json
      {
        "id": "A1",
        "name": "My Savings Account",
        "currency": "USD"
      }
      ```
      **Expected Output (201):**
      ```json
      {
        "id": "A1",
        "name": "My Savings Account",
        "currency": "USD"
      }
      ```

    ### 2. Get All Accounts

      **Method:** `GET`
      **URL:** `{{base_url}}/accounts`
      **Body:** None
      **Expected Output (200):**
      ```json
      [
        {
          "id": "A1",
          "name": "My Savings Account",
          "currency": "USD"
        }
      ]
      ```

    ### 3. Get Single Account

      **Method:** `GET`
      **URL:** `{{base_url}}/accounts/A1`
      **Body:** None
      **Expected Output (200):**
      ```json
      {
        "id": "A1",
        "name": "My Savings Account",
        "currency": "USD"
      }
      ```

    ### 4. Update Account

      **Method:** `PUT`
      **URL:** `{{base_url}}/accounts/A1`
      **Body:**
      ```json
      {
        "name": "Updated Savings Account",
        "currency": "EUR"
      }
      ```
      **Expected Output (200):**
      ```json
      {
        "id": "A1",
        "name": "Updated Savings Account",
        "currency": "EUR"
      }
      ```

    ### 5. Delete Account

      **Method:** `DELETE`
      **URL:** `{{base_url}}/accounts/A1`
      **Body:** None
      **Expected Output (200):**
      ```json
      {
        "message": "Account deleted successfully"
      }
      ```

  ## Income API

    ### 6. Create Income

      **Method:** `POST`
      **URL:** `{{base_url}}/income`
      **Body:**
      ```json
      {
        "id": "I1",
        "account_id": "A1",
        "date": "2025-01-15",
        "amount": 3000,
        "source": "Salary"
      }
      ```
      **Expected Output (201):**
      ```json
      {
        "id": "I1",
        "account_id": "A1",
        "date": "2025-01-15",
        "amount": 3000,
        "source": "Salary"
      }
      ```

    ### 7. Create Income (Second Entry)

      **Method:** `POST`
      **URL:** `{{base_url}}/income`
      **Body:**
      ```json
      {
        "id": "I2",
        "account_id": "A1",
        "date": "2025-02-15",
        "amount": 3200,
        "source": "Salary"
      }
      ```
      **Expected Output (201):**
      ```json
      {
        "id": "I2",
        "account_id": "A1",
        "date": "2025-02-15",
        "amount": 3200,
        "source": "Salary"
      }
      ```

    ### 8. Get All Income

      **Method:** `GET`
      **URL:** `{{base_url}}/income`
      **Body:** None
      **Expected Output (200):**
      ```json
      [
        {
          "id": "I1",
          "account_id": "A1",
          "date": "2025-01-15",
          "amount": 3000,
          "source": "Salary"
        },
        {
          "id": "I2",
          "account_id": "A1",
          "date": "2025-02-15",
          "amount": 3200,
          "source": "Salary"
        }
      ]
      ```

    ### 9. Get Single Income

      **Method:** `GET`
      **URL:** `{{base_url}}/income/I1`
      **Body:** None
      **Expected Output (200):**
      ```json
      {
        "id": "I1",
        "account_id": "A1",
        "date": "2025-01-15",
        "amount": 3000,
        "source": "Salary"
      }
      ```

    ### 10. Update Income

      **Method:** `PUT`
      **URL:** `{{base_url}}/income/I1`
      **Body:**
      ```json
      {
        "amount": 3500,
        "source": "Salary + Bonus"
      }
      ```
      **Expected Output (200):**
      ```json
      {
        "id": "I1",
        "account_id": "A1",
        "date": "2025-01-15",
        "amount": 3500,
        "source": "Salary + Bonus"
      }
      ```

    ### 11. Delete Income

      **Method:** `DELETE`
      **URL:** `{{base_url}}/income/I1`
      **Body:** None
      **Expected Output (200):**
      ```json
      {
        "message": "Income deleted successfully"
      }
      ```

  ## Transactions API

    ### 12. Create Transaction

      **Method:** `POST`
      **URL:** `{{base_url}}/transactions`
      **Body:**
      ```json
      {
        "id": "T1",
        "account_id": "A1",
        "date": "2025-01-20",
        "amount": 200,
        "type": "expense",
        "category": "Food",
        "note": "Groceries"
      }
      ```
      **Expected Output (201):**
      ```json
      {
        "id": "T1",
        "account_id": "A1",
        "date": "2025-01-20",
        "amount": 200,
        "type": "expense",
        "category": "Food",
        "note": "Groceries"
      }
      ```

    ### 13. Get All Transactions

      **Method:** `GET`
      **URL:** `{{base_url}}/transactions`
      **Expected Output (200):**
      ```json
      [
        {
          "id": "T1",
          "account_id": "A1",
          "date": "2025-01-20",
          "amount": 200,
          "type": "expense",
          "category": "Food",
          "note": "Groceries"
        }
      ]
      ```

    ### 14. Get Transactions by Date Range

      **Method:** `GET`
      **URL:** `{{base_url}}/transactions?from=2025-01-01&to=2025-01-10`
      **Expected Output (200):**
      ```json
      []
      ```

    ### 15. Get Single Transaction

      **Method:** `GET`
      **URL:** `{{base_url}}/transactions/T1`
      **Expected Output (200):**
      ```json
      {
        "id": "T1",
        "account_id": "A1",
        "date": "2025-01-20",
        "amount": 200,
        "type": "expense",
        "category": "Food",
        "note": "Groceries"
      }
      ```

    ### 16. Update Transaction

      **Method:** `PUT`
      **URL:** `{{base_url}}/transactions/T1`
      **Body:**
      ```json
      {
        "amount": 250,
        "note": "Groceries + snacks"
      }
      ```
      **Expected Output (200):**
      ```json
      {
        "id": "T1",
        "account_id": "A1",
        "date": "2025-01-20",
        "amount": 250,
        "type": "expense",
        "category": "Food",
        "note": "Groceries + snacks"
      }
      ```

    ### 17. Delete Transaction

      **Method:** `DELETE`
      **URL:** `{{base_url}}/transactions/T1`
      **Expected Output (200):**
      ```json
      {
        "message": "Transaction deleted successfully"
      }
      ```

  ## Statistics API ⭐

    ### 18. Get Statistics Summary

      **Method:** `GET`
      **URL:** `{{base_url}}/stats/summary`
      **Expected Output (200):**
      ```json
      {
          "by_category": {
              "bonus": 50000.0,
              "food": -10000.0
          },
          "stats": {
              "count": 2,
              "max": 50000.0,
              "mean": 20000.0,
              "median": 20000.0,
              "min": -10000.0,
              "std": 30000.0
          }
      }
      ```

    ### 19. Get Statistics Summary (Date Range)

      **Method:** `GET`
      **URL:** `{{base_url}}/stats/summary?from=2025-01-01&to=2025-01-10`
      **Expected Output (200):**
      ```json
      {
          "by_category": {
              "bonus": 50000.0
          },
          "stats": {
              "count": 1,
              "max": 50000.0,
              "mean": 50000.0,
              "median": 50000.0,
              "min": 50000.0,
              "std": 0.0
          }
      }
      ```

    ### 20. Get Income Forecast ⭐⭐

      **Method:** `GET`
      **URL:** `{{base_url}}/stats/income_forecast?n_months=3
      **Body:**
      ```json
      {
        "n_months": 3
      }
      **Expected Output (200):**
      ```json
      {
          "forecast": [
              {
                  "month": "2025-03",
                  "predicted_income": 300000.0
              },
              {
                  "month": "2025-04",
                  "predicted_income": 300000.0
              },
              {
                  "month": "2025-05",
                  "predicted_income": 300000.0
              }
          ],
          "history": [
              {
                  "income": 300000.0,
                  "month": "2025-01"
              },
              {
                  "income": 300000.0,
                  "month": "2025-02"
              }
          ]
      }
      ```


# Running Tests
  Run all tests:
  ```bash
  pytest tests/test_api.py -v
  ```
  **Expected output:**
  ```
  test_create_account_and_income_forecast PASSED
  test_transactions_summary PASSED
  test_account_crud_operations PASSED
  test_income_crud_operations PASSED
  test_transaction_crud_operations PASSED
  ...
  ========== X passed in X.XXs ==========
  ```