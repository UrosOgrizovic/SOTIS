import config from '../config';
import { authHeader } from '../helpers';


export const questionService = {
    getAll
};

function getAll() {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/questions/`, requestOptions)
        .then(handleResponse)
        .then(questions => {
            return questions.results;
        });
}

function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}