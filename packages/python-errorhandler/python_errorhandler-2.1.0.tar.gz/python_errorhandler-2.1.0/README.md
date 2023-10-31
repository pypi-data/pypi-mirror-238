This Python package, 'python_errorhandler', simplifies error handling in your code.

The `python_errorhandler` package streamlines error handling in your Django projects by providing a convenient decorator that reduces the complexity of managing exceptions. This package is authored by Nimesh Prajapati (prajapatin953@gmail.com) and is currently at version v1.0.0.

### How to Use the `error_handler` Decorator:

python_errorhandler
===================

Overview
--------
The `python_errorhandler` package simplifies error handling in Django, allowing you to streamline your code. With the provided `error_handler` decorator, you can easily manage exceptions and enhance your debugging experience. No more writing repetitive try-catch blocks—just import the package and apply the decorator with custom error messages to your functions.

Usage
-----
1. **Installation**:
   
   You can install the package using pip:
   
   pip install python-errorhandler

2. **Import**:

    Import the `error_handler` decorator in your Python script:
    
    from python_errorhandler import error_handler_decorator
    
3.**How to use**

    @error_handler_decorator(message="An error occurred while processing the data.")
    def process_data(data):
        pass
    
    message = you can pass your own custome message

    The error_handler decorator wraps your function and adds error-handling logic. If an exception occurs within the process_data function, it will display the provided error message, making it easier to identify and debug issues.

4. **Dependencies**
    This package depends on the following Python libraries:

    Django
    djangorestframework
    Ensure you have these dependencies installed in your environment when using python_errorhandler.

    For more details and updates, reach out to the author for questions or support.