function html2text(htmlElement: HTMLInputElement | null): string {
  if (htmlElement == null) {
    return "";
  }
  return htmlElement.value;
}

interface messageRequestBody {
  text: string;
  user_id: number;
}
const defaultRequest: RequestInit = {
  method: "GET",
  headers: { "content-type": "application/json;charset=UTF-8" },
};

interface fetchParameters {
  url: string;
  onSuccess: (arg0: Response) => void;
  onError: (arg0: any) => void;
  request: RequestInit;
}

function basicFetch(parameters: fetchParameters) {
  const promise = window.fetch(parameters.url, parameters.request);
  promise.then(parameters.onSuccess);
  promise.catch(parameters.onError);
}

export { html2text, messageRequestBody, basicFetch, defaultRequest };
