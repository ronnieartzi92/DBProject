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
    Sidebar
} from 'semantic-ui-react'
import {GoogleLogin, GoogleLogout } from 'react-google-login';
import Playlist from "./pages/Playlist";
import {HomePage} from "./HomePage";
import MyPlaylists from "./pages/MyPlaylists";
import MakeMePlaylist from "./pages/MakeMePlaylist";
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
        this.state = {visible :true, isLoggedIn : false, page: "home"};
    }

    hideFixedMenu = () => this.setState({visible: false});
    showFixedMenu = () => this.setState({visible: true});
    toggleVisibility = () => this.setState({ visible: !this.state.visible });

    stopQuestionsStartRest(answers = {}) {

        if (answers !== {}) {

            sdk.getQuestions(answers, 10).then((data) => {
                    console.log(data);
                },
                (reason) => {
                    alert("Server Not Responding....");
                }
            );
        }
    }


    responseGoogle(response) {
        console.log(response);
        if(response.ok){//todo ???
            this.setState({ isLoggedIn: true });
        }
    }
    logout(){
        this.setState({ isLoggedIn: false });
    }
    setPage(page){
        this.setState({ page: page });
    }

    render() {
        const {visible} = this.state;

        return (
            <div>


                <div>
                    <Button onClick={this.toggleVisibility}>Toggle Menu</Button>
                    <Sidebar.Pushable as={Segment}>
                        <Sidebar as={Menu} animation='overlay' width='thin' visible={visible} icon='labeled' vertical inverted>
                            <Menu.Item name='home' onClick={this.setPage.bind(this, "home")}>
                                <Icon name='home' />
                                Home
                            </Menu.Item>
                            <Menu.Item name='list layout' onClick={this.setPage.bind(this,"myplaylists")}>
                                <Icon name='list layout' />
                                My Playlists
                            </Menu.Item>
                            <Menu.Item name='music' onClick={this.setPage.bind(this,"makeplaylist")}>
                                <Icon name='music' />
                                Make Me A Playlist
                            </Menu.Item>
                        </Sidebar>
                        <Sidebar.Pusher>
                            <Segment basic>
                                <Header as='h3'>
                                    <Visibility /*onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu}*/ once={false}>
                                        <Segment inverted textAlign='center' style={{minHeight: 100, padding: '1em 0em'}} vertical>
                                            <Container>
                                                <Menu inverted pointing secondary size='large'>
                                                    <Menu.Item as='a' active></Menu.Item>
                                                    <Menu.Item position='right'>
                                                        {/*<Button as='a' inverted>Log in</Button>*/}
                                                        {!this.state.isLoggedIn && <GoogleLogin
                                                            clientId="658977310896-knrl3gka66fldh83dao2rhgbblmd4un9.apps.googleusercontent.com"
                                                            buttonText="Login"
                                                            onSuccess={this.responseGoogle}
                                                            onFailure={this.responseGoogle}
                                                        />}
                                                        {this.state.isLoggedIn &&
                                                        <GoogleLogout
                                                            buttonText="Logout"
                                                            onLogoutSuccess={this.logout}
                                                        >
                                                        </GoogleLogout>}

                                                        {/*<Button as='a' inverted style={{marginLeft: '0.5em'}}>Sign Up</Button>*/}
                                                    </Menu.Item>
                                                </Menu>
                                            </Container>
                                        </Segment>
                                    </Visibility>
                                    <Visibility /*onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu}*/ once={false}>
                                        <Segment inverted textAlign='center' style={{minHeight: 700, padding: '1em 0em', background: 'white', paddingTop: 0}} vertical>
                                    {this.state.page === "home" && HomePage}
                                    {this.state.page === "myplaylists" && <MyPlaylists/>}
                                    {this.state.page === "makeplaylist" && <MakeMePlaylist/>}
                                        </Segment>
                                    </Visibility>


                                </Header>
                                <Image src='/assets/images/wireframe/paragraph.png' />
                            </Segment>
                        </Sidebar.Pusher>
                    </Sidebar.Pushable>
                </div>

            </div>
        )
    }
}