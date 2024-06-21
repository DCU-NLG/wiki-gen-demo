import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';

function FormComponent(props) {
  const base_url = process.env.REACT_APP_BACKEND_BASE_ENDPOINT;

  // Unpack props
  const { onQuery,
    wikiPage, setWikiPage,
    formData, setFormData,
    showAlert, setShowAlert,
    alertMessage, setAlertMessage
  } = props;
  // States
  const [categories, setCategories] = useState([]);
  const [dataSources, setDataSources] = useState([]);
  const [languages, setLanguages] = useState({});
  const [models, setModels] = useState({});

  useEffect(() => {
    async function fetchFormData() {
      try {
        const response = await axios.get(`${base_url}/form-data`);
        setCategories(response.data.categories);
        setDataSources(response.data.data_sources);
        setLanguages(response.data.languages);
        setModels(response.data.models);
        setFormData({
          category: response.data.categories[0],
          dataSource: response.data.data_sources[0],
          language: Object.keys(response.data.languages)[0],
          model: Object.keys(response.data.models)[0], // Set initial model key
          subject: ''
        });
      } catch (error) {
        console.error('Error fetching form data:', error);
      }
    }
    fetchFormData();
  }, []);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowAlert(false);
    if (formData.subject.trim()) {
      // Reset wikipage on a new search
      if(wikiPage.title !== ''){
        setWikiPage({ title: '', content: '' })
      }
      onQuery({
        entity_name: formData.subject,
        category: formData.category,
        language: formData.language,
        data_source: formData.dataSource,
        model: formData.model, // Send model key to backend
      });
    } else {
      setAlertMessage('Subject cannot be empty');
      setShowAlert(true);
    }
  };

  return (
    <Container>
      <Row>
        <Col md={6}>
          <h2>Generate Wikipedia-like Page</h2>
          {showAlert && <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>{alertMessage}</Alert>}
          <Form onSubmit={handleSubmit}>
            <Form.Group controlId="categorySelect" className="mb-3">
              <Form.Label>Select Category:</Form.Label>
              <Form.Control
                as="select"
                name="category"
                value={formData.category}
                onChange={handleChange}
              >
                {categories.map((category) => (
                  <option key={category} value={category}>
                    {category}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="dataSourceSelect" className="mb-3">
              <Form.Label>Select Data Source:</Form.Label>
              <Form.Control
                as="select"
                name="dataSource"
                value={formData.dataSource}
                onChange={handleChange}
              >
                {dataSources.map((dataSource) => (
                  <option key={dataSource} value={dataSource}>
                    {dataSource}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="languageSelect" className="mb-3">
              <Form.Label>Select Language:</Form.Label>
              <Form.Control
                as="select"
                name="language"
                value={formData.language}
                onChange={handleChange}
              >
                {Object.entries(languages).map(([code, name]) => (
                  <option key={code} value={code}>
                    {name}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="modelSelect" className="mb-3">
              <Form.Label>Select Model:</Form.Label>
              <Form.Control
                as="select"
                name="model"
                value={formData.model}
                onChange={handleChange}
              >
                {Object.entries(models).map(([key, fullName]) => (
                  <option key={key} value={key}>
                    {fullName}
                  </option>
                ))}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="subjectInput" className="mb-3">
              <Form.Label>Subject:</Form.Label>
              <Form.Control
                type="text"
                name="subject"
                value={formData.subject}
                onChange={handleChange}
                placeholder="Enter the subject"
              />
            </Form.Group>
            <Button variant="primary" type="submit">
              Query
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default FormComponent;
