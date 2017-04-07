import React, { Component } from 'react';
import './App.css';

import { Navbar, Nav, NavItem } from 'react-bootstrap';
import { Link, withRouter } from 'react-router-dom';
import Routes from './Routes';

class App extends Component {
  render() {
    return (
      <div className="App container">
        <Navbar fluid collapseOnSelect>
          <Navbar.Header>
            <Navbar.Brand>
              <Link to="/">Scrum </Link>
            </Navbar.Brand>
            <Navbar.Collapse>
              <Nav pullRight>
                <NavItem> Login </NavItem>
              </Nav>
            </Navbar.Collapse>
          </Navbar.Header>
        </Navbar>
        <Routes />
      </div>
    );
  }
}

export default withRouter(App);
