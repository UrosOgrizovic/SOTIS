import config from '../config';
import { authHeader } from '../helpers';


export const domainService = {
    getAll,
    deleteDomain,
    addStudentToDomain
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

function deleteDomain(data) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'DELETE',
        headers: headers
    };

    return fetch(`${config.apiUrl}/domains/${data.id}`, requestOptions)
        .then(() => {})
}


function addStudentToDomain(data) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'PATCH',
        headers: headers,
        body: JSON.stringify({id: data.student})
    };

    return fetch(`${config.apiUrl}/domains/${data.domain.id}/add-student/`, requestOptions)
        .then(() => {})
}
function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}