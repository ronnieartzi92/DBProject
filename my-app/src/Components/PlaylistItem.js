/**
 * Created by guyy on 1/10/2018.
 */
import { Image, Item } from 'semantic-ui-react'
import React, {Component} from 'react'

export const PlayListItem = ({title, artist, imageURL}) => (
    <Item>
        <Item.Image size='tiny' src={imageURL} />
        <Item.Content verticalAlign='middle'>
            <Item.Header as='a'>{title}
                <div>{artist}</div>
            </Item.Header>
        </Item.Content>
    </Item>
);