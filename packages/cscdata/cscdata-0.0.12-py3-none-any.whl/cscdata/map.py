df2ck = {
    "int8": "Int8",
    "int16": "Int16",
    "int32": "Int32",
    "int64": "Int64",
    "float32": "Float32",
    "float64": "Float64",
    "uint8": "UInt8",
    "uint16": "UInt16",
    "uint32": "UInt32",
    "uint64": "UInt64",
    "bool": "UInt8",
    "string": "String",
    "object": "String",
    "datetime64[ns]": "DateTime",
    "timedelta[ns]": "Int64"
}


ck2df = {
    "Int8": "int8",
    "Int16": "int16",
    "Int32": "int32",
    "Int64": "int64",
    "UInt8": "uint8",
    "UInt16": "uint16",
    "UInt32": "uint32",
    "UInt64": "uint64",
    "Float32": "float32",
    "Float64": "float64",
    "String": "object",
    "FixedString": "object",
    "Date": "datetime64[ns]",
    "DateTime": "datetime64[ns]",
    "DateTime64": "datetime64[ns]",
    "Enum8": "category",
    "Enum16": "category",
    "Array": "object",
    "Nullable": "object",
    "UUID": "object",
    "IPv4": "object",
    "IPv6": "object",
    "Decimal": "object"
}

