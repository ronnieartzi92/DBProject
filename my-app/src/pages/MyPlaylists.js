/**
 * Created by guyy on 1/11/2018.
 */
import React, {Component} from 'react'
import { List, Segment } from 'semantic-ui-react'

export default class MyPlaylists extends Component {
    constructor(props, context) {
        super(props, context);
        const playlist = this.props.playlist ? this.props.playlist : [{name: "my songs", date: "01.01.2017"}, {name: "my songs 2222", date: "02.02.2017"}];
        this.state = {playlist};
    }



    startPlaylist(index){
        alert("play playlist #"+index);
    }
    render() {
        const playlist = this.state.playlist;

        if(!playlist || playlist.length === 0 )
            return <Segment inverted>
                    <div>You don't have any playlists saved</div>
                    </Segment>
        else return (
            <Segment inverted>
                <List divided inverted relaxed>
                    {playlist.map((item, index) => {
                        return <List.Item onClick={this.startPlaylist.bind(this,index)}  key={index}>
                            <List.Content>
                                <List.Header>{item.name}</List.Header>
                                {item.date}
                            </List.Content>
                        </List.Item>

                    })}
                </List>
            </Segment>
        )
    }
}
