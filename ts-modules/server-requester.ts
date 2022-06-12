alert("HEY");

const sendFormUrl: string = "/messages";
// const sendFormUrl: string = "/messages_post";

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

let request_body = {
  text: "simple test message",
  user_id: "awesome user id",
};
let postRequest: BasicRequest = {
  method: "POST",
  headers: { "content-type": "application/json;charset=UTF-8" },
  body: JSON.stringify(request_body) 
};

console.log(postRequest.body);

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

