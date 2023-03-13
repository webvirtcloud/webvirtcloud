import ky from 'ky';
import { redirect } from 'react-router-dom';

import { API_HOST } from '@/constants';

const request = ky.create({
  prefixUrl: API_HOST,
  hooks: {
    beforeRequest: [
      (request) => {
        const token = window.localStorage.getItem('token');

        if (token) {
          request.headers.set('Authorization', `Bearer ${token}`);
        }

        return request;
      },
    ],
    afterResponse: [
      (_request, _options, response) => {
        return response;
      },
      (request, options, response) => {
        if (response.status === 401) {
          window.localStorage.removeItem('token');

          redirect('/sign-in');
        }
      },
    ],
  },
});

export default request;
