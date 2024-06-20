import React, { useState, useEffect } from 'react';
import { Table, Button, FormCheck } from 'react-bootstrap';

const M = 3; // Local constant for the number of triplets to pre-select

function TriplesTable({ triples, onGenerate }) {
  const [selectedTriples, setSelectedTriples] = useState([]);

  useEffect(() => {
    // Pre-select the first M unique triplets
    const uniqueTriples = [...new Set(Object.keys(triples))].slice(0, M);
    setSelectedTriples(uniqueTriples.map(Number));
  }, [triples]);

  const handleCheckboxChange = (index) => {
    const updatedSelection = selectedTriples.includes(index)
      ? selectedTriples.filter(i => i !== index)
      : [...selectedTriples, index];
    setSelectedTriples(updatedSelection);
  };

  const handleGenerateClick = () => {
    const selected = selectedTriples.map(index => triples[index]);
    onGenerate(selected);
  };

  return (
    <div className="col-md-6 mt-4">
      <h2>Triples</h2>
      <Table bordered>
        <thead>
          <tr>
            <th scope="col">Select</th>
            <th scope="col">Subject</th>
            <th scope="col">Predicate</th>
            <th scope="col">Object</th>
          </tr>
        </thead>
        <tbody>
          {Object.entries(triples).map(([index, [subject, predicate, object]]) => (
            <tr key={index}>
              <td>
                <FormCheck
                  type="checkbox"
                  checked={selectedTriples.includes(Number(index))}
                  onChange={() => handleCheckboxChange(Number(index))}
                />
              </td>
              <td>{subject}</td>
              <td>{predicate}</td>
              <td>{object}</td>
            </tr>
          ))}
        </tbody>
      </Table>
      {selectedTriples.length > 0 && (
        <Button variant="primary" onClick={handleGenerateClick}>
          Generate
        </Button>
      )}
    </div>
  );
}

export default TriplesTable;
