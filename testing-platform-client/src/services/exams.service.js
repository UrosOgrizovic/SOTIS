import config from '../config';
import { authHeader } from '../helpers';


export const examService = {
    getAll,
    submitExam,
    getPersonalizedExams,
    addNewExam,
    deleteExam
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

function addNewExam(data) {
    const token = JSON.parse(localStorage.getItem('user')).token;
    
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(data)
    };

    return fetch(`${config.apiUrl}/exams/`, requestOptions)
        .then(handleResponse)
        .then(result => {
            return result;
        });
}

function submitExam(examData) {
    const token = JSON.parse(localStorage.getItem('user')).token;
    
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(examData)
    };

    return fetch(`${config.apiUrl}/exams/${examData['id']}/submitExam/`, requestOptions)
        .then(handleResponse)
        .then(result => {
            return result;
        });
}

function deleteExam(data) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'DELETE',
        headers: headers
    };

    return fetch(`${config.apiUrl}/exams/${data.id}`, requestOptions)
        .then(() => {})
}

function getPersonalizedExams(data) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/domains/${data.id}/personalized_exams`, requestOptions)
        .then(handleResponse)
        .then(exams => {
            return exams;
        });
}


function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}