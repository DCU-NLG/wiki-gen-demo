import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap';

const WiRDescr = `The Women in Red WikiProject focuses on creating content regarding women's biographies,
women's works, and women's issues. The objective is to turn "redlinks" on Wikipedia into blue ones, and by doing so,
reduce Wikipedia's systematic gaps in its coverage of under-represented groups`;

function FormComponent(props) {
  const base_url = process.env.REACT_APP_BACKEND_BASE_ENDPOINT;

  // Unpack props
  const { onQuery, wikiPage, setWikiPage, formData, setFormData, showAlert, setShowAlert, alertMessage, setAlertMessage } = props;

  // States
  const [dataSources, setDataSources] = useState([]);
  const [languages, setLanguages] = useState({});
  const [models, setModels] = useState({});

  useEffect(() => {
    async function fetchFormData() {
      try {
        const response = await axios.get(`${base_url}/form-data`);
        setDataSources(response.data.data_sources);
        setLanguages(response.data.languages);
        setModels(response.data.models);
        setFormData({
          dataSource: response.data.data_sources[0],
          language: Object.keys(response.data.languages)[0],
          model: [Object.keys(response.data.models)[0]], // Set initial model key as an array
          subject: '',
          gender: 'N\\A' // Set default gender
        });
      } catch (error) {
        console.error('Error fetching form data:', error);
      }
    }
    fetchFormData();
  }, []);

  const handleChange = (e) => {
    const { name, value, options } = e.target;
    if (name === 'model') {
      // Handle multi-select for models
      const selectedModels = [];
      for (const option of options) {
        if (option.selected) {
          selectedModels.push(option.value);
        }
      }
      setFormData({
        ...formData,
        [name]: selectedModels
      });
    } else {
      setFormData({
        ...formData,
        [name]: value
      });
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setShowAlert(false);
    if (formData.subject.trim()) {
      // Reset wikipage on a new search
      if (wikiPage.title !== '') {
        setWikiPage({ title: '', content: '' });
      }
      onQuery({
        entity_name: formData.subject,
        language: formData.language,
        data_source: formData.dataSource,
        model: formData.model, // Send model keys to backend as an array
        gender: formData.gender // Include gender in the query
      });
    } else {
      setAlertMessage('Entity cannot be empty');
      setShowAlert(true);
    }
  };

  return (
    <Container>
      <Row>
        <Col>
          <h2>Generate seed Wikipedia page</h2>
          {showAlert && <Alert variant="danger" onClose={() => setShowAlert(false)} dismissible>{alertMessage}</Alert>}
          <Form onSubmit={handleSubmit}>
            <div style={{ border: '1.5px solid', padding: '10px', marginBottom: '10px' }}>
              <Form.Group controlId="subjectInput" className="mb-3">
                <Form.Label>Entity:</Form.Label>
                <Form.Control
                  type="text"
                  name="subject"
                  value={formData.subject}
                  onChange={handleChange}
                  placeholder="Type in an entity (person, place, organization, artistic or intellectual work etc.)"
                />
              </Form.Group>
              {/* ----- WiR box ------*/}
              <div className="woman-in-red-box">
                <p style={{ color: 'white' }}>Or select a Woman in Red (filter by occupation):</p>
                <Row>
                    <Col md={6}>
                      <Form.Group controlId="occupationInput" className="mb-3">
                        <Form.Control
                            as="select"
                            name="occupation"
                            value={formData.occupation}
                            onChange={handleChange}
                        >
                          <option>-- Occupation --</option>
                        </Form.Control>
                      </Form.Group>
                      <Form.Group controlId="womanInRedSelect" className="mb-3">
                        <Form.Control
                          as="select"
                          name="womanInRed"
                          value={formData.womanInRed}
                          onChange={handleChange}
                        >
                          <option>-- Woman in Red --</option>
                        </Form.Control>
                      </Form.Group>
                    </Col>
                    <Col md={6} style={{ textAlign: 'left', fontSize: '0.8em', color: 'white' }}>
                      <p>{WiRDescr}</p>
                    </Col>
                  </Row>
                </div>
            </div>
            <Form.Group controlId="genderSelect" className="mb-3">
              <Form.Label>Select Grammatical Gender:</Form.Label>
              <Form.Control
                  as="select"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
              >
                <option value="N\\A">N/A</option>
                <option value="Male">Masculine</option>
                <option value="Female">Feminine</option>
                <option value="Neutral">Neutral</option>
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
              <Form.Label>Select at least one model:</Form.Label>
              <Form.Control
                as="select"
                name="model"
                value={formData.model}
                onChange={handleChange}
                multiple // Enable multiple selection
              >
                {Object.entries(models).map(([key, fullName]) => (
                  <option key={key} value={key}>
                    {fullName}
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
            <Button variant="primary" type="submit">
              Query Data Source
            </Button>
          </Form>
        </Col>
      </Row>
    </Container>
  );
}

export default FormComponent;