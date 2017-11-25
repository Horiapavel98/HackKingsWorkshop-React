import 'whatwg-fetch';
import React, { Component } from 'react';

import config from './config';
import Account from './Account';

import './App.css';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      customer1: {},
      customer2: {}
    };
  }

  getDataFromNessie(endpoint, id) {
    return new Promise((resolve, reject) => {
      fetch(`http://api.reimaginebanking.com/${endpoint}/${id}?key=${config.apiKey}`)
        .then((response) => {
          resolve(response.json());
        })
        .catch(reject);
    });
  }

  requestCustomerData() {
    const { endpoints, customers } = config;
    let customer1;
    let customer2;

    this.getDataFromNessie(endpoints.customers, customers.customer1.id).then((customerData) => {
      this.getDataFromNessie(endpoints.accounts, customers.customer2.accountId).then((accountData) => {
        customer1 = Object.assign({}, customerData, accountData);
        this.setState({ customer1 });
      });
    });

    this.getDataFromNessie(endpoints.customers, customers.customer2.id).then((customerData) => {
      this.getDataFromNessie(endpoints.accounts, customers.customer2.accountId).then((accountData) => {
        customer2 = Object.assign({}, customerData, accountData);
        this.setState({ customer2 });
      });
    });
  }

  componentDidMount() {
    setInterval(() => {
      this.requestCustomerData();
    }, 30000);
  }

  render() {
    const { customer1, customer2 } = this.state;

    return (
      <div className="App">
        <header className="App-header">
          <h1 className="App-title">Bank Balances</h1>
        </header>
        <main className="accounts">
          <Account customerName={customer1.first_name} accountBalance={customer1.balance} />
          <Account customerName={customer2.first_name} accountBalance={customer2.balance} />
        </main>
      </div>
    );
  }
}

export default App;
