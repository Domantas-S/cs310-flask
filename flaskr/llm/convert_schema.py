from schema import Record

with open("json_schema.json", "w") as f:
    f.write(str(Record.schema_json()))