import http.client
import json
import ssl

def get_ip_info(ip):
    conn = http.client.HTTPSConnection("IP-LOOKUP-API.proxy-production.allthingsdev.co", context=ssl._create_unverified_context())
    payload = json.dumps({"ip": ip})
    headers = {
        'x-api-key': 'aMFouLkMjcxGopFBPmzjWGMKQCkVKPDMsghukTvPHaPWzsqALZZFfGRtpBgvEKVVLGDJjDBavveHcoVKhuqjovsRWhkgGEQiyRmX',
        'x-app-version': '1.0.0',
        'x-apihub-key': 'vPEJ--4lAxelaTxs1lvBMaDlCXV3gugTXgVwyjlE037u2AL970',
        'x-apihub-host': 'IP-LOOKUP-API.allthingsdev.co',
        'x-apihub-endpoint': '07d744ae-ea6d-4f24-b757-882e5bbe8692',
        'Content-Type': 'application/json'
    }
    
    conn.request("POST", "/api/v1/iplookup/loc-find", payload, headers)
    res = conn.getresponse()
    data = res.read()
    response_json = json.loads(data.decode("utf-8"))

    if response_json["success"]:
        data = response_json["data"]
        city = data.get("city", "Unknown")
        country = data.get("country", "Unknown")
        lat, long = data.get("ll", [None, None])
        return {
            "city": city,
            "country": country,
            "latitude": lat,
            "longitude": long
        }
    else:
        return {
            "error": response_json.get("message", "An error occurred")
        }

# Example usage
ip = "196.188.126.80"
info = get_ip_info(ip)
print(info)



#google ai api Key

# AIzaSyC6AlqpdiaH3ZipthjDVyQ5ikd9rwQ69fM