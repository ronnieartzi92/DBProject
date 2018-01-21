/**
 * Created by guyy on 1/8/2018.
 */
import axios from 'axios';

axios.defaults.baseURL = 'http://delta-tomcat-vm.cs.tau.ac.il:40744/';
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
    savePlaylist: function (token, name, list) {
        let ids = [];
        list.forEach((item) => {
            ids.push(item.track_id)
        });
        return axios.post(`/playlist`, {name, songs: ids}, AuthHeader(token)).then(extractData);
    },
    getPlaylists: function (token) {
        return axios.get(`/playlist`, AuthHeader(token)).then(extractData);
    },
    getPlaylistSongs: function(token, playlistId) {
        return axios.get(`/playlist?id=${playlistId}`, AuthHeader(token)).then(extractData);
    },
    getArtistConcerts: function(token, artistId) {
        return axios.get(`/artist/events?id=${artistId}`, AuthHeader(token)).then(extractData);
    },
    searchForPlaylist: function (token, searchText, limit) {
        return axios.get(`/track/search?text=${searchText}&limit=${limit}`, AuthHeader(token)).then(extractData);
    },
    savePlaylistTags: function (token, id, tags) {
        return axios.post(`/playlist/tags?id=${id}`, {tags}, AuthHeader(token)).then(extractData);
    },
    getTags: function (token) {
        return axios.get(`/tag`,AuthHeader(token)).then(extractData);
    },
    makePlaylist: function (token, path) {
        return axios.get(`/track/${path}`,AuthHeader(token)).then(extractData);
    },
    getSimilarPlaylist: function (token, playId) {
        return axios.get(`/track/playlist_mode?playlist_id=${playId}`,AuthHeader(token)).then(extractData);
    }
}
