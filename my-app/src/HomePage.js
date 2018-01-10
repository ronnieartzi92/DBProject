/**
 * Created by guyy on 1/10/2018.
 */
import React, {Component} from 'react'
import {
    Button,
    Container,
    Grid,
    Header,
    Icon,
    Image,
    Segment,
    Visibility,
} from 'semantic-ui-react'
import image from './img/music.png'

export const HomePage = <div>
    {/*{ visible ? <FixedMenu /> : null }*/}


    <Visibility /*onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu}*/ once={false}>
        <Segment inverted textAlign='center' style={{minHeight: 700, padding: '1em 0em'}} vertical>

            <Container text>
                <Header as='h1' content='Songs Track' inverted
                        style={{fontSize: '4em', fontWeight: 'normal', marginBottom: 0, marginTop: '3em'}}/>
                <Header as='h2' content='Listen whatever you want whenever you want.' inverted
                        style={{fontSize: '1.7em', fontWeight: 'normal'}}/>
                <Button primary size='huge'>
                    Get Started
                    <Icon name='right arrow'/>
                </Button>
            </Container>
        </Segment>
    </Visibility>

    <Segment style={{padding: '8em 0em'}} vertical>
        <Grid container stackable verticalAlign='middle'>
            <Grid.Row>
                <Grid.Column width={8}>
                    <Header as='h3' style={{fontSize: '2em'}}>No matter which mood you In..</Header>
                    <p style={{fontSize: '1.33em'}}>
                        We can fit you the exactly music you up to, the music that gonna make you laugh,
                        cry, or both.
                    </p>
                    <Header as='h3' style={{fontSize: '2em'}}>No matter who you with or where you
                        are</Header>
                    <p style={{fontSize: '1.33em'}}>
                        Our music going to makes your time more delightful then ever.
                    </p>
                </Grid.Column>

                <Grid.Column floated='right' width={6}>
                    <Image bordered rounded size='large' src={image}/>
                </Grid.Column>
            </Grid.Row>
            <Grid.Row>
                <Grid.Column textAlign='center'>

                </Grid.Column>
            </Grid.Row>
        </Grid>
    </Segment>

</div>