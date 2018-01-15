/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import { Item } from 'semantic-ui-react'
import {PlayListItem} from './../Components/PlaylistItem';
import YoutubeFrame from "../Components/YoutubeFrame";
import {ArtistNextConcerts} from "../Components/ArtistNextConcert";
import sdk from "./../sdk/sdk"

const items = [{title: "123123", artist: "dsfsdfds", videoId: "2g811Eo7K8U", imageURL: "https://i.ytimg.com/vi/gA-NDZb29I4/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDLu2dZe9U8hgI1L0_518Ge3bd7Cg"},
    {title: "67867876876", artist: "dsfsdfds", videoId: "lrvqjdMcjjQ", imageURL: "https://i.ytimg.com/vi/gA-NDZb29I4/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDLu2dZe9U8hgI1L0_518Ge3bd7Cg"}];

const concerts = [{artistName : "justin bieber", imageURL : "https://i.ytimg.com/vi/gA-NDZb29I4/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDLu2dZe9U8hgI1L0_518Ge3bd7Cg", location: "New York", date: "01.01.2019", time: "20:00", url: "http://www.justinbiebermusic.com/"}];


export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {playlist: this.props.playlistSongs ? this.props.playlistSongs : items, currentPlayedIndex: 0, concerts};
    };


    playSong(index){
        this.setState({currentPlayedIndex : index});
        const currentArtistId = this.playlist[index].artist_id;
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
                    <ArtistNextConcerts concerts={concerts}/>
                </div>
            </div>
        )
    }
}