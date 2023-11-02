import axios from 'axios';

const pendingRequests = new Map();

const addPendingRequest = (config) => {
    const requestKey = getRequestKey(config);
    config.cancelToken = config.cancelToken || new axios.CancelToken((cancel) => {
        if (!pendingRequests.has(requestKey)) {
            pendingRequests.set(requestKey, cancel);
        }
    });
};

const removePendingRequest = (config) => {
    const requestKey = getRequestKey(config);
    if (pendingRequests.has(requestKey)) {
        const cancel = pendingRequests.get(requestKey);
        cancel('Request canceled');
        pendingRequests.delete(requestKey);
    }
};

const getRequestKey = (config) => {
    return `${config.method}:${config.url}`;
};

export { addPendingRequest, removePendingRequest }