import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form, FormCheck } from 'react-bootstrap';
import { FaCopy, FaCheck, FaEdit, FaSave } from 'react-icons/fa'; // Import the copy and check icons


function WikiPage({ title, content }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editableContent, setEditableContent] = useState(content);
  const [selectedSection, setSelectedSection] = useState(0);
  const [copyStatus, setCopyStatus] = useState(false);

  useEffect(() => {
    setEditableContent(content);
  }, [content]);

  const handleEditClick = () => {
    setIsEditing(!isEditing);
  };

  const handleContentChange = (e, model) => {
    setEditableContent({
      ...editableContent,
      [model]: e.target.value,
    });
  };

  const handleSaveClick = () => {
    setIsEditing(false);
  };

  const handlePushClick = () => {
    console.log('Push button clicked');
  };

  const handleCheckboxChange = (index) => {
    setSelectedSection(index);
  };

  const handleCopyClick = (text) => {
    navigator.clipboard.writeText(text).then(() => {
      setCopyStatus(true);
      setTimeout(() => setCopyStatus(false), 2000);
    }).catch(err => {
      console.error('Failed to copy text: ', err);
    });
  };

  const modelEntries = Object.entries(editableContent);

  return (
    <Container>
      <Row className="justify-content-md-center">
        <Col md={6} className="text-center">
          <Card className="mb-4">
            <Card.Header className="bg-white d-flex align-items-center justify-content-between">
              <div className="d-flex align-items-center">
                <img
                  src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/103px-Wikipedia-logo-v2.svg.png"
                  alt="Wikipedia Icon"
                  style={{ height: '30px' }}
                  className="mr-2"
                />
                <span className="h1 font-weight-bold">&nbsp;&nbsp;{title}</span>
              </div>
              <div>
                <Button variant="outline-primary" className="me-2" onClick={handlePushClick}>
                  Open on Wikipedia
                </Button>

                <Button
                  variant="outline-secondary"
                  onClick={isEditing ? handleSaveClick : handleEditClick}
                >
                  {isEditing ?
                      <FaSave style={{ fontSize: '1.1em' }}/>
                      :
                      <FaEdit style={{ fontSize: '1.2em'}} />
                  }
                </Button>

                <Button
                  variant="outline-secondary"
                  className="ms-2" // Add margin to the left
                  onClick={() => handleCopyClick(modelEntries[selectedSection][1])}
                >
                  {copyStatus ? <FaCheck style={{ color: 'green' }} /> : <FaCopy />}
                </Button>
              </div>
            </Card.Header>
            <Card.Body>
              {modelEntries.map(([model, text], index) => (
                <div key={model} className="mb-3 d-flex align-items-start">
                  <FormCheck
                    type="radio"
                    name="sectionSelect"
                    checked={selectedSection === index}
                    onChange={() => handleCheckboxChange(index)}
                    className="me-2"
                  />
                  <div style={{ flexGrow: 1 }}>
                    <h2>{model}</h2>
                    {isEditing ? (
                      <Form.Control
                        as="textarea"
                        rows={5}
                        value={text}
                        onChange={(e) => handleContentChange(e, model)}
                      />
                    ) : (
                      <div dangerouslySetInnerHTML={{ __html: text }} />
                    )}
                    {index < modelEntries.length - 1 && <hr />}
                  </div>
                </div>
              ))}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default WikiPage;