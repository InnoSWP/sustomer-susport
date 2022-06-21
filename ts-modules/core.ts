function html2text(htmlElement: HTMLInputElement | null): string {
  if (htmlElement == null) {
    return "";
  }
  return htmlElement.value;
}

interface MessageRequestBody {
  text: string;
  user_id: number;
}
const defaultRequest: RequestInit = {
  method: "GET",
  headers: { "content-type": "application/json;charset=UTF-8" },
};

interface FetchParameters {
  url: string;
  onSuccess: (arg0: Response) => void;
  onError: (arg0: any) => void;
  request: RequestInit;
}

function basicFetch(parameters: FetchParameters) {
  const promise = window.fetch(parameters.url, parameters.request);
  promise.then(parameters.onSuccess);
  promise.catch(parameters.onError);
}

export {
  html2text,
  MessageRequestBody,
  basicFetch,
  defaultRequest,
  FetchParameters,
};
