/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import { Item } from 'semantic-ui-react'
import {PlayListItem} from './../Components/PlaylistItem';
import YoutubeFrame from "../Components/YoutubeFrame";

const items = [{title: "123123", artist: "dsfsdfds", videoId: "2g811Eo8K8U", imageURL: "https://i.ytimg.com/vi/gA-NDZb29I4/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDLu2dZe9U8hgI1L0_518Ge3bd7Cg"},
    {title: "67867876876", artist: "dsfsdfds", videoId: "2g811Eo7K8U", imageURL: "https://i.ytimg.com/vi/gA-NDZb29I4/hqdefault.jpg?sqp=-oaymwEWCKgBEF5IWvKriqkDCQgBFQAAiEIYAQ==&rs=AOn4CLDLu2dZe9U8hgI1L0_518Ge3bd7Cg"}];



export default class Playlist extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {currentPlayedIndex: 0};
    };

    playSong(index){
        this.setState({currentPlayedIndex : index});
        debugger;
    }

    render() {
        const currVid = items[this.state.currentPlayedIndex].videoId;



        return(
            <div className="playlist-container">
                <div className="playlist-left">
                <Item.Group>
                    {items.map(function (item, index) {
                        return <PlayListItem onClick={()=> alert("hello")} key={index} title={item.title} artist={item.artist} imageURL={item.imageURL} videoId={item.videoId}/>
                    })}
                </Item.Group>
                </div>
                <div className="youtube-frame">
               <YoutubeFrame videoId={currVid}/>
                </div>
            </div>
        )
    }
}