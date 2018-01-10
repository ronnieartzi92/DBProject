/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import YouTube from 'react-youtube'

const opts = {
    height: '390',
    width: '640',
    playerVars: { // https://developers.google.com/youtube/player_parameters
        autoplay: 1
    }
};

export default class YoutubeFrame extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {videoId: this.props.videoId};
    };
    componentWillReceiveProps(nextProps){
        this.setState({videoId: nextProps.videoId});
    }


    render() {
        const vidID = this.state.videoId || "2g811Eo7K8U";

        return (
            <YouTube
                videoId={vidID}
                opts={opts}
                onEnd={this.props.onEnd}
                // onReady={this._onReady}
            />
        )
    }

    _onReady(event) {
        // access to player in all event handlers via event.target
        event.target.pauseVideo();
    }
}