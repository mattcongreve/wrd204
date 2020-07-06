# Building a Simple API with Falcon in Python

## Introduction

APIs or Application Programming Interfaces have made development between different projects or technologies much easier to share among the community. RESTful APIs, or in short, lightweight APIs that follow the general structure of a HTTP Request, are an important feature to build into your application as a developer.

With the combination of Python and the Falcon Web Framework, you can easily develop an API to help serve your application to your fellow developers.

### Warnings

This guide is primarily aimed towards Windows users. While some steps may be similar between others may be Windows specific.
This guide also expects you have beginner level knowledge of Python.

### Prerequisites

First, you'll need Python installed. With Windows 10, this can be done easily just by running `python` on your command prompt. This should prompt you to install directly from the Windows Store. If you'd prefer to not use the Microsoft store, you can obtain this directly from <https://www.python.org> . This guide focuses on versions newer than 3.3.

Secondly, you'll need to be prepared with a text editor and console to use. I recommend VS Code and Windows Terminal using Powershell.

## Building your API

1. Once you have python installed, it's recommended to setup a "Virtual environment" to contain all of the packages you intend to use for this project.

    Create your environment

    ```powershell
    python -m venv falcon_env
    ```

    Activate your environment

    ```powershell
    falcon_env\Scripts\activate.bat
    ```

2. Afterwords you'll need to use the package manager `pip` in order to install 2 packages you'll need for this tutorial:

    * `falcon` : The base package for the Falcon Framework you'll be using for this project
    * `waitress`: A minimal web server that will help you verify the functionality of your API

    ```powershell
    pip install falcon
    pip install waitress
    ```

    You're now ready to start building up your API!

3. To get started with using the falcon API framework, you need to build an application that can be hosted on a web server. The basic, bare-bones structure of a Falcon application is as follows:

    ```python
    import falcon

    app = falcon.API()
    ```

4. And that's it! To launch your application, execute `waitress-serve` against the application name and the app instance variable name. In this case, I named my file `example.py`.

    ```powershell
    waitress-service --port=8000 example:app
    ```

    Now that your API is running on a webserver, let's try sending requests to it in another powershell console with the `Invoke-RestMethod` commandlet

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000"
    ```

    However, when you run this, you should receive an error.

    ```powershell
    Invoke-RestMethod : The remote server returned an error: (404) Not Found.
    At line:1 char:1
    + Invoke-RestMethod -Uri "http://localhost:8000"
    + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-RestMethod], WebExc
       eption
        + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeRestMethodCommand
    ```

    This is because you have not defined any "routes", or in other words, URL paths pointing to resource objects within your application. By default, falcon returns a 404 for a resource not defined.

5. Routes are added to falcon applications via the function `add_route` against the falcon API instance. These routes are defined via a string indicating the path to be reached after the url, and then the definition of a resource. For example:

    ```python
    add_route('/example', example_class)
    ```

6. Resources are python classes that are defined to help indicate what a web request does when reaching that specific route. In the case of the url you would be testing on your local desktop, this would be `http://localhost:8000/example`

    So how do we define this resource? A simple class is instantiated, that's it. What is important is the functions that we definite underneath. For now I've just included a simple class structure.

    ```python
    class ExampleClass(object):
        def __init__(self):
            pass

    example_class = ExampleClass()

    app = falcon.API()

    app.add_route('/example', example_class)
    ```

7. Responders define how you respond to an incoming request on the route and class that you define. In a RESTful architecture, standard HTTP methods such as GET, POST, PUT, and DELETE are used for defining these requests. A responder function in your class is defined by the syntax `on_<method>`. These methods use the argument See an example of these functions defined below.

    ```python
    class ExampleClass(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            pass

        def on_post(self, req, resp):
            pass

        def on_put(self, req, resp):
            pass

        def on_delete(self, req, resp):
            pass
    ```

    Each of these functions will contain the logic behind what you intend to do behind each type of API request. You may notice that there are `self`, `req` and `resp` arguments being given to each of these classes. `self` is a just a widely accepted naming syntax to use when accessing the initialized properties of the class, defined by `__init__`. `req` and `resp` are specific arguments used to access certain properties of your incoming request. It's important to understand that these different responders should reflect what is being done on the backend of your API.

