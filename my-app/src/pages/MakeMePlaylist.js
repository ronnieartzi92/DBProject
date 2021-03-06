/**
 * Created by guyy on 1/11/2018.
 */
import React, {Component} from 'react'
import { Form, Button, Segment , Grid, Dropdown} from 'semantic-ui-react'
import Playlist from "./Playlist";
import GroupButtons from "../Components/GroupButtons";
import sdk from "./../sdk/sdk"


const suggestedWords = [
    ["pop","rock","alternative"],
    ["60s", "70s","80s","90s"],
    ["love", "beautiful", "hate"],
    ["2014", "2015","2016","2017"],
    ["Coldplay", "Sia","Ed Sheeran"],
    ["dance", "chillout"],
    ["acoustic", "downtempo"]
];


export default class MyPlaylists extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {showPlaylist : false, freeText: "", isLoading: false, tags: [], playlistSongs: [], suggestIndex: 0, playlistName: "", canSavePlaylist: true, optionalTags:[], songsLimit: 25};

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.savePlaylist = this.savePlaylist.bind(this);

        sdk.getTags(this.props.userToken).then( (data) =>{
            let tags = [];
            data.slice(0, 500).forEach((el) => {
                if(el.tag_name && !el.tag_name.includes(' '))
                 tags.push({key: el.id, value: el.tag_name, text: el.tag_name});
            });
            console.log("tags after process");
            console.log(tags);

            this.setState({optionalTags : tags});
        }, (reason)=> {
            this.setState({optionalTags: []});
            alert("Server Not Responding....");
        });
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
        this.setState({ isLoading: true, showPlaylist: false });
        sdk.searchForPlaylist(this.props.userToken, this.state.freeText, this.state.songsLimit).then( (data) =>{
            console.log(data);
            this.setState({playlistSongs : data, isLoading: false, showPlaylist: true, canSavePlaylist: true});
        }, (reason)=> {
            this.setState({playlistSongs: [], isLoading: false, showPlaylist: true});
            alert("Server Not Responding....");
        });
        event.preventDefault();
    }

    makePlaylist(clickType){
        this.setState({ isLoading: true, showPlaylist: false });
        sdk.makePlaylist(this.props.userToken, clickType).then( (data) =>{
            console.log(data);
            this.setState({playlistSongs : data, isLoading: false, showPlaylist: true, canSavePlaylist: true});
        }, (reason)=> {
            this.setState({playlistSongs: [], isLoading: false, showPlaylist: true});
            alert("Server Not Responding....");
        });
    }

    savePlaylist(event) {
        sdk.savePlaylist(this.props.userToken, this.state.playlistName, this.state.playlistSongs).then( (data) =>{
            console.log(data);
            this.setState({canSavePlaylist : false});
            alert("Your playlist saved successfully !");
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
    clearValFromTags(oldtag){
        let tags = [];
        this.state.optionalTags.forEach((tag) => {
            if(tag.value !== oldtag.value){
                tags.push(tag)
            }
        });
        this.setState({optionalTags : tags});
    }

    addFromTags(event, data){
        this.setState({ freeText: `${this.state.freeText} ${data.value}` });
        this.clearValFromTags(data);
    }

    render() {
      return (
          <div>
            <Segment loading={this.state.isLoading}>
                <Form onSubmit={this.handleSubmit}>
                    <Form.Group>
                    <Form.Field width="5" className="searchInput" >
                        <label>What do you want to hear ?</label>
                        <input name="freeText" value={this.state.freeText} onChange={this.handleInputChange} placeholder="I'm in a mood for..." required="required"/>
                    </Form.Field>
                    <Form.Field width="2" style={{marginTop: '4px'}}>
                        How many?
                    <input type='number' name="songsLimit" placeholder="25" max="50" min="5" value={this.state.songsLimit} onChange={this.handleInputChange}  />
                    </Form.Field>
                    <Form.Field id='form-button-control-public' control={Button} content='Play!' color="blue" style={{marginTop: "28px"}} />
                    </Form.Group>

                </Form>
                {/*<Dropdown placeholder='Choose from out most common tags...' fluid multiple search selection options={this.state.optionalTags} className="dropdown-input" />*/}

                {this.state.optionalTags.length >0 && <div className="dropdown-input"><Dropdown placeholder='Choose from our most common tags...' search selection options={this.state.optionalTags}  onChange={this.addFromTags.bind(this)} disabled={this.state.optionalTags.length === 0} text='Choose from our most common tags...'/></div>}

                {suggestedWords.length > this.state.suggestIndex && <div style={{marginTop: "30px", marginBottom: "20px"}}>
                    You can serach for things like:
                <GroupButtons options={suggestedWords[this.state.suggestIndex]} chooseOption={this.addOptionToSearch.bind(this)}/>
                </div>}

            </Segment>

              <Segment loading={this.state.isLoading}>
                  <Grid className="buttonsGrid">
                      <Grid.Row columns={5}>
                          <Grid.Column>
                              <Button size='big'  color='orange' onClick={this.makePlaylist.bind(this,'concert_tour')}>
                                  Take me to a show
                              </Button>
                              <div style={{marginTop: '10px'}}>Get songs of the 5 top artists with the most diverse places of events in the next year</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='yellow' onClick={this.makePlaylist.bind(this,'top_of_the_top')}>
                                  The top of the top
                              </Button>
                              <div style={{marginTop: '10px'}}>Get top songs of unique and top artists</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big'  color='olive' onClick={this.makePlaylist.bind(this,'artist_on_fire')}>
                                  Artists on fire
                              </Button>
                              <div style={{marginTop: '10px'}}>Get songs of the 5 artists who have the most events in the next year and have been listened the most</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='green' onClick={this.makePlaylist.bind(this,'something_new')}>
                                  Something new
                              </Button>
                              <div style={{marginTop: '10px'}}>Get songs that has been published in the last year from different artists</div>
                          </Grid.Column>
                          <Grid.Column>
                              <Button size='big' color='teal' onClick={this.makePlaylist.bind(this,'great_album')}>
                                  Gotta be a great album
                              </Button>
                              <div style={{marginTop: '10px'}}>Get the songs from the album which contain a top rates song</div>
                          </Grid.Column>

                      </Grid.Row>
                  </Grid>

              </Segment>
                {this.state.showPlaylist && this.state.playlistSongs.length >0 &&
                    <div>
                        {this.state.canSavePlaylist &&
                        <Form onSubmit={this.savePlaylist} style={{float: 'right', width: '70%'}}>
                            <Form.Group>
                                <Form.Input placeholder='PlaylistName' name='playlistName' value={this.state.playlistName}
                                            onChange={this.handleInputChange}/>
                                <Form.Button content='Save Playlist' color="red"/>
                            </Form.Group>
                        </Form>
                        }
                <Playlist playlistSongs={this.state.playlistSongs} userToken={this.props.userToken}/>
                    </div>}
              {this.state.showPlaylist && this.state.playlistSongs.length === 0 &&
              <Segment>
                  <div>We couldn't find any songs, or your search returns too many results :(</div>
                  <div>Try to rephrase your search</div>
              </Segment>
              }
          </div>
        )
    }
}