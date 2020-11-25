import config from '../config';
import { authHeader } from '../helpers';


export const choiceService = {
    getAll
};

function getAll() {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/choices/`, requestOptions)
        .then(handleResponse)
        .then(choices => {
            return choices.results;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}