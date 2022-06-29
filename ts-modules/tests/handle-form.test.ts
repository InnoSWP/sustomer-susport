/**
 * @jest-environment jsdom
 */
import * as source from "../handle-form";

const getDiv = () => {
  return document.createElement("div");
};

test("delete children of child-free container", () => {
  const container = getDiv();
  expect(source.deleteChildren(container)).toEqual(container);
});
test(" delete children of not child-free container", () => {
  const container = getDiv();
  const child = document.createElement("p");
  for (let i: number = 0; i < 10; i++) {
    container.appendChild(child);
  }
  expect(source.deleteChildren(container)).toEqual(getDiv());
});

test("test adding children", () => {
  const div = getDiv();
  const divReference = getDiv();
  let ps: HTMLElement[] = [];
  for (let i = 0; i < 10; i++) {
    ps.push(document.createElement("p"));
    divReference.appendChild(document.createElement("p"));
  }
  expect(source.addChildren(div, ps)).toEqual(divReference);
});

test("test empty append children", () => {
  const div = getDiv();
  expect(source.addChildren(div, []).children).toHaveLength(0);
});

test("form2text test cases", () => {
  const form = document.createElement("form");
  expect(source.form2text(form)).toBe("");
  const input = document.createElement("input");
  input.value = "test";
  input.id = "question_text";
  form.appendChild(input);
  expect(source.form2text(form)).toBe(input.value);
});

test("test requestFailure", () => {
  expect(source.requestFailure("error")).toBeUndefined();
});

test("Test add message", () => {
  const chat: source.ChatHistory = [];
  const entry: source.ChatEntry = {
    author: "test",
    text: "test test",
  };
  expect(source.addMessage(chat, entry)).toEqual([entry]);
});

// display message cases

test("display user message", () => {
  const message: source.ChatEntry = {
    author: source.userIsAuthor,
    text: "aa",
  };
  const res = source.displayMessage(message);
  expect(source.displayMessage(message).classList).toContain("user-message");
  expect(res.textContent).toBe(message.text);
});
test("display similar question", () => {
  const message: source.ChatEntry = {
    author: source.similarQuestionLabel,
    text: "aa",
  };
  const res = source.displayMessage(message);
  expect(source.displayMessage(message).classList).toContain(
    "similar-question"
  );
  expect(res.textContent).toBe(message.text);
});

test("display others message", () => {
  const message: source.ChatEntry = {
    author: "Jeff",
    text: "aa",
  };
  const res = source.displayMessage(message);
  expect(res.classList).toContain("others-message");
  expect(res.textContent).toBe(message.text);
});

// test("", () => {});
// test("", () => {});
// test("", () => {});
