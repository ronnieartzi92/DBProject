/**
 * Created by guyy on 1/11/2018.
 */
import React from 'react'
import { Button, Icon, Item, Label } from 'semantic-ui-react'


export const ArtistNextConcerts = ({concerts = []}) => {
    if(concerts === []) return <div>No Future Concerts :(</div>;

    return (
        <Item.Group divided>
            {concerts.map((item, index) => {
                return <Item key={index}>
                    <Item.Image src={item.imageURL} />
                    <Item.Content>
                        <Item.Header as='a'>{item.artistName}</Item.Header>
                        <Item.Meta>
                            <span className='cinema'>{item.location}</span>
                        </Item.Meta>
                        <Item.Description>{item.date} {item.time}</Item.Description>
                        <Item.Extra>
                            <Button primary floated='right' onClick={window.open.bind(this, item.url)}>
                                More details
                                <Icon name='right chevron' />
                            </Button>
                            <Label>Limited</Label>
                        </Item.Extra>
                    </Item.Content>
                </Item>

            })}
        </Item.Group>
    );
}