/**
 * Created by guyy on 1/10/2018.
 */
import { Item } from 'semantic-ui-react'
import React from 'react'

export const PlayListItem = ({title, artist, imageURL}) => {
    const image = imageURL ? imageURL : "http://www.pixempire.com/images/preview/social-youtube-circle-icon.jpg";
    return (
        <Item>
            <Item.Image size='tiny' src={image} />
            <Item.Content verticalAlign='middle'>
                <Item.Header as='a'>{title}
                    <div>{artist}</div>
                </Item.Header>
            </Item.Content>
        </Item>
    );
};