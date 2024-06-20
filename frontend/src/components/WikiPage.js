import React from 'react';

function WikiPage({ title, content }) {
  return (
    <div className="col-md-6" align="center">
      <div id="resultWindow" className="border rounded p-3">
        <div className="card mb-4">
          <div className="card-header bg-white">
            <img
              src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/103px-Wikipedia-logo-v2.svg.png"
              alt="Wikipedia Icon"
              className="mr-2"
              style={{ height: '30px' }}
            />
            <span className="h5 font-weight-bold">&nbsp;&nbsp;{title}</span>
          </div>
          <div className="card-body" dangerouslySetInnerHTML={{ __html: content }} />
        </div>
      </div>
    </div>
  );
}

export default WikiPage;
