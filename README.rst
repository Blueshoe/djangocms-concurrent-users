djangocms-concurrent-users  
==========================  

A Django-CMS plugin for blocking pages which are edited by another user.
This provides a simple mechanism to prevent two users working on the same page. Due to the
fact, that only the version of the last user hitting the save button is stored, data loss is very likely.

This plugin adds a hidden toolbar item in order to provide the required code to the client. Once the browser
enters a page, it checks for another user and gets blocked in case the page has been locked. If the page is
not edited at this moment, the client acquires a lock and hence blocks it for other users for the time of working.
The check if performed by polling the server with an specified interval. Once the client lefts the page, the lock 
is released and the next user will be able to make changes.



Features
========

* blocks a page with an overlay in case another user is already working on it
* reloads the page once it is released, in order to fetch the latest changes
* displays the username and time of the blocking user


Installation
============

To get started using ``djangocms-concurrent-users``:

- install it with ``pip``::

    $ pip install djangocms-concurrent-users


- add the plugins to ``INSTALLED_APPS``::

    INSTALLED_APPS = (
        ...
        'djangocms_concurrent_users',
        ...
    )


- run ``migrate``.

- add ``url(r'', include('djangocms_concurrent_users.urls', namespace='concurrent_users'), ),`` to your urls


Configuration
=============

 * ``CONCURRENT_BLOCKING_OFFSET``: Time to wait until the page is release just after the user left; is ``20`` by default; Must be larger than ``CONCURRENT_POLLING_INTERVAL``
 * ``CONCURRENT_POLLING_INTERVAL``: Interval for the clients to poll the server; is ``20`` by default; Must not be greater than ``CONCURRENT_BLOCKING_OFFSET``
 * ``CONCURRENT_BLOCK_EDITING``: Specifies if the blocking actually happens; is ``True`` by default;