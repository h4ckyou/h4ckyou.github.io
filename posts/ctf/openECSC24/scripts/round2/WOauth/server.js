const twMerge = createTailwindMerge(getDefaultConfig);

function login(e) {
    const r = "token%20id_token",
        t = "openid%20laundry%20amenities",
        o = "nonce",
        s = "implicit",
        i = "http://localhost:5173/";
    fetch(`${e}/api/v1/creds`).then(n => n.json().then(c => {
        const d = c.client_id;
        new XMLHttpRequest, fetch(`${e}/openid/authentication?response_type=${r}&client_id=${d}&scope=${t}&redirect_uri=${i}&grant_type=${s}&nonce=${o}`).then(b => {
            var f;
            const p = /access_token=[^&]+/;
            (f = b.body) == null || f.getReader().read().then(h => {
                var g;
                const y = new TextDecoder().decode(h.value),
                    x = (g = p.exec(y)) == null ? void 0 : g[0].split("=")[1];
                console.log(`ACCESS TOKEN: ${x}`), sessionStorage.setItem("accessToken", x), sessionStorage.setItem("admin", "0"), document.location.reload()
            })
        })
    }))
}

function loggedIn() {
    return sessionStorage.getItem("accessToken") !== null
}

function isAdmin() {
    return sessionStorage.getItem("admin") == "1"
}

function populateLaundriesAndAmenities(backendUri) {
    let laundries = [],
        amenities = [];
    fetch(`${backendUri}/api/v1/laundry`, {
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
            Host: `${backendUri}`
        }
    }).then(async l => {
        var e, r;
        laundries = eval(new TextDecoder().decode((r = await ((e = l.body) == null ? void 0 : e.getReader().read())) == null ? void 0 : r.value)), sessionStorage.setItem("laundries", JSON.stringify(laundries))
    }), fetch(`${backendUri}/api/v1/amenities`, {
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
            Host: `${backendUri}`
        }
    }).then(async a => {
        var e, r;
        amenities = eval(new TextDecoder().decode((r = await ((e = a.body) == null ? void 0 : e.getReader().read())) == null ? void 0 : r.value)), sessionStorage.setItem("amenities", JSON.stringify(amenities))
    })
}

function generateReport(e) {
    fetch(`${e}/api/v1/generate-report`, {
        headers: {
            Authorization: `Bearer ${sessionStorage.getItem("accessToken")}`,
            Host: `${e}`,
            "Content-Type": "application/json"
        },
        method: "POST",
        body: "{}"
    }).catch(r => console.log(r)).then(r => r == null ? void 0 : r.blob()).then(r => {
        if (!(r === void 0 || r.type === "application/json")) {
            var t = window.URL.createObjectURL(r);
            window.location.assign(t)
        }
    })
}

function logout() {
    sessionStorage.clear(), document.location.reload()
}
const PUBLIC_BACKEND_URI = "http://woauthalaundry.challs.open.ecsc2024.it";
export {
    PUBLIC_BACKEND_URI as P, get_spread_update as a, get_spread_object as b, login as c, logout as d, generateReport as g, isAdmin as i, loggedIn as l, populateLaundriesAndAmenities as p, twMerge as t
};
