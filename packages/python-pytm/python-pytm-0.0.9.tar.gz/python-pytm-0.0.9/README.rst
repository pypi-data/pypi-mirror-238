 .. image:: https://github.com/wasi0013/PyTM/raw/master/ext/images/PyTM-logo.png
    :target: https://github.com/wasi0013/PyTM/
    :alt: PyTM - Logo




**PУΓM** - a Time Management Tool
---------------------------------


|image1| |image2| |image3| |Contributors| |DownloadStats| |DocsStats|
=====================================================================

.. |image1| image:: https://badge.fury.io/py/python-pytm.png
   :target: https://badge.fury.io/py/python-pytm
.. |image2| image:: https://img.shields.io/pypi/l/python-pytm.svg
   :target: https://pypi.org/project/python-pytm/
.. |image3| image:: https://img.shields.io/pypi/pyversions/python-pytm.svg
   :target: https://pypi.org/project/python-pytm/
   :alt: Supported Python Versions
.. |Contributors| image:: https://img.shields.io/github/contributors/wasi0013/PyTM.svg
   :target: https://github.com/wasi0013/PyTM/graphs/contributors
   :alt: List of Contributors
.. |DownloadStats| image:: https://pepy.tech/badge/python-pytm
   :target: https://pepy.tech/project/python-pytm
   :alt: Download Stats
.. |DocsStats| image:: https://readthedocs.org/projects/pytm/badge/?version=latest
   :target: https://pytm.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status


Goals
-----

Project time management, billing and invoice generations.

Demo Invoice
------------

 .. image:: https://github.com/wasi0013/PyTM/raw/master/ext/images/Demo-Invoice.png
    :target: https://github.com/wasi0013/PyTM/
    :alt: PyTM - Demo Invoice

Installing PyTM
---------------

You can download it from Python Package Index! For example::

    pip install python-pytm

or, you can install it using pipenv too!::

    pipenv install python-pytm

Checkout the version by typing the following in your terminal/command prompt::

    pytm --version


For a list of all the available options or, arguments try::

    pytm --help

After installing python-pytm for the first time run the command::

    pytm init

This command will create a folder in the home directory with necessary data store files.

Basic commands:
---------------

Currently available commands are listed below:

Commands related to project
===========================

* Start a new/existing project::

    pytm project start PROJECT_NAME

* Remove a project::

    pytm project remove PROJECT_NAME

* Check status of a project::

    pytm project status PROJECT_NAME

* Check summary of a project::

    pytm project summary PROJECT_NAME

* Finish active project::

    pytm project finish

* Pause active project::

    pytm project pause

* Abort active project::

    pytm project abort

Commands related to Task
========================

* Start a new or existing task in the current active project::

    pytm task start TASK_NAME

* Remove a task::

    pytm task remove TASK_NAME

* current task's status::

    pytm task status

* Finish active task::

    pytm task finish

* Pause active task::

    pytm task pause

* Abort active task::

    pytm task abort

Others
======
Configure project, user and invoice info::

    pytm config project PROJECT_NAME
    pytm config user
    pytm config invoice

Generate Invoice::
    
    pytm invoice auto PROJECT_NAME
    pytm invoice manual

Check version::

    pytm --version
    pytm -v


For a list of all the available options or, arguments try::

    pytm --help


Running the tests
-----------------

* Clone this `repository <https://github.com/wasi0013/PyTM>`_

* Install dependencies::

    pip install -r requirements.txt

* run the tests::

    py.test


Built With :heart: using
------------------------

* `Python <https://python.org/>`_

Contributing
------------

Please read `CONTRIBUTING.rst <CONTRIBUTING.rst>`_ for details on our code of conduct, and the process for submitting pull requests to us. You are encouraged to contribute or, try it out.

Any bug reports/suggestions/improvements/feature requests are highly appreciated. Just let us know by `creating issues <https://github.com/wasi0013/PyTM/issues/new/>`_

Version
-------
We use `SemVer <http://semver.org/>`_. For the versions available, see the `tags on this repository <https://github.com/wasi0013/PyTM/tags>`_

Author
------
* `Wasi <https://www.wasi0013.com/>`_ - (`wasi0013 <https://github.com/wasi0013>`_)

See also the list of `contributors <https://github.com/wasi0013/PyTM/contributors>`_ who participated in this project.

License
-------
This project is licensed under the MIT License - see the `LICENSE <LICENSE>`_ file for details.


Acknowledgments
---------------
* This project is bootstrapped using `this cookiecutter package <https://github.com/audreyr/cookiecutter-pypackage>`_


**NOTE:** "*This Project is still a work in progress.*"
