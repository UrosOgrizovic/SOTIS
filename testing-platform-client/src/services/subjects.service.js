import config from '../config';
import { authHeader } from '../helpers';


export const subjectService = {
    getAll
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

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}