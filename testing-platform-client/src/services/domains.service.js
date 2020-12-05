import config from '../config';
import { authHeader } from '../helpers';


export const domainService = {
    getAll
};

function getAll() {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/domains/`, requestOptions)
        .then(handleResponse)
        .then(domains => {
            return domains.results;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}