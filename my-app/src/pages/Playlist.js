/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import { Item } from 'semantic-ui-react'
import {PlayListItem} from './../Components/PlaylistItem';
import YoutubeFrame from "../Components/YoutubeFrame";
import {ArtistNextConcerts} from "../Components/ArtistNextConcert";
import sdk from "./../sdk/sdk"
import {concerts, songsList} from "../utils/consts";


export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {playlist: this.props.playlistSongs ? this.props.playlistSongs : songsList, currentPlayedIndex: 0, concerts};
    };


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