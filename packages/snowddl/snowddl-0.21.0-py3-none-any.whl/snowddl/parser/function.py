from snowddl.blueprint import (
    FunctionBlueprint,
    Ident,
    SchemaObjectIdentWithArgs,
    NameWithType,
    DataType,
    StageWithPath,
    build_schema_object_ident,
)
from snowddl.parser.abc_parser import AbstractParser, ParsedFile


# fmt: off
function_json_schema = {
    "type": "object",
    "properties": {
        "language": {
            "type": "string"
        },
        "arguments": {
            "type": "object",
            "additionalProperties": {
                "type": "string"
            }
        },
        "returns": {
            "anyOf": [
                {
                    "type": "string"
                },
                {
                    "type": "object",
                    "additionalProperties": {
                        "type": "string"
                    }
                }
            ]
        },
        "body": {
            "type": "string"
        },
        "is_secure": {
            "type": "boolean"
        },
        "is_strict": {
            "type": "boolean"
        },
        "is_immutable": {
            "type": "boolean"
        },
        "is_memoizable": {
            "type": "boolean"
        },
        "runtime_version": {
            "type": ["number", "string"]
        },
        "imports": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "stage": {
                        "type": "string"
                    },
                    "path": {
                        "type": "string"
                    }
                },
                "required": ["stage"],
                "additionalProperties": False
            },
            "minItems": 1
        },
        "packages": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "minItems": 1
        },
        "handler": {
            "type": "string"
        },
        "comment": {
            "type": "string"
        }
    },
    "anyOf": [
        {
            "required": ["body", "returns"]
        },
        {
            "required": ["handler", "returns"]
        }
    ],
    "additionalProperties": False
}
# fmt: on


class FunctionParser(AbstractParser):
    def load_blueprints(self):
        self.parse_schema_object_files("function", function_json_schema, self.process_function)

    def process_function(self, f: ParsedFile):
        arguments = [NameWithType(name=Ident(k), type=DataType(t)) for k, t in f.params.get("arguments", {}).items()]

        if isinstance(f.params["returns"], dict):
            # Returns table
            returns = [NameWithType(name=Ident(k), type=DataType(t)) for k, t in f.params["returns"].items()]
        else:
            # Returns value
            returns = DataType(f.params["returns"])

        if f.params.get("imports"):
            imports = [
                StageWithPath(
                    stage_name=build_schema_object_ident(self.env_prefix, i["stage"], f.database, f.schema),
                    path=self.normalise_stage_path(i["path"]),
                )
                for i in f.params.get("imports")
            ]
        else:
            imports = None

        if f.params.get("packages"):
            packages = f.params.get("packages")
        else:
            packages = None

        base_name = self.validate_name_with_args(f.path, arguments)

        bp = FunctionBlueprint(
            full_name=SchemaObjectIdentWithArgs(
                self.env_prefix, f.database, f.schema, base_name, data_types=[a.type.base_type for a in arguments]
            ),
            language=f.params.get("language", "SQL"),
            body=f.params.get("body"),
            arguments=arguments,
            returns=returns,
            is_secure=f.params.get("is_secure", False),
            is_strict=f.params.get("is_strict", False),
            is_immutable=f.params.get("is_immutable", False),
            is_memoizable=f.params.get("is_memoizable", False),
            runtime_version=str(f.params.get("runtime_version")) if f.params.get("runtime_version") else None,
            imports=imports,
            packages=packages,
            handler=f.params.get("handler"),
            comment=f.params.get("comment"),
        )

        self.config.add_blueprint(bp)
