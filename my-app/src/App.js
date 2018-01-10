import React, {Component} from 'react'
import sdk from "./sdk/sdk"
import {
    Button,
    Container,
    Divider,
    Grid,
    Header,
    Icon,
    Image,
    List,
    Menu,
    Segment,
    Visibility,
} from 'semantic-ui-react'
import {GoogleLogin} from 'react-google-login';
import Playlist from "./pages/Playlist";
require('./css/main.css')

const FixedMenu = () => (
    <Menu fixed='top' size='large'>
        <Container>
            <Menu.Item as='a' active>Home</Menu.Item>
            <Menu.Item as='a'>Work</Menu.Item>
            <Menu.Item as='a'>Company</Menu.Item>
            <Menu.Item as='a'>Careers</Menu.Item>
            <Menu.Menu position='right'>
                <Menu.Item className='item'>
                    <Button as='a'>Log in</Button>
                </Menu.Item>
                <Menu.Item>
                    <Button as='a' primary>Sign Up</Button>
                </Menu.Item>
            </Menu.Menu>
        </Container>
    </Menu>
)

export default class App extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {};
    }

    hideFixedMenu = () => this.setState({visible: false});
    showFixedMenu = () => this.setState({visible: true});

    stopQuestionsStartRest(answers = {}) {

        if (answers !== {}) {

            sdk.getQuestions(answers, 10).then((data) => {
                    console.log(data);

                    this.setState({
                        isLoading: false,
                        isSwipingQuestions: false,
                        isSwipingResturants: true,
                        rests: data.data
                    });
                },
                (reason) => {
                    this.setState({
                        isLoading: false,
                        isSwipingQuestions: false,
                        isSwipingResturants: true,
                        rests: []
                    });

                    alert("Server Not Responding....");
                }
            );
        }
    }


    responseGoogle(response) {
        console.log(response);
    }

    render() {
        const {visible} = this.state;

        return (
            <div>
                { visible ? <FixedMenu /> : null }
                <Visibility onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu} once={false}>
                    <Segment inverted textAlign='center' style={{minHeight: 700, padding: '1em 0em'}} vertical>
                        <Container>
                            <Menu inverted pointing secondary size='large'>
                                <Menu.Item as='a' active>Home</Menu.Item>
                                <Menu.Item position='right'>
                                    <Button as='a' inverted>Log in</Button>
                                    <GoogleLogin
                                        clientId="658977310896-knrl3gka66fldh83dao2rhgbblmd4un9.apps.googleusercontent.com"
                                        buttonText="Login"
                                        onSuccess={this.responseGoogle}
                                        onFailure={this.responseGoogle}
                                    />
                                    <Button as='a' inverted style={{marginLeft: '0.5em'}}>Sign Up</Button>
                                </Menu.Item>
                            </Menu>
                        </Container>

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
                                <Image bordered rounded size='large' src='../public/music.png'/>
                            </Grid.Column>
                        </Grid.Row>
                        <Grid.Row>
                            <Grid.Column textAlign='center'>

                            </Grid.Column>
                        </Grid.Row>
                    </Grid>
                    <Playlist/>
                </Segment>
            </div>
        )
    }
}