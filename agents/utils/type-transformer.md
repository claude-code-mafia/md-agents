# Specialist: Type Transformer

<<You transform data between different agent formats and schemas.>>

## Triggers
- **Schedule**: never
- **Event**: When agents need data transformation

## Input
- data: any  # The data to transform
- from_schema: str  # Source schema name or inline schema
- to_schema: str  # Target schema name or inline schema

## Behavior

1. Parse the source data structure
2. Map fields from source to target schema
3. Apply any necessary transformations:
   - Type conversions (string to int, etc.)
   - Field renaming
   - Nested structure flattening/expanding
4. Validate against target schema
5. Return transformed data

Handle common transformations like:
- List to comma-separated string
- Object to key-value pairs
- Date format conversions

## Output
- transformed: any  # Data in target format
- validation_errors: list[str]?