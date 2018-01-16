/**
 * Created by guyy on 1/11/2018.
 */
import React, {Component} from 'react'
import { Form, Button, Segment , Grid} from 'semantic-ui-react'
import Playlist from "./Playlist";
import GroupButtons from "../Components/GroupButtons";
import sdk from "./../sdk/sdk"
import {songsList} from "../utils/consts";


const suggestedWords = [
    ["pop","rock","alternative"],
    ["60s", "70s","80s","90s"],
    ["love", "beautiful"],
    ["2014", "2015","2016","2017"],
    ["Coldplay", "Sia","Ed Sheeran"],
    ["dance", "chillout"],
    ["acoustic", "downtempo"]
];


export default class MyPlaylists extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {showPlaylist : false, freeText: "", isLoading: false, tags: [], playlistSongs: [], suggestIndex: 0, playlistName: "", canSavePlaylist: true};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.savePlaylist = this.savePlaylist.bind(this);
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
        alert('A search was submitted: '+this.state.freeText );
        sdk.searchForPlaylist(this.props.userToken, this.state.freeText).then( (data) =>{
            console.log(data);
            this.setState({playlistSongs : data, isLoading: false, showPlaylist: true});
        }, (reason)=> {
            this.setState({playlistSongs: songsList, isLoading: false, showPlaylist: true});
            alert("Server Not Responding....");
        });
        event.preventDefault();
    }

    savePlaylist(event) {
        sdk.savePlaylist(this.props.userToken, this.state.playlistName, this.state.playlistSongs).then( (data) =>{
            console.log(data);
            this.setState({canSavePlaylist : false});
        }, (reason)=> {
            alert("Server Not Responding....");
        });
        event.preventDefault();
    }


    addOptionToSearch(option){
        if(option === "none")
            this.setState({ suggestIndex: this.state.suggestIndex +1 });
        else this.setState({ freeText: `${this.state.freeText} ${option}`, suggestIndex: this.state.suggestIndex +1 });
    }


    render() {
      return (
          <div>
            <Segment>
                <Form onSubmit={this.handleSubmit} loading={this.state.isLoading}>
                    <Form.Group>
                    <Form.Field width="5" className="searchInput" >
                        <label>What do you want to hear ?</label>
                        <input name="freeText" value={this.state.freeText} onChange={this.handleInputChange} />
                    </Form.Field>
                    <Form.Field id='form-button-control-public' control={Button} content='Play!' color="blue" style={{marginTop: "28px"}} />
                    </Form.Group>

                </Form>
                {suggestedWords.length > this.state.suggestIndex && <div style={{marginTop: "30px", marginBottom: "20px"}}>
                    You can serach for things like:
                <GroupButtons options={suggestedWords[this.state.suggestIndex]} chooseOption={this.addOptionToSearch.bind(this)}/>
                </div>}
            </Segment>

              <Segment>
                  <Grid className="buttonsGrid">
                      <Grid.Row columns={5}>
                          <Grid.Column>
                              <Button size='big'  color='orange'>
                                  Take me to a show
                              </Button>
                              <div>Show me songs that .....</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='yellow'>
                                  Take me to a show
                              </Button>
                              <div>Show me songs that .....</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big'  color='olive'>
                                  Take me to a show
                              </Button>
                              <div>Show me songs that .....</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='green'>
                                  Take me to a show
                              </Button>
                              <div>Show me songs that .....</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='teal'>
                                  Take me to a show
                              </Button>
                              <div>Show me songs that .....</div>
                          </Grid.Column>
                      </Grid.Row>
                  </Grid>

              </Segment>
                {this.state.showPlaylist && this.state.playlistSongs.length >0 &&
                    <div>
                        {this.state.canSavePlaylist &&
                        <Form onSubmit={this.savePlaylist} style={{float: 'right'}}>
                            <Form.Group>
                                <Form.Input placeholder='PlaylistName' name='playlistName' value={this.state.playlistName}
                                            onChange={this.handleInputChange}/>
                                <Form.Button content='Save Playlist' color="red"/>
                            </Form.Group>
                        </Form>
                        }

                <Playlist playlistSongs={this.state.playlistSongs}/>
                    </div>}
              {this.state.showPlaylist && this.state.playlistSongs.length === 0 &&
              <div>
                  <div>We couldn't find any songs :(</div>
                  <div>Try to rephrase your search</div>
              </div>
              }
          </div>
        )
    }
}

