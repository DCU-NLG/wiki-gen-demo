import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

function TriplesTable({ triples, onGenerate }) {
  const [selectedTriples, setSelectedTriples] = useState([]);

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
      <table className="table table-bordered">
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
                <input
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
      </table>
      {selectedTriples.length > 0 && (
        <button
          type="button"
          className="btn btn-primary"
          onClick={handleGenerateClick}
        >
          Generate
        </button>
      )}
    </div>
  );
}

export default TriplesTable;
