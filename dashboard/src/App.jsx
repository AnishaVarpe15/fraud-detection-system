import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [cases, setCases] = useState([]);

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:8000/login", {
        email,
        password,
      });
      if (response.data.success) {
        setUser(response.data);
      } else {
        setError(response.data.message);
      }
    } catch (err) {
      setError("Something went wrong. Please try again.");
    }
  };

  const fetchCases = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:8000/flagged-cases");
      setCases(response.data);
    } catch (err) {
      console.error("Failed to fetch cases", err);
    }
  };

  useEffect(() => {
    if (user) {
      fetchCases();
    }
  }, [user]);

  const handleDecision = async (caseId, decision) => {
    try {
      await axios.post("http://127.0.0.1:8000/investigator-action", {
        case_id: caseId,
        user_id: user.user_id,
        decision: decision,
        notes: "",
      });
      fetchCases(); // refresh the list after the decision
    } catch (err) {
      console.error("Failed to submit decision", err);
    }
  };

  if (user) {
    return (
      <div className="dashboard">
        <h2>Welcome, {user.name} ({user.role})</h2>
        <h3>Flagged Transactions</h3>
        <table>
          <thead>
            <tr>
              <th>Case ID</th>
              <th>Transaction ID</th>
              <th>Amount</th>
              <th>Fraud Score</th>
              <th>Reason</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {cases.map((c) => (
              <tr key={c.case_id}>
                <td>{c.case_id}</td>
                <td>{c.transaction_id}</td>
                <td>₹{c.amount}</td>
                <td>{(c.fraud_score * 100).toFixed(1)}%</td>
                <td>{c.reason}</td>
                <td>{c.status}</td>
                <td>
                  {c.status === "pending" ? (
                    <>
                      <button
                        className="approve"
                        onClick={() => handleDecision(c.case_id, "approved")}
                      >
                        Approve
                      </button>
                      <button
                        className="reject"
                        onClick={() => handleDecision(c.case_id, "rejected")}
                      >
                        Reject
                      </button>
                    </>
                  ) : (
                    <em>Done</em>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    );
  }

  return (
    <div className="container">
      <h2>Investigator Login</h2>
      <form onSubmit={handleLogin}>
        <div className="form-group">
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
        </div>
        {error && <p className="error">{error}</p>}
        <button type="submit">Log In</button>
      </form>
    </div>
  );
}

export default App;