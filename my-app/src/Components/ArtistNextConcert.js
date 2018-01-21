/**
 * Created by guyy on 1/11/2018.
 */
import React from 'react'
import { Button, Icon, Item } from 'semantic-ui-react'


export const ArtistNextConcerts = ({concerts = []}) => {
    if(concerts === []) return <div>No Future Concerts :(</div>;
    return (

        <Item.Group divided>
            {concerts.map((item, index) => {
                const image = item.img ? item.img :
                    (index % 4 === 0 ? "https://securecdn.pymnts.com/wp-content/uploads/2017/08/concert.2-457x303.jpg" :
                        (index % 4 === 1 ? "https://www.ticketswest.com/media/1028/concert_Featured%20Event%20Tile.jpg" :
                            (index % 4 === 2 ? "https://scottkelby.com/wp-content/uploads/2009/08/concert1.jpg": "http://www.mehek.in/wp-content/uploads/2014/09/night-out-with-friends.jpg")));
                return <Item key={index}>
                    <Item.Image src={image} />
                    <Item.Content>
                        <Item.Header as='a' href={item.url} target="_blank">{item.title}</Item.Header>
                        <Item.Meta>
                            <span className='cinema'>{item.venue}</span>
                        </Item.Meta>
                        <Item.Meta>
                            <span className='cinema'>{item.city} - {item.country}</span>
                        </Item.Meta>
                        <Item.Description>{item.event_date}</Item.Description>
                        <Item.Extra>
                            <a href={item.url} target="_blank">
                            <Button primary floated='right' >
                                More details
                                <Icon name='right chevron' />
                            </Button>
                            </a>
                            {/*<Label>Soon !</Label>*/}
                        </Item.Extra>
                    </Item.Content>
                </Item>

            })}
        </Item.Group>
    );
}