/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import { Item ,Button, Form} from 'semantic-ui-react'
import {PlayListItem} from './../Components/PlaylistItem';
import YoutubeFrame from "../Components/YoutubeFrame";
import {ArtistNextConcerts} from "../Components/ArtistNextConcert";
import sdk from "./../sdk/sdk"
import Tags from 'react-tagging-input';


export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {playlist: this.props.playlistSongs, currentPlayedIndex: 0, concerts: [],
            tags: [], listId: this.props.listId, playlistName: this.props.playlistName, canSavePlaylist: false};
        this.playSong(0);
    };


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

    saveTags(){
        sdk.savePlaylistTags(this.props.userToken, this.state.listId, this.state.tags).then( (data) =>{
            console.log(data);
            this.setState({tags : []});
            alert("Tags Saved!");
        }, (reason)=> {
            alert("Server Not Responding....");
        });
    }

    playSong(index){
        this.setState({currentPlayedIndex : index});
        const currentArtistId = this.state.playlist[index].artist_id;
        sdk.getArtistConcerts(this.props.userToken, currentArtistId).then( (data) =>{
            console.log(data);
            this.setState({concerts : data});
        }, (reason)=> {
            this.setState({concerts : []});
            alert("Server Not Responding....");
        });
    }
    playNextSong(){
        if(this.state.currentPlayedIndex < this.state.playlist.length-1)
            this.playSong(this.state.currentPlayedIndex + 1);
        else this.playSong(0);
    }

    getSimilarPlaylist(){
        sdk.getSimilarPlaylist(this.props.userToken, this.state.listId).then( (data) =>{
            console.log(data);
            this.setState({playlist : data, currentPlayedIndex: 0, concerts: [], tags: [], listId: data.id, playlistName: null, canSavePlaylist: true});
        }, (reason)=> {
            alert("Server Not Responding....");
        });
    }

    savePlaylist(event) {
        sdk.savePlaylist(this.props.userToken, this.state.playlistName, this.state.playlist).then( (data) =>{
            console.log(data);
            this.setState({canSavePlaylist : false});
            alert("Your playlist saved successfully !");
        }, (reason)=> {
            alert("Server Not Responding....");
        });
        event.preventDefault();
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.type === 'checkbox' ? target.checked : target.value;
        const name = target.name;

        this.setState({
            [name]: value
        });
    }


    render() {
        const currVid = this.state.playlist &&
        this.state.playlist[this.state.currentPlayedIndex] ? this.state.playlist[this.state.currentPlayedIndex].video_id : "";
        const artistName = this.state.playlist &&
        this.state.playlist[this.state.currentPlayedIndex] ? this.state.playlist[this.state.currentPlayedIndex].artist_name : "the artist";
        return(
            <div className="playlist-container">
                {this.state.playlistName && <h2>{this.state.playlistName}</h2>}

                {this.state.canSavePlaylist &&
                <Form onSubmit={this.savePlaylist.bind(this)} style={{float: 'right', width: '70%'}}>
                    <Form.Group>
                        <Form.Input placeholder='PlaylistName' name='playlistName' value={this.state.playlistName}
                                    onChange={this.handleInputChange.bind(this)}/>
                        <Form.Button content='Save Playlist' color="red"/>
                    </Form.Group>
                </Form>
                }
                {this.state.listId && <div className="tags-container">
                    Add tags to this playlist:
                    <Tags
                        tags={this.state.tags}
                        placeholder="Add tags to your playlist..."
                        uniqueTags={true}
                        onAdded={this.onTagAdded.bind(this)}
                        onRemoved={this.onTagRemoved.bind(this)}/>
                    <Button size='mini' onClick={this.saveTags.bind(this)}>
                        Save Tags
                    </Button>
                </div>
                }
                {this.state.listId && <div className="similar-container">
                    <Button size='medium' color='blue' onClick={this.getSimilarPlaylist.bind(this)}>
                        Give me a similar playlist
                    </Button>
                </div>
                }
                <div className="playlist-left">
                <Item.Group>
                    {this.state.playlist.map((item, index) => {
                        return <div onClick={this.playSong.bind(this,index)} key={index}><PlayListItem key={index} title={item.track_name} artist={item.artist_name} imageURL={item.img} videoId={item.video_id} duration={item.duration}/></div>
                    })}
                </Item.Group>
                </div>
                <div className="youtube-frame">
               <YoutubeFrame videoId={currVid} onEnd={this.playNextSong.bind(this)}/>
                </div>
                {this.state.concerts.length > 0 && <div className="concerts">
                    <div style={{color: "black"}}>Check-Out {artistName}'s upcoming shows:</div>
                    <ArtistNextConcerts concerts={this.state.concerts}/>
                </div>
                }
            </div>
        )
    }
}