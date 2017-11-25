import React, { Component } from 'react';

import './account.css';

class Account extends Component {
    render() {
        const { customerName, accountBalance } = this.props;

        return (
            <section className="account">
                { customerName ? <h2>{ customerName }</h2> : <div className="empty"></div> }
                { accountBalance ? <p>£{ accountBalance }</p> : <div className="empty-small"></div> }
            </section>
        )
    }
}

export default Account;
