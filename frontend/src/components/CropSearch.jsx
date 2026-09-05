import React, { useState } from "react";
import axios from "axios";

const CropSearch = () => {
  const [crop, setCrop] = useState("");
  const [query, setQuery] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    try {
      setError("");
      setResult(null);

      const res = await axios.post("http://localhost:5000/api/query/search", {
        crop,
        query,
      });

      setResult(res.data.data[0]);
    } catch (err) {
      setError("No crop issue found");
    }
  };

  return (
    <div style={styles.container}>
      <h2>AgroNex Crop Disease Assistant</h2>

      <select
        value={crop}
        onChange={(e) => setCrop(e.target.value)}
        style={styles.input}
      >
        <option value="">Select Crop</option>
        <option>Paddy</option>
        <option>Tea</option>
        <option>Wheat</option>
        <option>Cardamom</option>
        <option>Rose</option>
        <option>Coconut</option>
        <option>Tulsi</option>
        <option>Banana</option>
        <option>Cotton</option>
        <option>Turmeric</option>
      </select>

      <input
        type="text"
        placeholder="Enter symptom..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={styles.input}
      />

      <button onClick={handleSearch} style={styles.button}>
        Search Solution
      </button>

      {error && <p style={{ color: "red" }}>{error}</p>}

      {result && (
        <div style={styles.card}>
          <h3>Result</h3>
          <p><strong>Crop:</strong> {result.crop}</p>
          <p><strong>Issue:</strong> {result.issue}</p>
          <p><strong>Symptom:</strong> {result.symptom}</p>
          <p><strong>Solution:</strong> {result.solution}</p>
        </div>
      )}
    </div>
  );
};

const styles = {
  container: {
    maxWidth: "500px",
    margin: "40px auto",
    padding: "20px",
    border: "1px solid #ddd",
    borderRadius: "10px",
    textAlign: "center",
  },
  input: {
    width: "100%",
    padding: "10px",
    marginBottom: "15px",
  },
  button: {
    padding: "10px 20px",
    cursor: "pointer",
  },
  card: {
    marginTop: "20px",
    padding: "15px",
    border: "1px solid green",
    borderRadius: "10px",
    textAlign: "left",
  },
};

export default CropSearch;