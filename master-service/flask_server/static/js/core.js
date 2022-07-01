function html2text(htmlElement) {
    if (htmlElement == null) {
        return "";
    }
    return htmlElement.value;
}
const defaultRequest = {
    method: "GET",
    headers: { "content-type": "application/json;charset=UTF-8" },
};
function basicFetch(parameters) {
    const promise = window.fetch(parameters.url, parameters.request);
    promise.then(parameters.onSuccess);
    promise.catch(parameters.onError);
}
export { html2text, basicFetch, defaultRequest, };
//# sourceMappingURL=core.js.map