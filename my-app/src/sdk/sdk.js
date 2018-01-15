/**
 * Created by guyy on 1/8/2018.
 */
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:8080/';
axios.defaults.headers.post['Content-Type'] = 'application/json';
axios.defaults.headers.put['Content-Type'] = 'application/json';

//
// const extractData = (response) => {
//     const data = response.data;
//     const requestId = response.headers["x-dfio-req-id"];
//     if(data) {
//         return data;
//     }else return {requestId};
// };

const AuthHeader = (token) => {
    return {
        headers: {
            Authentication: `OAuth ${token}`
        }
    }
};

export default {
    login: function () {
        return axios.get(`/session/new`)
    },
    savePlaylist: function (token, list) {
        return axios.post(`/playlist`, {list}, AuthHeader(token))
    },
    getPlaylists: function (token) {
        return axios.get(`/playlist`, AuthHeader(token))
    },
    getPlaylistSongs: function(token, playlistId) {
        return axios.get(`/playlist?id=${playlistId}`, AuthHeader(token))
    }
}
