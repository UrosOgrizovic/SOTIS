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
        .then(exams => {
            return exams;
        });
}