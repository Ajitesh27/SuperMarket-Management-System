import React, { Component } from "react";
import { Table } from "reactstrap";
import NewProductModal from "./NewProductModal";

import ConfirmRemovalModal from "./ConfirmRemovalModal";

class ProductList extends Component {
  render() {
    const stocks = this.props.stocks;
    return (
      <Table bgcolor='FDD897'>
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Quantity</th>
            <th>Unit price</th>
            <th>Stock level</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          {!stocks || stocks.length <= 0 ? (
            <tr>
              <td colSpan="6" align="center">
                <b>Oops, no one here yet</b>
              </td>
            </tr>
              
          ) : (
            stocks.map(product => (
              <tr key={product.pk}>
                <td>{product.name}</td>
                <td>{product.description}</td>
                <td>{product.quantity}</td>
                <td>{product.unit_price}</td>
                <td>{product.stock_level}</td>
                <td align="center">
                  <NewProductModal
                    create={false}
                    product={product}
                    resetState={this.props.resetState}
                  />
                  &nbsp;&nbsp;
                  <ConfirmRemovalModal
                    pk={product.pk}
                    resetState={this.props.resetState}
                  />
                </td>
              </tr>
              
            ))
          )}
        </tbody>
      </Table>
    );
  }
}

export default ProductList;