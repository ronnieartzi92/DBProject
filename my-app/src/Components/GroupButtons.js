/**
 * Created by guyy on 1/15/2018.
 */
import React from 'react'
import { Button } from 'semantic-ui-react'


export default class GroupButtons extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {options: this.props.options};
    };
    componentWillReceiveProps(nextProps){
        this.setState({options: nextProps.options});
    }


    render() {

        return (
            <Button.Group>
            {this.state.options.map((item, index) => {
                return <><Button onClick={this.props.chooseOption.bind(this, item)}>One</Button><Button.Or /></>
            })}
            </Button.Group>
        )
    }

}