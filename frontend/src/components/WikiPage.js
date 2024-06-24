import React, { useState, useEffect } from 'react';
import { Container, Row, Col, Card, Button, Form } from 'react-bootstrap';

function WikiPage({ title, content }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editableContent, setEditableContent] = useState(content);

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
              <Button
                variant="outline-primary"
                onClick={isEditing ? handleSaveClick : handleEditClick}
              >
                {isEditing ? 'Save' : 'Edit'}
              </Button>
            </Card.Header>
            <Card.Body>
              {modelEntries.map(([model, text], index) => (
                <div key={model} className="mb-3">
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
              ))}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
}

export default WikiPage;
