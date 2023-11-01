# PyWebWrench Library 🖥️

PyWebWrench is a Python library that enables you to view web pages and make HTTP requests using popular Python libraries such as Playwright and Requests.

## Usage 🚀

Follow these steps to use the PyWebWrench library:
1. Import the Library 📦
```python
from pyrequester import PyWebWrench
```
3. Create a PyWebWrench Object 👷
```python
pr = PyWebWrench(browser_name="firefox") # You can choose a different browser.
```
4. Render a Web Page 🌐
To view a web page, use the `render_page` function:
```python
page_content = pr.render_page(url="https://www.example.com")
print(page_content)
```
5. Control a Web Page 🎛️
To have more control over a web page, use the `control_page` function:
```python
page = pr.control_page(url="https://www.example.com")
# Perform additional operations
page.close()  # Don't forget to close the page when you're done.
```
6. Make HTTP Requests 📞
PyWebWrench uses the Requests library to make HTTP requests. You can use the `get`, `post`, `put`, `delete`, `patch`, and `head` functions for this purpose.

Example of a GET request:
```python
response = pr.get(url="https://api.example.com/data")
print(response.text)
```

## Error Handling ⚠️

`UnsupportedBrowserError`: You might encounter this error for unsupported browsers.

## Supported Browsers 🌐

-   Chromium
-   Chrome
-   Chrome Beta
-   Microsoft Edge
-   Microsoft Edge Beta
-   Microsoft Edge Dev
-   Firefox
-   Firefox ASAN
-   Webkit

## Dependencies 🔧

Before using PyWebWrench, make sure to install the following dependencies:

-   Playwright
-   Requests

You can install these dependencies using the following commands:

    pip install playwright
    pip install requests

## Conclusion 🎉

PyWebWrench is a handy Python library for viewing web pages and making HTTP requests. You can open, control, and send requests to web pages using the specified browsers. For more information about usage and functionality, you can explore the source code of PyWebWrench. 🔍

Feel free to contribute or report issues! 🙌
