# Render my mail

*Render My Mail* sets up a minimal flask frontend to extract flask tags from a
given HTML file and lets a user enter the values for it. The user is then
presented with a preview of the rendered template and can send it to an
arbitrary e-mail address.

## Configuration

Configuration takes place in a .yaml file that has to have the same name as the
main python file (render_my_mail.py), i.e. render_my_mail.yaml
An example configuration file can be found in the repository which looks like
this:

```yaml
template: example.html
subject: Your rendered Template
address: no-reply@mydomain.com
password: mysupersecretpassword
host: smtp.mydomain.com
port: 587
reply-to: reply-to-me@mydomain.com
debug: False
```

| Name | Description |
| ---- | ----------- |
| Template | The HTML that shall be rendered (an example.html is in the repository). |
| Subject | The subject of the e-mail that is sent. |
| Address | The sender address. |
| User | *Optional* The username of the sender account. (If not given, the value of *Address* will be used.) |
| Password | The password of the sender account. |
| Host | The SMTP server that shall send the e-mail. |
| Port | The port on which to contact the SMTP server. |
| Reply-To | The value of the Reply-to header of the e-mail. |
| Debug | *Optional* Whether to show error messages when e-mail sending fails or not |
