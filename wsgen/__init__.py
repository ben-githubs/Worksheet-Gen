# Worksheet Generator
import __main__
import logging
from pathlib import Path
import re

import jinja2

logger = logging.getLogger(__name__)

# Define default jinja environment
env = jinja2.Environment(
    loader = jinja2.PackageLoader('wsgen', ''),
    block_start_string = r'\jblock{',
    block_end_string = r'}',
    variable_start_string = r'\jvar{',
    variable_end_string = r'}',
    comment_start_string = r'\jcomm{',
    comment_end_string = r'\}'
)
# The worksheet class contains problem templates and is used to render a LaTeX source
# file to a path of your choice.
class Worksheet:
    def __init__(self, template='sample.tex', env=env, **kwargs):
        #  -- Args --
        # template:  the path to a tex file to serve as the base template for the worksheet
        # env:       jinja environment to use for template rendering (default is defined above)
        # kwargs:    customization options for the worksheet, mostly related to formatting
        logging.debug('Creating worksheet.')

        self.env = env
        self.template = template
        
        # Here we control if we should display question text on the worksheet, or show the solutions.
        # The default behaviour is to show both, but you can choose to omit one (for example, when
        # publishing a test and answer key seperately)
        self.render_problems = kwargs.get('render_problems', True)
        self.render_solutions = kwargs.get('render_solutions', True)

        # Some formatting and customization settings
        self.title = kwargs.get('title', 'Worksheet')
        self.lhead = kwargs.get('lhead', self.title)
        self.lhead = kwargs.get('chead', '')
        self.lhead = kwargs.get('rhead', '')
        self.lhead = kwargs.get('lfoot', '')
        self.lhead = kwargs.get('cfoot', '')
        self.lhead = kwargs.get('rfoot', r'Page \thepage of \pageref{LastPage}')

        # This internal lists holds a series of Problem objects for eventual rendering
        self._problems = list()
    

    def save_to_file(self, fname, overwrite=False):
        # Renders the worksheet into LaTeX source, then saves it as a file at a specified path.
        # -- Args --
        # fname:     the path at which to place the source file
        # overwrite: whether or not to replace an existing file at 'fname'. Defaults to no.

        # Clean input, check if path is valid, and check if a file alreasy exists there
        assert isinstance(fname, Path), f'Expected Path, got {type(fname)}'
        if not overwrite:
            assert not fname.exists(), f'There is already a file at {fname}'

        # Open a new file at 'path', and write in the contents of the source
        with fname.open(mode='w') as f:
            f.write(self.render())
    

    def render(self):
        # Returns the worksheet rendered as a LaTeX source file.
        logging.info('Rendering worksheet.')

        # First, we render each problem (and solution) into text form.
        problems = list()
        solutions = list()
        for p in self._problems:
            prob, sol = p.render(self.env)
            problems.append(prob)
            solutions.append(sol)
        
        # Then, we place those rendered forms into a jinja template, exporting
        # the customization variables specified in the worksheet construction.
        vars = {
            'title': self.title,
            'problems': problems,
            'render_problems': self.render_problems,
            'solutions': solutions,
            'render_solutions': self.render_solutions,
        }
        template = self.env.get_template(self.template)
        return template.render(**vars)
    
    # TODO: Adjust this to be a full-on list subclass so I don't have to define all these methods manually
    def append(self, prob):
        assert isinstance(prob, Problem), f'Expected Problem, got {type(prob)}'
        self._problems.append(prob)
    
    def clear(self):
        return self._problems.clear()
    
    def count(self):
        return self._problems.count()
    
    def insert(self, idx, prob):
        assert isinstance(prob, Problem), f'Expected Problem, got {type(prob)}'
        return self._problems.insert(idx, prob)
    
    def remove(self, elem):
        return self._problems.remove(elem)
    
    def pop(self, idx):
        return self._problems.pop(idx)


# Here, we define the basic layout of every problem. All problems will have these methods.
class ProblemBase:
    def __init__(self, title, template):
        # -- Args --
        # title:     what to name the problem
        # template:  path to the jinja template used to represent the problem and solution.
        assert type(title) == str, f'Expected str, got {type(title)}'
        assert isinstance(template, Path), f'Expected Path, got {type(template)}'

        self.title = title
        self.template = template

        # Every Problem subclass should define this variable, but just in case, it's defined here as well.
        self.vars = dict()
        # The 'setup' method should be defined uniquely in each Problem subclass.
        self.setup()
    

    def setup(self):
        # The setup method is unique to each problem, and should be overridden in each child class.
        logging.debug(('ProblemBase.setup is being called. Either you forgot to override \'setup\''
                        ' in your subclass, or you subclassed an object of ProblemBase instead of Problem.'))
    
    def render(self, env):
        # Returns LaTeX source code for the problem text and solution, as a tuple of strings.
        # -- Args --
        # env:  the jinja environment to use for rendering. This is usually provided by the Worksheet
        #       object callign this method.
        text = self.template.read_text()
        text_prob = ''
        text_sol = ''

        # The templates for problems should have a seperate block for problems and for solutions. Sadly, Jinja has
        # no convienient method of extracting specific blocks from a template, so I resorted to regex.
        # TODO: Instead of have the function raise an exception in the case of a missing block, have it log a warning that the block is missing.
        try:
            text_prob = re.search(r'\\jblock\{block problem\}((.|\n)+?)\\jblock\{endblock\}', text).group(1)
        except AttributeError:
            raise ValueError('block problem not found in file.')
        try:
            text_sol = re.search(r'\\jblock\{block solution\}((.|\n)+?)\\jblock\{endblock\}', text).group(1)
        except AttributeError:
            raise ValueError('block solution not found in file.')
        
        # havign saved the block texts to strings, we covert them into Template objects, then return them rendered.
        temp_prob = env.from_string(text_prob)
        temp_sol = env.from_string(text_sol)
        # TODO: Log a warning if self.vars is empty, since it means the user forgot to add to it in 'setup'.
        return (temp_prob.render(**self.vars).strip(), temp_sol.render(**self.vars).strip())

# This class exists to leverage inheritance and save work when making new Problems.
# Since any class which inherits from ProblemBase and overrides 'setup' will need
# the following in its constructor (to prevent ProblemBase.setup from being called
# instead of the local overridden version), I just made this buffer class that defines
# the constructor once for every subsequent Problem.
class Problem(ProblemBase):
    def __init__(self, *args, **kwargs):
        # Call the ProblemBase constructor, which sets up the title, templates, etc.
        super().__init__(*args, **kwargs)