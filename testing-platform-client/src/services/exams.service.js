import config from '../config';
import { authHeader } from '../helpers';


export const examService = {
    getAll
};

function getAll() {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/exams/`, requestOptions)
        .then(handleResponse)
        .then(exams => {
            return exams.results;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}