8. Both the request and response classes are what help you consume the incoming data on a request, transform that data into something actionable, and then modify the response to either indicate success or deliver data.

    The GET method of an RESTful web API is commonly used to specifically retrieve data, and have it delivered to the response. In a basic implementation, that would look like this:

    ```python
    class ExampleClass(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            resp.body = 'I am an example'
    ```

    And when requested, the response will show as expected.

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example"
    I am an example
    ```

9. There are multiple attributes that can be set in the response class to define how you want to respond to specific request. The most important ones to note are `body`, `media`, and `status`. Above, we used `body`. This defines the raw content that you are delivering in your response. In API implementations, you're usually returning your data back in a serializable method, whether that be with JSON, XML, YAML, etc. Falcon has a built in processor for this data that is defined by the `media` attribute. By default, this media is processed and converted from a python object into JSON representation.

    ```python
    class ExampleClass(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            resp.media = {
                'example_int': 42,
                'example_str': 'example',
                'example_list': [
                    'stuff',
                    'more_stuff',
                ],
                'example_dict': {
                    'falcon': 'awesome'
                }
            }
    ```

    Now if we retrieve the object with powershell again, we see that we're getting back a serialized object. (The actual response is JSON, but `Invoke-RestMethod` automatically converts JSON into powershell objects)

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example"

    example_int example_str example_list        example_dict
    ----------- ----------- ------------        ------------
             42 example     {stuff, more_stuff} @{falcon=awesome}
    ```

10. The `status` attribute is what helps us define our standard HTTP status code that the client will receive along with the response. These codes are implemented by default in Falcon for each specific request you are performing, however, if you decide to return a different status code, you can use the syntax `resp.status = falcon.HTTP_<code>` . In this example, I'm returning status code 501 (Not Implemented) to show to the client that the method being used is available, but either deprecated, not in use, or in development.

    ```python
    class ExampleClass(object):
        def __init__(self):
            pass

        def on_get(self, req, resp):
            resp.status = falcon.HTTP_501
    ```

    What the response looks like:

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example"
    Invoke-RestMethod : The remote server returned an error: (501) Not Implemented.
    At line:1 char:1
    + Invoke-RestMethod -Uri "http://localhost:8000/example"
    + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-RestMethod], WebExc
       eption
        + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeRestMethodCommand
    ```

11. So far, we've primarily dealt with the response class and defining how we respond to our client's base request. But what if our client was introducing URL parameters or body data? In those cases, we would primarily rely on data from the `Request` class, defined by `req` in our class functions. For a GET request, data is expected to be delivered via URL parameters. This data can be accessed via `req.get_param(<parameter_name)`, and is automatically converted from a string in the URL into a python object. In the below example, I'm defining a simple GET request to return a JSON dictionary, and to capitalize its contents if provided with the `capitalize` parameter. By default, I want it to be true if specified. (This would look like either <http://localhost:8000/example?capitalize> or <http://localhost:8000/example?capitalize=True>)

    ```python

    class ExampleClass(object):
        def __init__(self):
            pass

        def on_get(self, req, resp)
            capitalize = req.get_param('capitalize') or ''
            base_media = {'example_str': 'example'}
            if capitalize:
                media = {k: v.upper() for (k, v) in base_media.items()}
            else:
                media = base_media
            resp.media = media
    ```

    On our client, this would look like this when given different parameters

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example?capitalize=true"

    example_str
    -----------
    EXAMPLE


    Invoke-RestMethod -Uri "http://localhost:8000/example"

    example_str
    -----------
    example
    ```

12. The second most import request attribute to be aware of is `media`, similar to the `media` attribute in our response class defined earlier. This attribute is where JSON content that is delivered in the body of a web request is retrieved. Usually, this data can only be sent over in POST or PUT requests. Falcon will automatically conver this data from JSON into a python object to use. In a post or put request, data is expected to automatically be retrievable again via a GET request once posted. So for this example, I'm going to have the API save a file based on POST request contents, and automatically retrieve that file via a GET request. These definitions will be on the same route. In this last example, I tie this concept into the full class, and also provide error reporting. Explanations of each part are described in the example below.

    ```python
    class ExampleClass(object):
        def __init__(self):
            self.full_path = 'C:\\Users\\Matt Congreve\\AppData\\Local\\Temp\\example.txt' # Setting a initialized variable that can be used in both functions

        def on_post(self, req, resp):
            req_media = req.media # Defining my media to be extracted
            if 'content' in req_media: # Checking for if media has the "content" property with data to be written to the file
                content = req_media['content']
                try:
                    with open(self.full_path, 'w') as fd:
                        fd.write(content) # Writing the content specified
                    resp.media = {'ok': True} # Including a response that indicates success
                except Exception as ex:
                    resp.media = {'ok': False, 'exception': repr(ex)} # Including a response that indicates failure
                    resp.status = falcon.HTTP_500 # Specifying this is an application error
            else:
                resp.media = {'ok': False}
                resp.status = falcon.HTTP_422 # Specifying this is an issue with the content posted

        def on_get(self, req, resp):
            try:
                with open(self.full_path, 'r') as fd: # retrieving content
                    content = fd.read(fd)
                resp.media = {'ok': True, 'content': content} #presenting content in similar JSON structure as POST
            except Exception as ex:
                resp.media = {'ok': False, 'content': None, 'exception': repr(ex)} # Returning an error response and proper code like up above
                resp.status = falcon.HTTP_500
    ```

    With the above code, if you perform a GET on the resource, you'll get back an error, since the resource is not present yet.

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example"
    Invoke-RestMethod : {"ok": false, "content": null, "exception": "FileNotFoundError(2, 'No such file or directory')"}
    At line:1 char:1
    + Invoke-RestMethod -Uri "http://localhost:8000/example"
    + ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        + CategoryInfo          : InvalidOperation: (System.Net.HttpWebRequest:HttpWebRequest) [Invoke-RestMethod], WebExc
       eption
        + FullyQualifiedErrorId : WebCmdletWebResponseException,Microsoft.PowerShell.Commands.InvokeRestMethodCommand
    ```

    Therefore, let's actually use our API and issue a POST request! This can be done with the following powershell command parameters, fitting our JSON structure specified.

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example" -Method Post -Body (@{"content"="Example text to write to file"} | ConvertTo-Json ) -Headers @{"Content-Type"="application/json"}

      ok
      --
    True
    ```

    Our API returned a success, therefore, we have received confirmation that the data we have written is present. Now let's get that data with a GET request.

    ```powershell
    Invoke-RestMethod -Uri "http://localhost:8000/example"

      ok content
      -- -------
    True Example text to write to file
    ```

## Conclusion

Congratulations! You have now developed your own API with the Falcon Framework!

You can find more information on the Falcon Framework at the project's official documentation site: <https://falcon.readthedocs.io/en/stable/user/index.html>
