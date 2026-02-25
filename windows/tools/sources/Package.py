import json
import pathlib

package = {
    "name" : "Package-amd64.json",
    "package" : {
        "id" : {
            "path" : "",
        }
    }
}
pt = pathlib.Path(__file__).resolve()
f = pt.parent.parent.parent / "Package-amd64.json"
with open(f, "w") as f:
    json.dump(package, f, indent=4)
