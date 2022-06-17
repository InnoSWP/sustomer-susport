var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
alert("HEY");
const sendFormUrl = "/messages";
function displayServerResponse(message) {
    alert(message);
}
function sendRequest(request, url) {
    return __awaiter(this, void 0, void 0, function* () {
        return yield window.fetch(url, request);
    });
}
let request_body = {
    text: "simple test message",
    user_id: "awesome user id",
};
let postRequest = {
    method: "POST",
    headers: { "content-type": "application/json;charset=UTF-8" },
    body: JSON.stringify(request_body)
};
console.log(postRequest.body);
let response = sendRequest(postRequest, sendFormUrl);
response.then(function (value) {
    value.text().then(displayServerResponse, function onError(error) {
        alert("error " + error);
    });
}, function (error) {
    alert("Some error received: " + error);
});
//# sourceMappingURL=debug-script.js.map