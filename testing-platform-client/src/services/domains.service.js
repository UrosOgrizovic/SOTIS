import config from '../config';
import { authHeader } from '../helpers';


export const domainService = {
    getAll,
    get
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

function get(id) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    
    return fetch(`${config.apiUrl}/domains/${id}`, requestOptions)
        .then(handleResponse)
        .then(domain => {
            return domain;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}