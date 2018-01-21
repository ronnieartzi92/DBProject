/**
 * Created by guyy on 1/11/2018.
 */
import React, {Component} from 'react'
import { List, Segment } from 'semantic-ui-react'
import sdk from "./../sdk/sdk"
import Playlist from "./Playlist";

export default class MyPlaylists extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {isLoading: false};
        sdk.getPlaylists(this.props.userToken).then( (data) =>{
            console.log(data);
            this.setState({playlists : data, isLoading: false});
        }, (reason)=> {
            this.setState({playlists: [], isLoading: false});
            alert("Server Not Responding....");
        });
    }

    startPlaylist(id){
        this.setState({ isLoading: true, showPlaylist: false });
        sdk.getPlaylistSongs(this.props.userToken, id).then( (data) =>{
            console.log(data);
            this.setState({ showPlaylist: true, playlist: data, isLoading: false });
        }, (reason)=> {
            alert("Server Not Responding....");
            this.setState({isLoading: false, showPlaylist: false });
        });
    }
    render() {
        const playlists = this.state.playlists;
        console.log(playlists);
        if(!playlists || playlists.length === 0 || playlists===[] || playlists === undefined )
            return <Segment inverted>
                    <div>You don't have any playlists saved</div>
                    </Segment>
        else return (
            <div>
            <Segment inverted loading={this.state.isLoading}>
                <List divided inverted relaxed>
                    {playlists.map((item, index) => {
                        return <List.Item onClick={this.startPlaylist.bind(this,item.id)}  key={index}>
                            <List.Content>
                                <List.Header>{item.play_list_name}</List.Header>
                                {item.date_created}
                            </List.Content>
                        </List.Item>

                    })}
                </List>
            </Segment>
                {this.state.showPlaylist && this.state.playlist.songs.length >0 && <Segment className="playlist-segment">
                 <Playlist userToken={this.props.userToken} playlistSongs={this.state.playlist.songs} listId={this.state.playlist.id} playlistName={this.state.playlist.play_list_name}/>
                </Segment>}
                {this.state.showPlaylist && this.state.playlist.songs.length === 0 && <Segment>
                    <div>We couldn't find any songs :(</div>
                    <div>Try to rephrase your search</div>
                </Segment>}
            </div>

        )
    }
}
