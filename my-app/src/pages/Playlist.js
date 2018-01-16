/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import { Item ,Button} from 'semantic-ui-react'
import {PlayListItem} from './../Components/PlaylistItem';
import YoutubeFrame from "../Components/YoutubeFrame";
import {ArtistNextConcerts} from "../Components/ArtistNextConcert";
import sdk from "./../sdk/sdk"
import {concerts, songsList} from "../utils/consts";
import Tags from 'react-tagging-input';


export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {playlist: this.props.playlistSongs ? this.props.playlistSongs : songsList, currentPlayedIndex: 0, concerts, tags: [], listId: this.props.listId};
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

    render() {
        const currVid = this.state.playlist &&
        this.state.playlist[this.state.currentPlayedIndex] ? this.state.playlist[this.state.currentPlayedIndex].video_id : "";
        const artistName = this.state.playlist &&
        this.state.playlist[this.state.currentPlayedIndex] ? this.state.playlist[this.state.currentPlayedIndex].artist_name : "the artist";
        return(
            <div className="playlist-container">
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
                <div className="playlist-left">
                <Item.Group>
                    {this.state.playlist.map((item, index) => {
                        return <div onClick={this.playSong.bind(this,index)} key={index}><PlayListItem key={index} title={item.name} artist={item.artist_name} imageURL={item.img} videoId={item.video_id}/></div>
                    })}
                </Item.Group>
                </div>
                <div className="youtube-frame">
               <YoutubeFrame videoId={currVid} onEnd={this.playNextSong.bind(this)}/>
                </div>
                <div className="concerts">
                    <div style={{color: "black"}}>Check-Out {artistName}'s upcoming shows:</div>
                    <ArtistNextConcerts concerts={concerts}/>
                </div>
            </div>
        )
    }
}