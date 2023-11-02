from rich.table import Table
from tm_sl.com.printing import console, print_json
import json

test_data = [ 
    { "h1":"mydata", "h2":"arg 1" , "h3":"category 4"  } ,
    { "h1":"mydata", "h2":"arg 1" , "h4":"category 4?"  } ,
    { "h1":"mydata", "h2":"arg 1" , "h3": ['l1','l2','l3']  }
    ]

def c_json(data):
    print_json(json.dumps(data))

def json_as_table(data):
    table = Table(show_header=True, header_style="bold magenta")
    
    if isinstance(data, list):
        if len(data) == 0:
            console.print("Empty List!")
            return
        elif all(isinstance(item, dict) for item in data):
            # Get all unique headers across the list of dictionaries
            headers = {key for item in data for key in item.keys()}
            [table.add_column(header) for header in headers]

            for item in data:
                # Get values based on headers, if not exists then use an empty string
                values = [str(item.get(header, '')) for header in headers]
                table.add_row(*values)

            console.print(table)
        else:
            console.print("The list contains non-dict items, can't represent as a table.")
            return
    elif isinstance(data, dict):
        headers = list(data.keys())
        [table.add_column(header) for header in headers]
        table.add_row(*[str(value) for value in data.values()])
        console.print(table)
    else:
        console.print("Unsupported data type, can't represent as a table.")
        return
