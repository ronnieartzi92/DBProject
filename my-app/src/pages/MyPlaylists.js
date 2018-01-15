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
            const playlists = [{name: "my songs", date: "01.01.2017", id: 1}, {name: "my songs 2222", date: "02.02.2017", id: 2}];
            this.setState({playlists, isLoading: false});
            alert("Server Not Responding....");
        });
    }

    startPlaylist(id){
        alert("play playlist #"+id);
        this.setState({ isLoading: true });
        sdk.getPlaylistSongs(this.props.userToken, id).then( (data) =>{
            console.log(data);
            this.setState({ showPlaylist: true, playlistSongs: data.songs, isLoading: false });
        }, (reason)=> {
            alert("Server Not Responding....");
            this.setState({isLoading: false });
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
                                <List.Header>{item.name}</List.Header>
                                {item.date_created}
                            </List.Content>
                        </List.Item>

                    })}
                </List>
            </Segment>
                {this.state.showPlaylist && this.state.playlistSongs.length >0 && <Segment>
                 <Playlist playlistSongs={this.state.playlistSongs}/>
                </Segment>}
                {this.state.showPlaylist && this.state.playlistSongs.length === 0 && <Segment>
                    <div>We couldn't find any songs :(</div>
                    <div>Try to rephrase your search</div>
                </Segment>}
            </div>

        )
    }
}
