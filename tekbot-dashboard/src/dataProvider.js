import { fetchUtils } from 'react-admin';
import simpleRestProvider from 'ra-data-simple-rest';

const apiUrl = 'http://localhost:8000';
const httpClient = fetchUtils.fetchJson;
export default simpleRestProvider(apiUrl, httpClient);