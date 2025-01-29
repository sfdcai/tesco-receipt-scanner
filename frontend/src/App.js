// frontend/src/App.js
import React, { useState } from "react";
import { Container, Button, Table, Form, Alert } from "react-bootstrap";
import Chart from "chart.js/auto";

function App() {
  const [file, setFile] = useState(null);
  const [data, setData] = useState([]);
  const [error, setError] = useState("");

  const handleUpload = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://localhost:8000/upload", {
        method: "POST",
        body: formData,
      });
      const result = await response.json();
      if (response.ok) {
        setData(result);
        setError("");
      } else {
        setError(result.detail || "Failed to process receipt.");
      }
    } catch (err) {
      setError("An error occurred while uploading the receipt.");
    }
  };

  return (
    <Container>
      <h1>Tesco Receipt Scanner</h1>
      <Form>
        <Form.Group>
          <Form.Label>Upload Receipt</Form.Label>
          <Form.Control type="file" onChange={(e) => setFile(e.target.files[0])} />
        </Form.Group>
        <Button onClick={handleUpload}>Upload</Button>
      </Form>

      {error && <Alert variant="danger">{error}</Alert>}

      {data.length > 0 && (
        <Table striped bordered>
          <thead>
            <tr>
              <th>Product</th>
              <th>Price</th>
              <th>Barcode</th>
            </tr>
          </thead>
          <tbody>
            {data.map((item, index) => (
              <tr key={index}>
                <td>{item.product}</td>
                <td>{item.price}</td>
                <td>{item.barcode}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      )}
    </Container>
  );
}

export default App;