import { useState } from "react";

function App() {

  const [formData, setFormData] = useState({
    age: "",
    annual_income: "",
    tenure_months: "",
    avg_monthly_balance: "",
    monthly_transaction_count: "",
    balance_decline_percentage: "",
    unresolved_complaint_count: "",
    escalation_count: "",
    total_digital_logins: ""
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {

    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });

  };

  const predictChurn = async () => {

    try {

      const response = await fetch(
        "http://127.0.0.1:8000/predict",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            age: Number(formData.age),
            annual_income: Number(formData.annual_income),
            tenure_months: Number(formData.tenure_months),
            avg_monthly_balance:
              Number(formData.avg_monthly_balance),

            monthly_transaction_count:
              Number(formData.monthly_transaction_count),

            balance_decline_percentage:
              Number(formData.balance_decline_percentage),

            unresolved_complaint_count:
              Number(formData.unresolved_complaint_count),

            escalation_count:
              Number(formData.escalation_count),

            total_digital_logins:
              Number(formData.total_digital_logins)
          })
        }
      );

      const data = await response.json();

      setResult(data);

    } catch (error) {

      alert("Backend connection failed");

      console.log(error);

    }

  };

  return (

    <div style={styles.app}>

      {/* NAVBAR */}

      <div style={styles.navbar}>

        <h1 style={styles.logo}>
          ChurnZero AI
        </h1>

        <div style={styles.navLinks}>

          <span>Dashboard</span>
          <span>Predictions</span>
          <span>Analytics</span>
          <span>Retention</span>

        </div>

      </div>

      {/* HERO SECTION */}

      <div style={styles.hero}>

        <div>

          <h1 style={styles.heroTitle}>
            AI Banking Churn Intelligence
          </h1>

          <p style={styles.heroText}>
            Predict customer churn using AI and
            generate personalized retention strategies.
          </p>

        </div>

        <div style={styles.heroCard}>

          <h2>AI Monitoring</h2>

          <h1>99.98%</h1>

          <p>Real-Time Prediction Accuracy</p>

        </div>

      </div>

      {/* MAIN SECTION */}

      <div style={styles.mainSection}>

        {/* FORM */}

        <div style={styles.card}>

          <h2 style={styles.cardTitle}>
            Customer Information
          </h2>

          <div style={styles.formGrid}>

            <input
              style={styles.input}
              type="number"
              placeholder="Age"
              name="age"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Annual Income"
              name="annual_income"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Tenure Months"
              name="tenure_months"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Avg Monthly Balance"
              name="avg_monthly_balance"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Monthly Transactions"
              name="monthly_transaction_count"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Balance Decline %"
              name="balance_decline_percentage"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Unresolved Complaints"
              name="unresolved_complaint_count"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Escalation Count"
              name="escalation_count"
              onChange={handleChange}
            />

            <input
              style={styles.input}
              type="number"
              placeholder="Total Digital Logins"
              name="total_digital_logins"
              onChange={handleChange}
            />

          </div>

          <button
            style={styles.button}
            onClick={predictChurn}
          >
            Predict Customer Churn
          </button>

        </div>

        {/* RESULT */}

        <div style={styles.resultCard}>

          <h2 style={styles.cardTitle}>
            AI Prediction Results
          </h2>

          {result ? (

            <div>

              <h1 style={styles.riskText}>
                {result.risk_level} RISK
              </h1>

              <h2 style={styles.probability}>
                Churn Probability:
                {" "}
                {(result.churn_probability * 100).toFixed(2)}%
              </h2>

              <div style={styles.strategyBox}>

                <h3>Retention Strategies</h3>

                <ul>

                  {result.retention_recommendations.map(
                    (item, index) => (
                      <li key={index}>
                        {item}
                      </li>
                    )
                  )}

                </ul>

              </div>

            </div>

          ) : (

            <div style={styles.placeholder}>

              <h2>No Prediction Yet</h2>

              <p>
                Enter customer data and click
                predict to generate AI insights.
              </p>

            </div>

          )}

        </div>

      </div>

    </div>

  );

}

const styles = {

  app: {

    minHeight: "100vh",

    background:
      "linear-gradient(135deg, #dbeafe 0%, #bfdbfe 50%, #93c5fd 100%)",

    padding: "20px",

    fontFamily: "Arial",

    color: "#0f172a"
  },

  navbar: {

    display: "flex",

    justifyContent: "space-between",

    alignItems: "center",

    background: "white",

    padding: "20px 40px",

    borderRadius: "20px",

    marginBottom: "30px",

    boxShadow: "0px 4px 15px rgba(0,0,0,0.1)"
  },

  logo: {

    color: "#2563eb",

    fontSize: "32px"
  },

  navLinks: {

    display: "flex",

    gap: "30px",

    fontSize: "18px",

    fontWeight: "bold"
  },

  hero: {

    display: "flex",

    justifyContent: "space-between",

    alignItems: "center",

    background: "white",

    padding: "40px",

    borderRadius: "25px",

    marginBottom: "30px",

    boxShadow: "0px 4px 20px rgba(0,0,0,0.1)"
  },

  heroTitle: {

    fontSize: "50px",

    marginBottom: "20px",

    color: "#1e3a8a"
  },

  heroText: {

    fontSize: "20px",

    width: "70%"
  },

  heroCard: {

    background:
      "linear-gradient(135deg, #2563eb, #38bdf8)",

    padding: "40px",

    borderRadius: "20px",

    color: "white",

    textAlign: "center",

    minWidth: "250px"
  },

  mainSection: {

    display: "flex",

    gap: "30px"
  },

  card: {

    flex: 1,

    background: "white",

    padding: "30px",

    borderRadius: "25px",

    boxShadow: "0px 4px 20px rgba(0,0,0,0.1)"
  },

  resultCard: {

    flex: 1,

    background: "white",

    padding: "30px",

    borderRadius: "25px",

    boxShadow: "0px 4px 20px rgba(0,0,0,0.1)"
  },

  cardTitle: {

    fontSize: "32px",

    marginBottom: "30px",

    textAlign: "center"
  },

  formGrid: {

    display: "grid",

    gridTemplateColumns: "1fr 1fr",

    gap: "20px"
  },

  input: {

    padding: "18px",

    borderRadius: "15px",

    border: "2px solid #93c5fd",

    fontSize: "16px",

    outline: "none"
  },

  button: {

    width: "100%",

    marginTop: "30px",

    padding: "18px",

    border: "none",

    borderRadius: "15px",

    background:
      "linear-gradient(135deg, #2563eb, #38bdf8)",

    color: "white",

    fontSize: "18px",

    fontWeight: "bold",

    cursor: "pointer"
  },

  riskText: {

    fontSize: "50px",

    color: "#dc2626",

    textAlign: "center"
  },

  probability: {

    textAlign: "center",

    marginTop: "20px",

    marginBottom: "30px"
  },

  strategyBox: {

    background: "#eff6ff",

    padding: "20px",

    borderRadius: "15px"
  },

  placeholder: {

    textAlign: "center",

    marginTop: "100px",

    color: "#475569"
  }

};

export default App;