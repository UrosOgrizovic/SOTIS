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
        .then(questions => {
            return questions;
        });
}