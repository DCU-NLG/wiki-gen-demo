import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';

function FormComponent({ onQuery, wikiPage, setWikiPage }) {
  const [categories, setCategories] = useState([]);
  const [dataSources, setDataSources] = useState([]);
  const [languages, setLanguages] = useState({});
  const [models, setModels] = useState([]);
  const [formData, setFormData] = useState({
    category: '',
    dataSource: '',
    language: '',
    model: '',
    subject: ''
  });

  useEffect(() => {
    async function fetchFormData() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/form-data');
        setCategories(response.data.categories);
        setDataSources(response.data.data_sources);
        setLanguages(response.data.languages);
        setModels(response.data.models);
        setFormData({
          category: response.data.categories[0],
          dataSource: response.data.data_sources[0],
          language: Object.keys(response.data.languages)[0],
          model: response.data.models[0],
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
    if (formData.subject.trim()) {
      // reset wikipage on a new search
      if(wikiPage.title !== ''){
        setWikiPage({ title: '', content: '' })
      }
      onQuery({
        entity_name: formData.subject,
        category: formData.category,
        language: formData.language,
        data_source: formData.dataSource
      });
    } else {
      alert('Subject cannot be empty');
    }
  };

  return (
    <div className="col-md-8">
      <h1>Seed Wikipedia Generator</h1>
      <form onSubmit={handleSubmit}>
        <div className="form-group" style={{ paddingBottom: '15px' }}>
          <label htmlFor="categorySelect">Select Category:</label>
          <select className="form-control" id="categorySelect" name="category" value={formData.category} onChange={handleChange}>
            {categories.map(category => (
              <option key={category} value={category}>{category}</option>
            ))}
          </select>
        </div>
        <div className="form-group" style={{ paddingBottom: '15px' }}>
          <label htmlFor="dataSourceSelect">Select Data Source:</label>
          <select className="form-control" id="dataSourceSelect" name="dataSource" value={formData.dataSource} onChange={handleChange}>
            {dataSources.map(dataSource => (
              <option key={dataSource} value={dataSource}>{dataSource}</option>
            ))}
          </select>
        </div>
        <div className="form-group" style={{ paddingBottom: '15px' }}>
          <label htmlFor="languageSelect">Select Language:</label>
          <select className="form-control" id="languageSelect" name="language" value={formData.language} onChange={handleChange}>
            {Object.entries(languages).map(([code, name]) => (
              <option key={code} value={code}>{name}</option>
            ))}
          </select>
        </div>
        <div className="form-group" style={{ paddingBottom: '15px' }}>
          <label htmlFor="modelSelect">Select Model:</label>
          <select className="form-control" id="modelSelect" name="model" value={formData.model} onChange={handleChange}>
            {Object.entries(models).map(([key, value]) => (
              <option key={key} value={key}>{value}</option>
            ))}
          </select>
        </div>
        <div className="form-group" style={{ paddingBottom: '15px' }}>
          <label htmlFor="subjectInput">Subject:</label>
          <input type="text" className="form-control" id="subjectInput" name="subject" value={formData.subject} onChange={handleChange} />
        </div>
        <button type="submit" className="btn btn-primary">Query</button>
      </form>
    </div>
  );
}

export default FormComponent;
