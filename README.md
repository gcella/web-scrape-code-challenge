# web-scrape-code-challenge

Gabrielle Cella
4/17/16

This script takes in a url and prints out all email addresses found on the corresponding web page, as well as any email address found on pages within the same domain that are discoverable through links on the original web page.

To run this program:

```python find_email_addresses.py [URL]```

--------

Because this program deals with opening many weblinks, opening certain pages will not necessarily succeed. All HTTP errors are documented by printing the HTTP status code and response message to standard error. 
To surpress erros, run:

```python find_email_addresses.py [URL] 2> /dev/null```

To redirect errors, run:

```python find_email_addresses.py [URL] 2> error_file.txt```

---------

The solution I have implemented works by opening the original url, gathering all emails found on the web page, gathering all links found within the html of the web page, and for all found links within the same domain as the original url recursively search links while gathering emails.

My program performs differently on the two examples that were given. I suspect that the mit website was edited since these specs were written, because mit.edu redirects to web.mit.edu. I have written my program to account for redirects, but the domain web.mit.edu has many many discoverable pages with an extremely long list of emails (faculty members, students, student services, etc), so the performance is still different.

When accounting for jana.com, the AngularJS presented a challenge that I did not write a solution to within the time I allotted for this project. On the Jana website, links to other discoverable pages are not spelled out in a link tag within the html of the jana homepage, but rather the route is changed in a javascript function. Because there is no way to access the route change within that function, I was unable to explore all discoverable paths. After much googling, I did not find a solution to this problem that would account for all possible frameworks