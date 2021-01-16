import config from '../config';
import { authHeader } from '../helpers';


export const examService = {
    getAll,
    submitExam,
    getPersonalizedExams,
    addNewExam,
    deleteExam,
    getExamTakers,
    generateKnowledgeSpace,
    getXML,
    getPersonalizedQuestions,
    getExamGED,
    submitQuestion
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

function submitQuestion(questionData) {
    const token = JSON.parse(localStorage.getItem('user')).token;

    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    headers['X-CSRFToken'] = token;

    const requestOptions = {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(questionData)
    };
    console.log(questionData.answered_questions);
    let examId = questionData.answered_questions[0].exam.id;
    return fetch(`${config.apiUrl}/exams/${examId}/submitQuestion/`, requestOptions)
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

function getExamTakers(examId) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/exams/${examId}/examTakers`, requestOptions)
        .then(handleResponse)
        .then(students => {
            return students;
        });
}

function getPersonalizedQuestions(examId) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/exams/${examId}/personalizedQuestionsOrder`, requestOptions)
        .then(handleResponse)
        .then(students => {
            return students;
        });
}

function generateKnowledgeSpace(examId) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/exams/${examId}/generateKnowledgeSpace`, requestOptions)
        .then(handleResponse)
        .then(() => {
            return [];
        });
}


function getXML(examId) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers,
        responseType: 'blob'
    };

    return fetch(`${config.apiUrl}/exams/${examId}/getXML`, requestOptions)
        .then(handleResponse)
        .then(result => {
            return result;
        });
}


function getExamGED(examId) {
    const headers = authHeader();
    headers['Content-Type'] = 'application/json';
    const requestOptions = {
        method: 'GET',
        headers: headers
    };

    return fetch(`${config.apiUrl}/ged/${examId}/getByExamId`, requestOptions)
        .then(handleResponse)
        .then(result => {
            console.log(result);
            return result;
        });
}


function handleResponse(response) {
    return response.text().then(text => {
        return JSON.parse(text);
    });
}