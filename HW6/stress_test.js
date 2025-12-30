import http from 'k6/http';
import { sleep } from 'k6';

export const options = {
  stages: [
    // 1. Ramp up to 1000 users over 30 seconds
    { duration: '30s', target: 1000 }, 
    
    // 2. Sustain that load for 10 minutes
    { duration: '10m', target: 1000 }, 
  ]
};

export default function () {
  const BASE_URL = 'http://192.168.100.6:8000'; 
  const full_url = BASE_URL + '/work?ms=5000';

  http.get(full_url);

  sleep(0.1); 
}