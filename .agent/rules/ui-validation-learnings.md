# UI Validation Learnings

## Hidden Inputs and HTML5 Validation
* **Rule**: When building multi-step wizard UIs where sections are hidden using `display: none` (or similar mechanisms), **do not rely on native HTML5 `required` attributes for form validation**.
* **Reason**: If a native validation failure occurs on an input field that is currently hidden, the browser will silently block the form submission. The user will not receive any validation error popup because the browser cannot focus or scroll to the hidden element, making buttons appear "dead" or unresponsive.
* **Solution**: Add `novalidate` to the `<form>` element to bypass native browser validation, and implement custom JavaScript-based validation logic at each step or before the final submission to ensure users are appropriately warned of missing required fields.
