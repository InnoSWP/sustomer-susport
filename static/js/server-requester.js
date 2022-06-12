var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
const sendFormUrl = "/viewform";
function displayServerResponse(message) {
    alert(message);
}
function sendRequest(request, url) {
    return __awaiter(this, void 0, void 0, function* () {
        return yield window.fetch(url, request);
    });
}
let postRequest = {
    method: "POST",
    headers: { "content-type": "application/json;charset=UTF-8" },
    body: "token_id: awesomeToken, text:test",
};
let response = sendRequest(postRequest, sendFormUrl);
response.then(function (value) {
    value.text().then(displayServerResponse, function onError(error) {
        alert("error " + error);
    });
}, function (error) {
    alert("Some error received: " + error);
});
alert("HEY");
//# sourceMappingURL=server-requester.js.map