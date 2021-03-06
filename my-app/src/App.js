import React, {Component} from 'react'
import sdk from "./sdk/sdk"
import {
    Container,
    Header,
    Icon,
    Menu,
    Segment,
    Visibility,
    Sidebar,
} from 'semantic-ui-react'
import {GoogleLogin, GoogleLogout } from 'react-google-login';
import {HomePage} from "./HomePage";
import MyPlaylists from "./pages/MyPlaylists";
import MakeMePlaylist from "./pages/MakeMePlaylist";
import LoginModel from "./Components/LoginModel";
require('./css/main.css');



export default class App extends Component {
    constructor(props, context) {
        super(props, context);
        this.state = {visible :false, isLoggedIn : false, page: "home", modalOpen: false, formError : "", userToken : null};
    }

    hideFixedMenu = () => this.setState({visible: false});
    showFixedMenu = () => this.setState({visible: true});
    toggleVisibility = () => this.setState({ visible: !this.state.visible });
    openSignup = () => this.setState({modalOpen: true, modelType: "Sign Up"});
    openLogin = () => this.setState({modalOpen: true, modelType: "Login"});

    // validateEmail = (email) => {
    //     const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    //     return re.test(email.toLowerCase());
    // };

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


    responseGoogle = (response) => {
        console.log(response);
        if(response && response.profileObj){
            this.setState({isLoggedIn: true, userFullName: response.profileObj.name,
                            userToken: response.tokenId,
                            userImage : response.profileObj.imageUrl, visible: true});
        } console.log(response.tokenId);
    };

    setPage(page){
        this.setState({ page: page });
    }
    openMyPlaylists(){
        this.setPage("myplaylists");
    }

    logout = () => {
        this.setState({isLoggedIn: false, visible: false});
        this.setPage("home");
    };

    loginOrSignup = (email, password) => {
        if(!this.validateEmail(email)){
            this.setState({formError: "Email is not valid"});
        }
        else if(password.length < 5){
            this.setState({formError: "Password should be at least 5 chars"});
        }
        else{
            alert(email);
            this.setState({modalOpen: false, isLoggedIn :true, formError: ""});
        }

    };
    handleCloseModel = () => this.setState({ modalOpen: false });



    render() {
        const {visible} = this.state;

        return (
            <div>
                <LoginModel modalOpen={this.state.modalOpen} type={this.state.modelType} onSubmit={this.loginOrSignup} error={this.state.formError} handleClose={this.handleCloseModel} />

                <div>
                    {/*<Button onClick={this.toggleVisibility}>Toggle Menu</Button>*/}
                    <Sidebar.Pushable as={Segment}>
                        <Sidebar as={Menu} animation='overlay' width='thin' visible={true} icon='labeled' vertical inverted style={{top: '12px'}}>
                            <Menu.Item name='home' onClick={this.setPage.bind(this, "home")}>
                                <Icon name='home' />
                                Home
                            </Menu.Item>
                            {this.state.isLoggedIn && <Menu.Item name='list layout' onClick={this.setPage.bind(this,"myplaylists")}>
                                <Icon name='list layout' />
                                My Playlists
                            </Menu.Item>}
                            {this.state.isLoggedIn && <Menu.Item name='music' onClick={this.setPage.bind(this,"makeplaylist")}>
                                <Icon name='music' />
                                Make Me A Playlist
                            </Menu.Item>}
                        </Sidebar>
                        <Sidebar.Pusher>
                            <Segment basic style={{padding: '0'}}>
                                <Header as='h3'>
                                    <Visibility /*onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu}*/ once={false}>
                                        <Segment inverted textAlign='center' style={{minHeight: 100, padding: '1em 0em'}} vertical>
                                            <Container>
                                                <Menu inverted pointing secondary size='large'>
                                                    {/*<Menu.Item as='a' active></Menu.Item>*/}
                                                    <Menu.Item position='right' style={{width: '90%'}}>
                                                        {!this.state.isLoggedIn && <div>
                                                        {/*<Button as='a' inverted style={{marginLeft: '0.5em'}} onClick={this.openSignup.bind(this)}>Sign Up</Button>*/}
                                                        {/*<Button as='a' inverted onClick={this.openLogin.bind(this)}>Log in</Button>*/}
                                                        </div>}
                                                            {!this.state.isLoggedIn && <GoogleLogin
                                                            clientId="60150906703-els4j53jkve5kd9ijdf70s5l7k40ccsd.apps.googleusercontent.com"
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

                                                    </Menu.Item>
                                                    {this.state.isLoggedIn && <Menu.Item active position='right' onClick={this.openMyPlaylists.bind(this)}>
                                                        <img src={this.state.userImage} style={{marginRight : '20px'}} alt="User" />
                                                        Hey {this.state.userFullName}
                                                    </Menu.Item>
                                                    }
                                                </Menu>
                                            </Container>
                                        </Segment>
                                    </Visibility>
                                    <Visibility /*onBottomPassed={this.showFixedMenu} onBottomVisible={this.hideFixedMenu}*/ once={false}>
                                        <Segment inverted textAlign='center' style={{minHeight: 700, padding: '1em 0em', background: 'white', paddingTop: 0, marginLeft: "135px"}} vertical>
                                    {this.state.page === "home" && HomePage}
                                    {this.state.page === "myplaylists" && <MyPlaylists userToken={this.state.userToken}/>}
                                    {this.state.page === "makeplaylist" && <MakeMePlaylist userToken={this.state.userToken}/>}
                                        </Segment>
                                    </Visibility>


                                </Header>
                            </Segment>
                        </Sidebar.Pusher>
                    </Sidebar.Pushable>
                </div>

            </div>
        )
    }
}