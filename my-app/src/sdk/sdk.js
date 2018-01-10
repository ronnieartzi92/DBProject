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

export default {
    startSession: function () {
        return axios.get(`/session/new`)
    },
    rankByPrice: function (sessionId, price, rank) {
        return axios.put(`/session/rank/price/smaller/${sessionId}`, {price, rank})
    },
    rankByCategory: function (sessionId, category, rank) {
        return axios.put(`/session/rank/price/smaller/${sessionId}`, {category, rank})
    },
    getTopResturants: function(sessionId, count) {
        return axios.get(`/session/top/${sessionId}?count=${count}`)
    },
    getQuestions: function(answers, count) {
        return axios.post(`/restaurant/top/${count}`, answers)
    }
}
