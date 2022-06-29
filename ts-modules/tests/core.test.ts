/**
 * @jest-environment jsdom
 */
import * as core from "../core";

test("test html2text", () => {
  const htmlElement = document.createElement("input");
  expect(core.html2text(htmlElement)).toBe("");
  const str: string = "test string";
  htmlElement.value = str;
  expect(core.html2text(htmlElement)).toBe(str);

  expect(core.html2text(null)).toBe("");
});
