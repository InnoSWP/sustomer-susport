const sendFormUrl: string = "/viewform";

function displayServerResponse(message: string): void {
  alert(message);
}

interface BasicRequest {
  method: string;
  headers: {};
  body: string;
}

async function sendRequest(
  request: BasicRequest,
  url: string
): Promise<Response> {
  return await window.fetch(url, request);
}

interface RequestData {
  token_id: string;
}

let postRequest: BasicRequest = {
  method: "POST",
  headers: '"content-type": "application/json;charset=UTF-8"',
  body: "token_id: awesomeToken, text:test",
};

let response = sendRequest(postRequest, sendFormUrl);
response.then(
  function (value: Response) {
    value.text().then(displayServerResponse, function onError(error) {
      alert("error " + error);
    });
  },
  function (error) {
    alert("Some error received: " + error);
  }
);
