import React from "react";
import { Button, Form, FormGroup, Input, Label } from "reactstrap";

import axios from "axios";

import { API_URL } from "../constants";

class NewProductForm extends React.Component {
  state = {
    pk: 0,
    name: "",
    description: "",
    quantity: "",
    unit_price: "",
    stock_level: ""
  };

  componentDidMount() {
    if (this.props.product) {
      const { pk, name, description, quantity, unit_price, stock_level } = this.props.product;
      this.setState({ pk, name, description, quantity, unit_price, stock_level });
    }
  }

  onChange = e => {
    this.setState({ [e.target.name]: e.target.value });
  };

  createProduct = e => {
    e.preventDefault();
    axios.post(API_URL, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  editProduct = e => {
    e.preventDefault();
    axios.put(API_URL + this.state.pk, this.state).then(() => {
      this.props.resetState();
      this.props.toggle();
    });
  };

  defaultIfEmpty = value => {
    return value === "" ? "" : value;
  };

  render() {
    return (
      <Form onSubmit={this.props.product ? this.editProduct : this.createProduct}>
        <FormGroup>
          <Label for="name">Name:</Label>
          <Input
            type="text"
            name="name"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.name)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="description">Description:</Label>
          <Input
            type="text"
            name="description"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.description)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="quantity">Quantity:</Label>
          <Input
            type="text"
            name="quantity"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.quantity)}
          />
        </FormGroup>
        <FormGroup>
          <Label for="unit_price">Unit price:</Label>
          <Input
            type="text"
            name="unit_price"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.unit_price)}
          />
        </FormGroup>
         <FormGroup>
          <Label for="stock_level">Stock level:</Label>
          <Input
            type="text"
            name="stock_level"
            onChange={this.onChange}
            value={this.defaultIfEmpty(this.state.stock_level)}
          />
        </FormGroup>
        <Button>Submit</Button>
      </Form>
    );
  }
}

export default NewProductForm;