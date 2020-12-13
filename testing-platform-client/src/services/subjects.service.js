import config from '../config';
import { authHeader } from '../helpers';


export const subjectService = {
    getAll,
    addNewSubject
};

function getAll() {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/subjects/`, requestOptions)
        .then(handleResponse)
        .then(subjects => {
            return subjects.results;
        });
}

function addNewSubject(data) {
    const token = JSON.parse(localStorage.getItem('user')).token;
    
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    };

    return fetch(`${config.apiUrl}/subjects/`, requestOptions)
        .then(handleResponse)
        .then(result => {
            return result;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}