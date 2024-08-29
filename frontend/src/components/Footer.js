import React from 'react';
import { Container } from 'react-bootstrap';

function Footer() {
  return (
    <footer className="footer mt-auto py-3 bg-light fixed-bottom">
      <Container>
        <span className="text-muted">© 2024 some copyright</span>
      </Container>
    </footer>
  );
}

export default Footer;
