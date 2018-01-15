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

const concerts = [{artistName : "justin bieber", imageURL : "data:image/jpeg;base64,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", location: "New York", date: "01.01.2019", time: "20:00", url: "http://www.justinbiebermusic.com/"}];


export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {playlist: this.props.playlistSongs ? this.props.playlistSongs : items, currentPlayedIndex: 0, concerts};
        if(this.state.playlist.length > 0){
            this.playSong(0);
        }
    };


    playSong(index){
        this.setState({currentPlayedIndex : index});
        const currentArtistId = this.playlist[index].artistId;
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
        this.state.playlist[this.state.currentPlayedIndex] ? this.state.playlist[this.state.currentPlayedIndex].videoId : "";

        return(
            <div className="playlist-container">
                <div className="playlist-left">
                <Item.Group>
                    {this.state.playlist.map((item, index) => {
                        return <div onClick={this.playSong.bind(this,index)} key={index}><PlayListItem key={index} title={item.title} artist={item.artist} imageURL={item.imageURL} videoId={item.videoId}/></div>
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