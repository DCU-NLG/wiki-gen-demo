import React, { useState, useEffect } from 'react';
import { Table, Button, FormCheck } from 'react-bootstrap';

function TriplesTable({ triples, onGenerate }) {
  const M = process.env.REACT_APP_N_PRESELECT_TRIPLES; // Number of triplets to pre-select by unique predicate
  const [selectedTriples, setSelectedTriples] = useState([]);

  useEffect(() => {
    // Pre-select the first M unique triplets based on unique predicate
    const uniquePredicates = [];
    const uniqueTriples = [];
    for (const [index, [, predicate]] of Object.entries(triples)) {
      if (!uniquePredicates.includes(predicate) && uniqueTriples.length < M) {
        uniquePredicates.push(predicate);
        uniqueTriples.push(Number(index));
      }
    }
    setSelectedTriples(uniqueTriples);
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
