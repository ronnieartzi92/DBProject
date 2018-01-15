/**
 * Created by guyy on 1/11/2018.
 */
import React from 'react'
import { Button, Icon, Item, Label } from 'semantic-ui-react'

const openUrl = (url)=>{
    window.open(url, '_blank');
};


export const ArtistNextConcerts = ({concerts = []}) => {
    if(concerts === []) return <div>No Future Concerts :(</div>;

    return (

        <Item.Group divided>
            {concerts.map((item, index) => {
                return <Item key={index}>
                    {/*<Item.Image src={item.img} />*/}
                    <Item.Content>
                        <Item.Header as='a'>{item.title}</Item.Header>
                        <Item.Meta>
                            <span className='cinema'>{item.city} - {item.country}</span>
                        </Item.Meta>
                        <Item.Description>{item.date}</Item.Description>
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