import { useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8001";

function App() {
  const [page, setPage] = useState("home");

  // -------------------------
  // CREATE ACCOUNT
  // -------------------------
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [accountType, setAccountType] = useState("SAVINGS");
  const [message, setMessage] = useState("");
  const [createdAccount, setCreatedAccount] = useState(null);

  // -------------------------
  // VIEW ACCOUNT
  // -------------------------
  const [accountId, setAccountId] = useState("");
  const [account, setAccount] = useState(null);
  const [viewMessage, setViewMessage] = useState("");

  // -------------------------
  // DEPOSIT / WITHDRAW
  // -------------------------
  const [amount, setAmount] = useState("");
  const [actionMessage, setActionMessage] = useState("");

  // -------------------------
  // TRANSACTIONS
  // -------------------------
  const [transactions, setTransactions] = useState([]);
  const [transactionMessage, setTransactionMessage] = useState("");

  // =========================
  // CREATE ACCOUNT
  // =========================
  async function createAccount(event) {
    event.preventDefault();

    setMessage("");
    setCreatedAccount(null);

    try {
      const response = await fetch(`${API_URL}/api/accounts`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          name: name,
          email: email,
          accountType: accountType,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        setMessage(data.detail || "Unable to create account.");
        return;
      }

      setCreatedAccount(data);
      setMessage("Account created successfully!");

      // Clear form
      setName("");
      setEmail("");
      setAccountType("SAVINGS");
    } catch (error) {
      setMessage("Unable to connect to the bank API.");
    }
  }

  // =========================
  // GET ACCOUNT
  // =========================
  async function getAccount(event) {
    event.preventDefault();

    setAccount(null);
    setViewMessage("");
    setActionMessage("");

    try {
      const response = await fetch(
        `${API_URL}/api/accounts/${accountId}`
      );

      const data = await response.json();

      if (!response.ok) {
        setViewMessage(data.detail || "Account not found.");
        return;
      }

      setAccount(data);
    } catch (error) {
      setViewMessage("Unable to connect to the bank API.");
    }
  }

  // =========================
  // REFRESH ACCOUNT
  // =========================
  async function refreshAccount(id) {
    try {
      const response = await fetch(
        `${API_URL}/api/accounts/${id}`
      );

      const data = await response.json();

      if (response.ok) {
        setAccount(data);
      }
    } catch (error) {
      console.error("Unable to refresh account.");
    }
  }

  // =========================
  // DEPOSIT
  // =========================
  async function deposit(event) {
    event.preventDefault();

    setActionMessage("");

    if (!account) {
      setActionMessage("Please select an account first.");
      return;
    }

    if (Number(amount) <= 0) {
      setActionMessage("Deposit amount must be greater than 0.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/accounts/${account.account_id}/deposit`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: Number(amount),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setActionMessage(data.detail || "Deposit failed.");
        return;
      }

      setAccount(data);
      setActionMessage("Deposit successful!");
      setAmount("");
    } catch (error) {
      setActionMessage("Unable to connect to the bank API.");
    }
  }

  // =========================
  // WITHDRAW
  // =========================
  async function withdraw(event) {
    event.preventDefault();

    setActionMessage("");

    if (!account) {
      setActionMessage("Please select an account first.");
      return;
    }

    if (Number(amount) <= 0) {
      setActionMessage("Withdrawal amount must be greater than 0.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/accounts/${account.account_id}/withdraw`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            amount: Number(amount),
          }),
        }
      );

      const data = await response.json();

      if (!response.ok) {
        setActionMessage(data.detail || "Withdrawal failed.");
        return;
      }

      setAccount(data);
      setActionMessage("Withdrawal successful!");
      setAmount("");
    } catch (error) {
      setActionMessage("Unable to connect to the bank API.");
    }
  }

  // =========================
  // GET TRANSACTIONS
  // =========================
  async function getTransactions() {
    setTransactionMessage("");
    setTransactions([]);

    if (!account) {
      setTransactionMessage("Please select an account first.");
      return;
    }

    try {
      const response = await fetch(
        `${API_URL}/api/accounts/${account.account_id}/transactions`
      );

      const data = await response.json();

      if (!response.ok) {
        setTransactionMessage(
          data.detail || "Unable to load transactions."
        );
        return;
      }

      setTransactions(data);

      if (data.length === 0) {
        setTransactionMessage("No transactions found.");
      }

      setPage("transactions");
    } catch (error) {
      setTransactionMessage("Unable to connect to the bank API.");
    }
  }

  // =========================
  // GO BACK TO ACCOUNT
  // =========================
  async function returnToAccount() {
    if (account) {
      await refreshAccount(account.account_id);
    }

    setPage("view");
  }

  return (
    <div className="app">

      {/* HEADER */}
      <header>
        <h1>Simple Bank Application</h1>
        <p>Banking made simple</p>
      </header>

      {/* ===================== */}
      {/* HOME */}
      {/* ===================== */}

      {page === "home" && (
        <main className="card">
          <h2>Welcome</h2>

          <p>What would you like to do?</p>

          <div className="button-group">
            <button onClick={() => setPage("create")}>
              Create Account
            </button>

            <button onClick={() => setPage("view")}>
              View Account
            </button>
          </div>
        </main>
      )}

      {/* ===================== */}
      {/* CREATE ACCOUNT */}
      {/* ===================== */}

      {page === "create" && (
        <main className="card">
          <h2>Create Account</h2>

          <form onSubmit={createAccount}>
            <div className="form-group">
              <label>Name</label>

              <input
                type="text"
                value={name}
                onChange={(event) =>
                  setName(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Email</label>

              <input
                type="email"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                required
              />
            </div>

            <div className="form-group">
              <label>Account Type</label>

              <select
                value={accountType}
                onChange={(event) =>
                  setAccountType(event.target.value)
                }
              >
                <option value="SAVINGS">
                  Savings
                </option>

                <option value="CHECKING">
                  Checking
                </option>
              </select>
            </div>

            <div className="button-group">
              <button type="submit">
                Create Account
              </button>

              <button
                type="button"
                onClick={() => setPage("home")}
              >
                Back
              </button>
            </div>
          </form>

          {message && (
            <p className="message">
              {message}
            </p>
          )}

          {createdAccount && (
            <div className="account-result">
              <h3>Account Created</h3>

              <p>
                Account ID: {createdAccount.account_id}
              </p>

              <p>
                User ID: {createdAccount.user_id}
              </p>

              <p>
                Name: {createdAccount.user_name}
              </p>

              <p>
                Balance: ${createdAccount.balance}
              </p>

              <p>
                Type: {createdAccount.account_type}
              </p>
            </div>
          )}
        </main>
      )}

      {/* ===================== */}
      {/* VIEW ACCOUNT */}
      {/* ===================== */}

      {page === "view" && (
        <main className="card">
          <h2>View Account</h2>

          <form onSubmit={getAccount}>
            <div className="form-group">
              <label>Account ID</label>

              <input
                type="number"
                min="1"
                value={accountId}
                onChange={(event) =>
                  setAccountId(event.target.value)
                }
                required
              />
            </div>

            <div className="button-group">
              <button type="submit">
                View Account
              </button>

              <button
                type="button"
                onClick={() => {
                  setAccount(null);
                  setViewMessage("");
                  setActionMessage("");
                  setPage("home");
                }}
              >
                Back
              </button>
            </div>
          </form>

          {viewMessage && (
            <p className="message">
              {viewMessage}
            </p>
          )}

          {account && (
            <>
              <div className="account-result">
                <h3>Account Details</h3>

                <p>
                  <strong>Account ID:</strong>{" "}
                  {account.account_id}
                </p>

                <p>
                  <strong>User ID:</strong>{" "}
                  {account.user_id}
                </p>

                <p>
                  <strong>Name:</strong>{" "}
                  {account.user_name}
                </p>

                <p>
                  <strong>Balance:</strong> $
                  {Number(account.balance).toFixed(2)}
                </p>

                <p>
                  <strong>Account Type:</strong>{" "}
                  {account.account_type}
                </p>
              </div>

              <div className="bank-actions">
                <h3>Banking Actions</h3>

                <div className="form-group">
                  <label>Amount</label>

                  <input
                    type="number"
                    min="0.01"
                    step="0.01"
                    placeholder="Enter amount"
                    value={amount}
                    onChange={(event) =>
                      setAmount(event.target.value)
                    }
                  />
                </div>

                <div className="button-group">
                  <button onClick={deposit}>
                    Deposit
                  </button>

                  <button onClick={withdraw}>
                    Withdraw
                  </button>

                  <button onClick={getTransactions}>
                    Transactions
                  </button>
                </div>

                {actionMessage && (
                  <p className="message">
                    {actionMessage}
                  </p>
                )}
              </div>
            </>
          )}
        </main>
      )}

      {/* ===================== */}
      {/* TRANSACTIONS */}
      {/* ===================== */}

      {page === "transactions" && (
        <main className="card transaction-card">

          <h2>Transaction History</h2>

          {account && (
            <div className="transaction-account-info">
              <p>
                <strong>Account ID:</strong>{" "}
                {account.account_id}
              </p>

              <p>
                <strong>Name:</strong>{" "}
                {account.user_name}
              </p>

              <p>
                <strong>Current Balance:</strong> $
                {Number(account.balance).toFixed(2)}
              </p>
            </div>
          )}

          {transactionMessage && (
            <p className="message">
              {transactionMessage}
            </p>
          )}

          {transactions.length > 0 && (
            <div className="transaction-list">

              {transactions.map((transaction) => (
                <div
                  className="transaction-item"
                  key={transaction.txn_id}
                >
                  <p>
                    <strong>Transaction ID:</strong>{" "}
                    {transaction.txn_id}
                  </p>

                  <p>
                    <strong>Type:</strong>{" "}
                    {transaction.txn_type}
                  </p>

                  <p>
                    <strong>Amount:</strong> $
                    {Number(transaction.amount).toFixed(2)}
                  </p>

                  <p>
                    <strong>Date:</strong>{" "}
                    {new Date(
                      transaction.created_at
                    ).toLocaleString()}
                  </p>
                </div>
              ))}

            </div>
          )}

          <div className="button-group">
            <button onClick={returnToAccount}>
              Back to Account
            </button>

            <button onClick={() => setPage("home")}>
              Home
            </button>
          </div>

        </main>
      )}

    </div>
  );
}

export default App;