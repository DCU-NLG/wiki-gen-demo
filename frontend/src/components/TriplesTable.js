import React, { useState, useEffect } from 'react';
import { Table, Button, FormCheck, Spinner } from 'react-bootstrap';

function TriplesTable({ triples, onGenerate }) {
  const M = process.env.REACT_APP_N_PRESELECT_TRIPLES; // Number of triplets to pre-select by unique predicate
  const [selectedTriples, setSelectedTriples] = useState({});
  const [loading, setLoading] = useState(false); // State to manage loading spinner

  useEffect(() => {
    // Pre-select the first M unique triplets based on unique predicate
    const uniquePredicates = [];
    const uniqueTriples = {};
    let count = 0;
    for (const [index, [subject, predicate, object]] of Object.entries(triples)) {
      if (!uniquePredicates.includes(predicate) && count < M) {
        uniquePredicates.push(predicate);
        uniqueTriples[index] = [subject, predicate, object];
        count++;
      }
    }
    setSelectedTriples(uniqueTriples);
  }, [triples, M]);

  const handleCheckboxChange = (index) => {
    const updatedSelection = { ...selectedTriples };
    if (updatedSelection[index]) {
      delete updatedSelection[index];
    } else {
      updatedSelection[index] = triples[index];
    }
    setSelectedTriples(updatedSelection);
  };

  const handleGenerateClick = async () => {
    setLoading(true);
    await onGenerate(selectedTriples);
    setLoading(false);
  };

  return (
    <div>
      <h2>Triples</h2>
      &nbsp;
      <div className="scrollable-table">
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
                    checked={selectedTriples.hasOwnProperty(index)}
                    onChange={() => handleCheckboxChange(index)}
                  />
                </td>
                <td>{subject}</td>
                <td>{predicate}</td>
                <td>{object}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      </div>
      {Object.keys(selectedTriples).length > 0 && (
        <div className="fixed-button">
          <Button variant="primary" onClick={handleGenerateClick} disabled={loading}>
            {loading ? (
              <>
                <Spinner as="span" animation="border" size="sm" role="status" aria-hidden="true" />
                {' '} Generating...
              </>
            ) : (
              'Generate'
            )}
          </Button>
        </div>
      )}
    </div>
  );
}

export default TriplesTable;
