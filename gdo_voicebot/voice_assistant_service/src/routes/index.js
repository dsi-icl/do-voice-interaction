import fetch from "node-fetch";

export function sampleData(req, res) {
    res.json({data: "sampleData"});
}

export async function getData(requestUrl,robotAnswer){

    var url = new URL(requestUrl),
        params = {text:robotAnswer,lang:"en"};
    Object.keys(params).forEach(key =>
        url.searchParams.append(key, params[key]));
    let response = await fetch(url);
    let data = await response.arrayBuffer();

    return data;
}

export async function postData(url, data) {
    let jsondata;
    await fetch(url, {
        method: "post",
        headers: { "Content-type": "text/plain" },
        body: data
        })
        .then(res => res.json())
        .then(json => {
            jsondata = json;
        })
        .catch(error => {
            console.log("Error", error);
            return null;
        });

    return jsondata;
}