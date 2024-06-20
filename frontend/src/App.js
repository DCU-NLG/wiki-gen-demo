import React, { useState } from 'react';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css';
import FormComponent from './components/FormComponent';
import TriplesTable from './components/TriplesTable';
import WikiPage from './components/WikiPage';
import NavBar from './components/Navbar';
import Footer from './components/Footer';
import Instructions from './components/Instructions';
import Contact from './components/Contact';
import './App.css';

function App() {
  const [triples, setTriples] = useState([]);
  const [wikiPage, setWikiPage] = useState({ title: '', content: '' });
  const [formData, setFormData] = useState(null);

  const handleQuery = async (data) => {
    setFormData(data); // Store form data for later use
    try {
      const response = await axios.post('http://127.0.0.1:5000/query-triples', data);
      setTriples(response.data);
    } catch (error) {
      console.error('Error querying triples:', error);
    }
  };

  const handleGenerate = async (selectedTriples) => {
    if (formData) {
      try {
        const response = await axios.post('http://127.0.0.1:5000/generate', { model_name: formData.model, triplets: selectedTriples });
        setWikiPage({ title: response.data.title, content: response.data.content });
      } catch (error) {
        console.error('Error generating content:', error);
      }
    }
  };

  return (
    <Router>
      <NavBar />
      <div className="container-fluid">
        <Routes>
          <Route
            path="/"
            element={
              <div className="row">
                <FormComponent onQuery={handleQuery} wikiPage={wikiPage} setWikiPage={setWikiPage}/>
                {Object.keys(triples).length > 0 && <TriplesTable triples={triples} onGenerate={handleGenerate} />}
                {wikiPage.title && <WikiPage title={wikiPage.title} content={wikiPage.content} />}
              </div>
            }
          />
          <Route path="/instructions" element={<Instructions />} />
          <Route path="/contact" element={<Contact />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;
