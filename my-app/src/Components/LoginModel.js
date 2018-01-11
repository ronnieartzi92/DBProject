/**
 * Created by guyy on 1/11/2018.
 */
import React, { Component } from 'react'
import { Button, Header, Modal, Form , Message } from 'semantic-ui-react'

export default class LoginModel extends Component {
    constructor(props, context) {
        super(props, context);
        this.state ={ modalOpen: this.props.modalOpen || false, type : this.props.type, email: "", password: "", error: this.props.error, warning: false};
        this.handleInputChange = this.handleInputChange.bind(this);

    }
    componentWillReceiveProps(nextProps){
        this.setState({modalOpen: nextProps.modalOpen, type: nextProps.type, warning: nextProps.error !== "", error: nextProps.error});
    }


    handleOpen = () => this.setState({ modalOpen: true });

    handleClose = () => this.setState({ modalOpen: false });

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }


    render() {
        return (
            <Modal
                // trigger={<Button onClick={this.handleOpen}>Show Modal</Button>}
                open={this.state.modalOpen}
                onClose={this.handleClose}
                basic
                size='small'
            >
                <Header icon='browser' content={`${this.state.type} Form`} />
                {/*<Modal.Content>*/}
                    {/*<h3>{this.state.type} Form</h3>*/}
                {/*</Modal.Content>*/}
                <Modal.Actions>

                    <Form onSubmit={this.props.onSubmit.bind(this, this.state.email, this.state.password)} error={this.state.warning} className="loginForm">
                        <Form.Field >
                            <label>Email</label>
                            <input placeholder='Email' name="email"  onChange={this.handleInputChange}/>
                        </Form.Field>
                        <Form.Field >
                            <label>Password</label>
                            <input placeholder='Password' type="password" name="password" onChange={this.handleInputChange} />
                        </Form.Field>
                        <Message
                            error
                            header='Error'
                            content={this.state.error}
                        />
                        <Button type='submit'>Submit</Button>
                    </Form>
                </Modal.Actions>
            </Modal>
        )
    }
}
