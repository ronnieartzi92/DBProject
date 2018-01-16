/**
 * Created by guyy on 1/15/2018.
 */
import React, {Component} from 'react'
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
        const options = this.state.options;
        {/*{this.state.options.map((item, index) => {*/}
        {/*return <div><Button onClick={this.props.chooseOption.bind(this, item)}>One</Button><Button.Or /></div>*/}
        {/*})}*/}


        return (
            <div>
                {options.length === 2 &&
                <Button.Group>
                    <Button onClick={this.props.chooseOption.bind(this, options[0])}>{options[0]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[1])}>{options[1]}</Button>
                </Button.Group>}
                {options.length === 3 &&
                <Button.Group>
                    <Button onClick={this.props.chooseOption.bind(this, options[0])}>{options[0]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[1])}>{options[1]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[2])}>{options[2]}</Button>
                </Button.Group>}
                {options.length === 4 &&
                <Button.Group>
                    <Button onClick={this.props.chooseOption.bind(this, options[0])}>{options[0]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[1])}>{options[1]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[2])}>{options[2]}</Button>
                    <Button.Or/>
                    <Button onClick={this.props.chooseOption.bind(this, options[3])}>{options[3]}</Button>
                </Button.Group>}
                <Button color='black' onClick={this.props.chooseOption.bind(this, "none")} style={{marginLeft: "10px"}}>None</Button>

            </div>
        )
    }

}