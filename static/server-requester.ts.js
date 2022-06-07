const sendFormUrl = "/viewform"

function displayServerResponse(message) {
  alert(message)
}

async function sendRequest(request, url) {
  return await window.fetch(url, request)
}

let postRequest = {
  method: "POST",
  headers: '"content-type": "application/json;charset=UTF-8"',
  body: "token_id: awesomeToken, text:test"
}

let response = sendRequest(postRequest, sendFormUrl)
response.then(
  function(value) {
    value.text().then(displayServerResponse, function onError(error) {
      alert("error " + error)
    })
  },
  function(error) {
    alert("Some error received: " + error)
  }
)
