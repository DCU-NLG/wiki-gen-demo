import React from 'react';
import { Navbar, Nav } from 'react-bootstrap';
import { LinkContainer } from 'react-router-bootstrap';

function NavBar() {
  return (
    <Navbar className="justify-content-between" bg="primary" expand="lg" style={{marginBottom: "20px"}}>
      <Navbar.Brand href="/" style={{marginLeft: "20px"}}>Wikipedia Generator</Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="mr-auto">
          <LinkContainer to="/">
            <Nav.Link>Generate</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/instructions">
            <Nav.Link>Instructions</Nav.Link>
          </LinkContainer>
          <LinkContainer to="/contact">
            <Nav.Link>Contact</Nav.Link>
          </LinkContainer>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  );
}

export default NavBar;
