/**
 * Created by guyy on 1/11/2018.
 */
import React, {Component} from 'react'
import { Form, Button, Segment } from 'semantic-ui-react'
import Playlist from "./Playlist";
import Tags from 'react-tagging-input';

export default class MyPlaylists extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {showPlaylist : false, freeText: "", isLoading: false, tags: []};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }

    handleSubmit(event) {
        this.setState({ isLoading: true });
        alert('A name was submitted: ' );
        this.setState({ showPlaylist: true, isLoading: false });
        event.preventDefault();
    }

    onTagAdded(tag) {
        this.setState({
            tags: [...this.state.tags, tag]
        });
    }

    onTagRemoved(tag, index) {
        this.setState({
            tags: this.state.tags.filter((tag, i) => i !== index)
        });
    }

    render() {

      return (
          <div>
            <Segment>
                <Form onSubmit={this.handleSubmit} loading={this.state.isLoading}>
                    <Form.Field width="5" className="searchInput" >
                        <label>Free Text Search</label>
                        <input name="freeText" value={this.state.freeText} onChange={this.handleInputChange} />
                    <Tags
                    tags={this.state.tags}
                    placeholder="Add keywords to search by..."
                    onAdded={this.onTagAdded.bind(this)}
                    onRemoved={this.onTagRemoved.bind(this)} />
                    </Form.Field>
                    <Form.Field id='form-button-control-public' control={Button} content='Search' />
                </Form>
            </Segment>
                {this.state.showPlaylist && <Playlist/>}
          </div>

        )
    }
}

