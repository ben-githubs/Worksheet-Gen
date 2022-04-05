# About the Project
When I was tutoring, I developed a program for dynamically created mock-exams for students using LaTeX templates. I've recently cleaned up and refactored that code, allowing for package imports and better documentation. Feel free to use or modify for your own personal uses.

## Built with
- Python 3.x
- Jinja2

# Getting Started
To use locally, follow these steps.

## Prerequisites
Obviously, install Python. Any edition of Python 3 should do.
The only 3rd-party library used is Jinja2, which can be installed as follows:
    pip install Jinja2

## Installation
Clone the reposititory, or download the `wsgen` folder. Place it somewhere in your PYTHONPATH, or inside your project directory.

# Usage
To use `wsgen`, type `import wsgen` at the top of your python file.

To create new problems, create a subclass of Problem, then add a setup function, defining the logic.

    import wsgen

    class AddNumbers(wsgen.Problem):
        def setup(self):
            num1 = 5
            num2 = 7
            ans = num1 + num2

            self.vars = {
                'num1': num1,
                'num2': num2,
                'ans': ans
            }

New problems need a text template, and those are written in LateX and enclosed in Jinja blocks. Since LaTeX makes extensive use of burly braces, the default Jinja markers have been replaced:

    {% ... %} is now \jblock{ ... }
    {{ ... }} is now \jvar{ ... }
    {# ... #} is now \jcomm{ ... }

With this in mind, the template for our adding problem is

    \jblock{block problem}
        What is $\jvar{num1} + \jvar{num2}$?
    \jblock{endblock}

    \jblock{block solution}
        $\jvar{num1} + \jvar{num2} = \jvar{ans}$
    \jblock{endblock}

Finally, to create this worksheet, our main script should look like this:

    import wsgen

    class AddNumbers(wsgen.Problem):
        ...
    
    worksheet = wsgen.Worksheet()
    worksheet.append(AddNumbers('Adding', 'path_to_template'))
    worksheet.save_to_file('path_to_output')

# License
Free for personal use.