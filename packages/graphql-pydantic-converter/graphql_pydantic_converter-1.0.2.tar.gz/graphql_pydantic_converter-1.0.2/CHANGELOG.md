# 0.0.3
- Add unit tests to project
- Fix mutation input rendering for list items
- Generate graphql schema request with custom typeOf depth

# 0.1.0
- Changed default payload boolean value from True to False
- In query or mutation must be defined response properties
- Generating of pydantic dataclasses for response parsing

# 0.1.2
- Ignore generating of private graphql schema objects
- Add graphql_pydantic_converter.graphql_types.concatenate_queries function

# 1.0.0
- Migration to pydantic v2

# 1.0.1
- Change Map type to dict (key, value)

# 1.0.2
- Stringify mutation input strings
- Add __typename to payload
- create test folder as a module