import request from './request'
import { addPendingRequest, removePendingRequest } from './req_tool'

export function getDeviceList(params) {
    const  config = {
        url: '/api/v1/devices/list', method: 'get', params: params
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function getPackageList(device) {
    const config = {
        url: '/api/v1/devices/' + device + '/packagelist', method: 'get', params: {}
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function startAPP(data) {
    const config = {
        url: '/api/v1/devices/app', method: 'post', data
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function SyncTask(params) {
    const config = {
        url: '/task/sync', method: 'get', params: params
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function GetCaseInfo(id) {
    const config = {
        url: '/case/' + id, method: 'get',
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function getMetaFileList(params) {
    const config = {
        url: '/file/meta/list', method: 'get', params: params
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function installApp(data) {
    const config = {
        url: '/api/v1/devices/install', method: 'post', data
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function getPerfDataList(params) {
    const config = {
        url: '/api/v1/data', method: 'get', params: params
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function newPerfRecord(data) {
    const config = {
        url: '/api/v1/data', method: 'post', data
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function deletePerfRecord(id) {
    const config = {
        url: '/api/v1/data/' + id, method: 'delete'
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}

export function updatePerfRecord(id, data) {
    const config = {
        url: '/api/v1/data/' + id, method: 'patch', data
    }
    removePendingRequest(config);
    addPendingRequest(config);
    return request(config)
}