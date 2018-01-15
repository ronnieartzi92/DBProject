/**
 * Created by guyy on 1/8/2018.
 */
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:5000/';
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';


const extractData = (response) => {
    const data = response.data;
    if(data) return data;
    else return null;
};

const AuthHeader = (token) => {
    return {
        headers: {
            Authorization: `OAuth ${token}`
        }
    }
};

export default {
    login: function () {
        return axios.get(`/session/new`)
    },
    savePlaylist: function (token, list) {
        return axios.post(`/playlist`, {list}, AuthHeader(token)).then(extractData);
    },
    getPlaylists: function (token) {
        return axios.get(`/playlist`, AuthHeader(token)).then(extractData);
    },
    getPlaylistSongs: function(token, playlistId) {
        return axios.get(`/playlist?id=${playlistId}`, AuthHeader(token)).then(extractData);
    },
    getArtistConcerts: function(token, artistId) {
        return axios.get(`/artist/concers?id=${artistId}`, AuthHeader(token)).then(extractData);
    }
}
