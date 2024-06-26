import http from 'k6/http';
import {check} from "k6";

export default function () {
    const url = 'http://127.0.0.1:8000/AReq';
    const payload = JSON.stringify({'pan': 123, 'dad': 123});
    const params = {headers: {'Content-Type': 'application/json', 'X-Initiator-Service': '1800_CRAC', 'X-Call-ID': '20220724_1454', 'X-Initiator-Host': '102.102.102.102', 'X-MDM-ID': '1234567', 'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdWIxIiwiY2hhbm5lbCI6ImNoYW5uZWwxIn0.hFv_VLraxgsm419h7Xt6FJpPPGzZy4d_voKqyojGt3A', timeout: "60s"}
    };
    const response = http.post(url, payload, params);
    console.log(response.status)
    console.log(response.timings.duration)
    check(response, {"200": (r) => r.status === 200})
};