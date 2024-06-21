import React, { useState } from 'react';
import axios from 'axios';
import {BrowserRouter as Router, Routes, Route, Navigate} from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import FormComponent from './components/FormComponent';
import TriplesTable from './components/TriplesTable';
import WikiPage from './components/WikiPage';
import NavBar from './components/Navbar';
import Footer from './components/Footer';
import Instructions from './components/Instructions';
import Contact from './components/Contact';
import './App.css';

import { Container, Row } from 'react-bootstrap';

function App() {
  const base_url = process.env.REACT_APP_BACKEND_BASE_ENDPOINT;

  const [triples, setTriples] = useState([]);
  const [wikiPage, setWikiPage] = useState({ title: '', content: '' });
  const [formData, setFormData] = useState({
    category: '',
    dataSource: '',
    language: '',
    model: '',
    subject: ''
  });
  const [showAlert, setShowAlert] = useState(false);
  const [alertMessage, setAlertMessage] = useState('');

  const handleQuery = async (data) => {
    //setFormData(data); // Store form data for later use
    try {
      const response = await axios.post(`${base_url}/query-triples`, data);
      if (Object.keys(response.data).length === 0){
        setShowAlert(true);
        setAlertMessage("Unfortunately, no entity matching the subject was found");
      }
      setTriples(response.data);
    } catch (error) {
      console.error('Error querying triples:', error);
    }
  };

  const handleGenerate = async (selectedTriples) => {
    if (formData) {
      try {
        const response = await axios.post(
            `${base_url}/generate`,
            {
              model: formData.model,
              language: formData.language,
              dataSource: formData.dataSource,
              category: formData.category,
              triplets: selectedTriples
            }
        );

        setWikiPage({
          title: response.data.title,
          content: response.data.content
        });
      } catch (error) {
        console.error('Error generating content:', error);
      }
    }
  };

  return (
    <Router>
      <NavBar />
      <Container fluid className="app-container">
        <Routes>
          <Route
            path="/"
            element={
              <Row>
                  <FormComponent onQuery={handleQuery}
                                 wikiPage={wikiPage} setWikiPage={setWikiPage}
                                 formData={formData} setFormData={setFormData}
                                 showAlert={showAlert} setShowAlert={setShowAlert}
                                 alertMessage={alertMessage} setAlertMessage={setAlertMessage}/>
                  {Object.keys(triples).length > 0 && <TriplesTable triples={triples} onGenerate={handleGenerate} />}
                  {wikiPage.title && <WikiPage title={wikiPage.title} content={wikiPage.content} />}
              </Row>
            }
          />
          <Route path="/instructions" element={<Instructions />} />
          <Route path="/contact" element={<Contact />} />
          {/*default route / protection from unintended navigation */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Container>
      <Footer />
    </Router>
  );
}

export default App;
