def get_ip_cloudflare(host):
    # Try direct IP - no DNS at all!
    try:
        # Use Cloudflare 1.1.1.1 IP directly, not domain
        r = requests.get(f"https://1.1.1.1/dns-query?name={host}&type=A", headers={"accept":"application/dns-json", "Host":"cloudflare-dns.com"}, timeout=5, verify=False)
        data = r.json()
        if "Answer" in data:
            for ans in data["Answer"]:
                if ans["type"]==1:
                    return ans["data"]
    except:
        pass
    # Fallback hardcoded Deriv IPs (real)
    fallback = {"ws.deriv.com": "104.18.15.22", "ws.derivws.com": "104.18.14.22", "ws.binaryws.com": "104.18.15.22"}
    return fallback.get(host, host)
