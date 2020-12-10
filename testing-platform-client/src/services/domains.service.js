import config from '../config';
import { authHeader } from '../helpers';


export const domainService = {
    getAll,
    get,
    createLink
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

function createLink(link) {
    const token = JSON.parse(localStorage.getItem('user')).token;
    
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        // method: 'PUT',
        method: 'POST',
        headers: headers,
        body: JSON.stringify(link)
    };

    // return fetch(`${config.apiUrl}/domains/add_problem_attachment/`, requestOptions)
    return fetch(`${config.apiUrl}/problem_attachments/custom_create/`, requestOptions)
        .then(handleResponse)
        .then(result => {
            if (typeof result === "string")
                return false;
            return true;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}