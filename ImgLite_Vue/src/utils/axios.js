import axios from "axios";
import Cookies from 'js-cookie'

const baseURL = 'http://localhost:8000/api/'

const axiosDefaultInstance = axios.create({
    baseURL,
    timeout: 3000
})

const axiosCredentialsInstance = axios.create({
    baseURL,
    timeout: 3000
})
axiosCredentialsInstance.defaults.withCredentials = true

const uploadConfig = {
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/form-data'

    }
}

const registerConfig = {
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
}

const deleteConfig = {
    headers: {
        'X-CSRFToken': Cookies.get('csrftoken'),
        'X-Requested-With': 'XMLHttpRequest'
    }
}

export  {baseURL, axiosDefaultInstance, axiosCredentialsInstance, uploadConfig, registerConfig, deleteConfig}
