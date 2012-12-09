__author__ = 'robert'
import json

def get_lines(kind):
    end1 = "class "
    end2 = "(ndb.Model):"
    with open('datamodel.py') as f:
        lines = f.readlines()
    append = False
    chunk = []
    for line in lines:
        if append:
            if end1 in line and end2 in line:
                break
            chunk.append(line)
        if "class " + kind + "(ndb.Model):" in line:
            append = True

    return chunk

def get_form(kind):
    lines = get_lines(kind)
    form_lines = []
    form_lines.append("""<form action="" method="post">""")
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        is_string = "StringProperty" in line
        is_repeat = "repeated=True" in line
        is_int = "IntegerProperty" in line
        is_float = "FloatProperty" in line
        is_text = "TextProperty" in line
        is_key = "Key" in line
        is_date = "DateTimeProperty" in line
        assert [is_date, is_string, is_int, is_float, is_key, is_text].count(True) == 1
        if is_key or is_date:
            continue
        label = line.split("=")[0].strip()
        input_ = """<input type="text" name="{0}" />""".format(label)
        if is_repeat:
            input = ""
            for i in range(5):
                input_ += """<input type="text" name="{0}" />""".format(label + str(i))
        if is_text:
            input_ = """<textarea type="text" name="{0}" style="width: 500px; height: 200px"></textarea><br />""".format(label)
        input_ += "<br/>"
        form_line = "{label}: {input_}".format(label=label, input_=input_)
        form_lines.append(form_line)
    form_lines.append("""<input type="submit" value="Submit">""")
    form_lines.append("</form>")
    return "".join(form_lines)

def get_json(kind):
    lines = get_lines(kind)
    json_dicts = []
    #print lines, 'wtf'
    for xx in "abc":
        json_dict = {}
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            is_string = "StringProperty" in line
            is_repeat = "repeated=True" in line
            is_int = "IntegerProperty" in line
            is_float = "FloatProperty" in line
            is_text = "TextProperty" in line
            is_key = "Key" in line
            is_date = "DateTimeProperty" in line
            assert [is_date, is_string, is_int, is_float, is_key, is_text].count(True) == 1
            if is_key or is_date:
                continue
            label = line.split("=")[0].strip()
            #print label
            json_dict[label] = xx
        json_dicts.append(json_dict)
    return json.dumps(json_dicts)
