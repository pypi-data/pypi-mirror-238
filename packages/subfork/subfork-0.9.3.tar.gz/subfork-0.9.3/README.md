Subfork Python API
==================

This package provides the Subfork Python API and command line interface.


Installation
------------

The easiest way to install:

    $ pip install subfork


Quick Start
-----------

In order to authenticate with the Subfork API, you will first need to create
API access keys for your site at [subfork.com](https://www.subfork.com). To use
the Subfork Python API your site must have a verified domain. Then
instantiate a client using the site domain, port, access and secret keys:

    >>> import subfork
    >>> sf = subfork.get_client(domain, port, access_key, secret_key)


Configuration
-------------

Using the Subfork Python API requires basic authentication. To use
environment variables, set the following:

    $ export SUBFORK_HOST=<domain name>
    $ export SUBFORK_ACCESS_KEY=<access key>
    $ export SUBFORK_SECRET_KEY=<secret key>

To use a shared config file, copy the `example_subfork.yaml` file to `subfork.yaml`
at the root of your project and make required updates:

    $ cp example_subfork.yaml subfork.yaml
    $ nano subfork.yaml

Or set `$SUBFORK_CONFIG_FILE` to the path to `subfork.yaml`:

    $ export SUBFORK_CONFIG_FILE=/path/to/subfork.yaml

Minimum `subfork.yaml` file requirements include the client args:

    SUBFORK_HOST: <domain name>
    SUBFORK_ACCESS_KEY: <access key>
    SUBFORK_SECRET_KEY: <secret key>


Site Templates
--------------

Site data is stored in a separate `template.yaml` file and required for
testing and deploying sites. Basic site info includes:

- the domain name of the site, no http(s)
- the list of site template files and routes
- template and static file paths (optional)

For example:

    domain: example.fork.io
    pages:
      index:
        route: /
        file: index.html
      user:
        route: /user/<username>
        file: user.html


Basic Commands
--------------

To deploy a site:

    $ subfork deploy [template.yaml] -c <comment> [--release]

To test the site using the dev server:

    $ subfork run [template.yaml]

To process tasks:

    $ subfork worker [options]


Data
----

Data is organized into `datatypes` and must be JSON serializable. 

Insert a new datatype record, where `datatype` is the name of the
datatype, and `data` is a dictionary:

    >>> sf = subfork.get_client()
    >>> sf.get_data(datatype).insert(data)

Find data matching a list of search `params` for a given `datatype`:

    >>> results = sf.get_data(datatype).find(params)

where `params` is a list of `[key, op, value]`, for example:

    >>> results = sf.get_data(datatype).find([[key, "=", value]])

More info here:

    $ pydoc subfork.api.data


Workers
-------

Workers process tasks created either via API clients or users.
By default, running the `subfork worker` command will pull tasks from a
specified queue and process them.

    $ subfork worker [--queue <queue> --func <pkg.mod.func>]

For example:

    $ subfork worker --queue test --func subfork.worker.test

Workers can also be defined in the `subfork.yaml` file, and can contain
more than one worker specification:

    WORKER:
      worker1:
        queue: test
        function: subfork.worker.test
      worker2:
        queue: stress
        function: subfork.worker.stress

To create a task, pass function kwargs to a named task queue,
for example, passing `t=3` to worker2 defined above:

    >>> sf = subfork.get_client()
    >>> task = sf.get_queue("stress").create_task({"t": 3})

To get the results of completed tasks:

    >>> task = sf.get_queue("stress").get_task(taskid)
    >>> task.data()

Running a worker as a service:

See the `bin/worker` and `services/worker.service` files for an example of how
to set up a systemd worker service. 

Update the ExecStart and Environment settings with the correct values, and copy
the service file to /etc/systemd/system/ and start the service.

    $ sudo cp services/worker.service /etc/systemd/system/
    $ sudo systemctl daemon-reload
    $ sudo systemctl start worker
    $ sudo systemctl enable worker

Checking worker logs:

    $ sudo journalctl -u worker -f
