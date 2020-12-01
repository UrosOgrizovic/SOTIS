import config from '../config';
import { authHeader } from '../helpers';


export const examService = {
    getAll,
    submitExam
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

function submitExam(examChoices) {
    const token = JSON.parse(localStorage.getItem('user')).token;
    
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(examChoices)
    };

    return fetch(`${config.apiUrl}/exams/submitExam/`, requestOptions)
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