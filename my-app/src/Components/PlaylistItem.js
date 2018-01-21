/**
 * Created by guyy on 1/10/2018.
 */
import { Item } from 'semantic-ui-react'
import React from 'react'



export const PlayListItem = ({title, artist, imageURL, duration}) => {
    const image = imageURL ? imageURL : "http://www.pixempire.com/images/preview/social-youtube-circle-icon.jpg";

    const formatTime = (time) => {
        let minutes = Math.floor(time / 60);
        let seconds = time - (minutes * 60);
        if (minutes < 10) {minutes = "0"+minutes;}
        if (seconds < 10) {seconds = "0"+seconds;}
        return minutes+':'+seconds;
    };

    return (
        <Item>
            <Item.Image size='tiny' src={image} />
            <Item.Content verticalAlign='middle'>
                <Item.Header as='a'>{title}
                    <div>{artist}</div>
                    {duration && <div><small>{formatTime(parseInt(duration))}</small></div>}
                </Item.Header>
            </Item.Content>
        </Item>
    );
};